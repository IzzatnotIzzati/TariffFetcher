from textual import on, work
from textual.app import *
from textual.widgets import *
from tariffScraper import *
from numcheck import *

class TariffFetcher(App):
    from tariffScraper import tarriff
    
    """A Textual app to calculate TNB bill based on current tariff rates."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    
    CSS_PATH = "styles.tcss"

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    @work
    async def retrieve_data(self):
        """Retrieve data from the TNB website."""

        data = await self.tarriff()
        self.tariff.result = data

        if self.tariff.result is None:
            self.notify(self.tariff().err)
        else:
            self.notify(self.tariff().result)


    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        
        yield Header()
        
        

        with TabbedContent():
            
#             Introduction tab ################################

            with TabPane("Introduction", id="intro"):
                
                yield Label ("Click on any of these options below or select with Tab key to navigate.")
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
            
#             Main tab 
            
            with TabPane("Calculate", id="main"):
                
                yield Markdown("In construction 🚧🏗👷‍♂️")
                
                yield Button("Retrive JSON data", id="retrive")


                
        
        
        yield Footer()
        
        self.theme = (
            "textual-dark"
        
        ) # textual-dark and catppuccin-latte is aestheticcccc <3

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "catppuccin-latte" else "catppuccin-latte"
        )

    @on(Button.Pressed, "#start")
    def start(self):
        # Switch to Main tab
        self.query_one(TabbedContent).active = "main"

    @on(Button.Pressed, "#retrive")
    def retrive(self):
        yield Label("Fetching data...")
        yield Label(tarriff())
        yield Label("Data fetched successfully.")

        




        










if __name__ == "__main__":
    app = TariffFetcher()
    app.run()