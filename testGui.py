from textual import on
from textual.app import *
from textual.widgets import *

class TariffFetcher(App):
    """A Textual app to calculate TNB bill based on current tariff rates."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    
    CSS_PATH = "styles.tcss"
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        
        with TabbedContent():
            with TabPane("Introduction"):
                
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
            
            
            with TabPane("Main"):
                yield Markdown("JESSICA")
            with TabPane("Paul"):
                yield Markdown("PAUL")
        
        

        

        



        
        
        
        
        
        
        
        
        
        
        
        
        
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
        """Start the app."""



if __name__ == "__main__":
    app = TariffFetcher()
    app.run()