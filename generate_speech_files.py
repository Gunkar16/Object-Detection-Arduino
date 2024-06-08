from gtts import gTTS

def create_speech_file(text, filename):
    tts = gTTS(text)
    tts.save(filename)
    print(f"Saved '{text}' as {filename}")

# Create speech files
create_speech_file("Captured image", "image_capture.mp3")
create_speech_file("Processing the image, kindly wait", "image_processing.mp3")
