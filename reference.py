# Utk trial and error masa testing scrape data dari website TNB
# Use as reference utk buat function scraping kat functions.py (or maybe i should js do it here idk)

from bs4 import BeautifulSoup as bs
import requests
import json
from functions import containsNum
from decimal import Decimal

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

#for kWh, cent in zip(tariffkWh, tariffCent):
'''    kWh_text = kWh.get_text(strip=True)
    cent_text = cent.get_text(strip=True)

    if 'next' in kWh_text or 'first' in kWh_text: # alhamdulillah dapat fix
            kWhList.append({
            kWh_text
            })

    if containsNum(cent_text):
        centList.append({
            cent_text
        })''' # tak jalan, so I split them into two separate loops duhhh very un-slay and messy 💅



for cent in tariffCent:
    cent_text = cent.get_text(strip=True)
    if containsNum(cent_text):
        centList.append(cent_text)  # Store as string, not set

for kWh in tariffkWh:
    kWh_text = kWh.get_text(strip=True)
    if 'next' in kWh_text or 'first' in kWh_text:
        kWhList.append(kWh_text)  # Store as string, not set

for kWh, cent in zip(kWhList, centList):
    tariffPrices.append({
        'kWh': kWh,
        'cent': float(Decimal(cent) / Decimal('100')) # hurmm very janky la but it works ig
    })

tariffPrices = json.dumps(tariffPrices, indent=4)

# debug :( saya pon pening baca, dw
#print(centList)
#print(kWhList)
print(tariffPrices)