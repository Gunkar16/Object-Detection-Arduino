from playsound import playsound
import os
import argparse
from collections import Counter
from gtts import gTTS
from translate import Translator
import time

def translate_objects(object_names):
    translator = Translator(to_lang='hi')
    translated_objects = []
    for obj in object_names:
        try:
            translated_obj = translator.translate(obj)
            if translated_obj is None:
                raise ValueError("Translation returned None")
            translated_objects.append(translated_obj)
        except Exception as e:
            print(f"Error translating {obj}: {e}")
            translated_objects.append(obj)  # Use English name if translation fails
        time.sleep(0.5)  # Pause between translation requests to avoid rate limiting

    return translated_objects

def pluralize(word, count):
    if count == 1:
        return word
    if word.endswith("s") or word.endswith("x") or word.endswith("ch") or word.endswith("sh"):
        return word + "es"
    elif word.endswith("y"):
        return word[:-1] + "ies"
    else:
        return word + "s"

def translate_detection_results(detection_results):
    # Translate object names to Hindi
    translated_objects = translate_objects(detection_results)

    # Count the occurrences of each detected object
    object_counts = Counter(translated_objects)
    
    # Generate the translated message
    message = "यहाँ "
    count = sum(object_counts.values())
    if count == 0:
        message += "कोई वस्तु नहीं है।"
    elif count == 1:
        # Singular form for one object
        message += "एक "
        obj = next(iter(object_counts))
        message += f"{obj} आपके सामने है।"
    else:
        object_text = ", ".join([f"{count} {obj}" for obj, count in object_counts.items()])
        # Replace the last comma with 'aur'
        last_comma_index = object_text.rfind(",")
        if last_comma_index != -1:
            object_text = object_text[:last_comma_index] + " और" + object_text[last_comma_index + 1:]
        message += object_text + " आपके सामने हैं।"



    return message


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Translate detection results into spoken Hindi.")
    parser.add_argument("detection_results", nargs="+", help="List of detected objects")
    args = parser.parse_args()

    # Translate detection results into spoken Hindi
    translated_message = translate_detection_results(args.detection_results)

    # Convert text to speech
    tts = gTTS(translated_message, lang='hi')

    # Save the speech as a temporary file
    speech_file = "translated_speech_hindi.mp3"
    tts.save(speech_file)

    # Play the speech
    playsound(speech_file)

    # Remove the temporary file
    os.remove(speech_file)
