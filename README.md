# YtCaptionBridge

A lightweight REST API proxy for fetching YouTube video captions. Built with FastAPI and youtube-transcript-api, it provides a secure and rate-limited interface for accessing YouTube transcripts in multiple formats.

## Features

- 🎯 Simple REST API for YouTube captions
- 🌍 Multi-language support with translation
- 🔄 Multiple output formats (TXT, SRT, etc.)
- 🔒 Secure API key authentication
- ⚖️ Configurable rate limiting

## Quick Start

### Prerequisites

- Python 3.9+
- pip
- virtualenv (recommended)

### Installation

1. Clone the repository
```sh
git clone https://github.com/yourusername/YtCaptionBridge.git
cd YtCaptionBridge
```

2. Create and activate virtual environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```sh
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and update the configuration

## Running the Application

```sh
python run.py
```

The API will be available at `http://localhost:8000`

### Docker
Build and run using Docker:
```sh
docker build -t ytcaptionsbridge . 
docker run --name YtCaptionsBridge -p 8000:8000 ytcaptionsbridge 
```


## API Endpoints

### Get Transcript
```
GET /api/v1/transcripts/{video_id}/lang/{language}.{format}
```

Parameters:
- `video_id`: YouTube video ID
- `language`: Language code (e.g., 'en', 'es', 'fr')
- `format`: Output format ('txt', 'srt')
- `auto`: (optional) Use auto-generated captions
- `target_language`: (optional) Translate captions to this language

Example:
```
curl -X GET "http://localhost:8000/api/v1/transcripts/E4WlUXrJgy4/lang/en.txt" \
     -H "X-API-Key: your-secret-key-here"
```

## Configuration

The application can be configured using environment variables or a `.env` file. See `.env.example` for available options.

## License

[MIT License](LICENSE)

## Acknowledgments
- Uses [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api)