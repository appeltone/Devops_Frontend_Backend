from selenium import webdriver
from configparser import ConfigParser
import db_connector

config = ConfigParser()
config.read('config.ini')
id_to_search = config.get('front_end_testing', 'id_to_search')
id_expected_to_exist = config.get('front_end_testing', 'id_expected_to_exist')

# get properties from db
base_api_url = db_connector.get_item_from_config_table("api_url")
browser_type = db_connector.get_item_from_config_table("browser_type")

if browser_type == "Chrome":
    driver = webdriver.Chrome("D:\Selenium_Drivers\chromedriver.exe")
else:
    driver = webdriver.Chrome("D:\Selenium_Drivers\geckodriver.exe")

driver.get(base_api_url + "/get_user_data/" + id_to_search)

if id_expected_to_exist == "True":
    web_element = driver.find_element_by_id("user")
    if web_element:
        print("User found:")
        print(web_element.text)
    else:
        print("oopsy, positive test failed")
elif id_expected_to_exist == "False":
    web_element = driver.find_element_by_id("error")
    if web_element:
        print(web_element.text)
    else:
        print("oopsy, negative test failed")

driver.quit()
