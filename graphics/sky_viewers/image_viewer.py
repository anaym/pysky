from datetime import datetime
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget


class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self._image = QImage(self.size(), QImage.Format_RGB32)
        self.setMouseTracking(True)

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value
        self.repaint()

    def save_to_file(self, name: str=None):
        self.image.save(name if name is not None else datetime.now().strftime("%d.%m.%Y %H_%M_%S.jpg"))

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.drawImage(0, 0, self.image)
        painter.end()

    def resizeEvent(self, event):
        self.image = self.image.scaled(self.size())

