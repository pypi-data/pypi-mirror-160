from datetime import datetime

from rich.style import StyleType
from rich.console import RenderableType
from rich.panel import Panel
from rich.table import Table
from rich.padding import Padding
from textual.widget import Widget
from textual.reactive import Reactive


class Header(Widget):
    clock: Reactive[bool] = Reactive(True)

    def __init__(
        self,
        label: RenderableType,
        name: str | None = None,
    ):
        super().__init__(name=name)
        self.name = name or str(label)
        self.label = label
        self.layout_size = 1
        self.style = "bold white frame"
        self.layout_size = 2

    def get_clock(self) -> str:
        return datetime.now().time().strftime("%X")

    def render(self) -> Panel:
        header_table = Table.grid(padding=(0, 1), expand=True)
        header_table.style = self.style
        header_table.add_column(justify="left", ratio=0, width=8)
        header_table.add_column("title", justify="center", ratio=1)
        header_table.add_column("clock", justify="right", width=8)
        header_table.add_row("👯", self.label, self.get_clock() if self.clock else "")
        return header_table
