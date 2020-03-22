# importing voice, random, and sqlite3
import speech_recognition as sr
from gtts import gTTS
import playsound
import random
from employee import Employees
import sqlite3
import os

""" VOICE CODE """


def speak_text(speak):
    rand = random.randint(1, 10000)
    filename = 'file' + str(rand) + '.mp3'
    tts = gTTS(text=speak, lang='en')
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)


def get_audio():
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


# speak_text('Please enter an ID for the employee:')
#  id_name = input('Please enter an ID for the employee:')

def select_program():
    select = input(
        'Type in voice bot to use the \"voice bot\" to enter your employee data or type in \"manual\" to enter the data manually : ')
    if select == 'voice bot' or select == ' voice bot':
        voice_commands()
        # the voice commands function
    elif select == 'manual' or select == ' manual':
        manual_commands()
    else:
        select_program()
    # the manual commands function


speak_text('Please enter the first name of the employee:')
first_name = input('Please enter the first name of the employee:')

speak_text('Please enter the last name of the employee:')
last_name = input('Please enter the last name of the employee:')

speak_text('Please enter the pay of the employee:')
pay_emp = input('Please enter the pay of the employee:')

user_emp = Employees(id, first_name, last_name, pay_emp)

# ------------------------------------------------------------------

""" USING SQLITE3 TO STORE EMPLOYEE NAMES AND PAY INTO DATABASE """

conn = sqlite3.connect(':memory:')

c = conn.cursor()

c.execute(""" CREATE TABLE employees (
              employee_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
              first TEXT,
              last TEXT,
              pay INTEGER
            )""")

conn.commit()


# TO SAVE CHANGES, DROP TABLE THEN CREATE TABLE AGAIN

# inserting an employee into the database


def insert_emp(emp):  # inserts the employee name
    with conn:
        c.execute(""" INSERT INTO employees VALUES (?,?,?,?) """, (None, emp.first, emp.last, emp.pay))


conn.commit()


# delete employees from the database
def delete_emp(id_emp):  # deletes the employee # set that equal to the user input
    with conn:
        c.execute(""" DELETE FROM employees WHERE employee_id = :employee_id""",
                  {'employee_id': id_emp})


conn.commit()


# get all employees from the database
def get_employees():  # gets all employee names
    c.execute(""" SELECT * FROM employees """)
    return c.fetchall()


conn.commit()


# commands for inserting or deleting to the database

def manual_commands():
    print('Write insert to insert the employee into the data')
    print('Write delete to delete the employee from the data')
    print('Write get data to get the information of all employees')

    command = input('Insert, Delete, or Get employees?...')

    while command == 'Insert' or command == 'Delete' or command == 'Get employees':
        if command == 'Insert' or command == ' Insert':
            insert_emp(user_emp)
            speak_text(' employee successfully added')
            speak_text('Here are the employees up until now ')
            print('Here are the employees up until now ' + '\n' + str(get_employees()))
            loop_commands_function()

        elif command == 'Delete' or command == ' Delete':
            delete_employee = input(
                "Which employee do you want me to delete. Please select the id of the employee from the data below: " + '\n' + str(
                    get_employees()))
            delete_emp(delete_employee)
            speak_text('successfully deleted')
            speak_text('Here are the employees up until now ')
            print('Here are the employees up until now' + '\n' + str(get_employees()))
            loop_commands_function()

        elif command == 'Get employees' or command == ' Get employees':
            speak_text('Here are all the employees')
            print(str(get_employees()))
            loop_commands_function()
    else:
        print('\n' + 'Please say from one of the following commands')
        print('\n' + manual_commands())


def voice_commands():
    speak_text('\n Say insert to insert the employee into the data....')
    speak_text('Say delete to delete the employee from the data....')
    speak_text('Say get data to get the information of all employees...')
    print('Say insert to insert the employee into the data')
    print('Say delete to delete the employee from the data')
    print('Say get data to get the information of all employees')
    text = get_audio()
    if text == 'insert':
        insert_emp(user_emp)
        speak_text(' employee successfully added')
        speak_text('Here are the employees up until now ')
        print('Here are the employees up until now ' + '\n' + str(get_employees()))
        loop_commands_function()

    elif text == 'delete':
        delete_employee = input(
            "Which employee do you want me to delete. Please select the id of the employee from the data below: " + '\n' + str(
                get_employees()))
        delete_emp(delete_employee)
        speak_text('successfully deleted')
        speak_text('Here are the employees up until now ')
        print('Here are the employees up until now' + '\n' + str(get_employees()))
        loop_commands_function()

    elif text == 'get employees':
        speak_text('Here are all the employees')
        print(str(get_employees()))
        loop_commands_function()

    else:
        speak_text('Please say from one of the following commands')
        voice_commands()


conn.commit()
# --------------------------------------------------------------------

# using voice to enter or delete employee from the database


# -------------------------------------------------------------------------
conn.commit()


# a function to loop the program if the user wants to add, delete or update
def loop_commands_function():
    cont = input('Do you want me to continue? Write Yes or No')
    while cont == 'Yes' or cont == 'No':
        if cont == 'Yes' or cont == ' Yes':
            select_program()
        elif cont == 'No' or cont == ' No':
            break
    else:
        speak_text('please type in yes or no')
        print('Please type in Yes or No!')


select_program()

# ----------------------- TO DO!!!----------------------------
# THE LEAST TO DO... MAKE COLUMNS SO THAT THEY CAN BE DISTINGUISHED! E.G: IT SHOULD SAY FIRST NAME, LAST NAME , AND PAY
# --------------------------------------------------------------------DONE TO DO's-------------------------------------
# 1. TO DO : NEED TO ADD EMPLOYEES INTO THE DATABASE CONTINOUSLY! NO ERRORS THAT EMPLOYEE TABLE ALREADY EXISTS
# 2. How can I auto-increment the id?
# 3. Options should be available as to which employee to delete
# Write separate commands for manual and voice!
# use while loop if the statement is not equal to insert, delete, or get employees like the one
# Voice is not working because the input variable is coming in between
