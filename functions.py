from bs4 import BeautifulSoup as bs
import requests
import json
from decimal import Decimal






def containsNum(inputString):
    result = any(char.isdigit() or char == '.' for char in inputString)
    #print(f"Checking '{inputString}': {result}")  # hurm masatu 57.10 x lepas so kna tambah ni
    return result

