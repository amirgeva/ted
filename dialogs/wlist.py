from typing import Tuple, List

from dialogs.widget import Widget
from color import Color


class ListWidget(Widget):
    def __init__(self, win):
        super().__init__(win)
        self._items = []
        self._offset = 0
        self._cur = 0
        self._tab_stop = True

    def get_items(self) -> List[str]:
        return list(self._items)

    def get_selection(self) -> Tuple[str, int]:
        if self._cur >= len(self._items):
            return '', -1
        return self._items[self._cur], self._cur

    def set_selection(self, index: int):
        if 0 <= index < len(self._items):
            self._cur = index

    def clear(self):
        self._items = []
        self._offset = 0
        self._cur = 0

    def add_item(self, item: str):
        self._items.append(item)

    def remove_item(self, item):
        if isinstance(item, int) and 0 <= item < len(self._items):
            del self._items[item]
        elif isinstance(item, str):
            try:
                i = self._items.index(item)
                del self._items[i]
            except ValueError:
                pass

    def render(self):
        super().render()
        for y in range(self._window.height()):
            i = y + self._offset
            self._window.set_cursor(0, y)
            w = self._window.width()
            text = ' ' * w
            if i < len(self._items):
                text = self._items[i]
            highlight = Color.FOCUS if self.is_focus() else Color.TEXT_HIGHLIGHT
            color = Color.TEXT if i != self._cur else highlight
            if len(text) > w:
                text = text[0:w]
            if len(text) < w:
                text = text + ' ' * (w - len(text))
            self._window.text(text, color)

    def scroll(self):
        y = self._cur - self._offset
        if y < 0 or y >= self._window.height():
            self._offset = max(0, self._cur - self._window.height() // 2)

    def action_move_down(self):
        prev = self._cur
        self._cur += 1
        if self._cur >= len(self._items):
            self._cur = 0
        self.scroll()
        if prev != self._cur:
            self.speak('selection_changed')

    def action_move_up(self):
        prev = self._cur
        self._cur -= 1
        if self._cur < 0:
            self._cur = len(self._items) - 1
        self.scroll()
        if prev != self._cur:
            self.speak('selection_changed')
