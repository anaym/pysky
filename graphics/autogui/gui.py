from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QWidget

from graphics.autogui.cast_tools import to_widget
from graphics.autogui.item import Item
from graphics.autogui.label_item import LabelItem


class GUI(Item):
    def __init__(self, name: str):
        super().__init__(False)
        self._nested = []
        #self._layout.addLayout(LabelItem(name, True), 0, 0)
        self.setTitle(name)

    def add(self, item: Item) -> Item:
        self._nested.append(item)
        self.layout.addWidget(item, len(self._nested), 0)
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
        #widget = to_widget(self)
        #widget.setStyleSheet("QWidget {margin: 0px}")
        return self
