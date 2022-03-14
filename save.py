import pickle

"""
Module exports the Save class, methods of the class are static, and used to retrieve
and store Note class objects. 

"""

class Save():
    """Class has static methods to read a list of note objects from save file
    or write list of note objects to save file."""
    saveFile = "save_file"

    @staticmethod
    def saveNotes(noteList):
        """Method saves list of note objects or empty list, takes list of note instances/empty list to save."""
        fileObj = open(Save.saveFile, "wb")
        pickle.dump(noteList, fileObj)  
        fileObj.close()

    @staticmethod
    def getNotes():
        """Method returns list of note objects or empty list."""
        fileObj = open(Save.saveFile, "rb")
        fileContent =  pickle.load(fileObj)
        fileObj.close()
        return fileContent






                

