from PySide6.QtCore import QObject, Slot, Property, QUrl, Signal
from PySide6.QtGui import QGuiApplication
from PySide6.QtQuick import QQuickView
import sys

VIEW_URL = "view.qml"

class ClickModel(QObject):
    def __init__(self):
        QObject.__init__(self)
        self._count = 0
    
    def get_count(self):
        return self._count

    def set_count(self,val):
        print("Current: {}, new: {}".format(self.count,val))

        if val != self._count:
            self._count = val
            self.counter_changed.emit()
    
    counter_changed = Signal()
    counter = Property(int, get_count, set_count, notify = counter_changed) 

    @Slot()
    def increase(self):
        print("Increasing")
        self.count = self.count+1

app = QGuiApplication(sys.argv)
view = QQuickView()
url = QUrl(VIEW_URL)

click_model = ClickModel

ctxt = view.rootContext()
ctxt.setContextProperty("clickModel",click_model)

view.setSource(url)
view.show()

app.exec_()