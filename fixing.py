import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QListWidget, QPushButton, QListWidgetItem, QMenu, \
    QAction
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap


def GoToMainPage():
    main = MainPage()
    widget.addWidget(main)
    widget.resize(main.size())
    widget.setCurrentIndex(widget.currentIndex() + 1)


def GoToLoginPage():
    login = Login()
    widget.addWidget(login)
    widget.resize(login.size())
    widget.setCurrentIndex(widget.currentIndex() + 1)


def GoToBoardPage():
    board = Board()
    widget.addWidget(board)
    widget.resize(board.size())
    widget.setCurrentIndex(widget.currentIndex() + 1)


class Login(QDialog):
    user = "name"
    passw = " "

    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.loginbutton.clicked.connect(self.gotologin)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)
        self.user_name = ""
        self.user_password = ""

    def gotologin(self):
        self.user_name = self.username.text()
        self.user_password = self.password.text()
        print("successfully logged in with username: ", self.user_name, "and password: ", self.user_password)
        Login.user = self.user_name
        Login.passw = self.user_password
        GoToMainPage()

    def gotocreate(self):
        acc = CreateAcc()
        widget.addWidget(acc)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("signup.ui", self)
        self.signupbutton.clicked.connect(self.signupfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)

    def signupfunction(self):
        username = self.username.text()
        if self.password.text() == self.confirmpass.text():
            password = self.password.text()
            print("successfully created an Account with username: ", username, "and password: ", password)
            GoToLoginPage()
        else:
            print("The password is not equal")


class MainPage(QDialog):
    val = "nah"
    valtemp = "yah"

    def __init__(self):
        super(MainPage, self).__init__()
        loadUi("boardpage.ui", self)
        self.accountbutton.clicked.connect(self.gotoaccountfunction)
        self.addboardbutton.clicked.connect(self.namingboardfunction)
        self.deleteboardbutton.clicked.connect(self.deleteboardfunction)
        self.boardlist.itemDoubleClicked.connect(self.openboardfunction)

    def openboardfunction(self, item):
        MainPage.val = item.text()
        print(MainPage.val)
        GoToBoardPage()

    def namingboardfunction(self):
        namingboardtitle = NamingBoard()
        namingboardtitle.exec_()

    def addboardname(self):
        self.boardlist.addItem(MainPage.valtemp)

    def deleteboardfunction(self):
        board = self.boardlist.currentRow()
        item = self.boardlist.item(board)
        if item is None:
            return
        else:
            self.boardlist.takeItem(board)
            del item

    def gotoaccountfunction(self):
        account = Account()
        widget.addWidget(account)
        widget.resize(account.size())
        widget.setCurrentIndex(widget.currentIndex() + 1)


class NamingBoard(QDialog):

    def __init__(self):
        super(NamingBoard, self).__init__()
        loadUi("boardname.ui", self)
        self.okboardbutton.clicked.connect(self.inputboardname)
        self.addmemberbutton.clicked.connect(self.addmembertolist)
        self.removememberbutton.clicked.connect(self.removememberfunction)

    def removememberfunction(self):
        member = self.memberlist.currentRow()
        item = self.memberlist.item(member)
        if item is None:
            return
        else:
            self.memberlist.takeItem(member)
            del item

    def inputboardname(self):
        MainPage.valtemp = self.enterboardname.text()
        if MainPage.valtemp is not None:
            self.accept()
        GoToMainPage()

    def addmembertolist(self):
        member = self.memberlist.currentRow()
        item = self.addmember.text()
        if item is not None:
            self.memberlist.insertItem(member, item)
        self.addmember.clear()


class Account(QDialog):
    def __init__(self):
        super(Account, self).__init__()
        loadUi("account.ui", self)
        self.usernamelabel.setText(Login.user)
        self.passwordlabel.setText(Login.passw)
        self.backtomainpagebutton.clicked.connect(self.gotomainpage)
        self.logoutbutton.clicked.connect(self.gotologinpage)

    def gotologinpage(self):
        GoToLoginPage()

    def gotomainpage(self):
        GoToMainPage()


class Board(QDialog):
    def __init__(self):
        print("opening board")
        super(Board, self).__init__()
        loadUi("newboard.ui", self)

        self.addcolumnbutton.clicked.connect(self.addcolumnfunction)
        self.btmp_button.clicked.connect(self.gotomainpage)
        self.boardnamelabel.setText(MainPage.val)
        self.deleteitembutton.clicked.connect(self.deleteitemfunction)

    def gotomainpage(self):
        GoToMainPage()

    def addcolumnfunction(self):
        # create a new QListWidget
        list_widget = QListWidget()
        list_widget.setStyleSheet("color:rgb(255, 255, 255); font-size:12pt;")
        list_widget.setFixedSize(200, 400)

        # set the list widget to display items horizontally
        list_widget.setViewMode(QListWidget.IconMode)
        list_widget.setResizeMode(QListWidget.Adjust)

        # create an "Add Item" button
        add_button = QPushButton('Add Item')
        add_button.setFixedWidth(200)
        add_button.setStyleSheet("background-color:rgb(85, 170, 127); color:rgb(255, 255, 255); font-size:12pt;")
        add_item_button = QListWidgetItem()
        add_item_button.setSizeHint(add_button.sizeHint())
        list_widget.addItem(add_item_button)
        list_widget.setItemWidget(add_item_button, add_button)

        del_button = QPushButton('Delete')
        del_button.setFixedWidth(200)
        del_button.setStyleSheet("background-color:rgb(85, 170, 127); color:rgb(255, 255, 255); font-size:12pt;")
        del_item_button = QListWidgetItem()
        del_item_button.setSizeHint(del_button.sizeHint())
        list_widget.addItem(del_item_button)
        list_widget.setItemWidget(del_item_button, del_button)

        # connect the "Add Item" button's clicked signal to a slot that adds a new item to the list
        add_button.clicked.connect(lambda: self.add_item(list_widget, add_item_button))
        del_button.clicked.connect(list_widget.deleteLater)

        # add the list widget to the horizontal layout
        self.hrlayout.insertWidget(self.hrlayout.count() - 1, list_widget)
        list_widget.itemDoubleClicked.connect(self.opencardfunction)


    def add_item(self, list_widget, item):
        # create a new item and add it to the list
        new_item = QListWidgetItem('new item')
        list_widget.insertItem(list_widget.row(item), new_item)

    def deleteitemfunction(self):
        listitem = self.list_widget.currentRow()
        item = self.list_widget.item(listitem)
        if item is None:
            return
        else:
            self.list_widget.takeItem(listitem)
            del item


    def opencardfunction(self):
        card = Card()
        card.exec_()


class Card(QDialog):
    def __init__(self):
        super(Card, self).__init__()
        loadUi("card.ui", self)
        self.uploadIMGbutton.clicked.connect(self.uploadimagefunction)
        self.description.setReadOnly(False)
        self.editcardbutton.clicked.connect(self.submittext)

    def submittext(self):
        text = self.description.toPlainText()
        GoToBoardPage()

    def uploadimagefunction(self):
        # Open a file dialog and get the path to the selected image file
        filepath, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")

        # Get the size of the label
        label_width = self.IMGbox.width()
        label_height = self.IMGbox.height()

        # Create a QPixmap object from the image file and scale it to fit inside the label
        pixmap = QPixmap(filepath).scaled(label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Set the pixmap to the label
        self.IMGbox.setPixmap(pixmap)


app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
trello = Login()
widget.addWidget(trello)
widget.resize(trello.size())
widget.show()
app.exec_()
