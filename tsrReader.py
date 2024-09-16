import os
from tkinter.filedialog import askopenfilename
from tkinter import *

# Global Variables
selected_parameters = []
filename = "Please choose a file"

system_information_list = [
    'Model',
    'Serial number',
    'Firmware Version',
    'Authentication Code',
    'Registration Code',
    'HA Mode'
]

# Retrieve selected checkbox options
def getChecked():
    # Clear output file if exists
    open("output.txt", "w").close()

    for var in selected_parameters:
        value = var.get()
        if value:
            parseFile(filename, value)

    try:
        os.startfile("output.txt")
    except:
        print("Automatic file opening only supported on Windows OS")

    #quit()

# Open file selector and retrieve filepath
def getFile():
    global filename
    filename = askopenfilename()
    updateFilepathDisplay(filename)

# Function call to update label
def updateFilepathDisplay(filepath):
    displayVar.set(filepath)

# Close UI window
def quit():
    root.quit()

# Parse selected file for data; switch case for each checkbox selection
def parseFile(filepath, value):
    with open(filepath, "r", errors="ignore") as file:
        content = file.read()

        # Process read file depending on which checkboxes were selected
        if value == "System Information":
            start = content.index('\n--System Information--')
            end = content.index('\nInternal Instance')
            info_block = content[start:end]
            result = "--System Information--\n"
            info_block_split = info_block.split('\n')
            for line in info_block_split:
                if list(filter(line.startswith, system_information_list)):
                    result += line
                    result += '\n'
            write_output(result)
        if value == "Network Interfaces (Brief)":
            start = content.index('\n--Network Interfaces--\nName')
            end = content.index('\n#System : Status_END')
            info_block = content[start:end]
            write_output(info_block.split("#Blade")[0])

# Write parsed information to output txt
def write_output(information):
    outputFile = "output.txt"
    file = open(outputFile, "a")
    file.write(information)
    file.close
    print(information)

# General UI Settings
root = Tk()
root.geometry('850x550')
root.title("TSR Reader")

# Labels
displayVar = StringVar()
label_1 = Label(root, text="Selected File:", width=500, font=("bold", 10), anchor="w")
label_1.place(x=35, y=90)
displayLab = Label(root, textvariable=displayVar, width=500, font=("bold", 10), anchor="w")
displayLab.place(x=35, y=120)

# Conditions checkbutton

# Range needs to equal number of checkbox options
for i in range(6):
    option = StringVar(value="")
    selected_parameters.append(option)

Checkbutton(root, text="System Information", variable=selected_parameters[0], onvalue="System Information", offvalue="").place(x=130, y=150)
Checkbutton(root, text="Network Interfaces (Brief)", variable=selected_parameters[1], onvalue="Network Interfaces (Brief)", offvalue="").place(x=270, y=150)
Checkbutton(root, text="Network Interfaces (Detailed)", variable=selected_parameters[2], onvalue="Network Interfaces (Detailed)", offvalue="").place(x=410, y=150)
Checkbutton(root, text="Management Ports", variable=selected_parameters[3], onvalue="Management Ports", offvalue="").place(x=560, y=150)
Checkbutton(root, text="Zones", variable=selected_parameters[4], onvalue="Zones", offvalue="").place(x=130, y=180)
#Checkbutton(root, text="Placeholder", variable=selected_parameters[5], onvalue="Placeholder", offvalue="").place(x=270, y=180)

# Buttons
Button(root, text='Browse', command=getFile, width=20, bg='brown', fg='white').place(x=180, y=400)
Button(root, text='Submit', command=getChecked, width=20, bg='brown', fg='white').place(x=510, y=400)

# UI Window renderer
root.mainloop()