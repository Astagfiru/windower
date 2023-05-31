import ast
import os
import sys
import cruder
import calc
import datetime
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QListWidget, QPushButton, QListWidgetItem, QMenu, \
    QAction, QMessageBox, QSpinBox, QVBoxLayout, QWidget, QHBoxLayout, QSpacerItem, QSizePolicy, QLabel, QLineEdit, \
    QGridLayout
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
    RealUser = cruder.Reader("User", "")

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

        if cruder.PersonId(self.user_name, self.user_password) != "No":
            RealUser = cruder.Reader("User", cruder.PersonId(self.user_name, self.user_password))
            print("successfully logged in with username: ", self.user_name, "and password: ", self.user_password)
            Login.user = self.user_name
            Login.passw = self.user_password
            GoToMainPage()
        else:
            # Create a QMessageBox object
            msg = QMessageBox()

            # Set the message box icon and text
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Wrong Password or username!")

            # Set the message box title and button text
            msg.setWindowTitle("Damn!")
            msg.setStandardButtons(QMessageBox.Ok)

            # Display the message box and wait for the user to click a button
            msg.exec_()

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
        if self.password.text() == self.confirmpass.text() and cruder.IsAppropriate(username):
            password = self.password.text()
            user = cruder.user_crud.create(username, password)
            print("successfully created an Account with username: ", username, "and password: ", password)
            GoToLoginPage()
        else:
            # Create a QMessageBox object
            msg = QMessageBox()

            # Set the message box icon and text
            msg.setIcon(QMessageBox.Warning)
            msg.setText("The entered passwords are not the same or the user already exists!")

            # Set the message box title and button text
            msg.setWindowTitle("Damn!")
            msg.setStandardButtons(QMessageBox.Ok)

            # Display the message box and wait for the user to click a button
            msg.exec_()
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
        self.boardlist_2.itemDoubleClicked.connect(self.openboardfunction)

        for i in range(len(cruder.GetUserBoards(Login.user))):
            item = QtWidgets.QListWidgetItem(cruder.GetUserBoards(Login.user)[i].name)
            # Add the item to the list widget
            self.boardlist.addItem(item)

        for i in range(len(cruder.GetUserAsAddedBoards(Login.user))):
            item = QtWidgets.QListWidgetItem(cruder.GetUserAsAddedBoards(Login.user)[i].name)
            # Add the item to the list widget
            self.boardlist_2.addItem(item)



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
            cruder.delete_board_by_creator_and_name(Login.user, item.text())
            self.boardlist.takeItem(board)
            del item


    def gotoaccountfunction(self):
        account = Account()
        widget.addWidget(account)
        widget.resize(account.size())
        widget.setCurrentIndex(widget.currentIndex() + 1)


class NamingBoard(QDialog):
    members = []
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
            current_datetime = datetime.datetime.now()
            formatted_datetime = current_datetime.strftime("%d.%m")

            board = cruder.board_crud.create(f"{MainPage.valtemp}", f"{Login.user}",
                                             f"{self.members}", [], f"{formatted_datetime}")
        self.removemembersfunction()
        GoToMainPage()

    def addmembertolist(self):
        member = self.memberlist.currentRow()
        item = self.addmember.text()
        if item is not None and self.check(item):
            self.memberlist.insertItem(member, item)
            self.members.append(item)
        self.addmember.clear()

    def check(self, item):
        if item == "" or item in self.members:
            return False
        else:
            return True

