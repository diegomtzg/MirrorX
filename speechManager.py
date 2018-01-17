# Speech to Text Conversion
# Ike Kilinc

import sys

sys.path.append('/')
import speech_recognition as sr
import pyaudio
from audio_engine import *

def recognizeSpeech(formatFilter=None): # recognize speech using CMU Sphinx
    
    # print("formatFilter: ", formatFilter)
    r = sr.Recognizer() # obtain audio from the microphone
    with sr.Microphone() as source:
        print("Say something!")
        r.adjust_for_ambient_noise(source, duration=2)
        while(True):
        	try:
	        	# audio = r.listen(source, snowboy_configuration = ('snowboy-master/swig/Python3/', ['ok_mirror.pmdl']))
	        	audio = r.listen(source)
	        	recognized = r.recognize_google(audio).lower()
	        	print(recognized)
	        	if 'mirror' in recognized:
	        		break
	        except sr.UnknownValueError:
	        	print("Try again, google failed")
        play("voiceCommands/listening.wav")
        audio = r.listen(source)
        play("voiceCommands/listened.wav")
    try:
        output = r.recognize_google(audio).lower()
        # play("voiceCommands/listened.wav")
        print(output)
        if formatFilter==None:
            return output
        elif formatFilter=="location":
            output = filter(output)
            output = locationFilter(output)
        else:
            output = filter(output)
        print(output)
        return output
    except sr.UnknownValueError:
        # print("I could not understand audio")
        pass
    except sr.RequestError as e:
        print("Recognition error; {0}".format(e))

def filter(text): # format the text to be interpreted by Columbus
    if text == "": return None
    text = textNumbersToIntegers(text)
    text = correctCommands(text)
    return text

def textNumbersToIntegers(text): # turn text numbers into integers
    output = ''
    curNum = 0
    num = {"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,
        "eight":8,"nine":9,"ten":10,"eleven":11,"twelve":12,"thirteen":13,
        "fourteen":14,"fifteen":15,"sixteen":16,"seventeen":17,"eighteen":18,
        "nineteen":19,"twenty":20,"thirty":30,"fourty":40,"fifty":50,"sixty":60,
        "seventy":70,"eighty":80,"ninety":90,"hundred":100,"thousand":1000}
    for word in text.split():
        if word in num.keys():
            if word == "hundred" or word == "thousand":
                curNum = ((curNum%10) * num[word]) + ((curNum//10) * 10)
            else:
                curNum += num[word]
        else:
            if curNum != 0: output += ' ' + str(curNum)
            curNum = 0
            output += ' ' + word
    return output

def correctCommands(text):
    output = ""
    corrections = {"prima": "Prima"}
    for word in text.split():
        if word in corrections.keys():
            word = corrections[word]
        output += word + ' '
    return output

def locationFilter(text):
    prima = set(["prima", "Prima", "coffee", "tea", "rhema", "primo", "dreamer"])
    sorrells = set(["sorrells", "sorel's", "shirelles", "cirella's", "library"])

    for word in text.split():
        if word in prima:
            return "5Prima"
        elif word in sorrells:
            return "4Sorrells"
        elif isNumber(word):
            return word
    return ""

def isNumber(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def modeFilter(text):
    restroom = set(["restroom", "bathroom", "pee", "mens", "ladies", "poo",
                    "poop", "dump", "piss", "shit"])
    printer = set(["print", "printer", "paper"])
    popular = set(["popular", "common", "famous"])
    saved = set(["saved", "save", "favorite", "past"])
    specificDest = set(["specific", "particular"])
    helpOptions = set(["help", "options", "assistance", "mode", "modes"])

    for word in text.split():
        if word in restroom:
            return "nearestRestroom"
        elif word in printer:
            return "nearestPrinter"
        elif word in popular:
            return "popularDestinations"
        elif word in saved:
            return "savedDestinations"
        elif word in specificDest:
            return "specificDestination"
        elif word in helpOptions:
            return "help"
    return None

# def confirmFilter(text):
#     affirm = set(["yep", "yeah", "correct", "confirm", "confirmed"])
#     negate = set(["nope", "nah", "incorrect", "wrong"])
#     for word in text.split():
#         if word in affirm:
#             return "yes"
#         elif word in negate:
#             return "no"
#     return None






# if __name__ == '__main__':
# 	recognizeSpeech()


