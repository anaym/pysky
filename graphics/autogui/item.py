from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QGroupBox


class Item(QGroupBox):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.setLayout(self.layout)

    def try_save(self):
        raise NotImplementedError()

    def try_load(self):
        raise NotImplementedError()
