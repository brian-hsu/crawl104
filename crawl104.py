import sys

from loguru import logger as log
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from selenium.common.exceptions import ElementClickInterceptedException

from my_selenium import MySelenium
from locate104 import LocateOneZeroFour

# remove default level
log.remove()
# level DEBUG|INFO
log.add(sys.stderr, level="INFO", diagnose=True, backtrace=True)


class CrawlOneZeroFour(MySelenium, LocateOneZeroFour):

    def __int__(self, set_browser, target_url, headless):
        MySelenium.__init__(self, set_browser=set_browser, target_url=target_url, headless=headless)

    def go_search(self):
        __ERROR_CALL = "CrawlOneZeroFour.go_search"
        __SEARCH_LOCATE = self.css_locate['search_keyword']
        __SUBMIT = 'submit-buttons'

        # get url
        self.driver_get()
        self.wait_element(__SEARCH_LOCATE[__SUBMIT], f"[{__ERROR_CALL}:{__SUBMIT}]")

    def search_keyword(self, keys, value):
        __ERROR_CALL = "CrawlOneZeroFour.go_search"
        __SEARCH_LOCATE = self.css_locate['search_keyword']
        __SUBMIT = 'submit-buttons'
        __KEYWORD = 'keyword'
        __SEARCH_TYPE = 'search-type'
        find_keyword = self.find_element(__SEARCH_LOCATE[__KEYWORD], f"[{__ERROR_CALL}:{__KEYWORD}]")
        find_keyword.clear()
        find_keyword.send_keys(keys)
        # find_select_type = self.find_element(__SEARCH_LOCATE[__SEARCH_TYPE], f"[{__ERROR_CALL}:{__SEARCH_TYPE}]")
        # self.select_element(find_select_type, value)

    def job_cate(self, job_list):
        __ERROR_CALL = "CrawlOneZeroFour.job_cate"
        __SEARCH_LOCATE = self.css_locate['job_cate']
        __UL_LIST = 'result-list'
        __SUBMIT = 'submit'
        js_document_job_cate = "document.getElementById('jobCateLauncher').click();"
        # show job cate
        self.execute_script(js_document_job_cate)
        self.wait_element(__SEARCH_LOCATE[__UL_LIST], f"[{__ERROR_CALL}:{__UL_LIST}]", ec_mode="visi")
        ul_list_element = self.find_element("ul.result-list", f"[{__ERROR_CALL}:{__UL_LIST}]")
        log.debug(ul_list_element)
        ul_items = ul_list_element.find_elements_by_tag_name('li')
        log.debug(ul_items)

        find_count = len(job_list)
        for item in ul_items:
            log.debug(item.text)
            if item.text in job_list:
                item.find_element_by_css_selector('.result-list [type="checkbox"]').click()
                find_count -= 1
            elif find_count == 0:
                self.find_element(__SEARCH_LOCATE[__SUBMIT], f"[{__ERROR_CALL}:{__SUBMIT}]").click()
                break

    def exclusion_condition(self, value):
        __ERROR_CALL = "CrawlOneZeroFour.exclusion_condition"
        __SEARCH_LOCATE = self.css_locate['exclusion_condition']
        __TITLE_BUTTON = 'title_button'
        __EXCLUDE_SELECT = 'exclude_select'
        __STYLED_SELECT = 'styled-select'
        self.wait_element(__SEARCH_LOCATE[__TITLE_BUTTON], f"[{__ERROR_CALL}:{__TITLE_BUTTON}]", ec_mode="visi")
        self.find_element(__SEARCH_LOCATE[__TITLE_BUTTON], f"[{__ERROR_CALL}:{__TITLE_BUTTON}]").click()
        self.wait_element(__SEARCH_LOCATE[__STYLED_SELECT], f"[{__ERROR_CALL}:{__STYLED_SELECT}]", ec_mode="visi")
        self.find_element(__SEARCH_LOCATE[__STYLED_SELECT], f"[{__ERROR_CALL}:{__STYLED_SELECT}]").click()

        find_exclude_select = self.find_element(__SEARCH_LOCATE[__EXCLUDE_SELECT], f"[{__ERROR_CALL}:{__EXCLUDE_SELECT}]")

        self.select_element(find_exclude_select, value)

    @property
    def whole_submit(self):
        __ERROR_CALL = "CrawlOneZeroFour.whole_submit"
        __SEARCH_LOCATE = self.css_locate['whole_submit']
        __WHOLE_SUBMIT = 'whole_submit'
        __xWHOLE_SUBMIT = "//body//input[@id='searchSubmit']"
        __JOB_LIST = 'job-list'
        # self.find_element(__SEARCH_LOCATE[__WHOLE_SUBMIT], f"[{__ERROR_CALL}:{__WHOLE_SUBMIT}]").click()
        btn = self.find_element(__xWHOLE_SUBMIT, f"[{__ERROR_CALL}:{__xWHOLE_SUBMIT}]", selector='xpath')
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait_element(__SEARCH_LOCATE[__JOB_LIST], f"[{__ERROR_CALL}:{__JOB_LIST}]", ec_mode="visi")
        return self.page_source()

    @staticmethod
    def write_my_soup(source):
        soup = BeautifulSoup(source, 'html5lib')
        prettify_soup = soup.prettify()
        with open("soup.html", mode="w", encoding="utf8") as soup_file:
            soup_file.write(prettify_soup)

    @staticmethod
    def read_my_soup():
        soup_data = BeautifulSoup(open("soup.html", encoding="utf8"), "html5lib")
        data1 = soup_data.find('main')
        # log.debug(soup.prettify())
        log.debug(data1)

    @staticmethod
    def pq_test(page):
        doc = pq(page)

        for title in doc('.items .title').parent().parent().items():
            log.debug(title)
            log.debug('"' + title.attr['data-cno'] + '"')
            log.debug('"' + f"https://www.104.com.tw/company/{title.attr['data-cno']}?jobsource=m104_hotorder" + '"')

        # title = [re.sub(',', ' _ ', '"' + title.text() + '"') for title in doc('.items .title').items()]
        # title = ['"' + title.text() + '"' for title in doc('.items .title').items()]
        # log.debug(title)

    @staticmethod
    def pq_read_driver(page):
        doc = pq(page)

        # title = [re.sub(',', ' _ ', '"' + title.text() + '"') for title in doc('.items .title').items()]
        title = ['"' + title.text() + '"' for title in doc('.items .title').items()]
        log.debug(title)

        # company = [re.sub(',', ' _ ', '"' + company.text() + '"') for company in doc('li>a>.company').items()]
        company = ['"' + company.text() + '"' for company in doc('li>a>.company').items()]
        log.debug(company)

        # location = [re.sub(',', ' _ ', '"' + location.text() + '"') for location in doc('li>a>p:nth-child(4)').items()]
        location = ['"' + location.text() + '"' for location in doc('li>a>p:nth-child(4)').items()]
        log.debug(location)

        title_link = [f"\"https://m.104.com.tw/{link.attrib['href']}\"" for link in doc('ul.job-list > li > a')]
        log.debug(title_link)

        com_link = ['"' + f"https://www.104.com.tw/company/{title.attr['data-cno']}?jobsource=m104_hotorder" + '"' for title in
                    doc('.items .title').parent().parent().items()]
        log.debug(com_link)

        res = [[t, tl, c, cl, l] for (t, tl, c, cl, l) in zip(title, title_link, company, com_link, location)]
        log.debug(res)

        with open("104.csv", mode='a', encoding='utf8') as f:
            for sub_index in range(len(res)):
                log.info(','.join(res[sub_index]))
                f.write(','.join(res[sub_index]) + '\n')

    def next_page(self):
        __ERROR_CALL = "CrawlOneZeroFour.next_page"
        __SEARCH_LOCATE = self.css_locate['whole_submit']
        __NEXT_PAGE = 'next_page'
        __UL_LIST = 'job-list'

        self.page_scroll_bottom()
        check_next_page = self.wait_element(__SEARCH_LOCATE[__NEXT_PAGE], f"[{__ERROR_CALL}:{__NEXT_PAGE}]", ec_mode="vis", seconds=3)

        log.debug(check_next_page)
        if not check_next_page:
            exit("check_next_page fail")

        self.find_element(__SEARCH_LOCATE[__NEXT_PAGE], f"[{__ERROR_CALL}:{__NEXT_PAGE}]").click()
        return self.page_source()

    def search_area(self, area):
        __ERROR_CALL = "CrawlOneZeroFour.search_area"
        __SEARCH_LOCATE = self.css_locate['search_area']
        __MENU_LIST = 'area_menu'
        __AREA_TW = 'area_tw'
        __TW_LABEL = 'tw_label'
        __AREA_BUTTON = 'area_button'
        js_search_area = "document.getElementById('searchAreaFake').click();"
        # show job cate
        self.execute_script(js_search_area)
        menu_list = self.wait_element(__SEARCH_LOCATE[__MENU_LIST], f"[{__ERROR_CALL}:{__MENU_LIST}]", ec_mode="visi")
        if not menu_list:
            exit("Wait menu_list fail")

        self.find_element(__SEARCH_LOCATE[__AREA_TW], f"[{__ERROR_CALL}:{__AREA_TW}]").click()

        tw_area_list = self.find_element('#area-menu .scd-cate:nth-child(2) > ul:last-child', f"[{__ERROR_CALL}:'tw_area_list']")
        log.debug(tw_area_list)

        tw_label_items = tw_area_list.find_elements_by_tag_name('label')
        # tw_label_items = tw_area_list.find_elements_by_css_selector('.active > span')
        log.debug(tw_label_items)

        find_count = len(area)
        for item in tw_label_items:
            log.debug(item.text)

            if item.text in area:

                try:
                    item.find_element_by_css_selector('.scd-class [type="checkbox"]').click()
                    find_count -= 1
                except ElementClickInterceptedException:
                    wait_checkbox = 0
                    while not wait_checkbox:
                        log.debug("do scroll bottom")
                        self.page_scroll_bottom()
                        wait_checkbox = self.wait_element(f"//span[text()='{area}']", f"[{__ERROR_CALL}:{__MENU_LIST}]", ec_mode="visi",
                                                          selector='xpath')
                        log.debug(wait_checkbox)
                    item.find_element_by_css_selector('.scd-class [type="checkbox"]').click()
                    find_count -= 1

            elif find_count == 0:
                self.find_element(__SEARCH_LOCATE[__AREA_BUTTON], f"[{__ERROR_CALL}:{__AREA_BUTTON}]").click()
                break


