from google.cloud import texttospeech
from typing import Tuple, List
import time

class TextToSpeechGenerator:
    AVAILABLE_VOICES = [
        "Aoede",
        "Charon",
        "Fenrir",
        "Kore",
        "Leda",
        "Orus",
        "Puck",
        "Zephyr"
    ]

    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    def get_available_voices(self) -> List[str]:
        return self.AVAILABLE_VOICES

    def generate(self, text: str, name: str = "Kore") -> Tuple[bytes, float]:
        if name not in self.AVAILABLE_VOICES:
            raise ValueError(f"Invalid voice name. Must be one of: {', '.join(self.AVAILABLE_VOICES)}")
            
        start_time = time.time()
        
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            name=f"en-US-Chirp3-HD-{name}",
            language_code="en-US"
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        
        generation_time = time.time() - start_time
        
        return response.audio_content, generation_time

def main():
    # Example text to convert to speech
    text = """
    Hello! This is a test of the Google Cloud Text-to-Speech API 
    using Media Studio voices. You can customize this text as needed.
    """
    
    # Output file name
    output_file = "output.mp3"
    
    try:
        synthesize_media_studio_voice(text, output_file)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
