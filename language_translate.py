from googletrans import Translator
from gtts import gTTS
import os
import pygame
import tempfile

def translate_and_play(text, target_language='ja'):
    # Translate text
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    translated_text = translation.text

    # Save the translated text as an audio file
    with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
        tts = gTTS(translated_text, lang=target_language)
        tts.save(temp_audio.name)

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load and play the audio file
    pygame.mixer.music.load(temp_audio.name)
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Explicitly close and free the resources associated with the mixer
    pygame.mixer.music.stop()
    pygame.mixer.quit()

    # Clean up the temporary audio file
    os.remove(temp_audio.name)

    return translated_text

# if __name__ == "__main__":
#     # Example usage:
#     input_text = "Hello, how are you?"
#     target_language = "hi"  # Language code for Japanese

#     translated_text = translate_and_play(input_text, target_language)
#     print(f"Original text: {input_text}")
#     print(f"Translated text: {translated_text}")
