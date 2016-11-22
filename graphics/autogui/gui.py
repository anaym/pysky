from PyQt5.QtWidgets import QWidget

from graphics.autogui.cast_tools import to_widget
from graphics.autogui.item import Item
from graphics.autogui.label import Label


class GUI(Item):
    def __init__(self, name: str):
        super().__init__()
        self._nested = []
        self.addLayout(Label(name, True), 0, 0)
        self.setContentsMargins(10, 1, 1, 10)

    def add(self, item: Item) -> Item:
        self._nested.append(item)
        self.addLayout(item, len(self._nested) + 1, 0)
        return item

    def try_load(self):
        pass

    def try_save(self):
        for h in self._nested:
            if not h.try_save():
                h.try_load()

    def handle(self):
        self.try_save()
        self.try_load()

    def to_widget(self) -> QWidget:
        widget = to_widget(self)
        #widget.setStyleSheet("QWidget {margin: 0px}")
        return widget
