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
    QPushButton,
)
from PyQt5.QtCore import Qt, QFile, QJsonDocument, QJsonValue
from PyQt5.uic import loadUi  # Use loadUi directly


# Your Model class remains unchanged.
class Model:
    def __init__(self, config_data):
        self.pages = config_data

    def get_page_data(self, page_name):
        return self.pages.get(page_name, {})


# Separate ViewModel classes for each page.
class Page1ViewModel:
    def __init__(self, model):
        self.model = model
        self.counter = 0

    def get_data(self):
        return self.model.pages.get("Page 1", {}).get("data", "Data not found")

    def get_counter(self):
        return self.counter

    def increase_counter(self):
        self.counter += 1


class Page2ViewModel:
    def __init__(self, model):
        self.model = model
        self.counter = 0

    def get_data(self):
        return self.model.pages.get("Page 2", {}).get("data", "Data not found")

    def get_counter(self):
        return self.counter

    def increase_counter(self):
        self.counter += 1


class Page3ViewModel:
    def __init__(self, model):
        self.model = model
        self.counter = 0

    def get_data(self):
        return self.model.pages.get("Page 3", {}).get("data", "Data not found")

    def get_counter(self):
        return self.counter

    def increase_counter(self):
        self.counter += 1


# Update the ViewModel class to have a reference to the current ViewModel.
class ViewModel:
    def __init__(self, model):
        self.model = model
        self.current_page = None
        self.current_view_model = None  # Reference to the current ViewModel

    def get_page_content(self, page_name):
        return self.model.pages.get(page_name, {"ui": "Page not found."})

    def set_current_page(self, page_name):
        self.current_page = page_name

    def get_page_ui_file(self, page_name):
        page_data = self.model.get_page_data(page_name)

        # Check if the "ui" field is a valid QJsonValue
        if isinstance(page_data["ui"], QJsonValue):
            # Access the value of the QJsonValue directly
            return page_data["ui"].toString()

        # Check if the "ui" field is a string without QJsonValue wrapping
        if isinstance(page_data.get("ui"), str):
            return page_data.get("ui", "")

        # If "ui" field is not a valid QJsonValue or a string, return an empty string
        return ""

    def get_page_data_value(self, ui_file):
        page_name = self.get_page_name_from_ui_file(ui_file)
        page_data = self.model.get_page_data(page_name)

        # Ensure that page_data is a dictionary
        if isinstance(page_data, QJsonValue):
            page_data = page_data.toVariant()

        # Access the "data" field value from the page_data dictionary
        return page_data.get("data", "Data not found")

    def get_page_name_from_ui_file(self, ui_file):
        for page_name, data in self.model.pages.items():
            if data["ui"] == ui_file:
                return page_name
        return ""


# In the ViewModel, you can use specific methods for each page to handle the logic.
# For example, if you need to display specific data on Page 1, you'll use Page1ViewModel methods.
# Your View class remains unchanged, but you'll need to modify the logic for menu item selection.
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
        print(self.view_model.model.pages.keys())
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

        # Find the QLabel named 'data_label' in the loaded UI widget
        label_data = ui_widget.findChild(QLabel, "label")

        if label_data:
            # Add the loaded UI widget to the container
            self.ui_container.layout().addWidget(ui_widget)

            # Set the 'data_label' text with the "data" field value
            data_value = self.view_model.get_page_data_value(ui_file)
            label_data.setText(data_value)


# When a menu item is selected, set the corresponding ViewModel.
def show_page(self, current, previous):
    if current is None:
        return

    page_name = current.text()
    self.view_model.set_current_page(page_name)

    # Set the corresponding ViewModel based on the menu selection.
    if page_name == "Page 1":
        self.view_model.current_view_model = Page1ViewModel(self.view_model.model)
    elif page_name == "Page 2":
        self.view_model.current_view_model = Page2ViewModel(self.view_model.model)
    elif page_name == "Page 3":
        self.view_model.current_view_model = Page3ViewModel(self.view_model.model)

    # Load and display the appropriate UI widget based on the menu selection.
    ui_file = self.view_model.get_page_ui_file(page_name)
    if ui_file:
        self.load_ui_widget(ui_file)


# Your main code remains unchanged.

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load the JSON config file
    with open("3.AddConfig/config.json", "r") as file:
        data = QJsonDocument.fromJson(file.read().encode())

    model = Model(data.object())
    view_model = ViewModel(model)
    view = View(view_model)

    # Create QDockWidget for navigation menu
    menu_dock = QDockWidget("Navigation Menu", view)
    menu_dock.setWidget(view.list_widget)
    view.addDockWidget(Qt.LeftDockWidgetArea, menu_dock)

    view.show()

    sys.exit(app.exec_())
