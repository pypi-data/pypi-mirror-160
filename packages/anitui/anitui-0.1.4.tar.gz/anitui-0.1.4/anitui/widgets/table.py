import os
from rich.align import Align
from rich.console import RenderableType, Console
from rich.panel import Panel
from rich.style import StyleType
from rich.table import Table
from textual.widget import Widget


class Files(Widget):
    def __init__(
        self,
        *,
        tall: bool = True,
        style: StyleType = "white on dark_green",
        clock: bool = True,
        file_names: [str],
        rows: [os.DirEntry],
        selected: int,
        offset: int = 0,
    ) -> None:
        super().__init__()
        self.tall = tall
        self.style = style
        self.clock = clock
        self.rows = rows
        self.file_names = file_names
        self.selected = selected
        self.offset = offset

    def render(self) -> Panel:
        table = Table.grid(padding=(1, 1), expand=True)
        table.add_column("title", justify="left", ratio=1)
        table = self.add_rows(table)
        return table

    def add_rows(self, table) -> RenderableType:
        for i in range(self.offset, len(self.rows)):
            row = self.file_names[i]
            if i == self.selected:
                if self.rows[i].is_file():
                    table.add_row(Align(row, vertical="middle"), style="green")
                elif self.rows[i].is_dir():
                    table.add_row(
                        Align(row, vertical="middle"), style="light_slate_blue"
                    )
            else:
                if self.rows[i].is_file():
                    table.add_row(Align(row, vertical="middle"), style="white")
                elif self.rows[i].is_dir():
                    table.add_row(
                        Align(row, vertical="middle"), style="light_sky_blue1"
                    )
        return table
