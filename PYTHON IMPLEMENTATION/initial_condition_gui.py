import tkinter as tk
from tkinter import Scale
from tkinter import filedialog
from tkinter import Label
from tkinter import messagebox
import pickle

INITIAL_CONDITIONS =  {
            "Size" : 0, "I_Energy" : 0, "I_Age" : 0, "I_Distr" : "Uniform", 
            "Active" : 0, "C_Min" : 0, "C_Max" : 0, "C_Distr" : "Uniform", 
            "P_Distr" : "Uniform", 
            "Move" : 0, "Eat" : 0, "Rest" : 0, "Reproduce" : 0, 
            "Height" : 0, "Width" : 0
            }

def process_parameters(entries, root):
    global INITIAL_CONDITIONS
    INITIAL_CONDITIONS = {k : entries[k].get() for k in list(entries.keys())}
    root.destroy()

def save_as_file(entries):
    # WE DO NOT CHECK VALIDITY OF THE INITIAL DATA ! THAT'S A USER JOB FOR NOW
    actual_dict = {k : entries[k].get() for k in list(entries.keys())}
    file_path = filedialog.asksaveasfilename(
        title="Save File",
        defaultextension=".pkl",  # We save the file as pkl to use pickle
        filetypes=[ ("All Files", "*.*")]  # Set file type filters
    )
    
    if file_path:
        # Write some content to the chosen file
        with open(file_path, 'wb') as file:
            pickle.dump(actual_dict, file)

def load_from_file(entries):
    file_path = filedialog.askopenfilename(
        title="Open File",
        defaultextension=".pkl",  # We save the file as pkl to use pickle
        filetypes=[("All Files", "*.*")]  # Set file type filters
    )
    actual_dict = {}
    if file_path:
        # Write some content to the chosen file
        with open(file_path, 'rb') as file:
            actual_dict = pickle.load(file)
    
    for k in list(entries.keys()):
        entries[k].set(actual_dict[k])


