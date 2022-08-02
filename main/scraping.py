import os 
from selenium import webdriver
import os
import main.constants as const
from prettytable import PrettyTable
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait






class Scraping(webdriver.Chrome):
    def __init__(self, driver_path=const.DRIVER_PATH, teardown=False):
        """options = webdriver.ChromeOptions()
        options.add_argument("start-maximized");
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")"""
        self.driver_path = driver_path
        self.teardown = teardown
        self.product_data = []
        os.environ["PATH"] += self.driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        super(Scraping, self).__init__(options=options)
        self.implicitly_wait(15)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()
            print("Exiting...")

    

    def products_list(self):
        products_list = self.find_elements_by_class_name(
            'BXIkFb'
            )[0].find_elements_by_class_name('i0X6df')
        for div in products_list:
            product_name = (div.find_element_by_css_selector('div[data-sh-gr="line"]')
                .get_attribute("innerText")
                .strip())
            self.product_data.append(product_name)
        print(self.product_data)
        return products_list    
        
    def land_first_page(self):
        self.get(const.BASE_URL)


    def search(self):
        search_result = self.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
        search_result.send_keys('skincare')
        search_result.submit()

        more_btn = self.find_element_by_xpath('/html/body/div[7]/div/div[4]/div/div[1]/div/div[1]/span/g-popup/div[1]/div')
        more_btn.click()

        shopping_menu = self.find_element_by_xpath('/html/body/div[7]/div/div[6]/div/g-menu/g-menu-item[1]/div/a')
        shopping_menu.click()
    
    