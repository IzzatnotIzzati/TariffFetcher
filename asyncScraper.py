from bs4 import BeautifulSoup as bs
import aiohttp
import json
from decimal import Decimal
from numcheck import containsNum
import asyncio

class TariffResult:
    def __init__(self):
        self.result = None
        self.err = None

async def tarriff():  # fetch and return latest tariff
    tariff = TariffResult()
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.tnb.com.my/residential/pricing-tariffs') as response:
                html = await response.text()
                
        soup = bs(html, 'html.parser')

        # Get tariff in sen/kWh
        tariffCent = soup.find_all('td', class_='content', align='center', width='')

        # Get kWh amounts
        tariffkWh = soup.find_all('td', class_='content', valign='top')

        # Convert to JSON list
        tariffPrices = []
        kWhList = []
        centList = []

        for cent in tariffCent:
            cent_text = cent.get_text(strip=True)
            if containsNum(cent_text):
                centList.append(cent_text)

        for kWh in tariffkWh:
            kWh_text = kWh.get_text(strip=True)
            if 'next' in kWh_text or 'first' in kWh_text:
                kWhList.append(kWh_text)

        for kWh, cent in zip(kWhList, centList):
            tariffPrices.append({
                'kWh': kWh,
                'cent': float(Decimal(cent) / Decimal('100'))
            })

        tariff.result = json.dumps(tariffPrices, indent=4)
        return tariff

    except Exception as err:
        tariff.err = str(err)
        return tariff
    