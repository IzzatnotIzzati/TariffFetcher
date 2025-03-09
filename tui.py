'''
This calculator is too accurate and is not in line with TNB bill. Gets worse the higher the consumption.
'''



from textual import on, work
from textual.app import App, ComposeResult
from textual.widgets import *
from asyncScraper import tarriff
from numcheck import containsNum
import json
from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP

tariffRates = None
name = ""
totalUsage = None
icptRebate = None
icptSurcharge = None

class TariffFetcher(Static):
    """A Textual app to calculate TNB bill based on current tariff rates."""
    
    CSS_PATH = "styles.tcss"

    global name
    global totalUsage
    global icptRebate
    global icptSurcharge
    global tariffRates
    
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Insert name", type="text", id="name")
        yield Input(placeholder="Insert total electricity usage in kWh", type="integer", id="totalUsage")
        yield Input(placeholder="Insert ICPT rate in number for 600kWh and less (rebate, cent)", type="number", id="icptRebate")
        yield Input(placeholder="Insert ICPT rate in number for 1500kWh and above (surcharge, cent)", type="number", id="icptSurcharge")
        yield Button("Save & Calculate", id="barf") # button muntah balik semua value yg bru masuk
        yield Markdown('''
# Bill

Looks like you haven't started the calculation yet. Fill in the form above and click on "Save & Calculate" to begin.
                               
                       ''', id="calcResult")
        
        with Collapsible(title="Disclaimer*"):
            yield Markdown("""
This calculator is only used as a guide and does not include additional charges such as late payment fee, penalty, etc. Includes hardcoded 8% Service Tax (ST) if usage exceeds 600kWh which may not be accurate in all situations (eg: living in Pulau Langkawi, billing date less than 28 days, etc). This guide follows Tariff A (non-commercial use). Does not include subsidies.
""", id="calcResult")
    
        
    @on(Input.Submitted, "#name")
    def setName(self):
        global name
        name = self.query_one("#name") # finally working :D
        name = str(name.value)

    @on(Input.Submitted, "#totalUsage")
    def setUsage(self):
        global totalUsage
        totalUsage = self.query_one("#totalUsage")
        totalUsage = Decimal(totalUsage.value)

    @on(Input.Submitted, "#icptRebate")
    def setRebate(self):
        global icptRebate
        icptRebate = self.query_one("#icptRebate")
        icptRebate = Decimal(icptRebate.value)

    @on(Input.Submitted, "#icptSurcharge")
    def setSurcharge(self):
        global icptSurcharge
        icptSurcharge = self.query_one("#icptSurcharge")
        icptSurcharge = Decimal(icptSurcharge.value)

    @on(Button.Pressed, "#barf")
    def barf(self):
        global name
        global totalUsage
        global icptRebate
        global icptSurcharge
        global tariffRates
        self.setName()
        self.setUsage()
        self.setRebate()
        self.setSurcharge()
        self.calculate()
        
        billAmount = self.calculate()
#        self.mount(Markdown(f"""
        self.query_one("#calcResult", Markdown).update(f"""

# Bill
Name: {name if name else 'N/A'}
- Total Usage: {totalUsage} kWh
- ICPT Rebate Rate: {icptRebate if icptRebate else 'N/A'} cent
- ICPT Surcharge Rate: {icptSurcharge if icptSurcharge else 'N/A'} cent
- RE Fund: {'1.6%' if totalUsage > 300 else 'N/A'}
- SST: {'8%' if totalUsage > 600 else 'N/A'}
- Final Bill Amount: RM {billAmount:.2f}
""")



    def calculate(self) -> float:
        """kira bil guna rates progresif sama dgn kira cukai kat amerika syarikat"""
        global name
        global totalUsage
        global icptRebate
        global icptSurcharge
        global tariffRates
        taxedAmount = Decimal('0')
        # DO NOT WASTE YOUR TIME DEBUGGING THIS HERE, PLS GO TO calcReference.py TO DEBUG
        if totalUsage == None:
            self.notify("Missing usage data")
            return 0.0

        centRate = [Decimal(str(item['cent'])) for item in tariffRates] # YAYYY ITS WORKING, also this is for making list and hace the cent values in decimal so that it works with the calculator below

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

        # Kira ICPT adjustment (rebate, surcharge)
        if totalUsage <= 600:
            rebate = (Decimal(totalUsage * (Decimal(icptRebate) / Decimal(100)) )) # 2 sen for every kwh
            bill = bill - Decimal(rebate)
            print("Rebate amount: ", rebate)
            print("Final amount: ", bill)
        elif totalUsage > 600 and totalUsage <= 1500:
            bill = bill # no charge/rebate
        elif totalUsage > 1500:
            surcharge = (Decimal(totalUsage * (Decimal(icptSurcharge) / Decimal(100))))
            bill = bill + Decimal(surcharge)

        # Kira KWTBB (RE Fund)
        if totalUsage > 300:
            reFundCharge = Decimal(bill * Decimal(0.016)) # 1.6%
            bill = bill + reFundCharge



        if totalUsage > 600: # kira cukai klu lebih 600kwh
            taxedAmount = taxedAmount * Decimal('0.08')  # Calculate 8% tax directly

            totalBill = bill + taxedAmount

        else:
            totalBill = bill

        if totalBill < Decimal(3): #make sure dapat minimum charge
            totalBill = Decimal(3)

        bill = totalBill.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) # heard Decimal is standards compliant, idk but anyways i like precision :) dont floating point differes between amd and intel anyways, im coding on an amd laptop but cg is gonna test on intel laptop

