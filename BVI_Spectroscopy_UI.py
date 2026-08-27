import sys
import os
import winsound
import time

from PIL import Image, ImageTk

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from Element_Data import ELEMENT, ls_nm

from Spectrum_Creator import CreateSpec
from Spectrum_Reader import CreateWav

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

#functionality for the submit buttons. this uses functions from Spectrum_Creator.py and Spectrum_Reader.py to generate the spectrum and audio files
#(honestly, these functions should just be implemented here but I didn't know how I wanted to format my project when I started so I split them up)
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


    try:
        CreateSpec(stype, targs)
        CreateWav(stype, targs, duration)

    except Exception as e:
        messagebox.showerror("Generation Error", f"Failed to generate output files:\n{e}")
        return


    #display a confirmation screen on valid submission (the first few lines below this comment are just for formatting)
    targs = sorted(targs)
    for i in range(len(targs)):
        targs[i] += 300
    messagebox.showinfo("Submission Successful",
                        f"Selected Option: {selected_option}\nEntered Text: {targs}")

    #closes the window when user presses submit
    root.protocol("WM_DELETE_WINDOW", lambda: None)

    #launches the player UI after pressing submit
    imgfile, wavfile = "Spectrum.png", "Spectrum_to_audio.wav"
    root.withdraw()
    open_player_ui(root, imgfile, wavfile)

#global variable to track if the sound is currently playing (for use in open_player_ui functions)
is_playing = False
#global variable to track if the timer is currently running (for use in open_player_ui functions)
endtime = None
#unrelated to endtime, this is important for tracking times for the spectroscopy lab
start_time = None
lap_times = []


