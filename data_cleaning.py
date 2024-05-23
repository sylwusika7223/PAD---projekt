import pandas as pd
import requests
import re

#wczytanie scrapowanych danych
file_path = 'otodom-data.xlsx'
df = pd.read_excel(file_path)
df.columns = [col.strip() for col in df.columns]


#czyszczenia nazw lokalizacji (skróty)
def clean_location(location):
    location = re.sub(r'\bPrzy\b', '', location, flags=re.IGNORECASE)
    location = re.sub(r'\bAleje?\b', 'al.', location, flags=re.IGNORECASE)
    location = re.sub(r'\b(?:Aleja|aleje|Aleje)\b', 'al.', location)
    location = re.sub(r'\bulica\b', 'ul.', location, flags=re.IGNORECASE)
    location = re.sub(r'\bplacu?\b|\bPlac\b', 'pl.', location, flags=re.IGNORECASE)
    return location

df['Location'] = df['Location'].apply(clean_location)

#usunięcie powtórzeń po zamianie na skróty
df['Location'] = df['Location'].replace(r'\b(ul\.|al\.|pl\.) (\1)+', r'\1', regex=True)

#rozdzielenie na oddzielne części "Street", "Urban area", "District"
df[['Street', 'Urban area', 'District']] = df['Location'].str.split(', ', n=2, expand=True)

#regex żeby dopasować 'ul.', 'al.', or 'pl.' jako "Street"
street_pattern = re.compile(r'\b[Uu][Ll][.]?\b|\b[Aa][Ll][.]?\b|\b[Pp][Ll][.]?\b')

#dodatkowe rozdzielenie na podstawie "/" (błędny format danych wejściowych pobranych ze strony)
df[['Street', 'Urban area', 'District']] = df.apply(
    lambda row: row['Location'].split('/') if len(row['Location'].split(', ')) == 1 else row[['Street', 'Urban area', 'District']],
    axis=1, result_type='expand'
)

df['Street'] = df.apply(lambda row: '' if (not street_pattern.search(row['Location']) and not re.search(r'\d{1,3}$', row['Location'])) else row['Street'], axis=1)
df['Urban area'] = df.apply(lambda row: row['Location'].split(', ')[0] if (not street_pattern.search(row['Location']) and not re.search(r'\d{1,3}$', row['Location'])) else row['Urban area'], axis=1)
df[['District', 'Rest']] = df['District'].str.split(', ', n=1, expand=True)

df = df.drop(columns=['Location', 'Rest'])

#zamiana dzielnic (błędne nazwy danych wejściowych pobranych ze strony)
district_replacements = {
    "warszawski zachodni": "Warszawa",
    "Błonia Wilanowskie": "Wilanów",
    "piaseczyński": "Wilanów",
    "Sadyba": "Mokotów",
    "Augustówka": "Mokotów",
    "Chrzanów": "Bemowo",
    "Lesznowola": "Piaseczno",
    "Kobiałka": "Białołęka",
    "mazowieckie": "wołomiński",
    "Młynów": "Wola",
    "Muranów": "Śródmieście",
    "Niedźwiadek": "Ursus",
    "Nowolipki": "Wola",
    "Szamoty": "Ursus",
    "Urlychów": "Wola",
    "Wyględów": "Mokotów",
    "Żerań": "Białołęka"
}

df['District'] = df['District'].replace(district_replacements)

#pobieranie kursu walut (API NBP)
def get_exchange_rate(currency_code):
    url = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency_code}/?format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['rates'][0]['mid']
    else:
        return None

usd_to_pln = get_exchange_rate('usd')
eur_to_pln = get_exchange_rate('eur')

def convert_to_pln(price):
    if 'USD' in price:
        return float(price.replace('USD', '').replace(',', '.')) * usd_to_pln
    elif 'EUR' or '€' in price:
        return float(price.replace('EUR', '').replace('€', '').replace(',', '.')) * eur_to_pln
    else:
        return float(price.replace('PLN', '').replace(',', '.'))

#konwersja typów kolumn
df['Currency'] = df['Price'].apply(lambda x: 'USD' if 'USD' in x else ('EUR' if 'EUR' in x else 'PLN'))
df['Price'] = df['Price'].apply(convert_to_pln)

df['Price per m2'] = df['Price per m2'].str.replace(r'/m²', '')
df['Price per m2'] = df['Price per m2'].apply(convert_to_pln)

df['Price'] = df['Price'].apply(lambda x: f"{x:.2f} PLN")
df['Price per m2'] = df['Price per m2'].apply(lambda x: f"{x:.2f} PLN")

df['Rooms'] = df['Rooms'].str.extract('(\d+)').astype(int)

df['m2'] = df['m2'].str.replace(' m²', '').str.replace(',', '.').astype(float)

df['Floor'] = df['floor'].replace({'parter': 0})
df['Floor'] = df['Floor'].str.extract('(\d+)').astype(float)

#rozdzielenie kolumny wystawcy ogłoszenia - podział na ogłoszenia prywatne i biura nieruchomości
df[['Seller name', 'Seller type']] = df['Seller'].str.split(', ', n=1, expand=True)
df['Seller type'] = df['Seller type'].apply(lambda x: 'Biuro nieruchomości' if x == 'Biuro nieruchomości' else 'Oferta prywatna')
df['Estate agency'] = df.apply(lambda row: row['Seller name'] if row['Seller type'] == 'Biuro nieruchomości' else '', axis=1)

#ustalenie kolejności tabel na wyjściu
df = df[['Street', 'Urban area', 'District', 'm2', 'Rooms', 'Floor', 'Price', 'Price per m2', 'Currency', 'Seller type', 'Estate agency']]

#zapis do pliku
output_path = 'cleaned_data.xlsx'
df.to_excel(output_path, index=False, float_format='%g')

print(f'Dane zostały oczyszczone i zapisane do pliku: {output_path}')
