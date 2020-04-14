from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import selenium.common.exceptions
import time
import math


no_of_hotels=20
no_of_reviews=100
language="English"
city="Kuala Lampur"
headless=True
DEBUG=1
name_of_file="klampur.arff"

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
    hotel_data= []
    hotel_line= [None] * 5
    hotel_line[0]=city
    print("Starting to scrape ", no_of_reviews," reviews for",len(hotel_urls),"hotels...")
    counter=0

    # for every hotel
    for url in hotel_urls:    
        #go to site
        driver.get(url)
        #allowing site to load
        time.sleep(3)
        #get the hotel name
        try:
            hotel_line[1]=(driver.find_element_by_id('hp_hotel_name').text.strip('Hotel').strip().replace("\n"," "))
            if DEBUG: print(counter,") ",hotel_line[1]," : ",end="")
            counter=counter+1
            #get the overall review score 
            hotel_line[2]=(driver.find_element_by_class_name('bui-review-score--end').find_element_by_class_name('bui-review-score__badge').text)
            if DEBUG: print(hotel_line[2])
        except selenium.common.exceptions.NoSuchElementException:
            continue

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
        j=0
        while True:
            reviews=driver.find_elements_by_class_name("review_list_new_item_block")
            for review in reviews:
                #this try except block is to ignore ratings without comment title
                try:
                    #review title
                    hotel_line[3]=review.find_element_by_class_name("c-review-block__title").get_attribute("innerHTML").strip().replace("\n"," ")
                    if DEBUG: print(j,") ",review.find_element_by_class_name("c-review-block__title").get_attribute("innerHTML").strip()," : ",end="")
                    #review score
                    hotel_line[4]=review.find_element_by_class_name("bui-review-score__badge").get_attribute("aria-label").strip("Scored ").strip()
                    if DEBUG: print(hotel_line[4])
                    hotel_data.append(hotel_line[:])
                    j=j+1
                    if j==no_of_reviews:
                        break
                except Exception as e:
                    continue
            # even java has loop naming but python doesn't ;-;
            # this is to check if we're here because of the nested break                 
            if j==no_of_reviews:
                break
            # go to next page
            try:
                driver.find_element_by_class_name("pagenext").click()
            except selenium.common.exceptions.NoSuchElementException:
                break
            time.sleep(3)
        #print("------------")
        write_to_file(hotel_data)
        hotel_data=[]    

def write_to_file(data_to_write):
    f=open(name_of_file,"a")
    print("Writing to file...")
    for line in data_to_write:
        f.write("\""+line[0]+"\"")
        f.write(",")
        f.write("\""+line[1]+"\"")
        f.write(",")
        f.write(line[2])
        f.write(",")
        f.write("\""+line[3]+"\"")
        f.write(",")
        f.write(line[4])
        f.write("\n")
    f.close()

def initialize_file():
    print("initializing arff file")
    create=open(name_of_file,"x")
    create.close()

    header=open(name_of_file,"a")
    header.write("@relation booking.com\n")
    header.write("\n")
    header.write("@attribute city string\n")
    header.write("@attribute hotel_name string\n")
    header.write("@attribute hotel_rating numeric\n")
    header.write("@attribute comment string\n")
    header.write("@attribute comment_rating numeric\n")
    header.write("\n")
    header.write("@data\n")
    header.close()

def main():

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
    #set relation and attributes
    initialize_file()
    #get the urls for each hotel
    hotel_urls=scrape_hotel_urls(driver,no_of_hotels)
    #get data from each hotel
    scrape_hotel_data(driver,hotel_urls,no_of_reviews,language)

if __name__ == "__main__":
    main()





