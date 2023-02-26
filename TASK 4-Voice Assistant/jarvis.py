import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia

listener = sr.Recognizer()

machine = pyttsx3.init()

def talk(text):
    machine.say(text)
    machine.runAndWait()

def input_instruction():
    global instruction
   
    try:
       with sr.Microphone() as origin:
           print("listening....")
           speech = listener.listen(origin)
           instruction = listener.recognize_google(speech)
           instruction = instruction.lower()
           if "jarvis" in instruction:
                instruction = instruction.replace('jarvis', " ")
                print(instruction)
              
    except:
      pass
    return instruction

def play_Jarvis():

    instruction = input_instruction()
    print(instruction)
    if "play" in instruction:
        song = instruction.replace('play', "")
        talk("playing" + song)
        pywhatkit.playonyt(song)

    elif 'time' in instruction:
        time = datetime.datetime.now().strftime('%I:%M%p')
        talk('Current time'+ time)

    elif 'date' in instruction:
        date = datetime.datetime.now().strftime('%d /%m /%Y')
        talk("Today's date" + date)

    elif 'how are you' in instruction:
        talk('I am fine, how about you')

    elif 'What is your name' in instruction:
        talk('I am  Jarvis, what can i do for you?')
    
    elif 'who is' in instruction:
        human = instruction.replace('who is', " ")
        info = wikipedia.summary(human, 1)
        print(info)
        talk(info)

    else:
        talk('Please repeat')

play_Jarvis()        
