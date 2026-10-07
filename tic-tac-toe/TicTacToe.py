import tkinter as tk
from tkinter import messagebox
from itertools import cycle


class Logic:

    """
    Engine for X, O player handling and winner logic
    """


    def __init__(self):

        self.player = cycle(("X", "O"))
        self.matrix = []
        for i in range(3):
            self.matrix.append([])
            for j in range(3):
                self.matrix[i].append(None)


    def mainLogic(self, args = []):

        # Somewere I read that explicit is better than implicit
        row = args[0]
        col = args[1]
        frame = args[2]
        
        player = next(self.player)
        self.matrix[row][col] = player

        win = False
        if self.matrix[row][0] == self.matrix[row][1] and self.matrix[row][0] == self.matrix[row][2]:
            win = True
        if self.matrix[0][col] == self.matrix[1][col] and self.matrix[0][col] == self.matrix[2][col]:
            win = True
        if row == col:
            if self.matrix[0][0] == self.matrix[1][1] and self.matrix[0][0] == self.matrix[2][2]:
                win = True
            if self.matrix[2][0] == self.matrix[1][1] and self.matrix[2][0] == self.matrix[0][2]:
                win = True
        
        if win:
            frame.deactivate_all()
            messagebox.showinfo(title=None, message=f"vittoria di {player}")
            return player

        return player


class BtnFrame(tk.Frame):

    """
    Tkinter frame custom class where you can put at build time an integer number of buttons
    """
    
    def deactivate_all(self):
        for btn in self.winfo_children():
            btn["state"] = "disabled"


    def btn_action(self, event):
        __doc__ == """
        Function for the frame buttons
        Takes an event and handles it (I honestly don't know how)
        Calls the logic engine and passes it whatever it needs to work
        """
        btn = event.widget
        info = event.widget.grid_info()
        row = info["row"]
        column = info["column"]
        btn["text"] = self.logic.mainLogic(args = [row, column, self]) if btn["text"] == " " and btn["state"] != "disabled" else btn["text"]


    def __init__(self, rows, logic):

        __doc__ = """
        Custom tkinter frame that spawns a row x row button square
        ----------
        Attributes
        ----------
        rows : int
            the number of lines and/or columns for the square of buttons
        """

        rows = int(rows)
        tk.Frame.__init__(self)
        for i in range(rows ** 2):
            btn = tk.Button(self, 
                    text = " ",
                    padx = 50, 
                    pady = 50, 
                    fg = "white",
                    bg = "black"
            )
            btn.bind("<Button-1>", self.btn_action)
            btn.grid(row = i % rows, column = i // rows)
        self.logic = logic


class TicTacToe(tk.Tk):
    
    __doc__ = """
    Root window for tic tac toe
    It creates a 3x3 BtnFrame and packs it
    """


    def __init__(self, logic):
        tk.Tk.__init__(self)
        ROWS = 3
        frame = BtnFrame(ROWS, logic)
        frame.pack()


class Main:

    __doc__ == """
    Actual main class for tic tac toe
    ----------
    Methods
    ----------
    main()
        Main loop for tic tac toe
    """


    def __init__(self):
        pass


    def main():
        logic = Logic()
        root = TicTacToe(logic)
        root.mainloop()


if __name__ == "__main__":
    Main.main()
