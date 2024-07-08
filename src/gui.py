# pyinstaller ./src/gui.py --add-data="C:\...\venv\Lib\site-packages\tkinterDnD\*;."

import tkinter as tk
from tkinter import ttk
import tkinterDnD  # Importing the tkinterDnD module
import os.path
import unzip
import cleanup

# You have to use the tkinterDnD.Tk object for super easy initialization,
# and to be able to use the main window as a dnd widget
root = tkinterDnD.Tk()
root.title("AirCast Export Utility - Mukul Ramesh")
root.geometry('500x300')


stringvar = tk.StringVar()
stringvar.set('')

fullFilePaths = []

def updateLabelText(text):
    stringvar.set(text + "\n" + stringvar.get())
    root.update_idletasks()

def clearLabelText():
    stringvar.set('')
    root.update_idletasks()



def drop(event):
    # This function is called, when stuff is dropped into a widget
    if (len(fullFilePaths) == 0):
        clearLabelText()
    
    paths = str(event.data)

    for path in paths.split("} {"):
        path = path.removeprefix("{").removesuffix("}")

        pathSplit = path.split('/')

        fileName = pathSplit[-1]

        if (os.path.isfile(path)):
            fullFilePaths.append(path)
            updateLabelText(fileName)
        else:
            print("Ignoring because not a file: " + fileName)

def runUtility():
    if (len(fullFilePaths) == 0):
        clearLabelText()
        updateLabelText("You forgot to put the zip files in!")
    else:
        clearLabelText()
        updateLabelText("Working...")
        
        try:
            unzip.unzipList(fullFilePaths)
            updateLabelText("Unzipped files...")
            cleanup.makeCleanGraph()
            updateLabelText("Generated graphs...")
            unzip.deleteTempFiles()
            updateLabelText("Deleted temporary files...")
            os.startfile(os.path.realpath("./output/"))
            updateLabelText("Opening output folder...")
            root.destroy()
        except:
            stringvar.set("An problem occurred. Please see log file for more details.")


label = ttk.Label(root, text='Drag and drop the exported zip files into the box below!')
label.pack(ipadx=10, ipady=10)


# With DnD hook you just pass the command to the proper argument,
# and tkinterDnD will take care of the rest
# NOTE: You need a ttk widget to use these arguments
label_2 = ttk.Label(root, onfiledrop=drop,
                    textvar=stringvar, padding=10, relief="solid")
label_2.pack(fill="both", expand=True, padx=10, pady=10)

startButton = ttk.Button(root, text="Start Utility", command=runUtility)

startButton.pack(
    ipadx=5,
    ipady=10,
    expand=True,
    side=tk.LEFT
)

quitButton = ttk.Button(root, text="Quit", command=root.destroy)

quitButton.pack(
    ipadx=5,
    ipady=10,
    expand=True,
    side=tk.LEFT
)


root.mainloop()


