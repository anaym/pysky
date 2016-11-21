import datetime
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QWidget


def trackable_setter(self, name, value):
    super(self.__class__, self).__setattr__(name, value)
    if name in self.handlers:
        for h in self.handlers[name]:
            h(value)


def trackable_object(obj):
    obj.handlers = {}
    obj.__class__.__setattr__ = trackable_setter
    return obj


def _create_edit_widget(data_parent, data_name: str, parser, builder) -> QLineEdit:
    widget = QLineEdit("")

    def end_of_edit():
        try:
            value = parser(widget.text())
            if value is None:
                raise ValueError()
            data_parent.__setattr__(data_name, value)
            widget.setText(builder(value))
        except:
            widget.setText(builder(data_parent.__getattribute__(data_name)))

    widget.editingFinished.connect(end_of_edit)
    widget.handle = lambda: widget.setText(builder(data_parent.__getattribute__(data_name)))
    return widget


def _create_widget(parent: object, fname: str, ftype: type) -> QWidget:
    field = parent.__getattribute__(fname)
    if ftype == int or ftype == float or ftype == datetime:
        parser = fname if ftype != datetime else lambda s: datetime
        builder = str if type != datetime else lambda d: d.strftime(datetime_format)
        widget = _create_edit_widget(parent, parser, str)


def _create_group(widget: QWidget, name: str) -> QLayout:
    layout = QGridLayout()
    layout.addWidget(QLayout(name), 0, 0)
    layout.addWidget(widget, 0, 1)
    layout.handle = lambda: widget.update()
    return layout

def get_object_widget(obj: object, fields, types):
    if type(obj) == int or type(obj) == float or type(obj) == bool:
        raise TypeError('Primitive types unsupported!')
    layouts = []
    for fname in fields:
        widget = _create_group(obj, fname)
        layouts += _create_group(widget, fname)

