from elevenlabs.client import ElevenLabs

def generate_audio(text, output_file, api_key, voice_id="JBFqnCBsd6RMkjVDRZzb"):
    client = ElevenLabs(api_key=api_key)
    try:
        generator = client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )
        with open(output_file, "wb") as f:
            for chunk in generator:
                f.write(chunk)
        print(f"Podcast created: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None
