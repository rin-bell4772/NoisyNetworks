import sys
import argparse
import subprocess
import re
import numpy as np
import simpleaudio as sa


# Argument Parser
parser = argparse.ArgumentParser(description="play a little tune with ping!")
# -d: destination to ping
parser.add_argument(
    "-d", "--destination",
    type=str,
    default="google.com",
    help="The destination ip or DNS name"
)

# -l: lenth of melody
parser.add_argument(
    "-l", "--length",
    type=int,
    default=10,
    help="desired length of melody (and number of pings)"
)

# parse the arguments
args = parser.parse_args()

destination = args.destination
melody_length = args.length

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
        print(result.stdout)

        times = re.findall(r"time=([\d.]+)\s*ms", result.stdout)
        times = [float(t) for t in times]

        return times
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")

times = run_ping(destination,melody_length)

# C major Scale
# C B A G F E D C
notes = [261.63, 293.66, 329.63, 349.23, 392, 440, 493.88, 523.25]

def play_song(song, notes):

    for i in range(len(song)):
        frequency = notes[song[i]]
        duration = 1  # can be changed later
        sample_rate = 44100
        # generate sine wave
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        sine_wave = 0.5 * np.sin(2 * np.pi * frequency * t)

        # convert to 16-bit PCM
        audio_data = (sine_wave * 32767).astype(np.int16)

        play_object = sa.play_buffer(audio_data, 1, 2, sample_rate)
        play_object.wait_done()

def build_song(times):
    
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

def print_song(song):
 
    # C5 line
    for i in range(len(song)):
        if song[i] == 7:
            print("  C  ", end="")
        else:
            print("     ", end="")
    print()

    # B4 line
    for i in range(len(song)):
        if song[i] == 6:
            print("--B--", end="")
        else:
            print("-----", end="")
    print()
 
    # A4 line
    for i in range(len(song)):
        if song[i] == 5:
            print("  A  ", end="")
        else:
            print("     ", end="")
    print()

    # G4 line
    for i in range(len(song)):
        if song[i] == 4:
            print("--G--", end="")
        else:
            print("-----", end="")
    print()
 
    # F4 line
    for i in range(len(song)):
        if song[i] == 3:
            print("  F  ", end="")
        else:
            print("     ", end="")
    print()

    # E4 line
    for i in range(len(song)):
        if song[i] == 2:
            print("--E--", end="")
        else:
            print("-----", end="")
    print()
 
    # D4 line
    for i in range(len(song)):
        if song[i] == 1:
            print("  D  ", end="")
        else:
            print("     ", end="")
    print()

    # C4 line
    for i in range(len(song)):
        if song[i] == 0:
            print(" -C- ", end="")
        else:
            print("     ", end="")
    print()

def print_cat():
    
    bubble ="""
________________________  __________  __________  ________________________/
                        \\/          \\/          \\/
"""

    cat = """                      /^--^\\     /^--^\\     /^--^\\
                      \\____/     \\____/     \\____/
                     /      \\   /      \\   /      \\
                    |        | |        | |        |
                     \\__  __/   \\__  __/   \\__  __/
|^|^|^|^|^|^|^|^|^|^|^|^\\ \\^|^|^|^/ /^|^|^|^|^\\ \\^|^|^|^|^|^|^|^|^|^|^|^|
| | | | | | | | | | | | |\\ \\| | |/ /| | | | | | \\ \\ | | | | | | | | | | |
| | | | | | | | | | | | / / | | |\\ \\| | | | | |/ /| | | | | | | | | | | |
| | | | | | | | | | | | \\/| | | | \\/| | | | | |\\/ | | | | | | | | | | | |
#########################################################################
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |"""

    print(bubble)
    print(cat)

song = build_song(times)
print_song(song)
print_cat()
play_song(song, notes)
