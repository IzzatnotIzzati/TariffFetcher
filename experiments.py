# Utk trial and error masa testing scrape data dari website TNB

from bs4 import BeautifulSoup as bs
import requests
import json

response = requests.get('https://www.tnb.com.my/residential/pricing-tariffs')
soup = bs(response.text, 'html.parser')

# Dapatkan tarif dlm sen/kWh
tariffCent = soup.find_all('td', class_='content', align='center', width='')

# Tareik amnt kWh
tariffkWh = soup.find_all('td', class_='content', valign='top')

# Convert jd JSON list
tariffPrices = []
kWhList = []
centList = []

for kWh, cent in zip(tariffkWh, tariffCent):
    kWh_text = kWh.get_text(strip=True)
    cent_text = cent.get_text(strip=True)

    if 'next' in kWh_text or 'first' in kWh_text: # alhamdulillah dapat fix
        tariffPrices.append({
            'kWh': kWh_text,
            'cent': cent_text
        })

    if cent_text == '' or 'Domestic Tariff' in cent_text or 'sen/kWh' in cent_text:
        continue

def appendTariffPrices(kWh, cent):
        tariffPrices.append({
            'kWh': kWh,
            'cent': cent
        })

tariffPrices = json.dumps(tariffPrices, indent=4)


# debug :( saya pon pening baca, dw
print(tariffPrices + '\n')
print(tariffCent)
print(tariffkWh)