from PyQt5.QtWidgets import QGridLayout


class Item(QGridLayout):
    def __init__(self):
        super().__init__()

    def try_save(self):
        raise NotImplementedError()

    def try_load(self):
        raise NotImplementedError()
