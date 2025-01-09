import tkinter as tk
from tkinter import messagebox

# THIS IS JUST A DEMO OF HOW TO USE TKINTER

def process_parameters():
    param1 = entry1.get()
    param2 = entry2.get()
    # Example: Process the parameters here
    messagebox.showinfo("Parameters Received", f"Param1: {param1}, Param2: {param2}")

# Create the main window
root = tk.Tk()
root.title("Parameter Input GUI")

# Create labels and entry fields
label1 = tk.Label(root, text="Parameter 1:")
label1.grid(row=0, column=0, padx=10, pady=5)
entry1 = tk.Entry(root)
entry1.grid(row=0, column=1, padx=10, pady=5)

label2 = tk.Label(root, text="Parameter 2:")
label2.grid(row=1, column=0, padx=10, pady=5)
entry2 = tk.Entry(root)
entry2.grid(row=1, column=1, padx=10, pady=5)

# Create a submit button
submit_button = tk.Button(root, text="Submit", command=process_parameters)
submit_button.grid(row=2, column=0, columnspan=2, pady=10)

# Run the application
root.mainloop()
