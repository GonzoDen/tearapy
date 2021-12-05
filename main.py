from tkinter import *
import sqlite3

root = Tk()
root.title('Tearapy')
root.geometry('600x400')
root.eval('tk::PlaceWindow . center')

def chat():
	bonjour = Label(root, text = "Bonjour, " + textBox.get())
	bonjour.pack()

def analize():
	bonjour = Label(root, text = "Bon, " + textBox.get())
	bonjour.pack()


text = Label(root, text="Bonjour! Comment tu t'appelles?")
text.pack()

textBox = Entry(root, width=15)
textBox.pack()

button = Button(root, text="Chat", command = chat)
button.pack()

button = Button(root, text="Statistics", command = analize)
button.pack()

root.mainloop()