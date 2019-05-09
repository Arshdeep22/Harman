import speech_recognition as sr
from nltk.corpus import stopwords
import wikipedia
from weather import Weather, Unit
from selenium import webdriver
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import winspeech
import time
import sys,tweepy,csv,re,os
from textblob import TextBlob
import matplotlib.pyplot as plt
import requests
import pyautogui
from tkinter import *
import tkinter.messagebox

class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def DownloadData(self, searchTerm, NoOfTerms):
        # authenticating
        consumerKey = ''
        consumerSecret = ''
        accessToken = ''
        accessTokenSecret = ''
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)

        # input for term to be searched and how many tweets to search
        #searchTerm = input("Enter Keyword/Tag to search about: ")
        #NoOfTerms = int(input("Enter how many tweets to search: "))

        # searching for tweets
        try:
            self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)

        # Open/create a file to append data to
            csvFile = open('result.csv', 'a')

        # Use csv writer
            csvWriter = csv.writer(csvFile)
            
        except:
            print("Network error while downloading tweets, try again! ")

        # creating some variables to store info
        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0


        # iterating through tweets fetched
        for tweet in self.tweets:
            #Append to temp so that we can store in csv later. I use encode UTF-8
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            # print (tweet.text.translate(non_bmp_map))    #print tweet's text
            analysis = TextBlob(tweet.text)
            # print(analysis.sentiment)  # print tweet's polarity
            polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

            if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                neutral += 1
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                wpositive += 1
            elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                positive += 1
            elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                spositive += 1
            elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                wnegative += 1
            elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                negative += 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                snegative += 1


        # Write to csv and close csv file
        csvWriter.writerow(self.tweetText)
        csvFile.close()

        # finding average of how people are reacting
        positive = self.percentage(positive, NoOfTerms)
        wpositive = self.percentage(wpositive, NoOfTerms)
        spositive = self.percentage(spositive, NoOfTerms)
        negative = self.percentage(negative, NoOfTerms)
        wnegative = self.percentage(wnegative, NoOfTerms)
        snegative = self.percentage(snegative, NoOfTerms)
        neutral = self.percentage(neutral, NoOfTerms)

        # finding average reaction
        polarity = polarity / NoOfTerms

        # printing out data
        print("How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")
        print()
        print("General Report: ")

        if (polarity == 0):
            print("Neutral")
        elif (polarity > 0 and polarity <= 0.3):
            print("Weakly Positive")
        elif (polarity > 0.3 and polarity <= 0.6):
            print("Positive")
        elif (polarity > 0.6 and polarity <= 1):
            print("Strongly Positive")
        elif (polarity > -0.3 and polarity <= 0):
            print("Weakly Negative")
        elif (polarity > -0.6 and polarity <= -0.3):
            print("Negative")
        elif (polarity > -1 and polarity <= -0.6):
            print("Strongly Negative")

        print()
        print("Detailed Report: ")
        print(str(spositive) + "% people thought it was strongly positive")
        print(str(positive) + "% people thought it was positive")
        print(str(wpositive) + "% people thought it was weakly positive")
        print(str(neutral) + "% people thought it was neutral")
        print(str(wnegative) + "% people thought it was weakly negative")
        print(str(negative) + "% people thought it was negative")
        print(str(snegative) + "% people thought it was strongly negative")
        

        self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, NoOfTerms)


    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms):
        labels = ['Strongly Positive [' + str(spositive) + '%]','Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Weakly Negative [' + str(wnegative) + '%]', 'Negative [' + str(negative) + '%]',  'Strongly Negative [' + str(snegative) + '%]']
        sizes = [spositive,positive,wpositive,neutral,wnegative,negative,snegative]
        colors = ['darkgreen','lightgreen','yellowgreen','gold','lightsalmon', 'red','darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()
        reportText = "here is the report for you sir!"
        return reportText

def TwitterAnalysis(topic,tweetCount):
    winspeech.say("Analyzing the tweet sentiments for you!")
    sa = SentimentAnalysis()
    repo = sa.DownloadData(topic,tweetCount)
    reportText = "here is the report for you sir!"
    return repo

def weatherReport(loc):
    try:
        api_address='http://api.openweathermap.org/data/2.5/weather?appid=36ff039689070aecf3a6db6caaa27523&q='
        city = loc
        url = api_address + city
        json_data = requests.get(url).json()
        #format_add = json_data['base']
        print(json_data)
    except:
        print("Network error try again! ")

def WebsiteLogin(Word):
    try:
        Website = "https://www." + Word + ".com/"
        driver = webdriver.Firefox(executable_path = "C:\\Users\\Arshdeep singh\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\site-packages\\selenium\\webdriver\\firefox\\geckodriver.exe")
        driver.get(Website)
        driver.maximize_window()
        driver.implicitly_wait(30)
        if Word == "facebook":
            assert "Facebook" in driver.title
            #driver.get_screenshot_as_file("D:\\facebook.png")
            driver.find_element_by_id("email").send_keys("arshdeep.sekhon.16")
            driver.find_element_by_id("pass").send_keys("9056343865")
            driver.find_element_by_id("loginbutton").click()
            #driver.get_screenshot_as_file("D:\\facebook1.png")
        
        if Word == "gmail":
            assert "Gmail" in driver.title
            #driver.get_screenshot_as_file("D:\\Gmail.png")
            driver.find_element_by_id("identifierId").send_keys("arshdeep.sekhon16@gmail.com")
            driver.find_element_by_id("identifierNext").click()
            time.sleep(2)
            elem = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[1]/div/form/content/section/div/content/div[1]/div/div[1]/div/div[1]/input")
            elem.send_keys("9855481785")
            driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/content/span").click()
            #driver.get_screenshot_as_file("D:\\Gmail.png")
    except:
        print("Network error try again! ")
        
    #driver.quit()

def Wikipedia(Word):
    try:
        winspeech.say("loading the summary for you")
        #print("In Wikipedia function")
        page = wikipedia.page(Word)
        #wikipedia.exceptions.DisambiguationError
        summary_text = page.summary
        ##  print(page.images)
        return summary_text;
    except:
        print("Network error try again! ")
        

def Open(shortcut):
    try:
        print(shortcut)
        os.startfile(r"D:\Project Harman\Relaunched Harman\Shortcuts\{}.lnk".format(shortcut))
    except:
        print("No such directory found, try again!")

def tkinterMessageBox(title,textToDisplay):
    root = Tk()
    root.withdraw()
    tkinter.messagebox.showinfo(title,textToDisplay)
    #root.mainloop()
    text = "Here is the summary for you sir"
    return text;

def takeVoiceInput():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening :")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        #text = input()
        print("You said : {}".format(text))
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text)
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        ps = PorterStemmer()
        lemmatizer = WordNetLemmatizer()
        tags = []
        for f in filtered_sentence:
            tags.append(lemmatizer.lemmatize(ps.stem(f)))
        #return text,tags
            
    except:
        print("Sorry could not recognize what you said")
        tags = ['error']
        text = "error"
    return text,tags

