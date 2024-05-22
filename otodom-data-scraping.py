from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#initiate driver and declare url
driver = webdriver.Chrome()
driver.get("https://www.otodom.pl/")
driver.maximize_window()

# Zamknij przeglądarkę
driver.quit()