def inital_condition_GUI():
    # THIS MAY SEEMS NOT TOO GOOD BUT IN FACT IS PRETTY GOOD 
    root = tk.Tk()
    root.title("INITIAL CONDITION GUI")

    entries = {}

    # POPULATION SETTINGS
    label1 = Label(root, text = "POPULATION SETTINGS")
    label1.grid(row = 0, column = 1, padx=10, pady=0)

    # SIZE
    label2 = Label(root, text = "Size : ")
    label2.grid(row = 1, column = 0, padx=10, pady=0)
    entries["Size"] = (Scale(root, from_=0, to=100, orient="horizontal"))
    entries["Size"].set(0)
    entries["Size"].grid(row = 1, column = 2, padx=10, pady=0)

    # AVG MAX ENERGY
    label3 = Label(root, text = "Avg max energy : ")
    label3.grid(row = 2, column = 0, padx=10, pady=0)
    entries["I_Energy"] = (Scale(root, from_=0, to=1000, orient="horizontal"))
    entries["I_Energy"].set(0)
    entries["I_Energy"].grid(row = 2, column = 2, padx=10, pady=0)

    # AVG MAX AGE
    label4 = Label(root, text = "Avg max age : ")
    label4.grid(row = 3, column = 0, padx=10, pady=0)
    entries["I_Age"] = (Scale(root, from_=0, to=1000, orient="horizontal"))
    entries["I_Age"].set(0)
    entries["I_Age"].grid(row = 3, column = 2, padx=10, pady=0)

    # INITAL DISTRIBUTION
    label5 = Label(root, text = "Initial spatial distribution : ")
    label5.grid(row = 4, column = 0, padx=10, pady=0)
    modalities1 = ["Uniform", "Gaussian"]
    entries["I_Distr"] = (tk.StringVar(root))
    entries["I_Distr"].set(modalities1[0])  # Impostare un'opzione predefinita
    dropdown1 = tk.OptionMenu(root, entries["I_Distr"], *modalities1)
    dropdown1.grid(row = 4, column = 2,padx=10, pady=0)

    # WORLD SETTING
    label6 = Label(root, text = "WORLD SETTINGS")
    label6.grid(row = 5, column = 1, padx=10, pady=0)

    # DENSITY
    label7 = Label(root, text = "Active cell % : ")
    label7.grid(row = 6, column = 0, padx=10, pady=0)
    entries["Active"] = (Scale(root, from_=1, to=100, orient="horizontal"))
    entries["Active"].set(0)
    entries["Active"].grid(row = 6, column = 2, padx=10, pady=0)

    # MIN ENERGY
    label8 = Label(root, text = "Minimum energy : ")
    label8.grid(row = 7, column = 0, padx=10, pady=0)
    entries["C_Min"] = (Scale(root, from_=0, to=1000, orient="horizontal"))
    entries["C_Min"].set(0)
    entries["C_Min"].grid(row = 7, column = 2, padx=10, pady=0)

    # MAX ENERGY
    label9 = Label(root, text = "Maximum energy : ")
    label9.grid(row = 8, column = 0, padx=10, pady=0)
    entries["C_Max"] = (Scale(root, from_=0, to=1000, orient="horizontal"))
    entries["C_Max"].set(0)
    entries["C_Max"].grid(row = 8, column = 2, padx=10, pady=0)

    # CELL DISTRIBUTION
    label10 = Label(root, text = "Initial distribution : ")
    label10.grid(row = 9, column = 0, padx=10, pady=0)
    modalities2 = ["Uniform", "Gaussian", "Multicenter"]
    entries["C_Distr"] = (tk.StringVar(root))
    entries["C_Distr"].set(modalities2[0])  # Impostare un'opzione predefinita
    dropdown2 = tk.OptionMenu(root, entries["C_Distr"], *modalities2)
    dropdown2.grid(row = 9, column = 2,padx=10, pady=0)

    # PARAMETERS SETTINGS
    label11 = Label(root, text = "PARAMETERS SETTINGS")
    label11.grid(row = 10, column = 1, padx=10, pady=0)

    # PARAMETERS DISTRIBUTION
    label12 = Label(root, text = "Initial distribution : ")
    label12.grid(row = 11, column = 0, padx=10, pady=0)
    modalities3 = ["Uniform", "Selfish", "Altruistic", "Normal", "Selfish-Altruistic", "Selfish-Normal", "Altruistic-Normal"]
    entries["P_Distr"] = (tk.StringVar(root))
    entries["P_Distr"].set(modalities3[0])  # Impostare un'opzione predefinita
    dropdown3 = tk.OptionMenu(root, entries["P_Distr"], *modalities3)
    dropdown3.grid(row = 11, column = 2,padx=10, pady=0)

    # ACTIONS SETTINGS
    label13 = Label(root, text = "ACTIONS SETTINGS")
    label13.grid(row = 12, column = 1, padx=10, pady=0)

    # MOVING COST
    label14 = Label(root, text = "Moving cost : ")
    label14.grid(row = 13, column = 0, padx=10, pady=0)
    entries["Move"] = (Scale(root, from_=0, to=1000, orient="horizontal"))
    entries["Move"].set(0)
    entries["Move"].grid(row = 13, column = 2, padx=10, pady=0)

    # EAT COST
    label15 = Label(root, text = "Eating cost : ")
    label15.grid(row = 14, column = 0, padx=10, pady=0)
    entries["Eat"] = (Scale(root, from_=0, to=1000, orient="horizontal"))
    entries["Eat"].set(0)
    entries["Eat"].grid(row = 14, column = 2, padx=10, pady=0)

    # REST COST
    label16 = Label(root, text = "Resting cost : ")
    label16.grid(row = 15, column = 0, padx=10, pady=0)
    entries["Rest"] = (Scale(root, from_=0, to=1000, orient="horizontal"))
    entries["Rest"].set(0)
    entries["Rest"].grid(row = 15, column = 2, padx=10, pady=0)

    # REPRODUCE COST
    label17 = Label(root, text = "Reproduce base cost : ")
    label17.grid(row = 16, column = 0, padx=10, pady=0)
    entries["Reproduce"] = (Scale(root, from_=0, to=1000, orient="horizontal"))
    entries["Reproduce"].set(0)
    entries["Reproduce"].grid(row = 16, column = 2, padx=10, pady=0)

    # SCREEN SETTINGS
    label18 = Label(root, text = "SCREEN SETTINGS")
    label18.grid(row = 17, column = 1, padx=10, pady=0)

    # HEIGHT
    label19 = Label(root, text = "Height : ")
    label19.grid(row = 18, column = 0, padx=10, pady=0)
    entries["Height"] = (Scale(root, from_=0, to=1000, orient="horizontal"))
    entries["Height"].set(0)
    entries["Height"].grid(row = 18, column = 2, padx=10, pady=0)

    # WIDTH
    label20 = Label(root, text = "Height : ")
    label20.grid(row = 19, column = 0, padx=10, pady=0)
    entries["Width"] = (Scale(root, from_=0, to=1000, orient="horizontal"))
    entries["Width"].set(0)
    entries["Width"].grid(row = 19, column = 2, padx=10, pady=0)

    save_button = tk.Button(root, text="Save File", command=lambda: save_as_file(entries))
    save_button.grid(row = 20, column=0, padx = 10, pady = 0)

    load_file = tk.Button(root, text="Load file", command=lambda: load_from_file(entries))
    load_file.grid(row = 20, column=1, padx = 10, pady = 0)

    submit_button = tk.Button(root, text="Submit", command=lambda:process_parameters(entries, root), anchor="center")
    submit_button.grid(row=20, column=3, padx = 10, pady = 0)

    root.mainloop()

    return INITIAL_CONDITIONS

if __name__ == "__main__":
    pass