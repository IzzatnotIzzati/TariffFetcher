# Utk trial and error masa testing scrape data dari website TNB

from bs4 import BeautifulSoup as bs
import requests

response = requests.get('https://www.tnb.com.my/residential/pricing-tariffs')
soup = bs(response.text, 'html.parser')

# Dapatkan tarif dlm sen/kWh
tariffCent = soup.find_all('td', class_='content', align='center', width='')

# Tareik amnt kWh
tariffkWh = soup.find_all('td', class_='content', valign='top')

print(tariffkWh)
print(tariffCent)