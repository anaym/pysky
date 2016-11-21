import datetime

from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QLineEdit

#TODO: set focus?
#TODO: auto change value, after modigy in parent (use decorator)
def __end_of_edit(parser, builder, widget: QLineEdit, data_parent, data_name: str, nonable: bool):
    try:
        value = parser(widget.text())
        if value is None:
            raise ValueError()
        data_parent.__setattr__(data_name, value)
        widget.setText(builder(value))
    except:
        widget.setText(builder(data_parent.__getattribute__(data_name)))


def _create_widget(data_parent, data_name: str, parser, builder, nonable: bool) -> QLineEdit:
    widget = QLineEdit(builder(data_parent.__getattribute__(data_name)))
    widget.editingFinished.connect(lambda: __end_of_edit(parser, builder, widget, data_parent, data_name, nonable))
    return widget


def _on_change(w: QCheckBox, data_parent, data_name):
    data_parent.__setattr__(data_name, w.checkState())


def create_bool_widget(name: str, data_parent, data_name: str) -> QCheckBox:
    box = QCheckBox(name)
    box.setChecked(data_parent.__getattribute__(data_name))
    box.stateChanged.connect(lambda: _on_change(box, data_parent, data_name))
    return box


def create_float_widget(data_parent, data_name: str) -> QLineEdit:
    return _create_widget(data_parent, data_name, float, str, False)


def create_datetime_widget(data_parent, data_name: str, datetime_format: str) -> QLineEdit:
    parser = lambda s: datetime.datetime.strptime(s, datetime_format)
    builder = lambda d: d.strftime(datetime_format)
    return _create_widget(data_parent, data_name, parser, builder, False)
