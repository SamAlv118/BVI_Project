import tkinter as tk
from tkinter import messagebox

#Global variables for use in Spectrum_Creator.py
targs = []
stype = ''

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
                        f"Selected Option: {selected_option}\nEntered Text: {entered_text}")
    
def CreateUI():
    #creating the UI window
    root = tk.Tk()
    root.title("Spectrum Builder")
    root.geometry("500x320")
    root.resizable(True, True)
    global radio_var, text_entry, spinbox_var

    t_frame = tk.Frame(root)
    radio_frame = tk.Frame(t_frame)
    spinbox_frame = tk.Frame(t_frame)

    radio_var = tk.StringVar(value=False)  #false makes it empty by default

    radio1 = tk.Radiobutton(radio_frame, text="Emission", variable=radio_var, value="Emission", font = ("Arial", 13))
    radio2 = tk.Radiobutton(radio_frame, text="Absorbtion", variable=radio_var, value="Absorption", font = ("Arial", 13))
    radio1.pack

    text_label = tk.Label(root, text="Enter line wavelengths as integers seperated by commas.", font = ("Arial", 13))
    text_entry = tk.Entry(root, width=40, )

    spinbox_label = tk.Label(spinbox_frame, text="Duration (sec)", font=("Arial", 13))
    spinbox_var = tk.StringVar(value="5")
    spinbox = tk.Spinbox(spinbox_frame, from_ = 5, to = 60, textvariable=spinbox_var, width=5)

    submit_btn = tk.Button(root, text="Submit", command=submit, font = ("Arial", 13))

    #moving widgets around to make the UI less cramped
    t_frame.pack(pady=15, expand=True)
    radio1.pack(anchor='w', padx=10, expand=True)
    radio2.pack(anchor='w', padx=10, expand=True)
    spinbox_label.pack(side=tk.LEFT,padx=(10, 5), expand=True)
    radio_frame.pack(side=tk.LEFT, padx=20, expand=True)
    spinbox.pack(side=tk.LEFT,padx=5, expand=True)
    spinbox_frame.pack(side=tk.LEFT, padx=20, expand=True)
    text_label.pack(pady=(5, 20), expand=False)
    text_entry.pack(pady=10, expand=False)
    submit_btn.pack(pady=5, expand=True)

    #start the GUI event loop
    root.mainloop()

    return stype, targs, duration