def voiceOutput(text):
    winspeech.say(text)
    time.sleep(len(text)/15)


#if __name__== "__main__":


birthdays = {'arshdeep': ' 3 May', 'harman': '22 Mar', 'rashpal': '21 apr','daljit ': '27 dec'}
winspeech.initialize_recognizer(winspeech.INPROC_RECOGNIZER)    
os.startfile('HARMAN GUI FINAL_3.0.rmskin')
time.sleep(1)
pyautogui.press('enter')
pyautogui.hotkey('winleft', 'd')
winspeech.say("Hello! my name is Harman your personal assistant, How may I help you ?")
time.sleep(5)
#localtime = time.asctime( time.localtime(time.time()) )
#todaydate =  localtime[8:10]+" "+localtime[4:7]
#print(todaydate)
#if todaydate in list(birthdays.values()):
    #print(birthdays.(todaydate))


while 1:

    text, tags = takeVoiceInput()
    print(text)
    print(tags)

    for t in tags:
        if t=="open":
            try:
                Open(tags[1])
            except:
                print("try again")
        
        if t=="summari":
            summary_text = Wikipedia(tags[tags.index("summari")+1])
            #print(summary_text)
            voiceOutput(summary_text)
            Summary_report = tkinterMessageBox("Wikipedia summary",summary_text)

        if t=="facebook": 
            winspeech.say("Logging you in facebook.")
            WebsiteLogin("facebook")

        if t=="gmail" or t=="email": 
            winspeech.say("Logging you in gmail.")
            WebsiteLogin("gmail")
        
        if t == "weather":
            weatherReport(tags[tags.index("weather")+1])

        if t =="analysi" or t =="tweet" and t =="twitter":
            voiceOutput("sure sir !, which topic you want to analyze : ")
            print("sure sir !, which topic you want to analyze : ")
            twitterTopicText,twitterTopicTag = takeVoiceInput()
            #voiceOutput("how many tweets to search: ")
            count = 200
            report = TwitterAnalysis(twitterTopicText,count)
            winspeech.say("Here is the report for you sir")
            print(report)

        if t=="birthday":
            name = tags[tags.index("birthday")+1]
            if name in birthdays:
                voicetext = (birthdays[name] + ' is the birthday of ' + name)
                voiceOutput(voicetext)
            else:
                voicetext= 'I do not have birthday information for ' + name
                voiceOutput(voicetext)
                voicetext = 'What is their birthday?'
                voiceOutput(voicetext)
                bday = takeVoiceInput()
                birthdays[name] = bday[0]
                voicetext = 'Birthday database updated.'
                voiceOutput(voicetext)

        if t=="show" and t=="desktop":
            os.system("TASKKILL /F /IM Rainmeter.exe")


        if t=="minim":
            pyautogui.hotkey('winleft', 'down')
            
        if t=="minim":
            pyautogui.hotkey('winleft', 'up')
            
        if t=="shutdown":
            winspeech.say("Harman is shutting down.")
            time.sleep(2)
            os.system("TASKKILL /F /IM Rainmeter.exe")
            os.system("shutdown /s /t 1")

        if t=="restart":
            winspeech.say("Harman is shutting down.")
            time.sleep(2)
            os.system("TASKKILL /F /IM Rainmeter.exe")
            os.system("shutdown /r /t 1")
            
        if t=="bye":
            #time.sleep(10)
            winspeech.say("Harman is shutting down.")
            time.sleep(2)
            os.system("TASKKILL /F /IM Rainmeter.exe")
            sys.exit()

       


    