class Account(QDialog):
    def __init__(self):
        super(Account, self).__init__()
        loadUi("account.ui", self)
        self.usernamelabel.setText(Login.user)
        self.passwordlabel.setText(Login.passw)
        self.backtomainpagebutton.clicked.connect(self.gotomainpage)
        self.logoutbutton.clicked.connect(self.gotologinpage)
        self.updatebutton.clicked.connect(self.newInfoFx)

    def newInfoFx(self):
        if self.newconfirmpass.text() == self.newpassword.text() and self.newpassword.text() != "" and self.newusername.text() != "":
            cruder.user_crud.update(cruder.PersonId(Login.user, Login.passw), password=self.newpassword.text())
            Login.passw = self.newpassword.text()
            self.passwordlabel.setText(self.newpassword.text())
            cruder.user_crud.update(cruder.PersonId(Login.user, Login.passw), name=self.newusername.text())
            Login.user = self.newusername.text()
            self.usernamelabel.setText(self.newusername.text())
            self.newusername.setText("")
            self.newpassword.setText("")
            self.newconfirmpass.setText("")
        elif self.newconfirmpass.text() == "" and self.newpassword.text() == "":
            cruder.user_crud.update(cruder.PersonId(Login.user, Login.passw), name=self.newusername.text())
            Login.user = self.newusername.text()
            self.usernamelabel.setText(self.newusername.text())
            self.newusername.setText("")
        elif self.newconfirmpass.text() == self.newpassword.text() and self.newpassword.text() != "":
            cruder.user_crud.update(cruder.PersonId(Login.user, Login.passw), password=self.newpassword.text())
            Login.passw = self.newpassword.text()
            self.passwordlabel.setText(self.newpassword.text())
            self.newpassword.setText("")
            self.newconfirmpass.setText("")

    def gotologinpage(self):
        GoToLoginPage()

    def gotomainpage(self):
        GoToMainPage()


