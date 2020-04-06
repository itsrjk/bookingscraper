from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time



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
    # for every url, scrape the data and add to dictionary
    for url in hotel_urls:
        driver.get(url)
        time.sleep(5)
        print(driver.find_element_by_id('hp_hotel_name').text.strip('Hotel'))
        print(driver.find_element_by_class_name(
        'bui-review-score--end').find_element_by_class_name(
        'bui-review-score__badge').text)


  
def main():
    #misc webdriver options
    options=Options()
    options.add_argument("-headless")
    driver = webdriver.Chrome(options=options)
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





