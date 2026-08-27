import sys
import os
import winsound
import time
import wave                         

import tkinter as tk

#Global variables for use in Spectrum_Creator.py
targs = []
stype = ''

#this function will help us handle the user force closing the window
def onClose():
    #root.destroy()
    sys.exit(0)


#global variable to track if the sound is currently playing (for use in open_player_ui functions)
is_playing = False
#global variable to track if the timer is currently running (for use in open_player_ui functions)
endtime = None
#unrelated to endtime, this is important for tracking times for the spectroscopy lab
start_time = None
lap_times = []


#opens a player UI window for the user to interface with the audio playback and visible spectrum they just created
#imgfile is unused here but I will leave functionality commented instead of deleted in case the professor wants to include the spectrum in the window
# def open_player_ui(imgfile, wavfile):
def open_player_ui():
    
    #create a new window for the player UI
    player_window = tk.Tk()
    player_window.title("Spectrum & Audio Player")
    player_window.geometry("600x400")
    player_window.resizable(False, False)

    ###BVI ACCESSIBILITY FEATURE###
    player_window.focus_force()  #this makes the player window the active window so that the user can use the spacebar to play/stop the audio without having to click on the window first

    # -------------------------- DISABLED BY DEFAULT FOR STUDENTS ----------------------------------
    #load and display the image
    # if os.path.exists(imgfile):
    #     img = Image.open(imgfile)
    #     img = img.resize((450, 80))
    #     tk_im = ImageTk.PhotoImage(img) #convert to a format that tkinter can use and display, the png file data itself is useless for tkinter
    #     img_label = tk.Label(player_window, image=tk_im) #creates the display for the image, think of it like a canvas that is set aside for the image
    #     img_label.image = tk_im #creates a permanent copy of the image so python doesnt delete it when the function ends (wont display in that case)
    #     img_label.pack(pady=10)
    # else:
    #     messagebox.showerror("Error", "Image file 'Spectrum.png' not found.")
    #     player_window.destroy()
    #     return
    #------------------------------------------------------------------------------------------------

    #create a label so the user can tell if the audio is currently playing or not 
    status_label = tk.Label(player_window, text="Audio Stopped", font=("Arial", 11), fg="gray")
    status_label.pack(pady=40)

    def getDuration(path): 
        wav = wave.open(path, 'rb')
        total_frames = wav.getnframes()
        frame_rate = wav.getframerate()
        return total_frames/float(frame_rate)


    #functionality for the play button
    def play_sound():
        global is_playing, endtime, start_time, lap_times
        if os.path.exists(radio_var.get()):
            #re-initialize all of the parameters that we use for tracking the audio playback features
            wavfile = radio_var.get()
            stop_audio()  
            lap_times.clear() 
            start_time = time.time() 

            winsound.PlaySound(wavfile, winsound.SND_FILENAME | winsound.SND_ASYNC) #plays wavfile. snd_filename tells windows that the sound is a wav file. snd_async tells the player to allow the user to interface during the audio playback
            is_playing = True
            status_label.config(text="Playing", fg = "green") #this turns the play button into a stop button while the audio is playing
            play_button.config(text="⏸ Stop", command=stop_audio)  #this turns the play button into a stop button while the audio is playing

            ###BVI ACCESSIBILITY FEATURE###
            # player_window.bind('<space>', lambda event: stop_audio())  #rebinds the spacebar to the stop button, so the user can press space to stop the audio

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
        # player_window.bind('<space>', lambda event: play_sound())  #rebinds the spacebar to the play button after the audio is stopped


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


    radio_frame = tk.Frame(player_window)
    radio_frame.pack(pady=0)

    global radio_var
    radio_var = tk.StringVar(value = False)

    radio1 = tk.Radiobutton(radio_frame, text="Element 1", variable=radio_var, value="Spectrum_to_audio.wav", font = ("Arial", 13))
    radio2 = tk.Radiobutton(radio_frame, text="Element 2", variable=radio_var, value="Spectrum_to_audio2.wav", font = ("Arial", 13))
    radio3 = tk.Radiobutton(radio_frame, text="Element 3", variable=radio_var, value="Spectrum_to_audio3.wav", font = ("Arial", 13))
    radio4 = tk.Radiobutton(radio_frame, text="Element 4", variable=radio_var, value="Spectrum_to_audio4.wav", font = ("Arial", 13))
    radio1.pack(side="left", padx=5)
    radio2.pack(side="left", padx=5)
    radio3.pack(side="left", padx=5)
    radio4.pack(side="left", padx=5)

    radio_var.set("Spectrum_to_audio.wav")
    duration = int(getDuration(radio_var.get())) #This has to be down here because otherwise, the .get() method will not work

    btn_frame = tk.Frame(player_window)
    btn_frame.pack(pady=0)

    play_button = tk.Button(btn_frame, text="▶ Play", command=play_sound, font=("Arial", 13), width=10)
    play_button.pack(side="left", padx=10, pady=20)
 

    lap_button = tk.Button(btn_frame, text="⏱ Lap", command=lap, font=("Arial", 13), width=10)
    lap_button.pack(side="left", padx=10, pady=20)

    timeui_button = tk.Button(btn_frame, text="View Laps", command=lambda: open_time_ui(player_window, lap_times), font=("Arial", 13), width=10)
    timeui_button.pack(side="left", padx=10, pady=20)


    ###BVI ACCESSIBILITY FEATURE###
    #player_window.bind('<Return>', lambda event: open_time_ui(player_window, lap_times))

    # player_window.bind('<Z>', lambda event: lap())
    # player_window.bind('<z>', lambda event: lap())



    #realistically, the stop button isnt necessary but if someone sets the duration high and doesn't want to listen
    #to the entire audio, they can stop it early. Just a QOL feature
    # stop_button = tk.Button(btn_frame, text="⏸ Stop", command=stop_audio, font=("Arial", 12), width=10)
    # stop_button.pack(side=tk.LEFT, padx=10)  

    # Ensure audio stops if user closes the player window
    player_window.protocol("WM_DELETE_WINDOW", on_player_close)

    ###BVI ACCESSIBILITY FEATURE###
    player_window.bind('<Escape>', lambda event: on_player_close())  #binds the escape key to the on_player_close function, so the user can press escape to close the window

    player_window.mainloop()


def main():
    # imgfile, wavfile = "Spectrum.png", "Spectrum_to_audio.wav"
    # open_player_ui(imgfile, wavfile)
    open_player_ui()

main()

