import speech_recognition as sr

recognizer = sr.Recognizer()

while True:
    with sr.Microphone() as source:
        print("🎤 Say something (say 'stop' to exit)")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)

        if "stop" in text.lower():
            print("👋 Exiting...")
            break

    except:
        print("Could not understand")