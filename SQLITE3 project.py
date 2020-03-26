# importing voice, random, and sqlite3
import speech_recognition as sr
from gtts import gTTS
import playsound
import random
from employee import Employees
import sqlite3
import os
import re

#--------------------------------------------------------------------
def speak_text(speak):
    """
     This function makes the voice bot speak a specific command.

     THIS IS A CHANGE FOR GIT
    """
    rand = random.randint(1, 10000)
    filename = 'file' + str(rand) + '.mp3'
    tts = gTTS(text=speak, lang='en')
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

#----------------------------------------------------------------------------
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

# ------------------------------------------------------------------


conn = sqlite3.connect('employee.db')

c = conn.cursor()

'''  Create a table called 'employees'  using SQLITE3 to store data'''

c.execute(""" CREATE TABLE IF NOT EXISTS employees (
              employee_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
              first TEXT,
              last TEXT,
              pay INTEGER
            )""")

conn.commit()

#------------------------------------------------------------------------------------------------------
def insert_emp(emp):
    """

     This function inserts the employee data into the table

    """
    with conn:
        c.execute(""" INSERT INTO employees VALUES (?,?,?,?) """, (None, emp.first, emp.last, emp.pay))


conn.commit()
#-----------------------------------------------------------------------------------------------------------

def delete_emp(id_emp):
    """

    This function deletes the employee from the data

    """
    with conn:
        c.execute(""" DELETE FROM employees WHERE employee_id = :employee_id""",
                  {'employee_id': id_emp})


conn.commit()

#-----------------------------------------------------------------------------------------------------------



def get_employees():  # gets all employee names
    """

    This function prints out all the employees in the data


    """
    c.execute(""" SELECT * FROM employees """)
    return c.fetchall()


conn.commit()

#-----------------------------------------------------------------------------------------------------------



def manual_commands():
    """

    This function is executed when the user decides to edit the data manually. The if-elif-else statements are used to update, delete or get employees

    """

    print('\nWrite \"update\" to add another employee into the data')
    print('Write \"delete\" to delete an employee from the data')
    print('update or delete....?')
    command = input()

    if command == 'update' or command == ' update':
        employee_info()
        speak_text('Here are the employees up until now ')
        print('Here are the employees up until now ' + '\n' + str(get_employees()))
        loop_commands_function()

    elif command == 'delete' or command == ' delete':
        print("Which employee do you want me to delete. Please select the id of the employee from the data below: " + '\n' + str(get_employees()))
        delete_employee = input()
        delete_emp(delete_employee)
        speak_text('successfully deleted')
        speak_text('Here are the employees up until now ')
        print('\nHere are the employees up until now' + '\n' + str(get_employees()))
        loop_commands_function()

    elif command == 'Get employees' or command == ' Get employees':
        speak_text('Here are all the employees')
        print(str(get_employees()))
        loop_commands_function()
    else:
        print('\n' + 'Please say from one of the following commands')
        print('\n' + manual_commands())

#-----------------------------------------------------------------------------------------------------------

        
def voice_commands():
    """

    This function uses the voice bot to insert, delete, or get employees from the data. Similar to the manual_commands() function, but it just uses voice.

    """
    speak_text('\nSay update to insert another employee into the data....')
    speak_text('Say delete to delete the employee from the data....')
    speak_text('Say get employees to get the information of all employees...')

    print('\nSay update to insert the employee into the data')
    print('Say delete to delete the employee from the data')
    print('Say get employees to get the information of all employees')

    text = get_audio()

    if text == 'update':
        employee_info()
        speak_text('Here are the employees up until now ')
        print('Here are the employees up until now ' + '\n' + str(get_employees()))
        loop_commands_function()

    elif text == 'delete':
        print("Which employee do you want me to delete. Please select the id of the employee from the data below: " + '\n' +str(get_employees()))
        delete_employee = input()
        delete_emp(delete_employee)
        speak_text('employee successfully deleted')
        speak_text('Here are the employees up until now ')
        print('Here are the employees up until now' + '\n' + str(get_employees()))
        loop_commands_function()

    elif text == 'get employees':
        speak_text('\nHere are all the employees')
        print(str(get_employees()))
        loop_commands_function()

    else:
        speak_text('Please say from one of the following commands')
        voice_commands()


conn.commit()

#-----------------------------------------------------------------------------------------------------------


def employee_info():
    while True:
        speak_text('please enter the first name of the employee')
        print('\nPlease enter the first name of the employee:-')
        first_name = input()
        if re.findall('[a-z]', first_name):
            break

    while True:
        speak_text('please enter the last name of the employee')
        print('Please enter the last name of the employee:-')
        last_name = input()
        if re.findall('[a-z]', last_name):
            break

    while True:
        speak_text('please enter the pay of the employee')
        print('Please enter the pay of the employee:-')
        pay_emp = input()
        if re.findall("\d", pay_emp):
            break

    user_emp = Employees(first_name, last_name, pay_emp)

    speak_text('employee was successfully added to the database')

    return insert_emp(user_emp)

#-----------------------------------------------------------------------------------------------------------


def select_program():
    """
    This function makes the user select from writing manual commands to edit the employee data or use the voice bot

    """
    print('Type in voice bot to use the \"voice bot\" to enter your employee data or type in \"manual\" to enter the data manually :- ')
    select = input()
    if select == 'voice bot' or select == ' voice bot':
        voice_commands()
    elif select == 'manual' or select == ' manual':
        manual_commands()
    else:
        select_program()
        
        
    
conn.commit()

#-----------------------------------------------------------------------------------------------------------





def loop_commands_function():
    """

    This function asks the user if he/she wants to continue with the program


    """
    print('Do you want me to continue? Write Yes or No')
    cont = input()
    if cont == 'Yes' or cont == ' Yes':
        employee_info()
    elif cont == 'No' or cont == ' No':
        speak_text('thank you for your time')
        speak_text('goodbye now')
        exit()
    else:
        speak_text('please type in yes or no')
        print('Please type in Yes or No!')


employee_info()
select_program()

#-----------------------------------------------------------------------------------------------------------
