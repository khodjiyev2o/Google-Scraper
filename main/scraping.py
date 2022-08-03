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
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException,TimeoutException
import time 
import json
 
 





class Scraping(webdriver.Chrome):
    def __init__(self, driver_path=const.DRIVER_PATH, teardown=False):
        """options = webdriver.ChromeOptions()
        options.add_argument("start-maximized");
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")"""
        self.driver_path = driver_path
        self.teardown = teardown
        self.product_data = {}
        self.product_name = ''
        self.reviews_list = []
        self.short_messages = []
        self.overall_rating = ''
        self.price = ''
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
        try:
            all_reviews_link = self.find_element_by_xpath('/html/body/div[3]/div[2]/div/section[1]/div[2]/div/a')
            WebDriverWait(self,10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div/section[1]/div[2]/div/a')))
            all_reviews_link.click()
            self.allreviews()
            
        except NoSuchElementException:
            print('review page is not present in this product!')
            
    
          #  except StaleElementReferenceException:
           #     continue 
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
               el = self.find_elements_by_css_selector("div[class='LDQll']>span")[0]
               self.product_name = el.text
               self.product_data['self.product_name'] = self.product_name
               self.price = self.find_elements_by_class_name('drzWO')[0].text
               print(self.price)
               self.price = self.price.replace(u'\xa0', u' ')
               self.product_data['price'] = self.price

               self.overall_rating = self.find_elements_by_class_name('uYNZm')[0].text
               self.product_data['overall_rating'] = self.overall_rating
            except  StaleElementReferenceException:
                WebDriverWait(self,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="sh-osd__online-sellers-cont"]/tr/td[3]/span')))
                price = self.find_element_by_xpath('//*[@id="sh-osd__online-sellers-cont"]/tr/td[3]/span').text
                self.back() 
                time.sleep(3)
                
            
    def reviews(self):
        reviews_container = self.find_element_by_id(
            'sh-rol__reviews-cont'
            ).find_elements_by_class_name('z6XoBf')
        for review in reviews_container:
            message = review.find_elements_by_class_name('P3O8Ne')[0].text
            full_review = review.find_elements_by_class_name('g1lvWe')[0].text
            self.reviews_list.append(full_review)
            self.short_messages.append(message)
        self.product_data['reviews'] = self.reviews_list
        self.product_data['short_messages'] = self.short_messages
        print(f"this is {self.product_name}  : it costs {self.price} with rating {self.overall_rating}")    
        
        # Serializing json
     
            # Join new_data with file_data inside emp_details
           
    def allreviews(self):
        while True:
            print(f"Processing all reviews ..")
            try:
                self.reviews()
                WebDriverWait(self,10).until(EC.presence_of_element_located((By.CLASS_NAME, 'sh-btn__background')))
                
                more_btn = self.find_elements_by_class_name('sh-btn__background')[0]
                more_btn.click()
            except NoSuchElementException:
                print(f"Exiting. Last page !")
                break
            except IndexError:
                print(f"Exiting. Last page !")
                break
            except StaleElementReferenceException:
                print(f"Exiting. Last page !")
                break
            except TimeoutException:
                print(f"Exiting. Last page !")
                break


    def write_json(self):
        print(f"product name :{self.product_name}")
        print(f"product price :{self.price}")
        print(f"short_messages  :{self.short_messages}")
       
        # json_dump = json.dumps(self.product_data)

        # with open('data.json','w') as file:
        #     # First we load existing data into a dict.
        #    file.write(json_dump)
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
        # function to add to JSON
    
        
    
   