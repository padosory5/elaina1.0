import pickle
import json
import random
import tensorflow as tf
import tflearn
import numpy
import nltk
from nltk.stem.lancaster import LancasterStemmer
import speech_recognition as sr
from time import ctime
import webbrowser
import os
import playsound
from gtts import gTTS
import urllib.request


stemmer = LancasterStemmer()


client_id = "6er9p07etq"
client_secret = "VNMRk9SsZzUOZc9S34ryUNxcs73Fqy4PKRP7wyP1"

r = sr.Recognizer()


with open("intents.json", 'r', encoding='UTF-8', errors='ignore') as file:
    data = json.load(file)


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
'''
tf.compat.v1.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1500, batch_size=8, show_metric=True)
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
