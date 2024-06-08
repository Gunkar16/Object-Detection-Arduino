from gtts import gTTS
import os

def generate_speech(text, filename):
    tts = gTTS(text, lang='hi')
    tts.save(filename)

if __name__ == "__main__":
    # Text for "Image is being captured" in Hindi
    capture_text_hindi = "तस्वीर ली जा रही है।"
    # Text for "Processing the image" in Hindi
    processing_text_hindi = "तस्वीर प्रोसेस हो रही है, कृपया इंतजार करें।"

    # Generate speech files for Hindi
    generate_speech(capture_text_hindi, 'image_capture_hindi.mp3')
    generate_speech(processing_text_hindi, 'image_processing_hindi.mp3')
