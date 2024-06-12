from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# Creating a webdriver instance
driver = webdriver.Chrome("/Users/prakashsingh/Downloads/webdriver_1/chromedriver")
print('3333'*10, driver)
# This instance will be used to log into LinkedIn

# Opening linkedIn's login page
driver.get("https://linkedin.com/uas/login")

# waiting for the page to load
time.sleep(5)

# entering username
username = driver.find_element(By.ID, "username")

# In case of an error, try changing the element
# tag used here.

# Enter Your Email Address
username.send_keys("User_email")

# entering password
pword = driver.find_element(By.ID, "password")
# In case of an error, try changing the element
# tag used here.

# Enter Your Password
pword.send_keys("User_pass")

# Clicking on the log in button
# Format (syntax) of writing XPath -->
# //tagname[@attribute='value']
driver.find_element(By.XPATH, "//button[@type='submit']").click()
# In case of an error, try changing the
# XPath used here.
