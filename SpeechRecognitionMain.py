import winspeech
import sys
from WikipediaSummary import Wikipedia
from OpenWebsiteLogin import WebsiteLogin
import webbrowser
import os
import re
import subprocess

# mystr = 'This is a string, with words!'
# wordList  = re.sub("[^\w]", " ",  mystr).split()
winspeech.initialize_recognizer(winspeech.INPROC_RECOGNIZER)

winspeech.say("Hello! my name is Harman your personal assistant, How may I help you ?")

def OpenBrowserGetSearchWord(Word, listener):
    print("In OpenBrowserGetSearchWord function")
    address = 'https://www.google.com/#q='
    newword = address + Word
    webbrowser.open(newword)
    print("You Said @@ : %s" % Word)
    winspeech.listen_for_anything(MainFunction)
    return;

def MainFunction(result, listener):
    print("In MainFunction function")
    sentence = result
    print("You Said : %s" % sentence)
    stringarr = sentence.split(' ')

    if result == "open browser":
        winspeech.say("Which word you want to search ?")
        winspeech.listen_for_anything(OpenBrowserGetSearchWord)
    if stringarr[0] == "summary":
        Wikipedia(stringarr[2])

    if stringarr[0] == "login":
        print("1.Facebook \n2. Gmail")
        winspeech.listen_for_anything(WebsiteLogin)

    if result == "shut down":
        winspeech.stop_listening()
        subprocess.call(["shutdown", "/r", "/t", "/0"])

    if result == "stop":
        winspeech.stop_listening()
        sys.exit(0)


listener = winspeech.listen_for_anything(MainFunction)

while listener.is_listening():
    continue
