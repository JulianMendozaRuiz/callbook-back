# Callbook AI Backend

A FastAPI backend service for video calling with real-time transcription and translation capabilities.

## Features

- 🎥 **Video Calling**: LiveKit integration for high-quality video calls
- 🎤 **Real-time Transcription**: AssemblyAI integration for speech-to-text
- 🌍 **Translation**: Google Cloud Translate for multi-language support
- 🔒 **Secure Token Management**: Backend token generation to protect API keys
- 🌐 **CORS Support**: Configured for frontend integration
- 🐳 **Docker Ready**: Containerized for easy deployment

## Tech Stack

- **Framework**: FastAPI (Python)
- **Video**: LiveKit API
- **Transcription**: AssemblyAI
- **Translation**: Google Cloud Translate
- **Server**: Uvicorn
- **Environment**: Python 3.13+

## Project Structure

```
callbook-back/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── models/                 # Pydantic models
│   │   ├── transcription.py    # Transcription models
│   │   ├── translation.py      # Translation models
│   │   └── videocall.py        # Video call models
│   ├── routers/                # API route handlers
│   │   ├── transcription.py    # Transcription endpoints
│   │   ├── translation.py      # Translation endpoints
│   │   └── videocall.py        # Video call endpoints
│   └── services/
│       └── external/           # External service integrations
│           ├── assemblyai.py   # AssemblyAI service
│           ├── google_translate.py # Google Translate service
│           └── livekit.py      # LiveKit service
├── .env                        # Environment variables
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── compose.yaml               # Docker Compose configuration
└── README.md                  # This file
```

## Quick Start

### Prerequisites

- Python 3.13+
- LiveKit account and credentials
- AssemblyAI API key
- Google Cloud service account with Translate API enabled

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/JulianMendozaRuiz/callbook-back.git
   cd callbook-back
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your API credentials:
   ```bash
   SERVER_PORT=8000
   LIVEKIT_URL=wss://your-livekit-server.livekit.cloud
   LIVEKIT_API_KEY=your_livekit_api_key
   LIVEKIT_API_SECRET=your_livekit_api_secret
   ASSEMBLYAI_API_KEY=your_assemblyai_api_key
   GOOGLE_CLOUD_CREDENTIALS={"type":"service_account",...}
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

### Docker Setup

1. **Using Docker Compose** (Recommended)
   ```bash
   docker compose up --build
   ```

2. **Using Docker directly**
   ```bash
   docker build -t callbook-back .
   docker run -p 8000:8000 --env-file .env callbook-back
   ```

## API Endpoints

### Video Calling (`/videocall`)

- `POST /videocall/create-call` - Create a new video call room
- `POST /videocall/join-call` - Join an existing video call
- `GET /videocall/rooms` - List all active rooms
- `GET /videocall/rooms/{room_id}` - Get room information
- `GET /videocall/variables` - Get LiveKit environment variables

### Transcription (`/transcription`)

- `POST /transcription/token` - Generate AssemblyAI temporary token

### Translation (`/translation`)

- `POST /translation/translate` - Translate text to target language

## Usage Examples

### Create a Video Call

```bash
curl -X POST "http://localhost:8000/videocall/create-call" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "John Doe",
       "identity": "user_123"
     }'
```

### Generate Transcription Token

```bash
curl -X POST "http://localhost:8000/transcription/token"
```

### Translate Text

```bash
curl -X POST "http://localhost:8000/translation/translate" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Hello world",
       "target_language": "es"
     }'
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SERVER_PORT` | Port for the FastAPI server | No (default: 8000) |
| `LIVEKIT_URL` | LiveKit server WebSocket URL | Yes |
| `LIVEKIT_API_KEY` | LiveKit API key | Yes |
| `LIVEKIT_API_SECRET` | LiveKit API secret | Yes |
| `ASSEMBLYAI_API_KEY` | AssemblyAI API key | Yes |
| `GOOGLE_CLOUD_CREDENTIALS` | Google Cloud service account JSON (single line) | Yes |

### CORS Configuration

The server is configured to accept requests from:
- `http://localhost:4200`
- `http://127.0.0.1:4200`

To modify CORS settings, edit `app/main.py`.

## Development

### Running in Development Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Network Access

To make the server accessible from your local network:

1. Find your IP address:
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}'
   ```

2. Access the server from other devices:
   ```
   http://YOUR_IP_ADDRESS:8000
   ```

### API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Security Notes

- API keys are securely managed through environment variables
- Temporary tokens are generated for client-side usage
- Google Cloud credentials are stored as environment variables (no files in repository)
- CORS is configured for specific origins

## Deployment

### Docker Deployment

1. **Build for production**
   ```bash
   docker build --platform=linux/amd64 -t callbook-back .
   ```

2. **Push to registry**
   ```bash
   docker tag callbook-back your-registry.com/callbook-back
   docker push your-registry.com/callbook-back
   ```

### Environment Setup

Ensure all environment variables are properly configured in your deployment environment.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of a technical assessment for Callbook AI.

## Support

For questions or issues, please contact the development team.
