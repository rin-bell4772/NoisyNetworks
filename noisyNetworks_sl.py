import streamlit as st

import subprocess
import re
import numpy as np
import simpleaudio as sa


# Initialize session state variables
if 'run_pressed' not in st.session_state:
    st.session_state.run_pressed = False
if 'song' not in st.session_state:
    st.session_state.song = None
if 'times' not in st.session_state:
    st.session_state.times = None
if 'play_song_triggered' not in st.session_state:
    st.session_state.play_song_triggered = False

# Title
st.title("NoisyNetworks")

st.markdown(
    """
    Impressively, your neightborhood cats have learned how to sing!
    
    Not only that, but they can sing using the network?
    
    Enter a valid DNS or IP address like "google.com" and these silly
    cats will ping that address. Depending on the response latency, they will
    sing different notes!
    """
    )

# arguments
destination = st.text_input("destination DNS or IP")
length = st.slider("Length of song",value=5, min_value=0, max_value=14)


# maybe add loading bar

# run the ping command
def run_ping(destination, count):
    """
    Runs the Ping command with the -c flag

    :param destination: the DNS or IP destination of ping
    :param count: the number of times ping should be run.
    """
    try:
        result = subprocess.run(
                ["ping", "-c", str(count), destination],
            text=True,
            capture_output=True,
            check=True
        )
        # st.code(result.stdout)

        times = re.findall(r"time=([\d.]+)\s*ms", result.stdout)
        times = [float(t) for t in times]

        return times
    except subprocess.CalledProcessError as e:
        st.code(f"Error: {e.stderr}")


def build_song(times):
    
    if times is None:
        times = []

    minimum = min(times) if times else 0 
    maximum = max(times) if times else 7
    range = maximum - minimum

    interval = range / 8

    song = []

    for time in times:

        if time == max:
            # play lowest note
            note_index = 7
        else:
            note_index = int((time - minimum) / interval)

            # ensure the index is within bounds
            note_index = min(note_index, 7)

        song.append(note_index)

    return song



def play_song(song, notes):
    
    for i in range(len(song)):
            
        frequency = notes[song[i]]
        duration = 1
        sample_rate = 44100

        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        sine_wave = 0.5 * np.sin(2 * np.pi * frequency * t)

        # convert to 16-bit PCM
        audio_data = (sine_wave * 32767).astype(np.int16)

        play_object = sa.play_buffer(audio_data, 1, 2, sample_rate)
        play_object.wait_done()


def print_song(song):
    s = '&nbsp;'

    buff = ""
    # C5 line
    for i in range(len(song)):
        if song[i] == 7:
            buff += f"{s}{s}C{s}{s}"
        else:
            buff += f"{s}{s}{s}{s}{s}"
    buff += "<br>"

    # B4 line
    for i in range(len(song)):
        if song[i] == 6:
            buff += "--B--"
        else:
            buff += "-----"
    buff += "<br>"

    # A4 line
    for i in range(len(song)):
        if song[i] == 5:
            buff += f"{s}{s}A{s}{s}"
        else:
            buff += f"{s}{s}{s}{s}{s}"
 
    buff += "<br>"

    # G4 line
    for i in range(len(song)):
        if song[i] == 4:
            buff += "--G--"
        else:
            buff += "-----"
    buff += "<br>"

    # F4 line
    for i in range(len(song)):
        if song[i] == 3:
            buff += f"{s}{s}F{s}{s}"
        else:
            buff += f"{s}{s}{s}{s}{s}"

    buff += "<br>"

    # E4 line
    for i in range(len(song)):
        if song[i] == 2:
            buff += "--E--"
        else:
            buff += "-----"
    buff += "<br>"
 
    # D4 line
    for i in range(len(song)):
        if song[i] == 1:
            buff += f"{s}{s}D{s}{s}"
        else:
            buff += f"{s}{s}{s}{s}{s}"

    buff += "<br>"


    # C4 line
    for i in range(len(song)):
        if song[i] == 0:
            buff += f"{s}-C-{s}"
        else:
            buff += f"{s}{s}{s}{s}{s}"

    buff += "<br>"

    st.markdown(f"<pre>{buff}</pre>", unsafe_allow_html=True)

def print_cat():
        
    bubble ="""
________________________  __________  __________  ________________________/
                        \\/          \\/          \\/
"""

    cat = """                      /^--^\\     /^--^\\     /^--^\\<br>
                      \\____/     \\____/     \\____/<br>
                     /      \\   /      \\   /      \\<br>
                    |        | |        | |        |<br>
                     \\__  __/   \\__  __/   \\__  __/<br>
|^|^|^|^|^|^|^|^|^|^|^|^\\ \\^|^|^|^/ /^|^|^|^|^\\ \\^|^|^|^|^|^|^|^|^|^|^|^|<br>
| | | | | | | | | | | | |\\ \\| | |/ /| | | | | | \\ \\ | | | | | | | | | | |<br>
| | | | | | | | | | | | / / | | |\\ \\| | | | | |/ /| | | | | | | | | | | |<br>
| | | | | | | | | | | | \\/| | | | \\/| | | | | |\\/ | | | | | | | | | | | |<br>
#########################################################################<br>
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |<br>
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |<br>"""

    bubble = bubble.replace(" ", "&nbsp;")
    cat = cat.replace(" ", "&nbsp;")
    st.markdown(f"<pre>{bubble}</pre>", unsafe_allow_html=True)
    st.markdown(f"<pre>{cat}</pre>", unsafe_allow_html=True)




notes = [261.63, 293.66, 329.63, 349.23, 392, 440, 493.88, 523.25]


# run the ping command
run_pressed = st.button("Run")

if run_pressed:
    st.session_state.run_pressed = True

    with st.spinner("The cats are practicing..."):
        st.session_state.times = run_ping(destination, length)
    
    st.session_state.song = build_song(st.session_state.times)
    st.session_state.play_song_triggered = True

if st.session_state.run_pressed:
    print_song(st.session_state.song)
    print_cat()

    if st.session_state.play_song_triggered:
        play_song(st.session_state.song, notes)
        st.session_state.play_song_triggered = False

    replay = st.button("replay")

    if replay:
        st.session_state.play_song_triggered = True
        st.rerun()
