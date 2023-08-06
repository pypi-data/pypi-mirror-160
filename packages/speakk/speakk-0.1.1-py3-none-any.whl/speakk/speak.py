import colorama
from colorama import *
import pyttsx3
import os



def display(str):
    print(Style.BRIGHT+Fore.CYAN+Back.GREEN+" "+str+" "+Style.RESET_ALL+Fore.WHITE+Back.RESET)

def alert(str):
    print(Style.BRIGHT+Fore.BLACK+Back.LIGHTRED_EX+" "+str+" "+Style.RESET_ALL+Fore.WHITE+Back.RESET)

def speak(audio,int):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[int].id)
    engine.setProperty('rate',170)
    engine.say(audio)
    engine.runAndWait()

def terminal():
    loop = True
    while loop:
        t_command = str(input("Enter your command : "))
        if (t_command != "exit" and t_command != "quit"):
            if t_command[:2] == "cd":
                os.chdir(t_command[3:])
            elif t_command[:2] == "ls":
                os.system("cd")
            else:
                os.system(t_command)
        else:
            alert("Closing Terminal")
            loop == False
            break

def command(str):
    if (str == ""):
        os.system("cd")
    else:
        os.system(str)




