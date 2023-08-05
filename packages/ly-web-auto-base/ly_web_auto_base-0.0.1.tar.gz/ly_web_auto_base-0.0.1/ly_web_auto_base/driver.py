from selenium import webdriver


class Driver:

    driver = None

    @classmethod
    def get_driver(cls):
        if cls.driver is None:
            cls.driver = webdriver.Chrome()
            cls.driver.maximize_window()
        return cls.driver

    @classmethod
    def quit_driver(cls):
        if cls.driver is not None:
            cls.driver.quit()
        cls.driver = None
