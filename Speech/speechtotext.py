import random
import pyttsx3
import speech_recognition as sr

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Define prompts and responses
responses = {
    "how are you": ["I am good, how about you?"],
    "what is Python": ["Python is a versatile programming language popular for web development, AI, and more."],
    "who created Python": ["Python was created by Guido van Rossum in 1991."],
    "what is AI": ["AI stands for Artificial Intelligence, which simulates human intelligence in machines."],
}

# Default response if no match is found
default_response = "I am not sure about that. Can you rephrase or ask something else?"

def read_out_loud(message):
    # Check if message matches a key in the responses
    response = default_response
    for key in responses:
        if key in message.lower():
            response = random.choice(responses[key])
            break
    
    # Speak the response
    engine.say(response)
    engine.runAndWait()

def start_recognition():
    with sr.Microphone() as source:
        print("Listening...")
        try:
            # Listen to the speech
            audio = recognizer.listen(source)
            transcript = recognizer.recognize_google(audio)
            print(f"You said: {transcript}")
            
            # Process the transcript
            read_out_loud(transcript)
        except sr.UnknownValueError:
            print("Sorry, I did not catch that.")
        except sr.RequestError:
            print("Could not request results. Please check your internet connection.")

if __name__ == "__main__":
    print("Welcome to the Student Prompting System!")
    print("Ask a question by pressing Enter and speaking.")
    
    while True:
        user_input = input("Press Enter to start or type 'exit' to quit: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        start_recognition()
