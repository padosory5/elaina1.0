import random
import numpy
import speech_recognition as sr
from time import ctime
import webbrowser
import os
import playsound
import urllib.request
import pickle
import json
import tensorflow as tf
import tflearn
import numpy
import nltk
import requests
from nltk.stem.lancaster import LancasterStemmer

client_id = "6er9p07etq"
client_secret = "VNMRk9SsZzUOZc9S34ryUNxcs73Fqy4PKRP7wyP1"


stemmer = LancasterStemmer()


with open("intents.json", 'r', encoding='UTF-8', errors='ignore') as file:
    data = json.load(file)
'''
try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)
'''
words = []
labels = []
docs_x = []
docs_y = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tag"])

    if intent["tag"] not in labels:
        labels.append(intent["tag"])

words = [stemmer.stem(w.lower()) for w in words if w != "?"]
words = sorted(list(set(words)))

labels = sorted(labels)

training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []

    wrds = [stemmer.stem(w.lower()) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)

training = numpy.array(training)
output = numpy.array(output)

with open("data.pickle", "wb") as f:
    pickle.dump((words, labels, training, output), f)


net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 15)
net = tflearn.fully_connected(net, 15)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)
'''
try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=2000, batch_size=10, show_metric=True)
    model.save("model.tflearn")
'''
model.fit(training, output, n_epoch=2500, batch_size=15, show_metric=True)
model.save("model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    return numpy.array(bag)


def chat():
    speak("네 부르셨습니까?")

    voice_data = record_audio()

    print(">", voice_data)

    results = model.predict([bag_of_words(voice_data, words)])
    results_index = numpy.argmax(results)
    tag = labels[results_index]

    for tg in data["intents"]:
        if tg['tag'] == tag:
            responses = tg['responses']

    if tag == 'time':
        speak("현재 시간은" + ctime() + "입니다!")
    elif tag == 'search':
        url = 'https://google.com/search?q=' + voice_data
        webbrowser.get().open(url)
        speak(random.choice(responses))
    elif tag == 'file':  # 파일 내용추가, 파일 생성, 어떠한 파일
        file()
        speak(random.choice(responses))
    elif tag == 'file_add':
        file_add()
        speak(random.choice(responses))
    else:
        speak(random.choice(responses))


def record_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio, language="ko-KR")
        except Exception as e:
            speak("Exception: " + str(e))
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


def file():
    speak("어떤 파일을 생성해 드릴까요?")
    file_name = record_audio()
    speak("어떤 내용을 추가 할까요?")
    file_content = record_audio()
    with open(file_name + ".txt",  'w') as f:
        f.write(file_content)


def file_add():
    speak("무슨 파일에다가 내용을 추가 할까요?")
    file_name = record_audio()
    speak("어떤 내용을 추가 하고 싶으신가요?")
    file_content = record_audio()
    with open(file_name + ".txt", 'a') as f:
        f.write("\n" + file_content)


print("마이크를 통해 일레이나라고 말하면 일레이나가 대답합니다!")


while True:

    calling = record_audio()

    if calling.count("하야사카") > 0:
        chat()
    elif calling.count("셧다운") > 0:
        break
    else:
        continue
