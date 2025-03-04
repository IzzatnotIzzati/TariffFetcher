from numcheck import *
from asyncScraper import tarriff
import asyncio
import json


async def main():
    result = await tarriff()
    if hasattr(result, 'err') and result.err is not None:
        print(f"Error: {result.err}")
    else:
        if hasattr(result, 'result') and result.result is not None:
            print(json.loads(result.result))

if __name__ == "__main__":
    asyncio.run(main())

    # i regret using textual for this
    # but i'm too lazy to do that now, forced to learn async >:(
