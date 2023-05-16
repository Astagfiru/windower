import tkinter as tk
import tkinter.simpledialog


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


if __name__ == "__main__":
    # Create window
    root = tk.Tk()

    # Create BoardListPage instance
    board_list_page = BoardListPage(root)

    # Start GUI event loop
    root.mainloop()
