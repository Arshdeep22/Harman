import wikipedia
# from SpeechRecognitionMain import MainFunction

def Wikipedia(Word):
    print("In Wikipedia function")
    page = wikipedia.page(Word)
    print(page.summary)
    ##  print(page.images)
    return;