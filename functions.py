from bs4 import BeautifulSoup as bs
import requests



# Cari tariff TNB
def tarriff():
    url = 'https://www.tnb.com.my/residential/pricing-tariffs'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    tariff = soup.find('td', class_='').text
    print(tariff)
    return float(tariff)
    






def calcBill(tariff, energyUsage):
    return tariff * energyUsage