import tkinter as tk
from tkinter import messagebox

#Global variables for use in Spectrum_Creator.py
exclusions = []
stype = []

def submit():

    selected_option = radio_var.get()
    entered_text = text_entry.get()
    errors = []

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
                    exclusions.append(int(e.strip()))

        #this handles the case where only 1 wavelength is input 
        else:
            exclusions.append(int(entered_text))

    except ValueError:
        errors.append("Please enter a valid wavelength (Or leave blank for no absorption/emission)")       

    #adding the spectrum type to global variable so spectrum creator knows what kind of spectrum to use
    stype.append(selected_option)

    
    if selected_option == '0':
        errors.append("Please select a spectrum type.")

    #create a single warning box that compiles all errors instead of having to click through multiple boxes
    if errors:
        messagebox.showwarning("Input Error", "- " + "\n\n- ".join(errors))
        return


    #display a confirmation screen on valid submission
    messagebox.showinfo("Submission Successful",
                        f"Selected Option: {selected_option}\nEntered Text: {entered_text}")
    

#creating the UI window
root = tk.Tk()
root.title("Spectrum Builder")
root.geometry("400x300")
root.resizable(True, True)

radio_var = tk.StringVar(value=False)  #false makes it empty by default

radio1 = tk.Radiobutton(root, text="Emission", variable=radio_var, value="Emission", font = ("Arial", 13))
radio2 = tk.Radiobutton(root, text="Absorbtion", variable=radio_var, value="Absorption", font = ("Arial", 13))

text_label = tk.Label(root, text="Enter line wavelengths seperated by commas.", font = ("Arial", 13))
text_entry = tk.Entry(root, width=40, )

submit_btn = tk.Button(root, text="Submit", command=submit, font = ("Arial", 13))

#moving widgets around to make the UI less cramped
radio1.pack(pady=10, expand=True)
radio2.pack(pady=10, expand=True)
text_label.pack(pady=(20, 0), expand=True)
text_entry.pack(pady=20, expand=True)
submit_btn.pack(pady=10, expand=True)

#start the GUI event loop
root.mainloop()
