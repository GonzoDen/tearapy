import tkinter as tk
from tkinter import *
import sqlite3

class Tearapy(tk.Tk):

	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		self.title('Tearapy')
		self.geometry('600x400')
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
		text = Label(self, text = "Start talking to the bot! Type 'quit' to stop.")
		text.pack(side="top", fill="x", pady=10)

		#USER TALKING
		def send():
			u_message = Label(self, text = "You: " + message_box.get())
			u_message.pack()

		message_box = Entry(self, width=30)
		message_box.pack()

		button_send = Button(self, text = "send", command = send)
		button_send.pack()

		#TODO: MACHINE REPLY


		


if __name__ == "__main__":
    root = Tearapy()
    root.mainloop()