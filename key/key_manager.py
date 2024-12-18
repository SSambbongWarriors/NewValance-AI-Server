import os
import json

def get_OPENAI_key(filename='key.json', key='OPENAI_KEY'):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(script_dir, filename)

    try:
        with open(file_path, 'r') as file:
            key_file = json.load(file)
        return key_file.get(key)
    except FileNotFoundError:
        print(f"The file {filename} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"The file {filename} is not a valid JSON file.")

def get_TTS_key(filename='key.json', key='GOOGLE_TTS_KEY'):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(script_dir, filename)

    try:
        with open(file_path, 'r') as file:
            key_file = json.load(file)
        return key_file.get(key)
    except FileNotFoundError:
        print(f"The file {filename} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"The file {filename} is not a valid JSON file.")



