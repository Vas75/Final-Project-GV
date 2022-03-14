import tkinter as tk
import os

"""
Module responsible for the creation of custom dialog box used to get confirmation that the user 
wished to proceed with a note deletion. Module requires the instance ot the Notebook class as an argument for it's constructor function.

"""

class PromptWin(tk.Toplevel):
    """Class reponsible for creating second top level window that lets user confirm/cancel notes deletion. PromptWin extends tkinter Toplevel class. PromptWin constructor function requires the instance of the main window (Notebook)."""

    def __init__(self, mainWin): #Initialize and open prompt window
        super().__init__(mainWin)

        self.geometry("400x175")
        self.title("Delete")
        self.config(background = "orange", pady = 10)

        #dialog box message in label
        self.lblText = tk.Label(master = self, text = "Are you sure you want to delete these notes?", borderwidth = 1, relief = tk.RAISED, pady = 20, padx = 20)
        self.lblText.config(font = ("",13))
        self.lblText.pack(expand=True)

        #Frame to hold btns
        self.frameCtrls = tk.Frame(master = self, bg = "orange")
        self.frameCtrls.pack(expand = True)

        #image for delete btn
        self.imgDelete = tk.PhotoImage(file = "images" + os.sep + "myDeleteGif.gif")

        #image for cancel button
        self.imgCancel = tk.PhotoImage(file = "images" + os.sep + "myCancelGif.gif")
        
        #btns to confirm or cancel delete
        self.btnDelete = tk.Button(master = self.frameCtrls, text = "Delete", image = self.imgDelete, command = lambda: self.handleDel(mainWin))
        self.btnDelete.pack(side = tk.LEFT, padx = 10, pady = 20)

        self.btnCancel = tk.Button(master = self.frameCtrls, text = "Cancel", image = self.imgCancel, command = lambda: self.destroy()) #lambda function call .destroy() on window if deletion canceled
        self.btnCancel.pack(side = tk.LEFT, padx = 10, pady = 20)

    def handleDel(self, mainWin):
        """If delete is confirmed, deleteNote method called on the parent window, then self.destroy() closes the prompt window. """
        mainWin.deleteNote()
        self.destroy()
        
        


        
