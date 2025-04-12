"""
    Author : Francesco Bredariol
    Year : 2024/2025
    This Project is done for the academic purpose of 
    implementing the practical part of the Degree Thesis 
    in Artificial Intelligence and Data Analytics.
"""
import tkinter as tk
from tkinter import Scale
from tkinter import filedialog
from tkinter import Label
from tkinter import Entry
from tkinter import StringVar
from tkinter import OptionMenu
from tkinter import Spinbox
from tkinter import IntVar
import pickle

INITIAL_CONDITIONS =  {
            "Size" : 100, "I_Energy" : 100, "I_Age" : 100, "I_Maturity" : 18, "Radius" : 4, "I_Distr" : "Uniform", 
            "Active" : 100, "C_Min" : 100, "C_Max" : 150, "C_Regen" : 10, "C_Distr" : "Uniform", 
            "P_Distr" : "Uniform", 
            "Move" : 1, "Eat" : 1, "Rest" : 0, "Reproduce" : 5, 
            "Height" : 50, "Width" : 50,
            "N_Simulations" : 1, "Seed" : 37
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
        # It is a binary file!
        with open(file_path, 'rb') as file:
            actual_dict = pickle.load(file)
    
    for k in list(entries.keys()):
        entries[k].set(actual_dict[k])

def inital_condition_GUI():
    # THIS MAY SEEMS NOT TOO GOOD BUT IN FACT IS PRETTY GOOD 
    root = tk.Tk()
    root.title("INITIAL CONDITION GUI")

    entries = {}
    col1 = {
                "POPULATION SETTINGS" : ["Label"], 
                "Size" : ["Scale", 1, 100],
                "I_Energy" : ["Insert", "Avg Maximum Energy"], 
                "I_Age" : ["Insert", "Avg Maximum Age"], 
                "I_Maturity" : ["Insert", "Avg Maturity Age"],
                "I_Distr" : ["Menu", ["Uniform"]],
                "Radius" : ["Scale", 1, 10],
                "WORLD SETTINGS" : ["Label"],
                "Active" : ["Scale", 1, 100], 
                "C_Min" : ["Insert", "Minimun Cell Energy to live"], 
                "C_Max" : ["Insert", "Maximum Cell Energy contained"], 
                "C_Regen" : ["Insert", "Regeneration Energy Ratio"],
                "C_Distr" : ["Menu", ["Uniform", "Uniform no regen", "4 Islands", "4 Islands no regen"]],
                "Height" : ["Insert", "Height in pixel"], 
                "Width" : ["Insert", "Width in pixel"]
            }

    col2 =  {
                "PARAMETERS SETTINGS" : ["Label"], 
                "P_Distr" : ["Menu", ["Uniform", "Selfish", "Altruistic", "Normal", "Selfish-Altruistic", "Selfish-Normal", "Altruistic-Normal"]],
                "ACTIONS SETTINGS" : ["Label"],
                "Move" : ["Insert", "Move cost"],
                "Eat" : ["Insert", "Eat cost"], 
                "Rest" : ["Insert", "Rest cost"], 
                "Reproduce" : ["Insert", "Reproduce base cost"],
                "SIMULATION SETTINGS" : ["Label"],
                "N_Simulations" : ["Scale", 1, 100], 
                "Seed" : ["Insert", "Seed for the position generation"]
            }
    
    lab_col1 = []
    dropdown = []
    spinboxes = []
    lab_col2 = []

    def generate_column(col, labs, spins, drops, col_offset):
        for i, key in enumerate(list(col.keys())):
            labs.append(Label(root, text=key))
            labs[i].grid(row = i, column = 0 + col_offset, padx = 10,  pady = 3)
            if col[key][0] == "Insert":
                entries[key] = IntVar(root)
                entries[key].set(0)
                spins.append(Spinbox(root, from_=0, to=1000, textvariable=entries[key]))
                spins[-1].grid(row = i, column = 1 + col_offset, padx = 10,  pady = 3)
            if col[key][0] == "Menu":
                entries[key] = StringVar(root)
                mods = col[key][1]
                entries[key].set(mods[0])
                drops.append(OptionMenu(root, entries[key], *mods))
                drops[-1].grid(row = i, column = 1 + col_offset, padx = 10,  pady = 3)
            if col[key][0] == "Scale":
                lower = col[key][1]
                upper = col[key][2]
                entries[key] = Scale(root, from_=lower, to_=upper, orient="horizontal")
                entries[key].set(lower)
                entries[key].grid(row = i, column = 1 + col_offset, padx = 10, pady = 3)
    
    # COLUMNS PART
    
    generate_column(col1, lab_col1, spinboxes, dropdown, 0)
    generate_column(col2, lab_col2, spinboxes, dropdown, 3)

    # BUTTON PART

    actual_row = max(len(list(col1.keys())*2), len(list(col2.keys())*2))
    save_button = tk.Button(root, text="Save File", command=lambda: save_as_file(entries))
    save_button.grid(row = actual_row, column=0, padx = 10, pady = 6)

    load_file = tk.Button(root, text="Load file", command=lambda: load_from_file(entries))
    load_file.grid(row = actual_row, column=1, padx = 10, pady = 6)

    submit_button = tk.Button(root, text="Submit", command=lambda:process_parameters(entries, root), anchor="center")
    submit_button.grid(row= actual_row, column=3, padx = 10, pady = 6)

    root.mainloop()

    return INITIAL_CONDITIONS

if __name__ == "__main__":
    pass