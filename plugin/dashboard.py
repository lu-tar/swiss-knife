from textual.app import App, ComposeResult, RenderResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Header, Static
from textual.widget import Widget

class Hello(Widget):
    """Display a greeting."""

    def render(self) -> RenderResult:
        return ("Hi\n")

# Test layout + widget
class CombiningLayoutsExample(App):
    CSS_PATH = "combining_layouts.tcss"

    # on_mount = all'avvio
    def on_mount(self) -> None:
        self.title = "Test bench"
        self.sub_title = "and sub-title"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="app-grid"):
            with Static(id="left-pane"):
                yield Hello()
            
            with Horizontal(id="top-right"):
                yield Static("Horizontally")
                yield Static("Positioned")
                yield Static("Children")
                yield Static("Here")
            
            with Container(id="bottom-right"):
                yield Static("This")
                yield Static("panel")
                yield Static("is")
                yield Static("using")
                yield Static("grid layout!", id="bottom-right-final")


if __name__ == "__main__":
    app = CombiningLayoutsExample()
    app.run()
