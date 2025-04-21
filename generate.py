from google.cloud import texttospeech
from typing import Tuple, List
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor

class TextToSpeechGenerator:
    AVAILABLE_VOICES = [
        "Aoede", "Charon", "Fenrir", "Kore",
        "Leda", "Orus", "Puck", "Zephyr"
    ]
    LANGUAGE_CODE = "en-US"
    VOICE_MODEL = "en-US-Chirp3-HD"
    DEFAULT_VOICE = "Kore"

    def __init__(self, max_workers: int = 10):
        self.client = texttospeech.TextToSpeechClient()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def get_available_voices(self) -> List[str]:
        return self.AVAILABLE_VOICES.copy()

    async def generate(self, text: str, name: str = DEFAULT_VOICE) -> Tuple[bytes, float]:
        """Generate speech from text using specified voice.

        Args:
            text: The text to convert to speech
            name: Voice name to use (must be one of AVAILABLE_VOICES)

        Returns:
            Tuple of (audio_content_bytes, generation_time_in_seconds)

        Raises:
            ValueError: If voice name is invalid
        """
        self._validate_voice_name(name)
        
        start_time = time.time()
        loop = asyncio.get_running_loop()
        
        response = await loop.run_in_executor(
            self.executor,
            self._synthesize_speech,
            text,
            name
        )
        
        return response.audio_content, time.time() - start_time

    def _validate_voice_name(self, name: str) -> None:
        if name not in self.AVAILABLE_VOICES:
            raise ValueError(
                f"Invalid voice name. Must be one of: {', '.join(self.AVAILABLE_VOICES)}"
            )

    def _synthesize_speech(self, text: str, name: str) -> texttospeech.SynthesizeSpeechResponse:
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            name=f"{self.VOICE_MODEL}-{name}",
            language_code=self.LANGUAGE_CODE
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        return self.client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
