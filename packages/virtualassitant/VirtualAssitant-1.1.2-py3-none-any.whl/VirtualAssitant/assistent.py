import pyttsx3
import speech_recognition as sr #libreria para voz
engine = pyttsx3.init()
engine.setProperty('rate', 145)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) #se escoge la voz que se quiere escuchar

#recibe el texto que se le envía al crear el evento
def talk(text):
    engine.say(text)
    engine.runAndWait()
    if engine._inLoop:
        engine.endLoop()

#funcion para escuchar después de que nos pide la información
def listen():
    listener = sr.Recognizer()    
    with sr.Microphone() as source:
        talk("Te escucho...")
        listener.pause_treshold = 0.1              
        listener.adjust_for_ambient_noise(source)              
        pc = listener.listen(source)
        
    try:
        rec = listener.recognize_google(pc, language="es")
        rec = rec.lower()
    except sr.UnknownValueError: #excepción para cuando no reconoce lo que le hemos dicho
        print("No te entendí, intenta de nuevo")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return rec