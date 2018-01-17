# Audio Lecture - Pyaudio Demo
# Used by Ike Kilinc

# Code modified from https://people.csail.mit.edu/hubert/pyaudio/

###########################################################################
######################### Playing a WAV file ##############################
###########################################################################

# Existing Voice Recordings

# >> "What would you like to do? Say help for options."
# >> "Would you like directions to a specific destination, to get to a popular
# location, to get to your saved locations, to find the nearest restroom or
# printer, or to find God?"
# >> "Where would you like to go?"
# >> "Where are you now?"
# >> "You have arrived at your destination."
# >> "Click the space bar to return to the home screen or click enter to save this
# destination."


# Siri sound effects recorded from the following youtube video:
# https://www.youtube.com/watch?v=KfITibBsNwI


"""PyAudio Example: Play a WAVE file."""

import pyaudio
import wave
from array import array
from struct import pack


def play(file):
    CHUNK = 1024

    wf = wave.open(file, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()


###########################################################################
######################### Recording a WAV file ############################
###########################################################################
def record(outputFile):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(outputFile, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

#####################################################################
#####################################################################

# record("temp.wav")

# play("temp.wav")

