from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QWidget


def to_widget(layot: QGridLayout, bcolor: str=None):
    widget = QWidget()
    widget.setLayout(layot)
    if not bcolor is None:
        widget.setStyleSheet("QWidget {{ border: 1px solid {} }}".format(bcolor))
    return widget