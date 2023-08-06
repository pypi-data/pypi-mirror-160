from rich.console import Console

console = Console()


def entry_height(entry, table_width):
    padding = 1
    line = (len(entry) // table_width) + 1
    return line + padding


def table_size():
    console = Console()
    table_width = console.width - (console.width // 3)
    table_height = console.height - 2
    return table_height, table_width


def check_valid_select(entries, selected, offset):
    """Returns True if selected is within table view"""
    table_height, table_width = table_size()

    total_height = 1
    for i in range(offset, len(entries)):
        total_height += entry_height(entries[i], table_width)
        if total_height > table_height:
            return False
        if i == selected:
            return True
    return True
