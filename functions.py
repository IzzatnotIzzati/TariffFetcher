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

def containsNum(inputString):
    result = any(char.isdigit() or char == '.' for char in inputString)
    #print(f"Checking '{inputString}': {result}")  # hurm masatu 57.10 x lepas so kna tambah ni
    return result
    






def calcBill(tariff, energyUsage):
    return tariff * energyUsage