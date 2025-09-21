# Research Podcast Generator

This project as part of the larger project converts PDF research papers into podcast-style audio summaries using ElevenLabs TTS (eleven_flash_v2_5) and Gemini 2.5 Pro for text generation. It is intended to provide an informative spoken overview of technical papers. You can also adjust the language by specifying in the prompt. The pipeline supports dual TTS providers - choose between Google Cloud Text-to-Speech with Studio voices or ElevenLabs for audio generation. Google TTS uses the Long Audio API for extended content and automatically downloads both WAV and MP3 formats locally. Run with `python main.py google` or `python main.py elevenlabs` to select your preferred TTS provider.

## Features

- Extracts text from PDF documents.
- Generates podcast-style scripts from research papers using Gemini 2.5 Pro.
- Converts scripts to high-quality audio using ElevenLabs eleven_flash_v2_5.
- Supports single-voice or multi-voice (narrator + co-host) modes.
- Multi-voice mode creates dynamic conversations between narrator and co-host, enabled by setting `MULTI_VOICE=true` in your .env file.
- Supports custom voice selection via .env.
- Automatically saves generated audio to episodes/.

## Requirements

```bash
pip install -r requirements.txt
```

Dependencies include:

- requests – HTTP requests for PDF download and API calls
- PyPDF2 – PDF text extraction
- python-dotenv – environment variable management
- elevenlabs – ElevenLabs TTS client
- pydub – optional audio post-processing

## Setup

1. Create a `.env` file with your API keys:

```
ELEVENLABS_API_KEY=your_elevenlabs_key
GOOGLE_API_KEY=your_gemini_key
VOICE_ID=optional_voice_id
MULTI_VOICE=true
GOOGLE_APPLICATION_CREDENTIALS=path_to_service_account.json
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_CLOUD_STORAGE_BUCKET=your_bucket_name
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Download or provide the PDF file URL.
2. Run the pipeline:

```bash
python main.py google    # Use Google Cloud Text-to-Speech
python main.py elevenlabs # Use ElevenLabs TTS
```

- Extracted text will be processed by Gemini into a podcast-ready script.
- The script is converted to MP3 using ElevenLabs eleven_flash_v2_5.
- Audio files are saved into episodes/.

## Notes

- The output is intended as an overview of the research paper, not a full transcription.
- Scripts are designed to produce 15+ minutes of audio for detailed research papers.
- Voice defaults to a preset if VOICE_ID is not specified in .env.

## Folder Structure

```
├── episodes/         # Generated audio files
├── scripts/              # Python modules (text extraction, TTS, etc.)
├── .env              # API keys and voice configuration
├── requirements.txt
└── README.md
```
