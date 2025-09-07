import os
import io
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment

def generate_audio(parts_or_text, output_file, api_key):
    """
    Generate podcast audio.
    
    - Single-voice: parts_or_text is a string; uses narrator voice.
    - Multi-voice: parts_or_text is a list of (speaker, text) tuples; narrator uses VOICE_ID/NARRATOR_VOICE_ID, cohost uses COHOST_VOICE_ID.
    """
    multi_voice = os.getenv("MULTI_VOICE", "false").lower() == "true"
    client = ElevenLabs(api_key=api_key)
    
    # Multi-voice mode
    if multi_voice:
        final_audio = AudioSegment.silent(duration=200)
        for speaker, text in parts_or_text:
            if speaker == "narrator":
                voice_id = os.environ.get("VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")
            elif speaker == "cohost":
                voice_id = os.environ.get("COHOST_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")
            else:
                voice_id = os.environ.get("VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")
            
            try:
                audio_gen = client.text_to_speech.convert(
                    text=text,
                    voice_id=voice_id,
                    model_id="eleven_flash_v2_5",
                    output_format="mp3_44100_128",
                )
                audio_bytes = b"".join(chunk for chunk in audio_gen)
                segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")
                final_audio += segment + AudioSegment.silent(duration=300)
            except Exception as e:
                print(f"Error generating audio for {speaker}: {e}")
        
        final_audio.export(output_file, format="mp3")
        print(f"Multi-voice podcast generated: {output_file}")
    
    # Single-voice mode
    else:
        text = parts_or_text if isinstance(parts_or_text, str) else " ".join(t[1] for t in parts_or_text)
        voice_id = os.environ.get("VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")
        try:
            audio_gen = client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id="eleven_flash_v2_5",
                output_format="mp3_44100_128",
            )
            audio_bytes = b"".join(chunk for chunk in audio_gen)
            final_audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")
            final_audio.export(output_file, format="mp3")
            print(f"Podcast created: {output_file} (voice_id={voice_id})")
        except Exception as e:
            print(f"Error generating audio: {e}")

    return output_file
