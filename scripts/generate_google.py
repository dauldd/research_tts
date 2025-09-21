import os
import time
from pydub import AudioSegment
from google.cloud import texttospeech
from google.cloud import storage

def generate_long_audio(text, output_file, voice_params):
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    bucket_name = os.environ.get("GOOGLE_CLOUD_STORAGE_BUCKET")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    if not bucket_name:
        raise ValueError("GOOGLE_CLOUD_STORAGE_BUCKET environment variable not set.")

    client = texttospeech.TextToSpeechLongAudioSynthesizeClient()

    gcs_filename = f"tts_output_{int(time.time())}.wav"
    output_gcs_uri = f"gs://{bucket_name}/{gcs_filename}"

    input = texttospeech.SynthesisInput(text=text)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    parent = f"projects/{project_id}/locations/us-central1"

    request = texttospeech.SynthesizeLongAudioRequest(
        parent=parent,
        input=input,
        audio_config=audio_config,
        voice=voice_params,
        output_gcs_uri=output_gcs_uri,
    )

    print(f"Starting long audio synthesis...")
    operation = client.synthesize_long_audio(request=request)

    result = operation.result(timeout=600)
    print(f"Long audio synthesis completed. Output saved to: {output_gcs_uri}")

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(gcs_filename)

    wav_filename = output_file.replace('.mp3', '.wav')
    blob.download_to_filename(wav_filename)
    print(f"Downloaded WAV file: {wav_filename}")

    audio = AudioSegment.from_wav(wav_filename)
    audio.export(output_file, format="mp3")
    print(f"Converted to MP3: {output_file}")

    return output_file

def generate_audio(text, output_file, api_key=None):
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")

    voice_params = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Studio-Q",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )

    print(f"Using Long Audio API for text generation...")
    return generate_long_audio(text, output_file, voice_params)