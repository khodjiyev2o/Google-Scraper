from lib2to3.pgen2 import driver
import os
from pickle import TRUE
from sre_constants import SUCCESS 
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
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
import time 





class Scraping(webdriver.Chrome):
    def __init__(self, driver_path=const.DRIVER_PATH, teardown=False):
        """options = webdriver.ChromeOptions()
        options.add_argument("start-maximized");
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")"""
        self.driver_path = driver_path
        self.teardown = teardown
        self.product_data = []
        self.url = ''
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
            )[0].find_elements_by_class_name('i0X6df')[0]
        
        #for div in products_list:
         #   try:
        image = products_list.find_element_by_css_selector('a[data-what="0"]')
        image.click()
        self.about_page()
          #  except StaleElementReferenceException:
           #     continue 
                
              
            
            
        print(f"this is product data : {self.product_data}.There are overall : {len(self.product_data)}")

        return products_list    

    def about_page(self):
            WebDriverWait(self,10).until(EC.presence_of_element_located((By.CLASS_NAME, "_-pq")))
            the_links= self.find_elements_by_css_selector("div[class='_-pq']>a")
            links = []
            for link in the_links :
                link = link.get_attribute("href").strip()
                links.append(link)

            for link in links :
                self.get(link)
            try:
               price = self.find_element_by_xpath('//*[@id="sh-osd__online-sellers-cont"]/tr/td[3]/span').get_attribute("innerText").strip()
               print(price)
            except  StaleElementReferenceException:
                WebDriverWait(self,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sh-osd__online-sellers-cont"]/tr/td[3]/span')))
                price = self.find_element_by_xpath('//*[@id="sh-osd__online-sellers-cont"]/tr/td[3]/span').get_attribute("innerText").strip()
                self.back() 
                time.sleep(3)
                print(price)
                
            
            
    # def pagination(self):
    #    while True:
    #         print(f"Processing page ..")
    #         try:
    #             self.products_list()
    #             next_btn = self.find_element_by_id('pnnext')
    #             next_btn.click()
    #         except NoSuchElementException:
    #             print(f"Exiting. Last page !")
    #             break


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
        #time.sleep(3)
        self.url = self.current_url
    