if __name__ == "__main__":
    url = "https://m.104.com.tw/search"
    keyword_keys = "auto in test 測試 SDET 程式"
    keyword_keys2 = "auto 測試 in test 自動 SDET Quality 品質 QA SET"
    # work_area = ['台中市'] # for test
    work_area = ['台北市']  # 新北市
    option_value = "全職"
    job_cate_list = ["測試人員", "軟體設計工程師", "軟韌體測試工程師", "電腦組裝／測試"]
    exclude_value = "排除派遣"
    ts_crawlonezerofour = CrawlOneZeroFour("chrome", url, headless=1)
    ts_crawlonezerofour.go_search()
    ts_crawlonezerofour.search_area(work_area)

    ts_crawlonezerofour.exclusion_condition(exclude_value)
    ts_crawlonezerofour.search_keyword(keyword_keys, option_value)
    ts_crawlonezerofour.job_cate(job_cate_list)
    ts_crawlonezerofour.search_keyword(keyword_keys2, option_value)
    current_page = ts_crawlonezerofour.whole_submit
    ts_crawlonezerofour.pq_read_driver(current_page)

    more_page = ts_crawlonezerofour.next_page()
    while more_page:
        ts_crawlonezerofour.pq_read_driver(more_page)
        more_page = ts_crawlonezerofour.next_page()

    ts_crawlonezerofour.driver_close()


    # ts_crawlonezerofour = CrawlOneZeroFour("no_driver")
    # ts_crawlonezerofour.read_csv()
