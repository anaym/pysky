from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QPushButton

from graphics.autogui.item import Item


class CheckBoxSet(Item):
    def __init__(self, str_set, handler=None):
        super().__init__()
        self._src = set(str_set)
        self._selected = set()
        self._handlers = [] if handler is None else [handler]
        self._create_widget()
        self._create_buttons()

    def _create_widget(self):
        self._model = QStandardItemModel()
        for row in sorted(self._src):
            item = QStandardItem(row)
            item.setCheckState(False)
            item.setCheckable(True)
            self._model.appendRow(item)

        view = QListView()
        view.setModel(self._model)
        view.clicked.connect(lambda: self._on_change())

        self._widget = view
        self.addWidget(self._widget)

    def _create_buttons(self):
        bclear = QPushButton("none")
        bclear.clicked.connect(lambda: self._change_state_for_all(0))
        self.addWidget(bclear)
        ball = QPushButton("all")
        ball.clicked.connect(lambda: self._change_state_for_all(2))
        self.addWidget(ball)

    def _on_change(self):
        selected = set()
        for i in range(0, self._model.rowCount()):
            if self._model.item(i, 0).checkState() != 0:
                selected.add(self._model.item(i, 0).text())
        self._selected = selected
        for h in self._handlers:
            h(selected)

    def _change_state_for_all(self, mode):
        for i in range(0, self._model.rowCount()):
            self._model.item(i, 0).setCheckState(mode)
        self._on_change()

    @property
    def selected(self):
        return self._selected

    def connect(self, handler):
        self._handlers.append(handler)

    def try_load(self):
        pass

    def try_save(self):
        pass

