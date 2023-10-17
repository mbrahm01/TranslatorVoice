import tkinter as tk
from tkinter import ttk
from googletrans import Translator
from gtts import gTTS
import os
import tempfile

# Define language codes dictionary
language_codes = {
    'afrikaans': 'af',
    'albanian': 'sq',
    # ... (add more languages as needed)
    'zulu': 'zu'
}

class AutocompleteCombobox(ttk.Combobox):
    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list)
        self._hits = []
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._completion_list

    def autocomplete(self, delta=0):
        if delta:
            self.delete(0, tk.END)
        else:
            self.delete(self.position, tk.END)
        _hits = []
        _hits = [item for item in self._completion_list if item.lower().startswith(self.get().lower())]
        self._hits = _hits
        if _hits != self._completion_list:
            self._hits = _hits
            self.position = len(self.get())
            self['values'] = _hits
            self.event_generate('<Down>')

    def handle_keyrelease(self, event):
        if event.keysym in ('BackSpace', 'Left', 'Right', 'Up', 'Down', 'Shift_R', 'Shift_L', 'Control_R', 'Control_L'):
            return

        if event.keysym == 'Return':
            self._hits = []
            return

        if event.keysym == 'Tab':
            self.set(self._hits[0])
            return

        self.autocomplete(delta=1)

class TranslationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Translator")

        # Input Label and Entry for User Input
        tk.Label(root, text="Enter text in English:").pack(pady=5)
        self.input_entry = tk.Entry(root, width=50)
        self.input_entry.pack(pady=5)

        # Language Dropdown
        tk.Label(root, text="Select target language:").pack(pady=5)
        self.language_var = tk.StringVar()
        self.language_dropdown = AutocompleteCombobox(root, textvariable=self.language_var)
        self.language_dropdown.set_completion_list(list(language_codes.keys()))
        self.language_dropdown.pack(pady=5)

        # User Input Label and Entry
        tk.Label(root, text="OR enter text:").pack(pady=5)
        self.user_input_entry = tk.Entry(root, width=50)
        self.user_input_entry.pack(pady=5)

        # Translate Button
        tk.Button(root, text="Translate", command=self.translate_and_play).pack(pady=10)

    def translate_and_play(self):
        user_input = self.user_input_entry.get()
        if user_input:
            input_text = user_input
        else:
            input_text = self.input_entry.get()

        target_language = language_codes.get(self.language_var.get())

        if input_text and target_language:
            translated_text = self.translate_text(input_text, target_language)
            self.play_translated_audio(translated_text)
        else:
            print("Please enter text and choose a target language.")

    def translate_text(self, text, target_language):
        translator = Translator()
        translation = translator.translate(text, dest=target_language)
        return translation.text

    def play_translated_audio(self, translated_text):
        with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
            tts = gTTS(translated_text, lang="en")  # Assuming the translation is in English
            tts.save(temp_audio.name)

            # Play the audio
            os.system("start " + temp_audio.name)  # On Windows
            # os.system("mpg321 " + temp_audio.name)  # On Linux with mpg321 installed

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslationApp(root)
    root.mainloop()
