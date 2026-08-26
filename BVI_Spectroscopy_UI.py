import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sys
from Element_Data import ELEMENT, ls_nm
import os
import winsound
from PIL import Image, ImageTk

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

    imgfile, wavfile = "Spectrum.png", "Spectrum_to_audio.wav"
    root.withdraw()
    open_player_ui(root, imgfile, wavfile)

#global variable to track if the sound is currently playing (for use in open_player_ui functions)
is_playing = False

def open_player_ui(creatui, imgfile, wavfile):

    #create a new window for the player UI
    player_window = tk.Toplevel(creatui)
    player_window.title("Spectrum & Audio Player")
    player_window.geometry("600x400")
    player_window.resizable(False, False)

    #load and display the image
    if os.path.exists(imgfile):
        img = Image.open(imgfile)
        img = img.resize((450, 80))
        tk_im = ImageTk.PhotoImage(img) #convert to a format that tkinter can use and display, the png file data itself is useless for tkinter
        img_label = tk.Label(player_window, image=tk_im) #creates the display for the image, think of it like a canvas that is set aside for the image
        img_label.image = tk_im #creates a permanent copy of the image so python doesnt delete it when the function ends (wont display in that case)
        img_label.pack(pady=10)
    else:
        messagebox.showerror("Error", "Image file 'Spectrum.png' not found.")
        player_window.destroy()
        return

    #create a label so the user can tell if the audio is currently playing or not 
    status_label = tk.Label(player_window, text="Audio Stopped", font=("Arial", 11), fg="gray")
    status_label.pack(pady=5)

    #functionality for the play button
    def play_sound():
        global is_playing
        if os.path.exists(wavfile):
            winsound.PlaySound(wavfile, winsound.SND_FILENAME | winsound.SND_ASYNC) #plays wavfile. snd_filename tells windows that the sound is a wav file. snd_async tells the player to allow the user to interface during the audio playback
            is_playing = True
            status_label.config(text="Playing", fg = "green") #this turns the play button into a stop button while the audio is playing
    def stop_audio():
            global is_playing
            winsound.PlaySound(None, winsound.SND_PURGE) #none stops the audio playback. snd_purge tells windows to clear the audio "queue" which will otherwise lock your window so you cant exit
            is_playing = False
            status_label.config(text="Stopped", fg="black") #this turns the stop button back into a play button when the audio is stopped

    def on_player_close():
        stop_audio()
        player_window.destroy()
        root.destroy() #if the user closes the player window, we want to close the entire program, not just the player window
        sys.exit(0) #this is just a failsafe to make sure the program closes if the user closes the player window
                    #(sometimes the process doesnt end, even with root.destroy, not sure why)

    btn_frame = tk.Frame(player_window)
    btn_frame.pack(pady=10)

    play_button = tk.Button(btn_frame, text="▶ Play", command=play_sound, font=("Arial", 12), width=10)
    play_button.pack(side=tk.LEFT, padx=10)

    #realistically, the stop button isnt necessary but if someone sets the duration high and doesn't want to listen
    #to the entire audio, they can stop it early. Just a QOL feature
    stop_button = tk.Button(btn_frame, text="⏸ Stop", command=stop_audio, font=("Arial", 12), width=10)
    stop_button.pack(side=tk.LEFT, padx=10)

    # Ensure audio stops if user closes the player window
    player_window.protocol("WM_DELETE_WINDOW", on_player_close)

    
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

