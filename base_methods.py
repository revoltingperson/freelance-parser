from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


class BaseMethods:
    def __init__(self):
        self.driver = None

    def locate_element(self, locator) -> WebElement:
        locate: WebElement = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))
        return locate

    def locate_visible(self, locator, expiration_time=15) -> WebElement or bool:
        try:
            locate = WebDriverWait(self.driver, expiration_time).until(EC.visibility_of_element_located(locator))
        except Exception:
            pass
        else:
            return locate
        return False

    def locate_elements(self, locator):

        locate = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(locator))
        return locate

    def send_keys(self, locator, keys: str, send_enter=False):
        e = self.locate_element(locator)
        e.send_keys(keys)
        if send_enter:
            e.send_keys(Keys.ENTER)

    def click(self, locator):
        e = self.locate_element(locator)
        e.click()

    def drop_down_selector(self, locator, text: str):
        sel = Select(self.locate_element(locator))
        sel.select_by_visible_text(text)

