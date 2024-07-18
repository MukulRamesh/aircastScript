# pyinstaller ./src/gui.py --add-data="C:\...\venv\Lib\site-packages\tkinterDnD\*;."

import tkinter as tk
from tkinter import ttk
import tkinterDnD  # Importing the tkinterDnD module
import os.path
import unzip
import cleanup
import traceback

# --- Logging code ---
import sys
import datetime

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("log.txt", "a")

    def write(self, message):
        now = datetime.datetime.now()
        timedMessage = str(now) + " : " + message
        if (message != '\n'):
            self.log.write(timedMessage + '\n')
        self.terminal.write(message)

stdOut = sys.stdout
sys.stdout = Logger()
# --- End Logging code ---


# You have to use the tkinterDnD.Tk object for super easy initialization,
# and to be able to use the main window as a dnd widget
root = tkinterDnD.Tk()
root.title("AirCast Export Utility - Mukul Ramesh")
root.geometry('600x600')

label = ttk.Label(root, text='Drag and drop the exported zip files into the box below!')
label.pack(ipadx=10, ipady=10)

periodLabel = ttk.Label(root, text='Period Length \n(How far back should the graph go?) \nIf this value reaches earlier than the first entry, then the entire data set will be graphed.')
periodLabel.pack(ipadx=10, ipady=10)

periodLengthOptions = ["24 Hours", "1 Week", "2 Weeks", "3 Weeks", "30 Days", "60 Days", "90 Days"]
periodLengthText = tk.StringVar(root); periodLengthText.set(periodLengthOptions[2])
periodLengthDropDown = tk.OptionMenu(root, periodLengthText, *periodLengthOptions).pack()

averageLabel = ttk.Label(root, text='Averaging Length \n(What size block of time should I average?)')
averageLabel.pack(ipadx=10, ipady=10)

averageLengthOptions = ["15 Minutes", "30 Minutes", "1 Hour", "2 Hours", "6 Hours", "8 Hours","12 Hours", "24 Hours"]
averageLengthText = tk.StringVar(root); averageLengthText.set(averageLengthOptions[2])
averageLengthDropDown = tk.OptionMenu(root, averageLengthText, *averageLengthOptions).pack()

intervalLabel = ttk.Label(root, text='Tick Interval Length \n(How often should I place one tick on the x-axis?)')
intervalLabel.pack(ipadx=10, ipady=10)

intervalLengthOptions = ["1 Hour","6 Hours","12 Hours","1 Day", "7 Days", "14 Days"]
intervalLengthText = tk.StringVar(root); intervalLengthText.set(intervalLengthOptions[3])
intervalLengthDropDown = tk.OptionMenu(root, intervalLengthText, *intervalLengthOptions).pack()

dotIntervalLabel = ttk.Label(root, text='Dot Interval Length \n(How often should I place a dot?)')
dotIntervalLabel.pack(ipadx=10, ipady=10)

dotIntervalLengthOptions = ["1 Hour","6 Hours","12 Hours","1 Day", "7 Days", "14 Days"]
dotIntervalLengthText = tk.StringVar(root); dotIntervalLengthText.set(dotIntervalLengthOptions[2])
dotIntervalLengthDropDown = tk.OptionMenu(root, dotIntervalLengthText, *dotIntervalLengthOptions).pack()



titleTKVar = tk.BooleanVar()
ttk.Checkbutton(root,
                text='Title Inclusion (Should I title each graph?)',
                variable=titleTKVar,
                onvalue=True,
                offvalue=False).pack()


getOpenAQTKVar = tk.BooleanVar()
ttk.Checkbutton(root,
                text='Outside Air Quality Inclusion (Should I also graph outside air quality in Trenton?)',
                variable=getOpenAQTKVar,
                onvalue=True,
                offvalue=False).pack()
getOpenAQTKVar.set(True)


fullFilePaths = []

def updateLabelText(text):
    boxText.set(text + "\n" + boxText.get())
    root.update_idletasks()

def clearLabelText():
    boxText.set('')
    root.update_idletasks()

def drop(event):
    # This function is called, when stuff is dropped into a widget
    if (len(fullFilePaths) == 0):
        clearLabelText()

    paths = str(event.data)

    if "} {" in paths:
        splitPath = paths.split("} {")
    else:
        splitPath = paths.split(" ")

    for path in splitPath:
        path = path.removeprefix("{").removesuffix("}")

        pathSplit = path.split('/')

        fileName = pathSplit[-1].strip()

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

        periodLengthStr = periodLengthText.get()
        averageLengthStr = averageLengthText.get()
        intervalLengthStr = intervalLengthText.get()
        dotIntervalLengthStr = dotIntervalLengthText.get()
        includeTitle = titleTKVar.get()
        updateLabelText("Grabbed configured options...")

        try:
            unzip.unzipList(fullFilePaths)
            updateLabelText("Unzipped files...")
            cleanup.makeCleanGraph(periodLengthStr, averageLengthStr, intervalLengthStr, dotIntervalLengthStr, includeTitle)
            updateLabelText("Generated graphs...")
            unzip.deleteTempFiles()
            updateLabelText("Deleted temporary files...")
            os.startfile(os.path.realpath("./output/"))
            updateLabelText("Opening output folder...")
            root.destroy()
        except Exception as e:
            print(f"Config options: {periodLengthStr}, {averageLengthStr}, {intervalLengthStr}, {dotIntervalLengthStr}, {includeTitle}")
            boxText.set("An problem occurred. Please quit, and see log file for more details.")
            traceback.print_exception(e, file=sys.stdout)






# With DnD hook you just pass the command to the proper argument,
# and tkinterDnD will take care of the rest
# NOTE: You need a ttk widget to use these arguments
boxText = tk.StringVar()
boxText.set('')

label_2 = ttk.Label(root, onfiledrop=drop,
                    textvar=boxText, padding=10, relief="solid")
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
sys.stdout = stdOut # Need to set back to avoid error.

