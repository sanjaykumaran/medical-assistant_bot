import pyaudio
import whisper
import wave
from gtts import gTTS


import speech_recognition as sr

r = sr.Recognizer()

import openai
import os

def chatbot(prompt):
    # Set up the OpenAI API client
    openai.api_key = "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"

    # Set up the model and prompt
    model_engine = "text-davinci-003"
    headtopromt='Can you tell me short quick how to steps to help with'
    # headtopromt= "You are an AI assistant that helps people find information. Your output is being converted into speech, so be very concise. Your name is Access."
    
    prompt = headtopromt + prompt
    
    completion = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
    )

    response = completion.choices[0].text
    return(response)


def repeat_speech(audio):
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(audio.sample_width),
                    channels=1,
                    rate=audio.sample_rate,
                    output=True)

    # Write the audio data to the stream
    # stream.write(audio.get_raw_data())
    
    stream.write(audio)

    # Close the stream and terminate the PyAudio instance
    stream.stop_stream()
    stream.close()
    p.terminate()




def save_as_wav(audio):
    with open("audio.wav", "wb") as f:
        f.write(audio.get_wav_data())
    
    # # save audio as a wav file
    # with wave.open("audio.wav", "wb") as wav_file:
    #     wav_file.setnchannels(1)
    #     wav_file.setsampwidth(audio.sample_width)
    #     wav_file.setframerate(audio.sample_rate)
    #     wav_file.writeframes(audio.get_wav_data())

def say_something(text):
    tts = gTTS(text=text, lang='en')
    tts.save("audio.mp3")
    # os.system('xdg-open hello.mp3')  # For Linux/MacOS
    os.system("afplay audio.mp3")


def record_me():
    with sr.Microphone() as source:
        print("Speak Anything :")
        # print(source,sr.Recognizer())
        #r.adjust_for_ambient_noise(source, duration=1)
        # r.energy_threshold = 4000
        #r.adjust_for_ambient_noise(source, duration = 1)
        audio = r.listen(source,phrase_time_limit = 1)
        
        # repeat_speech(audio)
        
        save_as_wav(audio)
        
        
        
        model = whisper.load_model("base")
        result = model.transcribe("audio.wav",language= 'en', fp16=False)
        # print(result)
        return(result["text"]+"?")

def type_question():
    question = input("What would you like to ask: ")
    return(question)

if __name__ == "__main__":
    while(True):
        print("Started :")
        transcribed_question = (record_me())
        print(transcribed_question)
    
    
        # transcribed_question = type_question()
        
        
        response = (chatbot(transcribed_question))
        print(response)
        
        if ("911" in response):
            print("I can call 911 for you")
            say_something("I can call 911 for you")
        
        say_something(response)
    
        print("Stopped :")