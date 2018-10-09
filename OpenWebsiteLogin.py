# from SpeechRecognitionMain import MainFunction
from selenium import webdriver
import winspeech


def WebsiteLogin(Word, listener):
    choice = Word

    if choice == "one":
        word = "Facebook"

    elif choice =="two":
        word = "gmail"

    word = "google"
    Website = "https://www." + word + ".com/"
    driver = webdriver.Firefox()
    driver.get(Website)
    driver.maximize_window()
    driver.implicitly_wait(30)
    assert "Facebook" in driver.title
    driver.get_screenshot_as_file("D:\\facebook.png")
    driver.find_element_by_id("email").send_keys("arshdeep.sekhon.16")
    driver.find_element_by_id("pass").send_keys("9855481785")
    driver.find_element_by_id("loginbutton").click()
    driver.get_screenshot_as_file("D:\\facebook1.png")
    winspeech.listen_for_anything(MainFunction)
    driver.quit()