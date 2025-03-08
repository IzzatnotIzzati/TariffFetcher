# utk testing kira2, reference

from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
tariffRates = [{'kWh': 'For the first 200 kWh (1 - 200 kWh) per month', 'cent': 0.218}, {'kWh': 'For the next 100 kWh (201 - 300 kWh) per month', 'cent': 0.334}, {'kWh': 'For the next 300 kWh (301 - 600 kWh) per month', 'cent': 0.516}, {'kWh': 'For the next 300 kWh (601 - 900 kWh) per month', 'cent': 0.546}, {'kWh': 'For the next kWh (901 kWh onwards) per month', 'cent': 0.571}]
centRate = [item['cent'] for item in tariffRates]

totalUsage = int(input("usage: "))
totalBill = None
taxedAmount = None

# 1-200kWh
if totalUsage <= 200:
    bill = Decimal(totalUsage * centRate[0])
# 201-300kWh
elif totalUsage <= 300:
    bill = Decimal(200 * centRate[0] + (totalUsage - 200) * centRate[1])
# 301-600 kWh
elif totalUsage <= 600:
    bill = Decimal(200 * centRate[0] + 100 * centRate[1] + (totalUsage - 300) * centRate[2])
# 601-900kWh
elif totalUsage <= 900:
    bill = Decimal(200 * centRate[0] + 100 * centRate[1] + 300 * centRate[2] + (totalUsage - 600) * centRate[3])
    taxedAmount = Decimal((totalUsage - 600) * centRate[3])
# >900 kWh
else:
    bill = Decimal(200 * centRate[0] + 100 * centRate[1] + 300 * centRate[2] + 300 * centRate[3] + (totalUsage - 900) * centRate[4])
    taxedAmount = Decimal(300 * centRate[3] + (totalUsage - 900) * centRate[4])

if totalUsage < 600:
    rebate = (Decimal(totalUsage * Decimal(0.02))) # 2 sen for every kwh
    bill = bill - Decimal(rebate)
    print("Rebate amount: ", rebate)
    print("Final amount: ", bill)
elif totalUsage > 600 and totalUsage <= 1500:
    bill = bill # no charge/rebate
elif totalUsage > 1500:
    surcharge = (Decimal(totalUsage * Decimal(0.10)))
    bill = bill - Decimal(surcharge)


if totalUsage > 600: # kira cukai klu lebih 600kwh
    taxedAmount = (taxedAmount * Decimal(1.08)) - taxedAmount
    totalBill = bill + taxedAmount
else:
    totalBill = bill

bill = totalBill # heard it's standards compliant, idk but anyways i like precision :) dont floating point differes between amd and intel anyways, im coding on an amd laptop but cg is gonna test on intel laptop


print(totalBill.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
print("Unrounded: RM", totalBill)










'''
pening woi :( pls dont waste ur time trying to debug logic in class at tui files,
overburdening tnb's servers smh, like who refreshes tariff page for >10 times a day 💀 
(which is why i hardcoded tariffRates var here)
'''
