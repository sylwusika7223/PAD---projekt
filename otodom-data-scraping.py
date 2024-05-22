from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def write_to_excel(file, df, sheet_name):
    with pd.ExcelWriter(file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer: 
        df.to_excel(writer, index=False, sheet_name=sheet_name)

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

#lists to store data
location = []
prices = []
urls = []
offer_details = []
seller = []

#running the scraping func on each page
i = 1
while i <= 3:
    print('Working on page ' + str(i) + ' of ' + str(total_num))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    #the standard offer container without ptomoted ones
    listings_container = driver.find_element(By.CSS_SELECTOR, 'div[data-cy="search.listing.organic"]')
    
    #all offers list
    listings = listings_container.find_elements(By.CSS_SELECTOR, 'article[data-cy="listing-item"]')

    for listing in listings:
        #Price
        try:
            price_element = listing.find_element(By.CSS_SELECTOR, 'span.css-1uwck7i.e1a3ad6s0')
            price = price_element.text
        except:
            price = None
        prices.append(price)

        #Loc
        try:
            location_element = listing.find_element(By.CSS_SELECTOR, 'p.css-1dvtw4c.e12u5vlm0')
            location_text = location_element.text
        except:
            location_text = None
        location.append(location_text)

        #Url
        try:
            url_element = listing.find_element(By.CSS_SELECTOR, 'a[data-testid="listing-item-link"]')
            url = url_element.get_attribute('href')
        except:
            url = None
        urls.append(url)

        #Details
        try:
            details_element = listing.find_element(By.CSS_SELECTOR, 'div.css-1c1kq07.e12r8p6s0')
            details = details_element.find_elements(By.CSS_SELECTOR, 'dd')
        except:
            details = None
            
        offer_details.append(details)

        #Seller type and name
        try:
            seller_element = listing.find_element(By.CSS_SELECTOR, 'div.css-7rx3ki.e1ipr7st2')
            seller_name = seller_element.find_element(By.CSS_SELECTOR, 'div[data-testid="listing-item-owner-name"]').text
            seller_type = seller_element.find_element(By.CSS_SELECTOR, 'div.css-196u6lt.e1ipr7st4').text
            seller_info = f"{seller_name}, {seller_type}"
        except:
            try:
                seller_element = listing.find_element(By.CSS_SELECTOR, 'div.css-7rx3ki.e1ipr7st2')
                seller_info = seller_element.text
            except:
                seller_info = None

        seller.append(seller_info)
    i += 1

#check - length of the lists
print("Długość lokalizacji:", len(location))
print("Długość cen:", len(prices))
print("Długość linków:", len(urls))
print("Długość szczegółów:", len(details))
print("Długość sprzedawców:", len(seller))

#check - sample data
print("Lokalizacja:", location)
print("Ceny:", prices)
print("Linki:", urls)
print("Szczegóły:", details)
print("Sprzedawca:", seller)

#convert the lists into a dataframe
data = {'Location': location, 'Price': prices, 'Details': offer_details, 'URL': urls, 'Seller': seller}
df = pd.DataFrame(data)

#write df (data) to excel file
df.to_excel('otodom-date.xlsx', index=False)

driver.quit()