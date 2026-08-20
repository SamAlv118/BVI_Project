import tkinter as tk
from tkinter import messagebox

def submit():
    """Handle submit button click."""
    selected_option = radio_var.get()
    entered_text = text_entry.get().strip()

    # Validation checks
    if not selected_option:
        messagebox.showwarning("Input Error", "Please select a spectrum type.")
        return
    if not entered_text:
        messagebox.showwarning("Input Error", "Please enter some text.")
        return

    # Display the result
    messagebox.showinfo("Submission Successful",
                        f"Selected Option: {selected_option}\nEntered Text: {entered_text}")

# Create main window
root = tk.Tk()
root.title("Spectrum Builder")
root.geometry("300x200")
root.resizable(False, False)

# Variable to store selected radio button value
radio_var = tk.StringVar(value=False)  # Empty by default

# Create radio buttons
radio1 = tk.Radiobutton(root, text="Emission", variable=radio_var, value="Emission")
radio2 = tk.Radiobutton(root, text="Absorbtion", variable=radio_var, value="Absorbtion")

# Create text input
text_label = tk.Label(root, text="Enter line wavelengths seperated by commas.")
text_entry = tk.Entry(root, width=25)

# Create submit button
submit_btn = tk.Button(root, text="Submit", command=submit)

# Layout widgets
radio1.pack(pady=5)
radio2.pack(pady=5)
text_label.pack(pady=(10, 0))
text_entry.pack(pady=5)
submit_btn.pack(pady=10)

# Start the GUI event loop
root.mainloop()
