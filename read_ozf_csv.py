import re
import requests
import sys
from my_selenium import MySelenium
from locate104 import LocateOneZeroFour
from pyquery import PyQuery as pq
from collections import defaultdict
from loguru import logger as log

# remove default level
log.remove()
# level DEBUG|INFO
log.add(sys.stderr, level="INFO", diagnose=True, backtrace=True)


class Read_OZF_CSV(MySelenium, LocateOneZeroFour):
    def __int__(self, set_browser, target_url, headless):
        MySelenium.__init__(self, set_browser=set_browser, target_url=target_url, headless=headless)

    @staticmethod
    def read_csv():
        csv_dict = dict()
        with open("104.csv", encoding='utf8') as f:
            while True:
                line = f.readline()
                # print(line)
                interface_descriptions = re.finditer(
                    r"\"(?P<title>.*)\","
                    r"\"(?P<title_link>https://.*)\","
                    r"\"(?P<company>.*)\","
                    r"\"(?P<company_link>https://.*)\","
                    r"\"(?P<area>.*)\"",
                    line,
                    re.MULTILINE)

                for part in interface_descriptions:

                    # print(part.groupdict())
                    if part.group('company') not in csv_dict:
                        csv_dict[part.group('company')] = dict()
                        csv_dict[part.group('company')]["titles"] = list()
                        csv_dict[part.group('company')].update({"link": part.group('company_link')})
                        csv_dict[part.group('company')]['titles'].append(part.group('title'))

                    if part.group('title') not in csv_dict[part.group('company')]['titles']:
                        csv_dict[part.group('company')]['titles'].append(part.group('title'))

                if not line:
                    break

        # import yaml
        # print(yaml.dump(csv_dict, allow_unicode=True, sort_keys=False, default_flow_style=False))

        return csv_dict

    def com_list(self):
        csv = self.read_csv()
        find_urgent = dict()
        title_count = 0
        my_res = 0
        log.debug(csv)
        for keys in csv.keys():
            log.debug(keys)
            log.debug(csv[keys]['link'])
            log.debug(csv[keys]['titles'])
            title_count += len(csv[keys]['titles'])
            page_s = self.go_com_page(csv[keys]['link'], keys)
            my_res = self.pq_find_job(page_s, keys, csv[keys]['titles'], find_urgent)

        log.debug(title_count)
        self.filter_csv(my_res)

    def request_com(self, keyword):

        url = f"https://m.104.com.tw/custSearch/custlist?keyword={keyword}&jobsource=m_menucust"

        payload = {}
        headers = {
            "Host": "m.104.com.tw",
            "Referer": "https://m.104.com.tw/custSearch?jobsource=m_menucust",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)

    def go_com_page(self, url, com_name):
        __ERROR_CALL = "Read_OZF_CSV.go_com_page"
        __SUBMIT = ".buttons-submit > h2"
        __INLINE = "div > .d-inline"
        __BUTTON = ".buttons > .buttons-submit"
        __xBUTTON = "//body//button/h2"
        __PAGINATION = ".pagination > .pagination__count"

        # get url
        self.driver_get(url)
        self.wait_element(__SUBMIT, f"[{__ERROR_CALL}:{__SUBMIT}]", ec_mode='visi')
        inline = self.find_element(__INLINE, f"[{__ERROR_CALL}:{__INLINE}]")
        log.info(inline.text)
        self.wait_element(__BUTTON, f"[{__ERROR_CALL}:{__BUTTON}]", ec_mode='visi')
        if inline.text == com_name:
            log.info('pass')
            # btn = self.find_element(__BUTTON, f"[{__ERROR_CALL}:{__BUTTON}]")
            # btn.click()
            btn = self.find_element(__xBUTTON, f"[{__ERROR_CALL}:{__xBUTTON}]", selector='xpath')
            self.driver.execute_script("arguments[0].click();", btn)

            self.wait_element(__PAGINATION, f"[{__ERROR_CALL}:{__PAGINATION}]")
            return self.page_source()
        else:
            exit(f"Fail to check inline.text is {com_name}")

    @staticmethod
    def pq_find_job(page, com_name, job_list, res):
        # self.driver_close()
        icon_pin = ".container-fluid > .row .jb_icon_pin"
        doc = pq(page)
        log.debug(f"first res: {res}")
        result = defaultdict(list)

        for title in doc(icon_pin).parent().parent().items():
            log.debug(title.text())
            if title.text() in job_list:
                result[com_name].append(title.text())

        log.debug(result)
        res.update(result)
        log.debug(f"end res: {res}")
        return res

    @staticmethod
    def filter_csv(res):
        write_list = list()
        with open("104.csv", encoding='utf8') as f:
            while True:
                line = f.readline()
                # print(line)
                interface_descriptions = re.finditer(
                    r"\"(?P<title>.*)\","
                    r"\"(?P<title_link>https://.*)\","
                    r"\"(?P<company>.*)\","
                    r"\"(?P<company_link>https://.*)\","
                    r"\"(?P<area>.*)\"",
                    line,
                    re.MULTILINE)
                for part in interface_descriptions:
                    # log.debug(part.groupdict())
                    if part.group('company') in res.keys() and part.group('title') in res[part.group('company')]:
                        write_list.append(
                            f"\"{part.group('company')}\",\"{part.group('title')}\",\"{part.group('area')}\",\"{part.group('title_link')}\","
                        )

                if not line:
                    break
        log.debug(write_list)

        log.debug(len(write_list))
        with open("urgent104.csv", mode='a', encoding='utf8') as fr:
            for i in range(len(write_list)):
                log.debug(write_list[i])
                fr.write(write_list[i] + '\n')


