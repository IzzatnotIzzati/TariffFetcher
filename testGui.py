from textual.app import *
from textual.widgets import *

class TariffFetcher(App):
    """A Textual app to calculate TNB bill based on current tariff rates."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    
    CSS_PATH = "styles.tcss"
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        
        with Collapsible(title="Introduction"):
            yield Markdown(
            """

            This app fetches the current tariff rates from the TNB website and calculates the bill based on the given usage \n
            and ICPT rate along with RE fund if any, including tax.

            Press `d` to toggle dark mode, ^Q to quit.
            """
            )
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        yield Footer()
        
        self.theme = (
            "textual-dark"
        
        ) # textual-dark and catppuccin-latte is aestheticcccc <3

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "catppuccin-latte" else "catppuccin-latte"
        )


if __name__ == "__main__":
    app = TariffFetcher()
    app.run()