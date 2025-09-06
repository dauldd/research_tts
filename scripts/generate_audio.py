import os
from elevenlabs.client import ElevenLabs

def generate_audio(text, output_file, api_key):
    voice_id = os.environ.get("VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")  # default if not set
    client = ElevenLabs(api_key=api_key)
    try:
        audio_generator = client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )
        with open(output_file, "wb") as f:
            for chunk in audio_generator:
                f.write(chunk)
        print(f"Podcast created: {output_file} (voice_id={voice_id})")
        return output_file
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None