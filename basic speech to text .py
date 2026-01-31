import speech_recognition as sr

# Create a recognizer object
recognizer = sr.Recognizer()

# Use microphone as source
with sr.Microphone() as source:
    print("🎤 Speak something...")

    # Adjusts for background noise
    recognizer.adjust_for_ambient_noise(source)

    # Listen to the audio
    audio = recognizer.listen(source)

    print("⏳ Recognizing...")

    try:
        # Convert speech to text using Google API
        text = recognizer.recognize_google(audio)

        print("📝 You said:", text)

    except sr.UnknownValueError:
        print("❌ Sorry, I could not understand your voice")

    except sr.RequestError:
        print("⚠️ Network error or API unavailable")