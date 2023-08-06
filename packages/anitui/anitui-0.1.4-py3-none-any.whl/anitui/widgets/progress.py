from rich import box
from rich.align import Align

from rich.console import RenderableType
from rich.panel import Panel
from rich.pretty import Pretty

from textual.geometry import Offset
from textual.widget import Reactive, Widget
from rich.table import Table


class Progress(Widget):

    style: Reactive[str] = Reactive("")

    def __init__(self, *, name: str | None = None, watch_list) -> None:
        super().__init__(name=name)
        self.watch_list = watch_list

    def construct_watch_list(self):
        data = self.watch_list
        table = Table.grid(padding=(1, 2), expand=True)
        table.style = self.style
        table.add_column("Title")
        table.add_column("Episode", justify="right", ratio=1, style="red")
        for anime in data:
            title = anime["media"]["title"]["english"]
            episode = anime["progress"]
            table.add_row(str(title), str(episode))
        return table

    def render(self) -> RenderableType:
        table = self.construct_watch_list()

        return Panel(
            table,
            title="Watch List",
            border_style="green",
            style=self.style,
        )
