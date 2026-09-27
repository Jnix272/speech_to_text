# Description: This script takes user's speech input and converts it to text. The text is then sent to the Mistral
# API and the response is spoken back to the user.
import re
import requests
import json
import pyttsx3 as tts
import speech_recognition as sr

# Constants
URL = "http://localhost:11434/api/generate"
HEADER = {
    "Content-Type": "application/json"
}

def make_request(prompt):
    data = {
        "prompt": prompt,
        "model": "mistral",
        "stream": False,
    }

    try:
        responses = requests.post(URL, headers=HEADER, data=json.dumps(data))
        responses.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Error sending request: {e}"

    if responses.status_code == 200:
        data = responses.json()
        actual_response = data['response']
        actual_response = re.sub(r'\d', '', actual_response)
        return actual_response
    else:
        return responses.status_code, responses.text

def recognize_speech():
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Say something")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("You said: {}".format(text))
        return text
    except:
        raise Exception("Sorry, could not recognize your voice")

# Initialize the text-to-speech engine
def text_to_speech(prompt):
    engine = tts.init()
    engine.say(prompt)
    engine.runAndWait()

# Main function to run the program
def main():
    # Get user input
    text = recognize_speech()
    response = make_request(text)
    if response:
      print("Mistral: ", response)
      text_to_speech(response)

    else:
        print("No response from the API")

if __name__ == "__main__":
    main()