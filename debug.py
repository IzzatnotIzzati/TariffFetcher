# Utk trial and error masa testing scrape data dari website TNB

from bs4 import BeautifulSoup as bs
import requests
import json
from functions import *

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

print("\nCollecting cent values:")
for cent in tariffCent:
    cent_text = cent.get_text(strip=True)
    print(f"Value: '{cent_text}'")
    if containsNum(cent_text):
        centList.append({
            'value': cent_text
        })

# Then collect kWh ranges
print("\nCollecting kWh ranges:")
for kWh in tariffkWh:
    kWh_text = kWh.get_text(strip=True)
    print(f"Value: '{kWh_text}'")
    if 'next' in kWh_text or 'first' in kWh_text:
        kWhList.append({
            'range': kWh_text
        })
    else:
        continue


tariffPrices.append({
    'kWh': kWhList,
    'cent': centList
})



tariffPrices = json.dumps(tariffPrices, indent=4)


# debug :( saya pon pening baca, dw
print(centList)
print(kWhList)