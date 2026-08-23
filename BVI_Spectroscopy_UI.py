import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sys
from Element_Data import ELEMENT, ls_nm

#Global variables for use in Spectrum_Creator.py
targs = []
stype = ''

#this function will help us handle the user force closing the window
def onClose():
    root.destroy()
    sys.exit(0)

#this function adds compatibility with combobox presets
#i don't know how the event parameter works but it needs to be here
def elmnt_gen(event):
    #grabs the string from the combobox selection and creates a string of the wavelengths
    selected_element = combo_var.get()
    str = ls_nm(selected_element)

    #delete anything currently stored in the text box and replace with preset wavelengths
    text_entry.delete(0, tk.END)
    text_entry.insert(0, str)

def submit():

    global stype, targs, duration

    #without this clear line, we get duplicates of each target wavelength
    targs.clear()

    duration = int(spinbox_var.get())
    selected_option = radio_var.get()
    entered_text = text_entry.get()
    errors = []

    #adding the spectrum type to global variable so spectrum creator knows what kind of spectrum to use
    stype = selected_option

    #try and except to catch unwanted characters
    try:

        #does not populate the global list with anything if no values are input
        if entered_text == '':
            entered_text = "None"

        #add each wavelength to a global list to be used in the spectrum creator
        elif len(entered_text) > 1:
            colors = entered_text.split(",")
            for e in colors:
                if int(e) > 700 or int(e) < 300:
                    errors.append("Only wavelengths between 300nm and 700nm are permitted.")
                else:
                    targs.append(int(e.strip()))

        #this handles the case where only 1 wavelength is input 
        else:
            if int(entered_text) < 300 or int(entered_text) > 700:
                errors.append("Only wavelengths between 300nm and 700nm are permitted.")
            else:
                targs.append(int(entered_text))

    except ValueError:
        errors.append("Please enter a valid integer wavelength (Or leave blank for no absorption/emission)")       

    
    if selected_option == '0':
        errors.append("Please select a spectrum type.")

    #create a single warning box that compiles all errors instead of having to click through multiple boxes
    if errors:
        messagebox.showwarning("Input Error", "- " + "\n\n- ".join(errors))
        return


    #display a confirmation screen on valid submission
    messagebox.showinfo("Submission Successful",
                        f"Selected Option: {selected_option}\nEntered Text: {sorted(targs)}")

    #closes the window when user presses submit
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    root.destroy()
    
def CreateUI():
    global radio_var, text_entry, spinbox_var, combo_var, root

    #creating the UI window
    root = tk.Tk()
    root.title("Spectrum Builder")
    root.geometry("500x320")
    root.resizable(False, False)

    t_frame = tk.Frame(root)
    radio_frame = tk.Frame(t_frame)
    spinbox_frame = tk.Frame(t_frame)

    combo_label = tk.Label(root, text="Select a Preset Spectrum (optional): ", font=("Arial", 13))
    combo_var = tk.StringVar()
    combo = ttk.Combobox(root, width=27, textvariable=combo_var, state="readonly")
    combo['values'] = list(ELEMENT.keys())

    #<<ComboboxSelected>> is the backend name for selecting an option
    #in a combobox in tkinter. this method is basically saying "when 
    #an element is selected, perform elmnt_gen" 
    combo.bind("<<ComboboxSelected>>", elmnt_gen)

    radio_var = tk.StringVar(value=False)  #false makes it empty by default

    radio1 = tk.Radiobutton(radio_frame, text="Emission", variable=radio_var, value="Emission", font = ("Arial", 13))
    radio2 = tk.Radiobutton(radio_frame, text="Absorbtion", variable=radio_var, value="Absorption", font = ("Arial", 13))
    radio1.pack

    text_label = tk.Label(root, text="Enter wavelengths as integers seperated by commas.", font = ("Arial", 13))
    text_entry = tk.Entry(root, width=40, )

    spinbox_label = tk.Label(spinbox_frame, text="Duration (sec)", font=("Arial", 13))
    spinbox_var = tk.StringVar(value="5")
    spinbox = tk.Spinbox(spinbox_frame, from_ = 5, to = 60, textvariable=spinbox_var, width=5)

    submit_btn = tk.Button(root, text="Submit", command=submit, font = ("Arial", 13))

    #moving widgets around to make the UI less cramped
    t_frame.pack(pady=15, expand=False)
    radio1.pack(anchor='w', padx=10, expand=False)
    radio2.pack(anchor='w', padx=10, expand=False)
    spinbox_label.pack(side=tk.LEFT,padx=(10, 5), expand=False)
    radio_frame.pack(side=tk.LEFT, padx=20, expand=False)
    spinbox.pack(side=tk.LEFT,padx=5, expand=False)
    spinbox_frame.pack(side=tk.LEFT, padx=20, expand=False)
    text_label.pack(pady=(5, 20), expand=False)
    text_entry.pack(pady=10, expand=False)
    combo_label.pack(pady=(5,20), expand=False)
    combo.pack(pady=5, expand=False)
    submit_btn.pack(pady=5, expand=False)

    #handle user closing window without throwing errors 
    root.protocol("WM_DELETE_WINDOW", onClose)

    #start the GUI event loop
    root.mainloop()
    
    return stype, targs, duration

