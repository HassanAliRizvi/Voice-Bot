# SQLITE3 PROJECT THAT STORES ESSENTIAL EMPLOYEE INFORMATION

## Table of contents


Welcome to my SQLITE3 project that stores employee information. Users can either manually type in the information or use the voice bot to either insert or delete the employee or get employees from the data. 

## VOICE COMMANDS

### Modules to import for the voice bot
	import speech_recognition as sr  
	from gtts import gTTS  
	import playsound  
	import random  

### The speak_text() function makes the voice bot talk using the playsound and gTTS module while the get_audio() function takes in input from the user for a specific command.

	def speak_text(speak):
	    """
	     This function makes the voice bot speak a specific command.
	    """
	    rand = random.randint(1, 10000)
	    filename = 'file' + str(rand) + '.mp3'
	    tts = gTTS(text=speak, lang='en')
	    tts.save(filename)
	    playsound.playsound(filename)
	    os.remove(filename)


	def get_audio():
	    """

	    This function takes input from the user through the microphone and returns an exception if the command is not understood by the voice bot

	    """
	    r = sr.Recognizer()
	    with sr.Microphone() as source:
		audio = r.listen(source)
		said = ''

		try:
		    said = r.recognize_google(audio)
		    print(said)
		except Exception as e:
		    print('Exception' + str(e))
	    return said


	speak_text('welcome to my SQLITE project that stores employee information into a database.')
	speak_text('you can enter the data manually or use the voice bot')


# CREATING THE DATABASE

# Modules for the database
	from employee import Employees  
	import sqlite3 
	import os  
	import re
	 
