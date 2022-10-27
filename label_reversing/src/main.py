import sys
import time

from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QCloseEvent
from ui.main_form import Ui_MainWindow
from threading import Thread, Event

class Signal_label(QObject):
    label_change = Signal(str)

class Mainwindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Mainwindow, self).__init__()
        self.setupUi(self)
        
        self.label_message = Signal_label()
        self.label_message.label_change.connect(self.label_change_signal_handler)

        self.label_change_thread = Thread(target = self.label_change_proc,args=(self.label_message, ))
        self.exit_event = Event()
        #self.label_change_thread.start()

    def label_change_proc(self, label_message : Signal_label):
        while self.exit_event.is_set() == False:
            time.sleep(.2)
            label_message.label_change.emit("ddat")
    
    @Slot(str)
    def label_change_signal_handler(self, label_message : str):
        self.label_ddat.setText(label_message)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.exit_event.set()
        return super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Mainwindow()
    window.show()
    app.exec()