from google.cloud import texttospeech

def synthesize_media_studio_voice(text, output_file):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    name = "Kore"
    voice = texttospeech.VoiceSelectionParams(
        name="en-US-Chirp3-HD-" + name,
        language_code="en-US"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio written to {output_file}")

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
