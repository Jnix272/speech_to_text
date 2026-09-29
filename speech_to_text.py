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
        response_text = responses.text
        data = json.loads(response_text)
        actual_response = data['response']
        actual_response = re.sub(r'\d', '', actual_response)
        return actual_response
    else:
        return responses.status_code, responses.text

# Initialize recognizer and microphone once at module level
r = sr.Recognizer()
mic = None
try:
    mic = sr.Microphone()
except OSError:
    print("Warning: No default microphone found.")

def recognize_speech():
    if not mic:
        raise Exception("Microphone not available")

    with mic as source:
        print("Say something")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("You said: {}".format(text))
        return text
    except Exception:
        raise Exception("Sorry, could not recognize your voice")

# Initialize the text-to-speech engine once at module level
engine = None
try:
    engine = tts.init()
except Exception as e:
    print(f"Warning: TTS engine could not be initialized: {e}")

def text_to_speech(prompt):
    if not engine:
        print(f"TTS (disabled): {prompt}")
        return

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