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

    print("Starting scrape for city : ",city)

    time.sleep(3)
	
def scrape_hotel_urls(driver,no_of_hotels):
    #why am i sorting by distance from city centre?
    #cause booking.com puts a shamelessly sponsored property of each result on top ffs
    driver.find_element_by_link_text("Distance from city centre").click()
    time.sleep(3)
    hotel_urls=list()
    i=0

    print("Getting hotel urls...")

    while True:
        hotels_h3 = driver.find_elements_by_class_name('sr-hotel__title')
        #get the urls from each hotel
        for hotel in hotels_h3:
            hotel_link=hotel.find_element_by_class_name("hotel_name_link").get_attribute("href")
            hotel_urls.append(hotel_link)
            i=i+1
            if i==no_of_hotels:
                return hotel_urls
        driver.find_element_by_xpath("//*[@title='Next page']").click()
        time.sleep(3)

def scrape_hotel_data(driver,hotel_urls,no_of_reviews,language):

    print("Starting to scrape ", no_of_reviews," reviews for",len(hotel_urls),"hotels...")

    # for every hotel
    for url in hotel_urls:    
        #go to site
        driver.get(url)
        #allowing site to load
        time.sleep(3)
        #get the hotel name
        print(driver.find_element_by_id('hp_hotel_name').text.strip('Hotel').strip()," : ",end="")
        #get the overall review score
        print(driver.find_element_by_class_name('bui-review-score--end').find_element_by_class_name('bui-review-score__badge').text)

        #go to the reviews tab
        reviews_button=driver.find_element_by_id("show_reviews_tab")
        reviews_button.click()
        time.sleep(3)

        #filter by new to old
        select = Select(driver.find_element_by_id('review_sort'))
        select.select_by_value("f_recent_desc")
        time.sleep(3)

        #filter by language
        #driver.find_element_by_class_name("bui-input-checkbutton").click()

        #scrape reviews
        j=1  
        while True:
            reviews=driver.find_elements_by_class_name("review_list_new_item_block")
            for review in reviews:
                #this try except block is to ignore ratings without comment title
                try:
                    #review title
                    print(j,") ",review.find_element_by_class_name("c-review-block__title").get_attribute("innerHTML").strip()," : ",end="")
                    #review score
                    print(review.find_element_by_class_name("bui-review-score__badge").get_attribute("aria-label").strip("Scored ").strip())
                    j=j+1
                    if j==no_of_reviews+1:
                        break
                #except selenium.common.exceptions.NoSuchElementException:
                except Exception as e:
                    continue
            # even java has loop naming but python doesn't ;-;
            # this is to check if we're here because of the nested break                 
            if j==no_of_reviews+1:
                break
            # go to next page
            driver.find_element_by_class_name("pagenext").click()
            time.sleep(3)
        print("------------")

def main():

    no_of_hotels=20
    no_of_reviews=100
    language="English"
    city="Singapore"
    headless=False

    #webdriver options
    options=Options()
    options.add_argument("-headless") if headless else options
    driver = webdriver.Chrome(options=options)
    
    print("Starting chrome...")

    #this tool only works for booking.com
    driver.get('https://www.booking.com/')

    print("Opened booking.com")

    #set whatever values needed
    choose_city(driver,city)

    #get the urls for each hotel
    hotel_urls=scrape_hotel_urls(driver,no_of_hotels)
    #get data from each hotel
    scrape_hotel_data(driver,hotel_urls,no_of_reviews,language)

if __name__ == "__main__":
    main()





