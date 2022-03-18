from PySide2.QtCore import QObject, Slot, Property, QUrl, Signal, QTimer
from PySide2.QtGui import QGuiApplication
from PySide2.QtQuick import QQuickView
import sys

VIEW_URL = "view.qml"


class CountdownModel(QObject):
    """CountdownModel is the model class for the GUI. It holds the counter property
     and handles event generated by the click on the button."""

    def __init__(self):
        QObject.__init__(self)
        # Value to count from
        self.total = 30
        self._remaining = 30
        # Timer
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.process_timer)

    def set_remaining(self, val):
        if val != self._remaining:
            self._remaining = val
            self.remaining_changed.emit()
            # If the timer is inactive, update also a value to count from
            if not self.timer.isActive():
                self.total = self.remaining

    remaining_changed = Signal()
    # Property holding actual remaining number of seconds
    remaining = Property(int, lambda self: self._remaining, set_remaining, notify=remaining_changed)

    timeout = Signal()

    @Slot()
    def process_timer(self):
        """Handler for the timer event.
        Decrease the remaining value or stop the timer and emit timeout signal if the time is over"""
        if self.remaining == 1:
            self.timer.stop()
            self.remaining = self.total     # Reset the timer value
            self.timeout.emit()
            return
        self.remaining -= 1

    @Slot()
    def start(self):
        """Start the countdown"""
        print("Starting")
        print(self.total,self.remaining)
        self.timer.start()

    @Slot()
    def pause(self):
        """Pause the countdown"""
        print("Pausing")
        print(self.total,self.remaining)
        self.timer.stop()

    @Slot()
    def stop(self):
        """Stop (and reset) the countdown"""
        print("Stopping")
        print(self.total,self.remaining)
        self.timer.stop()
        self.remaining = self.total


app = QGuiApplication(sys.argv)
view = QQuickView()
url = QUrl(VIEW_URL)
countdown_model = CountdownModel()

ctxt = view.rootContext()
ctxt.setContextProperty("countdownModel", countdown_model)

view.setSource(url)
view.show()
app.exec_()

zmenaa