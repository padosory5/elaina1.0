import random
import numpy
import speech_recognition as sr
from time import ctime
import webbrowser
import os
import playsound
import urllib.request
from model import bag_of_words
from model import model
from model import words
from model import labels
from model import data

client_id = "6er9p07etq"
client_secret = "VNMRk9SsZzUOZc9S34ryUNxcs73Fqy4PKRP7wyP1"

r = sr.Recognizer()


def chat():
    print("마이크는 통해 일레이나와 대화해보세요")
    while True:

        voice_data = record_audio()

        print(">", voice_data)

        results = model.predict([bag_of_words(voice_data, words)])
        results_index = numpy.argmax(results)
        tag = labels[results_index]

        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

        if tag == 'goodbye':
            speak(random.choice(responses))
            break
        elif tag == 'time':
            speak("현재 시간은" + ctime() + "입니다!")
        elif tag == 'search':
            url = 'https://google.com/search?q=' + voice_data
            webbrowser.get().open(url)
            speak(random.choice(responses))
        elif tag == 'file':
            with open('fileTest.txt', 'w') as f:
                f.write("안녕하세요!")
            speak(random.choice(responses))
        else:
            speak(random.choice(responses))


def record_audio():
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            voice_data = r.recognize_google(audio, language="ko-KR")
        except sr.UnknownValueError:
            print("죄송합니다만 다시한번 얘기해주실수 있나요?")
        except sr.RequestError:
            print("현재 서비스가 다운되어있습니다")
        return voice_data


def speak(audio_string):
    encText = urllib.parse.quote(audio_string)
    data = "speaker=nbora&volume=0&speed=0&pitch=1&format=mp3&text=" + encText
    url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
    request.add_header("X-NCP-APIGW-API-KEY", client_secret)
    response = urllib.request.urlopen(request, data=data.encode('UTF-8'))
    rescode = response.getcode()
    if(rescode == 200):
        print(audio_string)
        response_body = response.read()
        with open('1111.mp3', 'wb') as f:
            f.write(response_body)
        playsound.playsound("1111.mp3")
        os.remove("1111.mp3")
    else:
        print("Error Code:" + rescode)


chat()
