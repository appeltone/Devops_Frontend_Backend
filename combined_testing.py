from backend_testing import *
from selenium import webdriver
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

id = config.get('back_end_testing', 'id_to_insert')
username = config.get('back_end_testing', 'username_to_insert')
url = config.get('back_end_testing', 'rest_api_base_url') + id
json_payload = {'user_name': username}
is_new_user = True

# test backend
if (run_post_add_user_request(url, json_payload, id, is_new_user)):
    print("Successful - POST request with ID " + id + " and username " + username + " successful")

if (run_get_request(url, id)):
    print("Successful - GET request with ID " + id + " returned username " + username)

if (check_user_added_to_db(username, id)):
    print("Successful - username " + username + " inserted to DB - !!! yeppee")

# test frontend - verify user is added by webelement locator
driver = webdriver.Chrome("D:\Selenium_Drivers\chromedriver.exe")
driver.get("http://127.0.0.1:5001/users/get_user_data/" + id)

if is_new_user:
    web_element = driver.find_element_by_id("user")
    if web_element and web_element.text == username:
        print("User found using Selenium element locator: ")
        print("-------------------------------------------")
        print(web_element.text)
    else:
        raise Exception("test failed")

driver.quit()
