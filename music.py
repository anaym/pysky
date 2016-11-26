from PyQt5 import QtWidgets
from PyQt5.QtMultimedia import QSound

# TODO: dead whe parent dead!!!
# TODO: gui
app = QtWidgets.QApplication([])
s = QSound('resources\music.wav')
s.setLoops(QSound.Infinite)
s.play()
app.exec()
