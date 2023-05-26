from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QListWidgetItem, QPushButton, QHBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # create a horizontal layout
        layout = QHBoxLayout(self)

        # create an "Add Column" button
        add_column_button = QPushButton('Add Column')
        add_column_button.clicked.connect(self.add_column)

        # add the "Add Column" button to the layout
        layout.addWidget(add_column_button)

    def add_column(self):
        # create a new QListWidget
        list_widget = QListWidget()

        # set the list widget to display items horizontally
        list_widget.setViewMode(QListWidget.IconMode)
        list_widget.setFlow(QListWidget.LeftToRight)

        # create an "Add Item" button
        add_button = QPushButton('Add Item')
        add_item_button = QListWidgetItem()
        add_item_button.setSizeHint(add_button.sizeHint())
        list_widget.addItem(add_item_button)
        list_widget.setItemWidget(add_item_button, add_button)

        # connect the "Add Item" button's clicked signal to a slot that adds a new item to the list
        add_button.clicked.connect(lambda: self.add_item(list_widget, add_item_button))

        # add the list widget to the horizontal layout
        layout = self.layout()
        layout.addWidget(list_widget)

    def add_item(self, list_widget, item):
        # create a new item and add it to the list
        new_item = QListWidgetItem('New Item')
        list_widget.insertItem(list_widget.row(item), new_item)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()