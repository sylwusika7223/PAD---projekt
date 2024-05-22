from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#initiate driver and declare url
driver = webdriver.Chrome()
driver.get("https://www.otodom.pl/")
driver.maximize_window()

#accept cookies button
cookies_button = driver.find_element(by=By.XPATH, value='//button[@id="onetrust-accept-btn-handler"]')
cookies_button.click()

#input "Warszawa" as loc
location_input = driver.find_element(By.CSS_SELECTOR, 'button[data-cy="search.form.location.button"]')
location_input.click()

location_search_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.css-15dyjke input[aria-label="Wpisz lokalizację"]'))
)
location_search_box.send_keys("Warszawa")

location_checkbox = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input#mazowieckie\\/warszawa\\/warszawa\\/warszawa'))
)
location_checkbox.click()


driver.quit()