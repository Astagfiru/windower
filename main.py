import tkinter as tk
from tkinter import *
from tkinter import ttk


class App:
    def __init__(self, master):
        self.master = master
        self.board = tk.Frame(self.master)
        self.board.pack()

        self.columns = []

        self.add_column_button = tk.Button(self.board, text="Add Column", command=self.add_column)
        self.add_column_button.pack(side="top", pady=5)

    def add_column(self):
        column_frame = tk.Frame(self.board, bd=1, relief="solid")
        column_frame.pack(side="left", padx=5, pady=5, fill="y")

        column_title = tk.Entry(column_frame)
        column_title.pack(side="top", pady=5)

        card_frame = tk.Frame(column_frame)
        card_frame.pack(side="top", pady=5)

        add_card_button = tk.Button(card_frame, text="Add Card", command=lambda: self.add_card(card_frame))
        add_card_button.pack(side="left", padx=5)

        self.columns.append(column_frame)

    def add_card(self, card_frame):
        card_entry = tk.Entry(card_frame)
        card_entry.pack(side="top", pady=5)


window = Tk()
notebook = ttk.Notebook(window)  # widget that manages a collection of windows/displays
notebook.pack(fill='both', expand=True)


def add_tab():
    tab = ttk.Frame(notebook)
    notebook.add(tab, text='New Tab')


tab1 = Frame(notebook)

canvas = tk.Canvas(tab1, width=200, height=100, bg='pink')
canvas.pack(fill='both', expand=True)

style = ttk.Style()
style.configure('My.TButton', font=('TkDefaultFont', 25), background='pink', foreground='Blue')

button_login = ttk.Button(tab1, text='Login', style='My.TButton', )
button_login.place(relx=0.5, rely=0.3, anchor='center')
button_signup = ttk.Button(tab1, text='Signup', style='My.TButton')
button_signup.place(relx=0.5, rely=0.5, anchor='center')


def open_new_window(self):
    new_window = tk.Toplevel(self.master)
    new_window.title("New Window")

    label = tk.Label(new_window, text="This is a new window!")
    label.pack()


tab2 = ttk.Frame(notebook)
button = ttk.Button(tab2, text='Create Board', style='My.TButton', command=add_tab())
button.pack(side='top')

notebook.add(tab1, text="Main page")
notebook.add(tab2, text='Board')

tab3 = Frame(notebook)
notebook.add(tab3, text='tab3')
tab_app = App(tab3)

window.mainloop()
