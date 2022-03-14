import tkinter as tk
from tkinter import messagebox
from note import Note
from save import Save
from promptWin import PromptWin

"""Main module of the program, has notebook class that extends tkinter. 
Creates the program gui via a tkinter window and responds to any events triggered by the user."""

class Notebook(tk.Tk):
    #class scoped variables for window colors and text
    color1 = "orange"
    color2 = "green"
    appTitle = "Vas's Note Book"
    subjFrameTitle = "Your Subjects"
    instructions = "1. In the left panel, enter subject name, and press GET to get the saved notes for that subject. Also, at the bottom of the panel is the CLOSE PROGRAM button, which can be used to shut down the application at anytime.\n\n" + \
        "2. In the right panel, create or edit the notes, enter the name of a subject to save to, and click SAVE NOTES. If the subject does not exist, it will be created, and the notes will be saved to it. This is how new subjects can be added to your list.\n\n" + "3. Also in the right panel, you can enter a subject name, and click DELETE SUBJECT to remove that subject and all notes associated with it. Warning, this cannot be undone."  
    
    
    #getNotes will return a list of saved note instances or empty list
    notesList = Save.getNotes() 
    
    #Initialize the Notebook instance
    def __init__(self):
        tk.Tk.__init__(self)
        self.title(Notebook.appTitle)
        self.geometry("1100x700")

        #subjects frame 
        self.subjFrame = tk.Frame(master = self, width = 300, height = 200, bg = Notebook.color1, borderwidth = 5, relief = tk.RAISED)
        self.subjFrame.pack(side = tk.LEFT, fill = tk.BOTH, padx = 5, pady = 5)
         #used to stop frame from shrinking to wrap widget
        self.subjFrame.pack_propagate(False)
        
        #label for subjects frame
        self.titleLabel = tk.Label(master = self.subjFrame, text = Notebook.subjFrameTitle, width = 20, height = 2, borderwidth = 2, relief = tk.SOLID)
        self.titleLabel.config(font = ("sans-serif", 16)) #used to change font of label
        self.titleLabel.pack(pady = 1)

        #frame for subjects section widgets, will have text entry, submit btn and dynamically made labels of subjects
        self.controlFrame = tk.Frame(master = self.subjFrame, bg = Notebook.color2)
        self.controlFrame.pack(side = tk.BOTTOM, fill = "x")

        #button to close main window
        self.btnCloseMain = tk.Button(master = self.controlFrame,  bg = "red", fg = "white", text = "CLOSE PROGRAM", command = self.closeProgram)
        self.btnCloseMain.pack(side = tk.BOTTOM, pady = 5)

        #subjects control frame widgets
        self.controlEntry = tk.Entry(master = self.controlFrame, width = 17, font=('sans-serif', 16))
        self.controlEntry.insert(0, "Get subject notes...") 
        self.controlEntry.pack(side = tk.LEFT, padx = 5, pady = 10)

        self.controlBtn = tk.Button(master = self.controlFrame, text = "GET", command = self.renderSubjText)
        self.controlBtn.config(font = ("sans-serif", 11)) #change control btn font
        self.controlBtn.pack(side = tk.RIGHT, padx = 5, pady = 10)

        #notes frame
        self.notesFrame = tk.Frame(master = self, bg = Notebook.color2, borderwidth = 5, relief = tk.RAISED)
        self.notesFrame.pack(side = tk.RIGHT, fill = tk.BOTH, expand = True, padx = 5, pady = 5)
       
        #textbox for notes frame
        self.textArea = tk.Text(master = self.notesFrame, padx = 5, pady = 5, wrap = tk.WORD)
        self.textArea.insert("0.0", Notebook.instructions)
        self.textArea.config(font = ("sans-serif bold", 16)) #configure text area font
        self.textArea.pack(padx = 10, pady = 10, fill = "y", expand = True)

        #create frame for notes controls/widgets
        self.noteControlPanel = tk.Frame(master = self.notesFrame, bg = Notebook.color1)
        self.noteControlPanel.pack(padx = 10, pady = 10, fill = "x")
        
        #delete btn to delete the subject TODO
        self.deleteBtn = tk.Button(master = self.noteControlPanel, text = "DELETE SUBJECT", bg = "red", fg = "white", command = self.openPromptWin)
        self.deleteBtn.pack(side = tk.RIGHT, padx = 5)

        #entry for subject title to be saved
        self.saveEntry = tk.Entry(master = self.noteControlPanel, width = 17, font=('sans-serif', 16))
        self.saveEntry.insert(0, "Save/Delete subject")
        self.saveEntry.pack(side = tk.LEFT, padx = 5, pady = 10)

        #button to save note/create subject
        self.saveBtn = tk.Button(master = self.noteControlPanel, text = "SAVE NOTES", command = self.saveNote)
        self.saveBtn.config(font = ("sans-serif", 11))
        self.saveBtn.pack(side = tk.LEFT, padx = 5, pady = 10)

        #On load of app, if note objects exist, note subjects are rendered 
        if len(Notebook.notesList) > 0:
            self.renderSubjTitles()

        for note in Notebook.notesList:
            print(note.getSubject())

    #instance methods******************************************************************************************
    def renderSubjTitles(self):
        """Adds label for each subject to subjects frame."""
        self.clearSubjFrame() #clear subjFrame first so do not repeat subject labels

        for note in Notebook.notesList: #Make a subject label for each note object
            title = note.getSubject()
            self.subjectTitle = tk.Label(master = self.subjFrame, text = title, width = 20, height = 2, relief = tk.RIDGE, border = 1)
            self.subjectTitle.config(font = ("", 16))
            self.subjectTitle.pack(side = tk.TOP, pady = 1)
            
        
    def renderSubjText(self):
        """User enters subject title, presses submit btn, if exists, note object found and rendered to user"""
        notesFound = False   #flag used to signal if the note being search is found
        subjTitle = self.controlEntry.get().strip()  #local scoped var holding entry's text

        #If subject title entered matches any note, render note text in text area
        for note in Notebook.notesList:
            if note.getSubject() == subjTitle:
                text = note.getText()
                self.changeTextboxText(self.textArea, text) #Remove text from box, render new text
                self.changeEntryText(self.saveEntry, subjTitle) #To display curr note subject to user. 
                notesFound = True

        if not notesFound:
            self.informUser(title = "Not Found", message = "Sorry, no subject by that name.")


    def saveNote(self):
        """
        Method finds correct note object, updates it, resaves all notes, 
        if note obj not found, addNewNote called to make it.
        
        """

        PLACE_HOLDER = "Save/Delete subject"
        PROMPTS = (
            "Enter the name of a subject.",
            "Subject title must be at least 1 character long.",
            "The subject title can be 20 charaters of less."
        )
        MAX_LENGTH = 20
        noteFound = False #flag to signal if note was found

        subjTitle = self.saveEntry.get().strip() #Get notes from text box

        #Below conditions ensure that input is of correct length and not the placeholder text from the entry.
        if subjTitle == PLACE_HOLDER:
            self.informUser(title = "Subject Name", message = PROMPTS[0])
        elif len(subjTitle) == 0:
            self.informUser(title = "Too Short", message = PROMPTS[1])
        elif len(subjTitle) > MAX_LENGTH:
            self.informUser("Too Long", PROMPTS[2])
        else:
            noteText = self.textArea.get("0.0", tk.END) #Get the note text from text box.
        
            for note in Notebook.notesList: #Search notelist for note object to update
                if subjTitle == note.getSubject():
                    note.setText(noteText)
                    Save.saveNotes(Notebook.notesList[0:])
                    noteFound = True

            if not noteFound:
                self.addNewNote(subjTitle, noteText) #If no matching note obj is found, new note obj is made, saved, and rendered.


    def addNewNote(self, title, text):
        """Creates new note object, adds them to list of note objects, rerenders updated list of subjects, takes title of note subject and note text as args."""
        newNote = Note(title, text)
        Notebook.notesList.append(newNote)
        Save.saveNotes(Notebook.notesList[0:])
        self.renderSubjTitles()


    def deleteNote(self):
        """Method handles deletion of note instance."""
        noteFound = False #local scoped flag var
        
        subjTitle = self.saveEntry.get().strip() #Start/end white space removed, titles may include any other chars.
        
        for note in Notebook.notesList: #Attempt to find matching note obj in notesList
            if subjTitle == note.getSubject():
                noteFound = True
                break
        
        if noteFound: #Iv noteFound flag is True, filter out the note, assign the filtered list to Notebook.noteList.
            Notebook.notesList = list(filter(lambda note: subjTitle != note.getSubject(), Notebook.notesList))
            Save.saveNotes(Notebook.notesList[0:])
            self.renderSubjTitles()    
            self.changeEntryText(self.saveEntry, "") #After note deleted clear save entry's text.
            self.changeTextboxText(self.textArea, f"{subjTitle} notes deleted.") #After note deleted render message confirming delete. 
        else:
            self.informUser("Not Found", "Subject not found.") #If not found, inform the user.



    def clearSubjFrame(self):
        """Removes current subject labels in subjects frame to avoid duplicating labels when rendering."""
        for label in self.subjFrame.winfo_children():
            if label != self.titleLabel and label != self.controlFrame: #To avoid destoying title label and control widgets.
                label.destroy()


    def informUser(self, title, message):
        """Takes arguments for title of message box and message"""
        return messagebox.showinfo(title=title, message=message) #Made general so can display other mssgs if needed.


    def openPromptWin(self):
        """Called when user cliks delete btn of main window, opens new window to confirm/cancel note delete."""
        promptWin = PromptWin(self)
        promptWin.grab_set() #Events directed to this window and containded widgets.

    def closeProgram(self):
        """Shuts down program on user click."""
        self.destroy()

    def changeEntryText(self, entry, text): 
        """Called to change text of an entry as needed. Args are the entry reference and new text."""
        entry.delete(0, tk.END) 
        entry.insert(0, text) 

    def changeTextboxText(self, textbox, text):
        """Deletes contents of textbox and renders text argument to the box. Takes ref to textbox and new text as args."""
        textbox.delete("0.0", tk.END)
        textbox.insert("0.0", text) 
        
       

def main():
    Notebook().mainloop()
    

if __name__ == "__main__":
    main()

