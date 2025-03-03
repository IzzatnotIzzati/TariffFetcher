from textual import on, work
from textual.app import App, ComposeResult
from textual.widgets import *
from asyncScraper import tarriff
from numcheck import containsNum

class TariffFetcher(Static):
    """A Textual app to calculate TNB bill based on current tariff rates."""
    
    CSS_PATH = "styles.tcss"

    def compose(self) -> ComposeResult:
        yield Label("Placeholder, calculator will be here.")


class Intro(Static):
    """Introduce user to app"""

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
    





class MainApp(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")] 
    
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
    
    @on(Button.Pressed, "#start")
    def start(self):
        # Switch to Main tab
        self.query_one(TabbedContent).active = "calc"

if __name__ == "__main__":
    app = MainApp()
    app.run()