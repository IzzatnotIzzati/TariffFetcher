from textual import on, work
from textual.app import App, ComposeResult
from textual.widgets import *
from asyncScraper import tarriff
from numcheck import containsNum
import json

tariffRates = None

class TariffFetcher(Static):
    """A Textual app to calculate TNB bill based on current tariff rates."""
    
    CSS_PATH = "styles.tcss"

    name = ""
    totalUsage = None
    icptRebate = None
    icptSurcharge = None
    
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Insert name", id="name")
        yield Input(placeholder="Insert total electricity usage in kWh", id="totalUsage")
        yield Input(placeholder="Insert ICPT rate in number for 600kWh and less (rebate)", id="icptRebate")
        yield Input(placeholder="Insert ICPT rate in number for 1500kWh and above (surcharge)", id="icptSurcharge")
        yield Button("Output everything (barf)", id="barf") # button muntah balik semua value yg bru masuk
        with Collapsible(title="Disclaimer*"):
            yield Markdown("""
This calculator is only used as a guide and does not include additional charges such as late payment fee, penalty, etc. Includes hardcoded 8% Service Tax (ST) if usage exceeds 600kWh which may not be accurate in all situations (eg: living in Pulau Langkawi, billing date less than 28 days, etc). This guide follows Tariff A (non-commercial use). Does not include subsidies.
""")
    
        
    @on(Input.Submitted, "#name")
    def setName(self):
        name = self.query_one("#name") # finally working :D
        self.name = str(name.value)
        self.notify(self.name)

    @on(Input.Submitted, "#totalUsage")
    def setUsage(self):
        totalUsage = self.query_one("#totalUsage")
        self.totalUsage = float(totalUsage.value)
        self.notify(str(self.totalUsage))

    @on(Input.Submitted, "#icptRebate")
    def setRebate(self):
        icptRebate = self.query_one("#icptRebate")
        self.icptRebate = float(icptRebate.value)
        self.notify(str(self.icptRebate))

    @on(Input.Submitted, "#icptSurcharge")
    def setSurcharge(self):
        icptSurcharge = self.query_one("#totalUsage")
        self.icptSurcharge = float(icptSurcharge.value)
        self.notify(str(self.icptSurcharge))

    @on(Button.Pressed, "#barf")
    def barf(self):
        self.mount(Markdown(f"""
Name: {self.name}
Usage (kWh): {self.totalUsage}
Rebate: {self.icptRebate}
Surcharge: {self.icptSurcharge}
        """))

    def calculate(self):
        print("placeholder for calculator")


    

                           





class Intro(Static):

    """Introduce user to app"""

    async def on_mount(self) -> None:
        tariffRates = await tarriff()
        if hasattr(tariffRates, 'err') and tariffRates.err is not None:
            self.notify(f"Unable to fetch latest tariff rates. This calculator requires an internet connection. Restart the program once connected to the internet.")
            self.query_one("#tariff-display", Markdown).update("[ERROR] " + str(tariffRates.err))
        else:
            if hasattr(tariffRates, 'result') and tariffRates is not None:
                rates = json.loads(tariffRates.result)
                self.tariffRates = rates
                
                # Tukar jd list markdown
                markdown_content = "## Current TNB Tariff Rates\n\n"
                for rate in self.tariffRates:
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
