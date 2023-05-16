from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class SeleniumTests:
    def __init__(self, webdriver: webdriver.Safari) -> None:
        self._driver = webdriver

    def run(self):
        self.__check_authorization()
        self.__order_existing_stuff()
        self.__check_stuff_addition()

    def __check_authorization(self):
        base_url = 'http://127.0.0.1:5555/pages/index.html'
        self._driver.get(base_url)

        time.sleep(0.5)

        login = self._driver.find_element(value='email')
        password = self._driver.find_element(value='password')
        button = self._driver.find_element(by=By.CLASS_NAME, value='buttonLogIn')
        assert(login is not None)
        assert(password is not None)
        assert(button is not None)

        login.clear()
        login.send_keys('Nice man')
        password.clear()
        password.send_keys('Bad password')
        button.send_keys(Keys.ENTER)
        time.sleep(0.5)
        self._driver.switch_to.alert.accept()

        assert(self._driver.current_url == base_url)

        login.clear()
        login.send_keys('thyheart')
        password.clear()
        password.send_keys('YANABUDGETE')
        button.send_keys(Keys.ENTER)
        time.sleep(0.5)
        self._driver.switch_to.alert.accept()
        time.sleep(0.5)
        success_url = 'http://127.0.0.1:5555/pages/managerStorage.html'
        assert(self._driver.current_url == success_url)

    def __order_existing_stuff(self):
        addProduct = self._driver.find_element(by=By.CLASS_NAME, value='addPr')
        addProduct.send_keys(Keys.ENTER)
        time.sleep(0.5)

        category = self._driver.find_element(by=By.NAME, value='categorAddProduct')
        name = self._driver.find_element(by=By.NAME, value='detailsAddProduct')
        count = self._driver.find_element(by=By.NAME, value='costAddProduct')
        cost = self._driver.find_element(by=By.NAME, value='countAddProduct')
        button = self._driver.find_element(by=By.CLASS_NAME, value='btnAddProductToDB')

        assert(category is not None)
        assert(name is not None)
        assert(count is not None)
        assert(button is not None)
        assert(cost is not None)

        category.clear()
        name.clear()
        count.clear()
        cost.clear()
        category.send_keys('Табличка')
        name.send_keys('каменная')
        count.send_keys('5000')
        cost.send_keys('5')

        button.send_keys(Keys.ENTER)
        time.sleep(0.5)

        self._driver.switch_to.alert.accept()

    def __check_stuff_addition(self):
        order_stuff_href = self._driver.find_element(by=By.PARTIAL_LINK_TEXT, value='Заказать товары')
        order_stuff_href.send_keys(Keys.ENTER)
        time.sleep(0.5)

        category = self._driver.find_element(by=By.CLASS_NAME, value='categoryInput')
        name = self._driver.find_element(by=By.CLASS_NAME, value='nameProduct')
        count = self._driver.find_element(by=By.CLASS_NAME, value='countProduct')
        button = self._driver.find_element(by=By.CLASS_NAME, value='btnOrder')
        assert(category is not None)
        assert(name is not None)
        assert(count is not None)
        assert(button is not None)

        category.clear()
        name.clear()
        count.clear()
        category.send_keys('Гробищще')
        name.send_keys('Новый')
        count.send_keys('5')
        button.send_keys(Keys.ENTER)
        time.sleep(0.5)
        
        self._driver.switch_to.alert.accept()
        
if __name__ == '__main__':
    # driver = webdriver.Safari('./safaridriver')
    driver = webdriver.Safari()
    # driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',desired_capabilities={'browserName':'safari','version':'safariversion','platform':'MAC'})
    driver.maximize_window()

    SeleniumTests(driver).run()

    driver.close()
    print('ALL PASSED')