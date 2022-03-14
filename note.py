"""
Module exports the Note class, which is used to create instances of note. Each instace has methods to return note subject and text. The setText method is used to change the text attribute of the instance. The constructor function requires the note subject and 
the note text as arguements. 

"""

class Note():
    """Returns note objects, instance variables for subject and text of note, includes methods to get subject and text of note, and set note text."""
    def __init__(self, subject, text):
        """Initialize instances of note class."""
        self.subject = subject
        self.text = text

    def getSubject(self):
        return self.subject
    
    def getText(self):
        return self.text

    def setText(self, newText):
        self.text = newText

    def __str__(self):
        return f"subject: {self.subject}\ntext: {self.text}"


