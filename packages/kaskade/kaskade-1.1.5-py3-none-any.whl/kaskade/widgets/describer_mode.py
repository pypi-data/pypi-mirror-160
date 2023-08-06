import re
from typing import Any, Callable, List, Optional, Union

from rich.align import Align
from rich.panel import Panel
from rich.text import Text
from textual import events
from textual.keys import Keys
from textual.reactive import Reactive

from kaskade import styles
from kaskade.kafka.models import GroupMember
from kaskade.renderables.groups_table import GroupsTable
from kaskade.renderables.members_table import MembersTable
from kaskade.renderables.paginated_table import PaginatedTable
from kaskade.renderables.partitions_table import PartitionsTable
from kaskade.utils.circular_list import CircularList
from kaskade.widgets.tui_widget import TuiWidget

CLICK_OFFSET = 1

TABLE_BOTTOM_PADDING = 4

TITLE_LEFT_PADDING = 3


class Tab:
    def __init__(self, name: str, render: Callable[[], Any]):
        self.name = name
        self.render = render


class DescriberMode(TuiWidget):
    has_focus = Reactive(False)
    table: Optional[PaginatedTable] = None
    page = 1
    row = 0

    def __init__(self, name: Optional[str] = None):
        super().__init__(name)
        self.tabs = CircularList(
            [
                Tab("partitions", self.render_partitions),
                Tab("groups", self.render_groups),
                Tab("members", self.render_members),
            ]
        )
        self.tabs.index = 0

    def render_members(self) -> MembersTable:
        members: List[GroupMember] = (
            sum([group.members for group in self.tui.topic.groups], [])
            if self.tui.topic
            else []
        )
        return MembersTable(
            members,
            page_size=self.size.height - TABLE_BOTTOM_PADDING,
            page=self.page,
            row=self.row,
        )

    def render_partitions(self) -> PartitionsTable:
        return PartitionsTable(
            self.tui.topic.partitions if self.tui.topic else [],
            page_size=self.size.height - TABLE_BOTTOM_PADDING,
            page=self.page,
            row=self.row,
        )

    def render_groups(self) -> GroupsTable:
        return GroupsTable(
            self.tui.topic.groups if self.tui.topic else [],
            page_size=self.size.height - TABLE_BOTTOM_PADDING,
            page=self.page,
            row=self.row,
        )

    def title(self) -> Text:
        return Text.from_markup(
            " ── ".join(
                [
                    "[bold]{}[/]".format(tab.name)
                    if tab == self.tabs.current
                    else "[dim white]{}[/]".format(tab.name)
                    for tab in self.tabs.list
                ]
            )
        )

    def render(self) -> Panel:
        if self.table is not None:
            self.page = self.table.page
            self.row = self.table.row

        if self.tabs.current is not None:
            self.table = self.tabs.current.render()

        to_render: Union[Align, PaginatedTable] = (
            Align.center("Not selected", vertical="middle")
            if self.tui.topic is None or self.table is None
            else self.table
        )

        body_panel = Panel(
            to_render,
            title=self.title(),
            border_style=styles.BORDER_FOCUSED if self.has_focus else styles.BORDER,
            box=styles.BOX,
            title_align="left",
            padding=0,
        )

        return body_panel

    def on_focus(self) -> None:
        self.has_focus = True
        self.tui.focusables.current = self

    def on_blur(self) -> None:
        self.has_focus = False

    def on_key(self, event: events.Key) -> None:
        if self.table is None:
            return

        key = event.key
        if key == "[":
            self.table.previous_page()
        elif key == "]":
            self.table.next_page()
        elif key == "{":
            self.table.first_page()
        elif key == "}":
            self.table.last_page()
        elif key == Keys.Up:
            self.table.previous_row()
        elif key == Keys.Down:
            self.table.next_row()
        elif key == ">":
            self.next_tab()
        elif key == "<":
            self.previous_tab()

        self.refresh()

    def reset(self) -> None:
        self.table = None
        self.page = 0
        self.row = 0

    def next_tab(self) -> None:
        self.tabs.next()
        self.table = None
        self.page = 0
        self.row = 0

    def previous_tab(self) -> None:
        self.tabs.previous()
        self.table = None
        self.page = 0
        self.row = 0

    async def on_mouse_scroll_up(self) -> None:
        await self.tui.set_focus(self)
        if self.table is not None:
            self.table.next_row()

        self.refresh()

    async def on_mouse_scroll_down(self) -> None:
        await self.tui.set_focus(self)
        if self.table is not None:
            self.table.previous_row()

        self.refresh()

    async def on_click(self, event: events.Click) -> None:
        if self.table is not None:
            self.table.row = event.y - CLICK_OFFSET

        if event.y == 0:
            title = self.title().plain
            for tab in self.tabs.list:
                for start, end in [
                    (f.start(), f.start() + len(tab.name))
                    for f in re.finditer(tab.name, title)
                ]:
                    if start <= event.x - TITLE_LEFT_PADDING < end:
                        self.tabs.current = tab
                        self.reset()

        self.refresh()
