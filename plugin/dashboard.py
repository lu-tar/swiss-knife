from textual.app import App, ComposeResult, RenderResult
from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Static

# Primo widget
class Hello(Widget):
    """Display a greeting."""
    BORDER_TITLE = "Hello Widget"
    def render(self) -> RenderResult:
        return "Hello, [b]World[/b]!"

# Classe di base
class UtilityContainersExample(App):
    CSS_PATH = "utility_containers.tcss"
    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical(classes="column"):
                yield Static("One")
                yield Static("Two")
            with Vertical(classes="column"):
                yield Static("Three")
                yield Static("Four")


if __name__ == "__main__":
    app = UtilityContainersExample()
    app.run()
