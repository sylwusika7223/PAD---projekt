from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd

def write_to_excel(file, df, sheet_name):
    with pd.ExcelWriter(file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer: 
        df.to_excel(writer, index=False, sheet_name=sheet_name)

#main scraping function
def scrape():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    #the standard offer container without ptomoted ones
    listings_container = driver.find_element(By.CSS_SELECTOR, 'div[data-cy="search.listing.organic"]')
    
    #all offers on site
    listings = listings_container.find_elements(By.CSS_SELECTOR, 'article[data-cy="listing-item"]')

    for listing in listings:
        #price
        try:
            price_element = listing.find_element(By.CSS_SELECTOR, 'span.css-1uwck7i.e1a3ad6s0')
            price = price_element.text
        except:
            price = None
        prices.append(price)

        #loc
        try:
            location_element = listing.find_element(By.CSS_SELECTOR, 'p.css-1dvtw4c.e12u5vlm0')
            location_text = location_element.text
        except:
            location_text = None
        location.append(location_text)

        #url
        try:
            url_element = listing.find_element(By.CSS_SELECTOR, 'a[data-testid="listing-item-link"]')
            url = url_element.get_attribute('href')
        except:
            url = None
        urls.append(url)

        #details
        try:
            details_element = listing.find_element(By.CSS_SELECTOR, 'div.css-1c1kq07.e12r8p6s0')
            details = details_element.find_elements(By.CSS_SELECTOR, 'dd')
            rooms_text = details[0].text if len(details) > 0 else None
            m2_text = details[1].text if len(details) > 1 else None
            m2_price_text = details[2].text.replace(' ', '').replace('zł/m²', '') if len(details) > 2 else None
            floor_text = details[3].text if len(details) > 3 else None
        except:
            rooms_text = None
            m2_text = None
            m2_price_text = None
            floor_text = None

        rooms.append(rooms_text)
        m2.append(m2_text)
        m2_price.append(m2_price_text)
        floor.append(floor_text)

        #seller type and name
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

    #click the next page button
    next_page_button = driver.find_element(By.CSS_SELECTOR, 'li.css-gd4dj2:last-child')
    actions = ActionChains(driver)
    actions.move_to_element(next_page_button).click().perform()
    time.sleep(5)


#initiate driver and declare url
website = 'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/warszawa?&market=SECONDARY&&limit=72'
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(website)

time.sleep(2)

#accept cookies button
cookies_button = driver.find_element(by=By.XPATH, value='//button[@id="onetrust-accept-btn-handler"]')
cookies_button.click()

#get total number of result sites
total_value = driver.find_element(By.XPATH, '(//li[contains(@class, "css-1tospdx")])[last()]')
total_num = int(total_value.text)

#lists to store data
location = []
prices = []
m2_price = []
rooms = []
m2 = []
floor = []
urls = []
seller = []

#running the scraping func on each page
i = 1
while i <= total_num:
    print('Working on page ' + str(i) + ' of ' + str(total_num))
    try: 
        scrape()
    except Exception as e:
        print(e)
        pass
    i += 1

#check - length of the lists
print("Długość lokalizacji:", len(location))
print("Długość cen:", len(prices))
print("Długość cen za m2:", len(m2_price))
print("Długość liczby pokojów:", len(rooms))
print("Długość metrażu:", len(m2))
print("Długość piętra:", len(floor))
print("Długość linków:", len(urls))
print("Długość sprzedawców:", len(seller))

#check - sample data
print("Lokalizacja:", location)
print("Ceny:", prices)
print("Cena za m2:", m2_price)
print("Pokoje:", rooms)
print("Metraż:", m2)
print("Piętro:", floor)
print("Linki:", urls)
print("Sprzedawca:", seller)

#convert the lists into a dataframe
data = {'Location': location, 'Price': prices, 'Price per m2': m2_price, 'Rooms': rooms, 'm2': m2 , 'floor': floor , 'URL': urls, 'Seller': seller}
df = pd.DataFrame(data)

#write df (data) to excel file
df.to_excel('otodom-data.xlsx', index=False)

driver.quit()