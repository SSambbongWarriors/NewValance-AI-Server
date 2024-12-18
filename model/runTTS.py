import os
import sys
import subprocess

API_KEY_STRING=""
PROJECT_ID=""

'''
pip install google-cloud-texttospeech sounddevice numpy
'''

def install_dependencies():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-cloud-texttospeech", "sounddevice","numpy"])

install_dependencies()

casual_f_name=[]
formal_f_name=[]


import numpy as np
#import sounddevice as sd
import google.cloud.texttospeech as tts
from datetime import datetime



def list_voices(language_code=None):
    client = tts.TextToSpeechClient(client_options={"api_key": API_KEY_STRING,"quota_project_id": PROJECT_ID})
    response = client.list_voices(language_code=language_code)
    voices = sorted(response.voices, key=lambda voice: voice.name)

    print(f" Voices: {len(voices)} ".center(60, "-"))
    for voice in voices:
        languages = ", ".join(voice.language_codes)
        name = voice.name
        gender = tts.SsmlVoiceGender(voice.ssml_gender).name
        rate = voice.natural_sample_rate_hertz
        print(f"{languages:<8} | {name:<24} | {gender:<8} | {rate:,} Hz")
        
    

# Ensure 'generated_audio' folder exists
output_folder = "generated_audio"
os.makedirs(output_folder, exist_ok=True)

def save_audio(content, filename):
    """Save audio content to a file."""
    filepath = os.path.join(output_folder, filename)
    with open(filepath, "wb") as audio_file:
        audio_file.write(content)
    print(f"Audio saved to: {filepath}")

def tts_with_casual_voice(text):
    """Generate TTS audio with a casual voice and save to file."""

    global casual_f_name

    try:
        client = tts.TextToSpeechClient(client_options={"api_key": API_KEY_STRING, "quota_project_id": PROJECT_ID})
        voice_name = "ko-KR-Standard-A"

        language_code = "-".join(voice_name.split("-")[:2])
        text_input = tts.SynthesisInput(text=text)
        voice_params = tts.VoiceSelectionParams(language_code=language_code, name=voice_name)
        audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

        # 시간 추가
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"casual_voice_output_{current_time}.wav"

        casual_f_name.append(f"/home/elicer/capstone_1216/generated_audio/{filename}")

        response = client.synthesize_speech(
            input=text_input,
            voice=voice_params,
            audio_config=audio_config,
        )
       
        if response.audio_content:
            print("Audio content received successfully.")
            save_audio(response.audio_content, filename)
        else:
            print("Error: No audio content returned in response.")

    except Exception as e:
        print("Google TTS Error (Casual Voice): ", e)

def tts_with_formal_voice(text):
    """Generate TTS audio with a formal voice and save to file."""
    global formal_f_name

    try:
        client = tts.TextToSpeechClient(client_options={"api_key": API_KEY_STRING, "quota_project_id": PROJECT_ID})
        voice_name = "ko-KR-Standard-B"

        language_code = "-".join(voice_name.split("-")[:2])
        text_input = tts.SynthesisInput(text=text)
        voice_params = tts.VoiceSelectionParams(language_code=language_code, name=voice_name)
        audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

        # 시간 추가
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"formal_voice_output_{current_time}.wav"

        formal_f_name.append(f"/home/elicer/capstone_1216/generated_audio/{filename}")

        response = client.synthesize_speech(
            input=text_input,
            voice=voice_params,
            audio_config=audio_config,
        )

        if response.audio_content:
            print("Audio content received successfully.")
            save_audio(response.audio_content, filename)
        else:
            print("Error: No audio content returned in response.")
        

    except Exception as e:
        print("Google TTS Error (Formal Voice): ", e)

    

def runTTS(casual, formal):
    
    for sentence in casual:
        tts_with_casual_voice(sentence)
    

    for sentence in formal:
        tts_with_formal_voice(sentence)

    return casual_f_name, formal_f_name


if __name__=="__main__":
    runTTS(casual, formal)

    
    