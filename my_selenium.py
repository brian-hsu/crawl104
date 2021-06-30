import sys
import time

from selenium.webdriver.support import expected_conditions as EC
from loguru import logger as log
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException, InvalidArgumentException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

# remove default level
log.remove()
log.add(sys.stderr, level="DEBUG", diagnose=True, backtrace=True)


class MySelenium:

    def __init__(self, set_browser, target_url=None, emulation=True, headless=False):
        if set_browser == "no_driver":
            pass
        else:
            log.info("start chrome_driver")
            self.driver = self.chrome_driver(emulation, headless)
            self.url = target_url

    def chrome_driver(self, emulation=1, headless=0):
        log.debug(headless)
        options = webdriver.ChromeOptions()

        options.add_argument('--disable-gpu')
        options.add_argument('--start-maximized')

        if emulation:
            mobile_emulation = {"deviceName": "iPhone 6/7/8 Plus"}
            options.add_experimental_option("mobileEmulation", mobile_emulation)

        if headless:
            log.debug('do headless')
            options.add_argument('--headless')

        try:
            driver = webdriver.Chrome(

                options=options,
                executable_path=ChromeDriverManager().install()
            )
        except SessionNotCreatedException as e:
            log.error(e)
        else:
            return driver

    def driver_get(self,url=0):
        if not url:
            url = self.url
        try:
            self.driver.get(url)
        except InvalidArgumentException as e:
            log.error(e)

    def driver_close(self):
        self.driver.close()
        log.info("Close Web Driver")

    def wait_element(self, element_locator, element_name, selector='css', seconds=5, ec_mode="presence"):
        locator_method = By.CSS_SELECTOR
        if selector != "css":
            locator_method = By.XPATH

        ec_use = EC.presence_of_element_located
        if ec_mode != "presence":
            ec_use = EC.visibility_of_element_located

        i = 0
        while i < 3:
            try:
                wait_element = WebDriverWait(self.driver, seconds).until(
                    ec_use(
                        (locator_method, element_locator)
                    )
                )
                return wait_element
            except TimeoutException:
                i += 1
                log.warning(f'{element_name} is Timeout')
                log.error(f'Fail try {i} count')

        return 0

    def find_element(self, element_locator, element_name, selector='css'):
        locator_method = By.CSS_SELECTOR
        if selector != "css":
            locator_method = By.XPATH

        try:
            return self.driver.find_element(locator_method, element_locator)
        except NoSuchElementException as e:
            log.error(e)
            log.debug(f'{element_name} no such element')

    def find_multi_elements(
            self,
            multi_elements_locator,
            multi_elements_name,
            selector='css'
    ):

        locator_method = By.CSS_SELECTOR
        if selector != "css":
            locator_method = By.XPATH

        try:
            return self.driver.find_elements(locator_method, multi_elements_locator)

        except NoSuchElementException as e:
            log.error(e)
            log.debug(f'{multi_elements_name} no such element')

    @staticmethod
    def select_element(element_found, option_value):
        select = Select(element_found)
        select.select_by_visible_text(option_value)
        # select.select_(option_value)

    def execute_script(self, javascript_document):
        self.driver.execute_script(javascript_document)

    def back_page(self):
        return self.driver.back()

    def page_source(self):
        return self.driver.page_source

    def page_scroll_bottom(self):
        return self.execute_script("window.scrollTo(0, document.body.scrollHeight)")


if __name__ == "__main__":
    ts_my_selenium = MySelenium("chrome")
    ts_my_selenium.driver_get("https://www.google.com")
    time.sleep(2)
    ts_my_selenium.driver_close()
