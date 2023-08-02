import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtCore import QObject, pyqtSignal


class CounterModel:
    def __init__(self):
        self._counter = 0

    def get_counter(self):
        return self._counter

    def increment_counter(self):
        self._counter += 1


class CounterViewModel(QObject):
    counter_updated = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self._model = CounterModel()
        self._counter = self._model.get_counter()

    def increment_counter(self):
        self._model.increment_counter()
        self._counter = self._model.get_counter()
        self.counter_updated.emit(self._counter)

    def get_counter(self):
        return self._counter


class CounterView(QMainWindow):
    def __init__(self, viewmodel):
        super().__init__()

        self.viewmodel = viewmodel
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("MVVM Counter Example")
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        self.counter_label = QLabel("Counter: 0")
        layout.addWidget(self.counter_label)

        self.button = QPushButton("Increment")
        self.button.clicked.connect(self.viewmodel.increment_counter)
        layout.addWidget(self.button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.viewmodel.counter_updated.connect(self.update_counter_label)

    def update_counter_label(self, counter):
        self.counter_label.setText(f"Counter: {counter}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewmodel = CounterViewModel()
    view = CounterView(viewmodel)
    view.show()
    sys.exit(app.exec_())
