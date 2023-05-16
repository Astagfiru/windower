import tkinter as tk
from tkinter import ttk

class MyButtonStyle(ttk.Style):
    def __init__(self, master):
        super().__init__(master)
        self.configure('My.button1', font=('TkDefaultFont', 25), background='pink', foreground='blue')
        self.congigure('My.button2', font=('Ariel',20), bg='black', fg='white')
        self.congigure('My.button3', font=('Courier New', 20), bg='purple', fg='yellow')
        self.congigure('My.button4', font=('Helvetica', 25), bg='brown', fg='green')


class MainPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Main Page")
        self.pack()

        # create login and signup buttons
        self.login_button = tk.Button(self, text="Login", command=self.show_login)
        self.login_button.pack()
        self.signup_button = tk.Button(self, text="Sign up", command=self.show_signup)
        self.signup_button.pack()

    def show_login(self):
        # destroy this frame and create new frame in full screen
        self.master.destroy()
        login_window = tk.Tk()
        login_window.title("Login Page")
        LoginPageFrame(login_window)

    def show_signup(self):
        # destroy this frame and create new frame in full screen
        self.master.destroy()
        signup_window = tk.Tk()
        signup_window.title("Sign up Page")
        SignupPageFrame(signup_window)


class LoginPageFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(padx=10, pady=10)

        # create username and password labels and entry widgets
        self.username_label = tk.Label(self, text="Username:")
        self.username_label.grid(row=0, column=0, sticky="w")
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=1)

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.grid(row=1, column=0, sticky="w")
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1)

        # create login button
        self.login_button = tk.Button(self, text="Enter(1)", command=self.show_board_list)
        self.login_button.grid(row=2, column=1, sticky="e")

    def show_board_list(self):
        self.destroy()
        board_window = tk.Toplevel(self.master)
        board_window.title("Board List Page")
        BoardListPageFrame(board_window)


class BoardListPage:
    def __init__(self, master):
        self.master = master
        self.board_buttons = []

        # Create "Create Board" button
        self.create_board_button = tk.Button(master, text="Create Board", command=self.create_board)
        self.create_board_button.pack()

    def create_board(self):
        # Get board name from user input
        board_name = tkinter.simpledialog.askstring("Create Board", "Enter board name:")

        # Create board button and delete button
        board_frame = tk.Frame(self.master)
        board_button = tk.Button(board_frame, text=board_name, command=lambda: self.open_board_page(board_name))
        delete_button = tk.Button(board_frame, text="X", command=lambda: self.delete_board(board_frame))

        # Pack board button and delete button into frame
        board_button.pack(side=tk.LEFT)
        delete_button.pack(side=tk.LEFT)

        # Pack frame into window
        board_frame.pack()

        # Add board button to list of buttons
        self.board_buttons.append(board_frame)

    def open_board_page(self, board_name):
        # Create new window for board page
        board_page_window = tk.Toplevel(self.master)
        board_page_window.title(board_name)

        # Add label to board page window
        label = tk.Label(board_page_window, text="This is the " + board_name + " board page!")
        label.pack()

    def delete_board(self, board_frame):
        # Remove board button from list of buttons
        self.board_buttons.remove(board_frame)

        # Destroy board button widget
        board_frame.destroy()
class SignupPageFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(padx=10, pady=10)

        # create email, username, password, and verify password labels and entry widgets
        self.email_label = tk.Label(self, text="Email:")
        self.email_label.grid(row=0, column=0, sticky="w")
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=0, column=1)

        self.username_label = tk.Label(self, text="Username:(2)")
        self.username_label.grid(row=1, column=0, sticky="w")
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=1, column=1)

        self.password_label = tk.Label(self, text="Password:(2)")
        self.password_label.grid(row=2, column=0, sticky="w")
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=2, column=1)

        self.verify_label = tk.Label(self, text="Verify password:")
        self.verify_label.grid(row=3, column=0, sticky="w")
        self.verify_entry = tk.Entry(self, show="*")
        self.verify_entry.grid(row=3, column=1)

        # create enter button
        self.enter_button = tk.Button(self, text="Enter(2)", command=self.master.destroy)
        self.enter_button.grid(row=4, column=1, sticky="e")


root = tk.Tk()
app = MainPage(master=root)
app.mainloop()