class Board(QDialog):
    item_val = ""
    item_id = 1
    def __init__(self):
        print("opening board")
        super(Board, self).__init__()

        loadUi("newboard.ui", self)
        self.addcolumnbutton.clicked.connect(self.addcolumnfunction)
        self.btmp_button.clicked.connect(self.gotomainpage)
        self.boardnamelabel.setText(MainPage.val)
        self.calbutton.clicked.connect(self.runcalculator)
        a = cruder.Reader("Board", cruder.BoardId(self.boardnamelabel.text()))
        b = cruder.get_all_user_nicknames()
        b.remove(a.creator)
        d = ast.literal_eval(a.users)
        c = [x for x in b if x not in d]
        self.comboBox_2.addItems(c)
        vbox = QHBoxLayout()
        vbox.setSpacing(0)
        THEboard = cruder.Reader("Board", cruder.BoardId(self.boardnamelabel.text()))
        columns = ast.literal_eval(THEboard.columns)


        columns_q = len(columns)
        if columns_q > 0:
            d = len(ast.literal_eval(a.columns))
            for i in range(d):
                column = cruder.Reader("Column", columns[i])
                print(column.title, i)
                # create a new QLabel and add it to the QHBoxLayout
                label = QLabel(column.title)
                label.setAlignment(Qt.AlignTop)
                vbox.addWidget(label)
                label.setStyleSheet("color:rgb(255, 255, 255); font-size:12pt;")

                # create a new QListWidget
                list_widget = QListWidget()
                list_widget.setStyleSheet("color:rgb(255, 255, 255); font-size:12pt;")
                list_widget.setFixedSize(200, 400)

                # set the list widget to display items horizontally
                list_widget.setViewMode(QListWidget.IconMode)
                list_widget.setResizeMode(QListWidget.Adjust)

                # create an "Add Item" button
                add_button = QPushButton('+')
                add_button.setFixedWidth(70)
                add_button.setStyleSheet("background-color:rgb(85, 170, 127); color:rgb(255, 255, 255); font-size:12pt;")
                add_item_button = QListWidgetItem()
                add_item_button.setSizeHint(add_button.sizeHint())
                list_widget.addItem(add_item_button)
                list_widget.setItemWidget(add_item_button, add_button)

                # create a "Delete"button and add it to the QHBoxLayout
                del_button = QPushButton('X')
                del_button.setFixedWidth(10)
                del_button.setStyleSheet("background-color:red; color:rgb(255, 255, 255); font-size:12pt;")
                del_item_button = QListWidgetItem()
                del_item_button.setSizeHint(del_button.sizeHint())
                vbox.addWidget(list_widget)
                vbox.addWidget(del_button)
                cards = ast.literal_eval(column.cards)
                if cards is not None:
                    print(cards)
                    for i in range(len(cards)):
                        card = cruder.Reader("Card", int(cards[i]))
                        print(card.title)
                        new_item = QListWidgetItem(card.title)
                        new_item.setSizeHint(QSize(new_item.sizeHint().width(), new_item.sizeHint().height()))
                        list_widget.insertItem(list_widget.row(add_item_button), new_item)

                # add a spacer item to the QHBoxLayout to push the next column to the right
                spacer_item = QSpacerItem(20, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
                vbox.addItem(spacer_item)

                # set the alignment of the QHBoxLayout to left
                vbox.setAlignment(Qt.AlignLeft)

                # connect the "Add Item" button's clicked signal to a slot that adds a new item to the list
                add_button.clicked.connect(lambda: self.add_item(list_widget, add_item_button, column))

                # connect the "Delete" button's clicked signal to a slot that removes thelist widget and delete button
                del_button.clicked.connect(lambda: self.delete_column(vbox, list_widget, column, del_button))

                # add the QHBoxLayout to the horizontal layout
                self.hrlayout.insertLayout(self.hrlayout.count() - 1, vbox)
                list_widget.itemDoubleClicked.connect(self.opencardfunction)

                # adjust the spacing between the QHBoxLayouts to stack them close to each other
                self.hrlayout.setSpacing(0)
                list_widget.setStyleSheet(
                    "QListWidget::item { min-width: 190px; max-width: 200px; background-color: #666666; color: white; margin-left: 3px;}")
                print(d)
        else:
            print("No Columns on this Board")
        print("Вошел мистер: " + Login.user)
        print("В страницу: " + self.boardnamelabel.text())


        if cruder.checkifyouanauthor(Login.user, self.boardnamelabel.text()):
            self.comboBox_2.setVisible(True)
            self.comboBox_2.setEnabled(True)
            self.pushButton.setVisible(True)
            self.pushButton.setEnabled(True)
            self.pushButton_2.setVisible(True)
            self.pushButton_2.setEnabled(True)
        else:
            self.comboBox_2.setVisible(False)
            self.comboBox_2.setEnabled(False)
            self.pushButton.setVisible(False)
            self.pushButton.setEnabled(False)
            self.pushButton_2.setVisible(False)
            self.pushButton_2.setEnabled(False)

        self.pushButton.clicked.connect(self.AddUser)
        self.pushButton_2.clicked.connect(self.RemoveUser)

        a_array = ast.literal_eval(a.users)
        for i in range(len(a_array)):
            item = QtWidgets.QListWidgetItem(a_array[i])
            # Add the item to the list widget
            self.memberlist.addItem(item)



    def AddUser(self):
        if self.comboBox_2.currentText() != '':
            a = cruder.Reader("Board", cruder.BoardId(self.boardnamelabel.text()))
            b = ast.literal_eval(a.users)
            b.append(str(self.comboBox_2.currentText()))
            cruder.board_crud.update(a.id, users=str(b))
            print(b)
            self.memberlist.addItem(self.comboBox_2.currentText())
            current_index = self.comboBox_2.currentIndex()
            self.comboBox_2.removeItem(current_index)

    def RemoveUser(self):
        a = cruder.Reader("Board", cruder.BoardId(self.boardnamelabel.text()))
        b = ast.literal_eval(a.users)
        member = self.memberlist.currentRow()
        item = self.memberlist.item(member)
        b.remove(str(item.text()))
        cruder.board_crud.update(a.id, users=str(b))
        self.memberlist.takeItem(member)
        del item

        a = cruder.Reader("Board", cruder.BoardId(self.boardnamelabel.text()))
        b = cruder.get_all_user_nicknames()
        b.remove(a.creator)
        d = ast.literal_eval(a.users)
        c = [x for x in b if x not in d]
        e = list(set([x for x in c if x]))
        self.comboBox_2.clear()
        self.comboBox_2.addItems(e)

    def runcalculator(self):
        calc.Calculator.run(self)
    def gotomainpage(self):
        GoToMainPage()

    def addcolumnfunction(self):
        dialog = MyDialog()
        text = ''
        if dialog.exec_() == QDialog.Accepted:
            text = dialog.text()
        if text != '':
            print(text)
            vbox = QHBoxLayout()
            vbox.setSpacing(0)
            a = cruder.Reader("Board", cruder.BoardId(self.boardnamelabel.text()))
            print(a.id)
            b = ast.literal_eval(a.columns)
            print(b)
            c = len(b)
            column = cruder.column_crud.create(text, '[]')
            print(column.id)
            b.append(column.id)
            cruder.board_crud.update(a.id, columns=str(b))
            column = cruder.Reader("Column", column.id)
            # create a new QLabel and add it to the QHBoxLayout
            label = QLabel(text)
            label.setAlignment(Qt.AlignTop)
            vbox.addWidget(label)
            label.setStyleSheet("color:rgb(255, 255, 255); font-size:12pt;")

            # create a new QListWidget
            list_widget = QListWidget()
            list_widget.setStyleSheet("color:rgb(255, 255, 255); font-size:12pt;")
            list_widget.setFixedSize(200, 400)

            # set the list widget to display items horizontally
            list_widget.setViewMode(QListWidget.IconMode)
            list_widget.setResizeMode(QListWidget.Adjust)

            # create an "Add Item" button
            add_button = QPushButton('+')
            add_button.setFixedWidth(70)
            add_button.setStyleSheet("background-color:rgb(85, 170, 127); color:rgb(255, 255, 255); font-size:12pt;")
            add_item_button = QListWidgetItem()
            add_item_button.setSizeHint(add_button.sizeHint())
            list_widget.addItem(add_item_button)
            list_widget.setItemWidget(add_item_button, add_button)

            # create a "Delete"button and add it to the QHBoxLayout
            del_button = QPushButton('X')
            del_button.setFixedWidth(10)
            del_button.setStyleSheet("background-color:red; color:rgb(255, 255, 255); font-size:12pt;")
            del_item_button = QListWidgetItem()
            del_item_button.setSizeHint(del_button.sizeHint())
            vbox.addWidget(list_widget)
            vbox.addWidget(del_button)

            # add a spacer item to the QHBoxLayout to push the next column to the right
            spacer_item = QSpacerItem(20, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
            vbox.addItem(spacer_item)

            # set the alignment of the QHBoxLayout to left
            vbox.setAlignment(Qt.AlignLeft)
            column = cruder.Reader("Column", column.id)
            # connect the "Add Item" button's clicked signal to a slot that adds a new item to the list
            add_button.clicked.connect(lambda: self.add_item(list_widget, add_item_button, column))

            # connect the "Delete" button's clicked signal to a slot that removes thelist widget and delete button
            del_button.clicked.connect(lambda: self.delete_column(vbox, list_widget, column, del_button))



            # add the QHBoxLayout to the horizontal layout
            self.hrlayout.insertLayout(self.hrlayout.count() - 1, vbox)
            list_widget.itemDoubleClicked.connect(self.opencardfunction)

            # adjust the spacing between the QHBoxLayouts to stack them close to each other
            self.hrlayout.setSpacing(0)
            list_widget.setStyleSheet(
                "QListWidget::item { min-width: 190px; max-width: 200px; background-color: #666666; color: white; margin-left: 3px;}")
        else:
            pass

    def delete_column(self, hbox, list_widget, column, del_button):
        # remove the QHBoxLayout from the horizontal layout
        self.hrlayout.removeItem(hbox)

        # get the QListWidget and Delete button from the QHBoxLayout
        list_widget = hbox.itemAt(0).widget()
        del_button = hbox.itemAt(1).widget()

        # remove the QListWidget and Delete button from their parent and delete them
        hbox.removeWidget(list_widget)
        hbox.removeWidget(del_button)
        list_widget.deleteLater()
        del_button.deleteLater()


        del_button.setVisible(False)
        del_button.setEnabled(False)



        #Text
        # print(self.boardnamelabel.text(), list_widget.text())
        print(11111, type(column.id), column.id)
        board1 = cruder.Reader("Board", cruder.BoardId(self.boardnamelabel.text()))
        a1 = ast.literal_eval(board1.columns)
        a1.remove(column.id)
        cruder.board_crud.update(board1.id, columns=a1)
        cruder.column_crud.delete(column.id)



    def add_item(self, list_widget, item, column):
        dialog = MyDialog()
        text = ''
        if dialog.exec_() == QDialog.Accepted:
            text = dialog.text()

        # create a new item and add it to the list
        if text != '':
            column = cruder.Reader("Column", column.id)
            card = cruder.card_crud.create(text, '', '', column.id, '')
            arr = ast.literal_eval(column.cards)
            print(column.cards)
            arr.append(str(card.id))
            print(arr)
            cruder.column_crud.update(column.id, cards=arr)
            new_item = QListWidgetItem(text)
            new_item.setSizeHint(QSize(new_item.sizeHint().width(), new_item.sizeHint().height()))
            list_widget.insertItem(list_widget.row(item), new_item)

        else:
            pass

    # def deleteitemfunction(self): # Добавил
    #     print("0's check")
    #     current_row = self.list_widget.currentRow()
    #     print("1's check" + current_row)
    #     if current_row != -1:  # Check if any item is selected
    #         print("2's check")
    #         item = self.list_widget.item(current_row)
    #         print("3's check")
    #         if item is not None:
    #             self.list_widget.takeItem(current_row)
    #             del item
    #     else:
    #         print("4's check")
    #         print("No item selected.")


    def opencardfunction(self, item):
        Board.item_val = item.text()
        print("Item val is", Board.item_val)
        Board.item_id = cruder.CardId(Board.item_val)
        print("id is ", Board.item_id)
        card = Card()
        card.exec_()


class MyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("My Dialog")

        self.label = QLabel("Enter some text:")
        self.line_edit = QLineEdit()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        layout = QVBoxLayout()
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.ok_button)
        hlayout.addWidget(self.cancel_button)

        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addLayout(hlayout)
        self.setLayout(layout)

        # self.editcardbutton.clicked.connect()

    def text(self):
        return self.line_edit.text()

    def edit_inputs_edit(self):
        card_title = self.cardtitle.Text()
        card_description = self.description.Text()
        # card_image = self.

class Card(QDialog):


    def __init__(self):
        super(Card, self).__init__()
        loadUi("card.ui", self)
        self.uploadIMGbutton.clicked.connect(self.uploadimagefunction)
        self.description.setReadOnly(False)
        self.editcardbutton.clicked.connect(self.submittext)
        self.cardtitle.setText(Board.item_val)
        card = cruder.Reader("Card", Board.item_id)
        print("Card is", card.title, card.description)
        self.description.setPlainText(card.description)
        # Get the size of the label
        label_width = self.IMGbox.width()
        label_height = self.IMGbox.height()
        filepath = card.thumbnail
        pixmap = QPixmap(filepath).scaled(label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.IMGbox.setPixmap(pixmap)

    def submittext(self):
        card = cruder.Reader("Card", Board.item_id)
        text = self.description.toPlainText()
        cruder.card_crud.update(card.id, description=text)
        #                                                        Изменение описания определенной карточки столбца доски пользователя
        GoToBoardPage()

    def uploadimagefunction(self):
        # Open a file dialog and get the path to the selected image file
        filepath, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        card = cruder.Reader("Card", Board.item_id)
        # Get the size of the label
        label_width = self.IMGbox.width()
        label_height = self.IMGbox.height()

        # Create a QPixmap object from the image file and scale it to fit inside the label
        pixmap = QPixmap(filepath).scaled(label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        nf = os.path.basename(filepath)
        cruder.card_crud.update(card.id, thumbnail=nf)
        # Set the pixmap to the label
        self.IMGbox.setPixmap(pixmap)
        #                                               Изменение-загрузка в базу данных этой карточки изображения столбец-доска-пользователь


app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
trello = Login()
widget.addWidget(trello)
widget.resize(trello.size())
widget.show()
app.exec_()
