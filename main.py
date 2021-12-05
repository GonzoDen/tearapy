import tkinter as tk
from tkinter import *
import sqlite3

import random

## imported THERAPIST

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import random
import json
import pickle

from tensorflow.python.framework import ops

class Tearapy(tk.Tk):

	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		self.title('Tearapy')
		self.geometry('300x500')
		self.eval('tk::PlaceWindow . center')

		container = tk.Frame(self)
		container.pack(side="top", fill = "both", expand = True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}
		for page in (StartPage, Chat):
			page_name = page.__name__
			frame = page(parent = container, controller = self)
			self.frames[page_name] = frame
			frame.grid(row=0, column=0, sticky="nsew") #put the new frame on the top

		self.show_frame("StartPage")

	def show_frame(self, page_name):
		frame = self.frames[page_name]
		frame.tkraise()

	
class StartPage(tk.Frame):

	def __init__(self, parent, controller): #read on deacoupling the pages
		tk.Frame.__init__(self, parent)
		self.controller = controller
		text = Label(self, text = "Bonbon")
		text.pack(side="top", fill="x", pady=10)

		button_chat = Button(self, text = "Start Chatting", command = lambda: controller.show_frame("Chat"))
		button_chat.pack()


class Chat(tk.Frame):

	def __init__(self, parent, controller): 
		tk.Frame.__init__(self, parent)
		self.controller = controller
		text = Label(self, text = "Start talking to the bot! Type 'quit' to stop.") #add QUIT option
		text.pack(side="top", fill="x", pady=10)

		#responses = ["hello", "dorou", "kudai"] #TODO - connect ChatBot

	def preprocess(self):
        with open("intents.json") as file:
            data = json.load(file) #TODO: import json importing another file/ds with for todo upgrading

            ## extracting data
        try:
            #delete pickle.file if you change anything in intents file
            with open("data.pickle", "rb") as f:
                    words, labels, training, output = pickle.load(f)
        except:
            words = []
            labels = []
            docs_x = [] #what pattern (i)
            docs_y = [] #what tag it's part of

            for intent in data["intents"]:
                for pattern in intent["patterns"]: #pattern == what user asks 
                    wrds = nltk.word_tokenize(pattern)
                    words.extend(wrds)
                    docs_x.append(wrds)
                    docs_y.append(intent["tag"])

                if intent["tag"] not in labels:
                    labels.append(intent["tag"])

            words = [stemmer.stem(w.lower()) for w in words if w != "?"] #stemming == finding a root of the word, so bot can identify words
            words = sorted(list(set(words))) #removing duplicates

            labels = sorted(labels)

            training = []
            output = []

            out_empty = [0 for _ in range(len(labels))] 

            for x, doc in enumerate(docs_x):
                bag = [] #database for detecting the presence 

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

            ##  developing a model:

        ops.reset_default_graph()

        net = tflearn.input_data(shape=[None, len(training[0])])
        net = tflearn.fully_connected(net, 8) #first hidden layer 
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(output[0]), activation="softmax") #allow us to get probabilities for each output
        net = tflearn.regression(net) 

        model = tflearn.DNN(net) #training

        try:
            model.load("model.tflearn")
        except:
        ## training and saving the model
            model = tflearn.DNN(net)
            model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
            model.save("model.tflearn")

    def bag_of_words(self, s, words):
        bag = [0 for _ in range(len(words))]

        s_words = nltk.word_tokenize(s)
        s_words = [stemmer.stem(word.lower()) for word in s_words]

        for se in s_words:
            for i, w in enumerate(words):
                if w == se:
                    bag[i] = 1
                
        return numpy.array(bag)


	def reply(self, *args): #TODO separate printing user reply from bot giving an example
		u_message = Label(self, text = "You: " + message_box.get())
		u_message.pack()

		bot_message = Label(self, text = "Tearapist: " + str(random.choice(responses)))
		bot_message.pack()

		inp = message_box.get()

        self.preprocess()
        self.bag_of_words()
        results = self.model.predict([bag_of_words(inp, words)])
        results_index = numpy.argmax(results)
        tag = labels[results_index]

        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

		message_box = Entry(self, width=30)
		message_box.pack()

		button_send = Button(self, text = "send", command = reply) 
		button_send.pack()

if __name__ == "__main__":
    root = Tearapy()
    root.mainloop()