if __name__ == "__main__":
    data = {
        '凡谷興業有限公司': {
            'titles': ['Internet程式設計師(B組)', 'Internet程式設計師(C組)', '網站可靠性工程師(SRE，Site Reliability Engineer)', '遊戲核心開發工程師(GoLang)', '網頁前端工程師',
                       '應用服務開發工程師', '全端工程師', 'SRE網站可靠性工程師', '機率工程師', '前端工程師', '自動化測試開發工程師', '自動化測試軟體開發工程師', '程式開發工程師', '遊戲程式設計師',
                       'Internet程式設計師(A組)', 'WEB 軟體工程師', 'WEB前端網頁工程師', '商務平台後端工程師', 'Java工程師', '系統分析師', '遊戲前端工程師', 'APP軟體開發工程師', 'PHP網頁工程師',
                       '網頁系統工程師', '數據系統分析師', '數據工程師', '軟體系統工程師', '網頁系統全端工程師', '資料庫架構師(DBA資料庫管理工程師)', '影像串流工程師', '影音串流工程師', 'API後端系統工程師',
                       'Scrum Master (軟體開發)'],
            'link': 'https://www.104.com.tw/company/1a2x6bi8ln?jobsource=m104_hotorder'},
        '尊博科技股份有限公司': {
            'titles': ['軟體測試工程師', '遊戲測試工程師', '軟體工程師(C/C++/C# )', '軟體工程師(Unity3D/C#)', '資料庫管理師(MySQL)', '軟體工程師(Java)', 'Unity軟體工程師(APP)',
                       '軟體後端工程師(Java/C#)'], 'link': 'https://www.104.com.tw/company/5ucjyv4?jobsource=m104_hotorder'}
    }
    # ts_role = data['凡谷興業有限公司']
    # my_read = Read_OZF_CSV("chrome", headless=1)
    # job = my_read.go_com_page(ts_role['link'], "凡谷興業有限公司")
    # filter_res = dict()
    # my_res = 0
    # for key in data.keys():
    #     log.debug(key)
    #     log.debug(data[key]['link'])
    #     log.debug(data[key]['titles'])
    #     page = my_read.go_com_page(data[key]['link'], key)
    #     my_res = my_read.pq_find_job(page, key, data[key]['titles'], filter_res)
    #
    # log.debug(my_res)
    # my_read.filter_csv(filter_res)

    start_read = Read_OZF_CSV("chrome", headless=1)
    start_read.com_list()

    start_read.driver_close()
    # job = my_read.go_com_page(ts_role['link'], "凡谷興業有限公司")
    # res = my_read.pq_find_job(job, "凡谷興業有限公司", ts_role['titles'], res)

    # my_read = Read_OZF_CSV("no_driver")
    # my_read.com_list()
