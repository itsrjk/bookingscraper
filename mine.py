from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



def choose_city(driver,city):
    search_field = driver.find_element_by_id('ss')
    search_field.send_keys(city)
    driver.find_element_by_class_name('sb-searchbox__button').click()
    wait = WebDriverWait(driver, timeout=10).until(
        EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'sr-hotel__title')))

	
def scrape_hotels(driver):
    #find the hotel class
    hotels = driver.find_elements_by_class_name('sr-hotel__title')
    hotel_urls=list()
    #get the urls from each hotel
    for hotel in hotels:
        hotel_link=hotel.find_element_by_class_name("hotel_name_link").get_attribute("href")
        hotel_urls.append(hotel_link)
    
    
    print(hotel_urls)



options=Options()
options.add_argument("-headless")
driver = webdriver.Chrome(options=options)
driver.get('https://www.booking.com/')
choose_city(driver,"Singapore")

scrape_hotels(driver)



