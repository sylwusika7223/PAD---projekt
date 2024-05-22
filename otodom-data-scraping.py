from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#initiate driver and declare url
website = 'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/warszawa?&market=SECONDARY&&limit=72'
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(website)

#accept cookies button
cookies_button = driver.find_element(by=By.XPATH, value='//button[@id="onetrust-accept-btn-handler"]')
cookies_button.click()

#get total number of result sites
total_value = driver.find_element(By.XPATH, '(//li[contains(@class, "css-1tospdx")])[last()]')
total_num = int(total_value.text)
print(total_num)

driver.quit()