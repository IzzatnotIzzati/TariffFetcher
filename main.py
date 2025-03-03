from numcheck import *
from tariffScraper import tarriff
import json

result = tarriff()
if hasattr(result, 'err') and result.err is not None:
    print(f"Error: {result.err}")
else:
    print(result.result)
