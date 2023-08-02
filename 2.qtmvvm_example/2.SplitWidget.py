import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLabel,
    QDockWidget,
    QListWidget,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt, QFile
from PyQt5.uic import loadUi  # Use loadUi directly


class Model:
    def __init__(self):
        current_dict = "2.qtmvvm_example"
        self.pages = {
            "Page 1": current_dict + "/page1.ui",
            "Page 2": current_dict + "/page2.ui",
            "Page 3": current_dict + "/page3.ui",
        }


class ViewModel:
    def __init__(self, model):
        self.model = model
        self.current_page = None

    def get_page_ui_file(self, page_name):
        return self.model.pages.get(page_name, "")

    def set_current_page(self, page_name):
        self.current_page = page_name


class View(QMainWindow):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Display Different UI Widgets Example")
        self.setGeometry(100, 100, 600, 400)

        # Create QListWidget for navigation menu
        self.list_widget = QListWidget(self)
        self.list_widget.addItems(self.view_model.model.pages.keys())
        self.list_widget.currentItemChanged.connect(self.show_page)

        # Create a central widget to hold the content view
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a layout to arrange the QListWidget and content view vertically
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.list_widget)

        # Create a QWidget to hold the UI widgets
        self.ui_container = QWidget()
        layout.addWidget(self.ui_container)

        # Set a layout for the ui_container
        self.ui_container.setLayout(QVBoxLayout())

    def show_page(self, current, previous):
        if current is None:
            return

        page_name = current.text()
        self.view_model.set_current_page(page_name)

        # Load and display the appropriate UI widget based on the menu selection
        ui_file = self.view_model.get_page_ui_file(page_name)
        if ui_file:
            self.load_ui_widget(ui_file)

    def load_ui_widget(self, ui_file):
        # Remove the existing UI widget from the container, if any
        while self.ui_container.layout().count():
            item = self.ui_container.layout().takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Load the UI widget from the .ui file using loadUi function
        ui_widget = loadUi(ui_file)

        # Add the loaded UI widget to the container
        self.ui_container.layout().addWidget(ui_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create instances of Model, ViewModel, and View
    model = Model()
    view_model = ViewModel(model)
    view = View(view_model)

    # Create QDockWidget for navigation menu
    menu_dock = QDockWidget("Navigation Menu", view)
    menu_dock.setWidget(view.list_widget)
    view.addDockWidget(Qt.LeftDockWidgetArea, menu_dock)

    view.show()

    sys.exit(app.exec_())
