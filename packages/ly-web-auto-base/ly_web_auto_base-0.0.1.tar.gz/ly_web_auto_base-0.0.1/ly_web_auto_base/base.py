from selenium.webdriver.support.wait import WebDriverWait
import time


class Base:

    def __init__(self, driver):
        self.driver = driver

    def base_find_element(self, loc, timeout=30, poll=0.5):
        return WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll)\
                .until(lambda x: x.find_element(*loc))

    def base_find_elements(self, loc, timeout=30, poll=0.5):
        return WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll)\
                .until(lambda x: x.find_elements(*loc))

    def base_send_keys(self, loc, value):
        element = self.base_find_element(loc)
        element.clear()
        element.send_keys(value)

    def base_click(self, loc):
        self.base_find_element(loc).click()

    def base_decide_element(self, loc, wait_time=10):
        try:
            self.base_find_element(loc, wait_time)
            return True
        except:
            return False

    def base_screenshot(self):
        self.driver.get_screenshot_as_file("../images/{}".format(time.strftime("%Y-%m-%d %H:%M:%S")))

    def base_get_text(self, loc):
        return self.base_find_element(loc).text

    def base_get_attribute(self, loc, name="href"):
        return self.base_find_element(loc).get_attribute(name)

    def base_get_url(self):
        return self.driver.current_url

    def base_back(self):
        self.driver.back()

    def base_get_title(self):
        return self.driver.title

    def base_switch_windows(self, title):
        for windows in self.driver.window_handles:
            self.driver.switch_to_window(windows)
            if title in self.base_get_title():
                break
            time.sleep(0.5)

    def base_close_current_window(self):
        self.driver.close()

    def base_implement_js(self, js):
        self.driver.execute_script(js)

    def base_get_modular_text(self, loc):
        contents = []
        elements = self.base_find_elements(*loc)
        for element in elements:
            contents.append(element.text)
        return contents

    def base_get_current_location(self):
        current_location_js = "document.documentElement.scrollTop"
        return self.base_implement_js(current_location_js)

    def base_decide_element_is_enable(self, loc):
        return self.base_find_element(loc).is_enabled()

    def base_list_get_next_page_state(self, loc):
        if self.base_get_attribute(loc, "class").rfind("layui-disabled") == -1:
            return False
        return True