#opens a player UI window for the user to interface with the audio playback and visible spectrum they just created
def open_player_ui(rootui, imgfile, wavfile):

    #create a new window for the player UI
    player_window = tk.Toplevel(rootui)
    player_window.title("Spectrum & Audio Player")
    player_window.geometry("600x400")
    player_window.resizable(False, False)

    ###BVI ACCESSIBILITY FEATURE###
    player_window.focus_force()  #this makes the player window the active window so that the user can use the spacebar to play/stop the audio without having to click on the window first

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
        global is_playing, endtime, start_time, lap_times
        if os.path.exists(wavfile):
            #re-initialize all of the parameters that we use for tracking the audio playback features
            stop_audio()  
            lap_times.clear() 
            start_time = time.time() 

            winsound.PlaySound(wavfile, winsound.SND_FILENAME | winsound.SND_ASYNC) #plays wavfile. snd_filename tells windows that the sound is a wav file. snd_async tells the player to allow the user to interface during the audio playback
            is_playing = True
            status_label.config(text="Playing", fg = "green") #this turns the play button into a stop button while the audio is playing
            play_button.config(text="⏸ Stop", command=stop_audio)  #this turns the play button into a stop button while the audio is playing

            ###BVI ACCESSIBILITY FEATURE###
            player_window.bind('<space>', lambda event: stop_audio())  #rebinds the spacebar to the stop button, so the user can press space to stop the audio

            #tkinter likes milliseconds for the "after" function parameter
            ms = duration * 1000
            endtime = player_window.after(ms, stop_audio)  #this sets a timer to stop the audio after the duration (in ms) is up


    #functionality for whatever function is used to stop the audio playback
    def stop_audio():
        global is_playing, endtime, start_time, lap_times
        #specifically "is not" because this checks if the variable is the same as the assigned "None" object, not just if the assigned value = "None"
        #this if statement basically handles if the user presses stop before the playback finishes
        if endtime is not None:  
            player_window.after_cancel(endtime)  #cancels the timer if it's still running but doesnt overwrite the timer value
            endtime = None 

        start_time = None  #resets the start time when the audio is stopped

        winsound.PlaySound(None, winsound.SND_PURGE)
        is_playing = False
        status_label.config(text="Audio Stopped", fg="black")
        play_button.config(text="▶ Play", command=play_sound)  #this turns the stop button back into a play button when the audio is stopped

        ###BVI ACCESSIBILITY FEATURE###
        player_window.bind('<space>', lambda event: play_sound())  #rebinds the spacebar to the play button after the audio is stopped


    #functionality for the lap button (important for calculating specific emission/absorption lines)
    def lap():
        global start_time, lap_times, is_playing
        if is_playing and start_time is not None:
            timestamp = round((time.time() - start_time), 2) #can change the rounding but 2 decimals seems fine
            lap_times.append(timestamp)
            status_label.config(text=f"Lap {len(lap_times)}: {timestamp} sec", fg="blue")


    #handles closing the player window
    def on_player_close():
        stop_audio()
        player_window.destroy()
        root.destroy() #if the user closes the player window, we want to close the entire program, not just the player window
        sys.exit(0) #this is just a failsafe to make sure the program closes if the user closes the player window
                    #(sometimes the process doesnt end, even with root.destroy, not sure why)


    #creating the lap times display window
    def open_time_ui(playerui, lap_times):

        time_window = tk.Toplevel(playerui)
        time_window.title("Lap Times")
        time_window.geometry("300x200")
        time_window.resizable(False, False)

        time_window.focus_force() 

        list_label = tk.Label(time_window, text="Lap Times (seconds):", font=("Arial", 12))
        list_label.pack(pady=5)

        list_frame = tk.Frame(time_window)
        list_frame.pack(pady=5, fill=tk.BOTH, expand=True)

        #probably wont need a scrollbar for most cases but its safe to have it
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=("Arial", 12))
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        if not lap_times:
            listbox.insert(tk.END, "No lap times recorded.")
        else:
            for i in range(len(lap_times)):
                listbox.insert(tk.END, f"Lap {i+1}: {lap_times[i]} sec")


        #simple definition for handling the closing of the time ui
        def close_time_ui():
            time_window.destroy()


        time_window.protocol("WM_DELETE_WINDOW", close_time_ui)

        ###BVI ACCESSIBILITY FEATURE###
        time_window.bind('<Escape>', lambda event: close_time_ui())


    btn_frame = tk.Frame(player_window)
    btn_frame.pack(pady=10)

    play_button = tk.Button(btn_frame, text="▶ Play", command=play_sound, font=("Arial", 13), width=10)
    play_button.pack(side=tk.LEFT, padx=10)

    ###BVI ACCESSIBILITY FEATURE###
    player_window.bind('<space>', lambda event: play_sound()) 

    lap_button = tk.Button(btn_frame, text="⏱ Lap", command=lap, font=("Arial", 13), width=10)
    lap_button.pack(side=tk.LEFT, padx=10)

    timeui_button = tk.Button(btn_frame, text="View Laps", command=lambda: open_time_ui(player_window, lap_times), font=("Arial", 13), width=10)
    timeui_button.pack(side=tk.LEFT, padx=10)


    ###BVI ACCESSIBILITY FEATURE###
    player_window.bind('<Return>', lambda event: open_time_ui(player_window, lap_times))

    player_window.bind('<Z>', lambda event: lap())
    player_window.bind('<z>', lambda event: lap())



    #realistically, the stop button isnt necessary but if someone sets the duration high and doesn't want to listen
    #to the entire audio, they can stop it early. Just a QOL feature
    # stop_button = tk.Button(btn_frame, text="⏸ Stop", command=stop_audio, font=("Arial", 12), width=10)
    # stop_button.pack(side=tk.LEFT, padx=10)  

    # Ensure audio stops if user closes the player window
    player_window.protocol("WM_DELETE_WINDOW", on_player_close)

    ###BVI ACCESSIBILITY FEATURE###
    player_window.bind('<Escape>', lambda event: on_player_close())  #binds the escape key to the on_player_close function, so the user can press escape to close the window

    
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

    radio_var = tk.StringVar(value=False)  #false makes it empty by default

    radio1 = tk.Radiobutton(radio_frame, text="Emission", variable=radio_var, value="Emission", font = ("Arial", 13))
    radio2 = tk.Radiobutton(radio_frame, text="Absorption", variable=radio_var, value="Absorption", font = ("Arial", 13))
    radio1.pack

    text_label = tk.Label(root, text="Enter wavelengths as integers separated by commas.", font = ("Arial", 13))
    text_entry = tk.Entry(root, width=40)
    text_entry.insert(0, "Enter wavelengths in nanometers or leave blank for a continuous spectrum.")

    spinbox_label = tk.Label(spinbox_frame, text="Duration (sec)", font=("Arial", 13))
    spinbox_var = tk.StringVar(value="5")
    spinbox = tk.Spinbox(spinbox_frame, from_ = 5, to = 120, textvariable=spinbox_var, width=5)

    combo_label = tk.Label(root, text="Select a Preset Spectrum (optional): ", font=("Arial", 13))
    combo_var = tk.StringVar()
    combo = ttk.Combobox(root, width=27, textvariable=combo_var, state="readonly")
    combo['values'] = list(ELEMENT.keys())   #this ONLY displays the element names in the combobox dropdown, see below for retrieving the wavelengths.
    combo.set("Select an Element with a preset spectrum.") #this is actually a BVI accessibility feature, if we populate the combobox with
                                                           #a default value, the screen reader will read it out as a prompt to the user.
                                                           #this same method is used above in the text_entry box but I didn't want to comment this on both

    #<<ComboboxSelected>> is the backend name for selecting an option
    #in a combobox in tkinter. this method is basically saying "when 
    #an element is selected, perform elmnt_gen" which fills the combobox 
    #text area with the wavelengths for that element.
    combo.bind("<<ComboboxSelected>>", elmnt_gen)

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

    ###BVI ACCESSIBILITY FEATURE###
    root.bind('<Escape>', lambda event: onClose())  #binds the escape key to the onClose function, so the user can press escape to close the window
    root.bind('<Return>', lambda event: submit())  #binds the enter key to the submit function, so the user can press enter to submit the form

    #start the GUI event loop
    root.mainloop()
    
    return stype, targs, duration

def main():
    CreateUI()

main()

