from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import selenium.common.exceptions
import time
import math



def choose_city(driver,city):
    search_field = driver.find_element_by_id('ss')
    search_field.send_keys(city)
    driver.find_element_by_class_name('sb-searchbox__button').click()
    wait = WebDriverWait(driver, timeout=10).until(
        EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'sr-hotel__title')))
	
def scrape_hotel_urls(driver):
    #find the hotel class
    hotels_h3 = driver.find_elements_by_class_name('sr-hotel__title')
    hotel_urls=list()

    #get the urls from each hotel
    for hotel in hotels_h3:
        hotel_link=hotel.find_element_by_class_name("hotel_name_link").get_attribute("href")
        hotel_urls.append(hotel_link)
    
    return hotel_urls

def scrape_hotel_data(driver,hotel_urls):
    no_of_reviews=100
    # for every hotel
    for url in hotel_urls:
        #go to site
        driver.get(url)
        #allowing site to load
        time.sleep(2)
        #get the hotel name
        print(driver.find_element_by_id('hp_hotel_name').text.strip('Hotel').strip()," : ",end="")
        #get the overall review score
        print(driver.find_element_by_class_name('bui-review-score--end').find_element_by_class_name('bui-review-score__badge').text)

        #go to the reviews tab
        reviews_button=driver.find_element_by_id("show_reviews_tab")
        reviews_button.click()
        time.sleep(1)

        #select new to old
        select = Select(driver.find_element_by_id('review_sort'))
        select.select_by_value("f_recent_desc")
        time.sleep(1)

        #mine reviews
        no_of_pages=math.ceil(no_of_reviews/10)
        j=1   
        for i in range(0,no_of_pages):
            reviews=driver.find_elements_by_class_name("review_list_new_item_block")
            for review in reviews:
                try:
                    #review title
                    print(j,") ",review.find_element_by_class_name("c-review-block__title").get_attribute("innerHTML").strip()," : ",end="")
                    #review score
                    print(review.find_element_by_class_name("bui-review-score__badge").get_attribute("aria-label").strip("Scored ").strip())
                except selenium.common.exceptions.NoSuchElementException:
                    continue
                j=j+1           
            driver.find_element_by_class_name("pagenext").click()
            time.sleep(2)
        print("------------")        
    driver.quit()


  
def main():
    #misc webdriver options
    options=Options()
    #options.add_argument("-headless")
    driver = webdriver.Chrome(options=options)
    #driver=webdriver.Firefox(options=options)
    #link
    driver.get('https://www.booking.com/')
    #go to city
    choose_city(driver,"Singapore")
    #get the urls for each hotel
    hotel_urls=scrape_hotel_urls(driver)
    #get data from each hotel
    scrape_hotel_data(driver,hotel_urls)

if __name__ == "__main__":
    main()