#        self.query_one(Markdown, "#calcResult").update(f'''
# Bill
#
#Bill Details for {name if name else 'N/A'}
#- Total Usage: {totalUsage} kWh
#- ICPT Rebate Rate (cent): {icptRebate if icptRebate else 'N/A'}
#- ICPT Surcharge Rate (cent): {icptSurcharge if icptSurcharge else 'N/A'}
#- RE Fund: {'1.6%' if totalUsage > 300 else 'N/A'}
#- SST: {'8%' if totalUsage > 600 else 'N/A'}
#- Final Bill Amount: RM {bill:.2f}                                             
#
#''')




        return(totalBill.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
        
    





                           





class Intro(Static):

    """Introduce user to app"""

    async def on_mount(self) -> None:
        global tariffRates
        
        tariffRates = await tarriff()
        if hasattr(tariffRates, 'err') and tariffRates.err is not None:
            self.notify(f"Unable to fetch latest tariff rates. This calculator requires an internet connection. Restart the program once connected to the internet.")
            self.query_one("#tariff-display", Markdown).update("[ERROR] " + str(tariffRates.err))
        else:
            if hasattr(tariffRates, 'result') and tariffRates is not None:
                rates = json.loads(tariffRates.result)
                tariffRates = rates
                
                # Tukar jd list markdown
                markdown_content = "## Current TNB Tariff Rates\n\n"
                for rate in tariffRates:
                    markdown_content += f"- **{rate['kWh']}**\n"
                    markdown_content += f"  - Rate: RM {rate['cent']} per kWh\n"
                
                # update
                self.query_one("#tariff-display", Markdown).update(markdown_content)
                self.notify(f"Successfully fetched latest tariffs from TNB!")


    

    def compose(self) -> ComposeResult:
        
        yield Label("Click on any of these options below or select with Tab key to navigate.")
        
        with Collapsible(title="Introduction"):
            yield Markdown(
                """
This app fetches the current tariff rates from the TNB website and calculates the bill based on the given usage and ICPT rate along with RE fund if any, including tax.

Press `d` to toggle dark mode, ^Q to quit.
                """
            )
                    
        with Collapsible(title="Steps to use"):
            yield Markdown(
                """
Click on Start or on the "Calculate" tab to start. Follow the on-screen instructions.
                """
            )
            yield Button("Start", id="start")

        with Collapsible(title="Current tariff rates"):
            yield Markdown("Loading tariff rates...", id="tariff-display")

    

class MainApp(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")] 
    
    @on(Button.Pressed, "#start")
    def start(self):
        # Switch to Main tab
        self.query_one(TabbedContent).active = "calc"
        
    def compose(self) -> ComposeResult:
        yield Header()
        
        with TabbedContent():
            
            with TabPane("Introduction", id="intro"):
        
                yield Intro()
                
            with TabPane("Calculate", id="calc"):
            
                yield TariffFetcher()
        
        yield Footer()

        self.theme = "gruvbox"

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "gruvbox" if self.theme == "catppuccin-latte" else "catppuccin-latte"
        )


if __name__ == "__main__":
    app = MainApp()
    app.run()

