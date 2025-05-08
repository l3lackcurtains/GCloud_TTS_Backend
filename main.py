from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, field_validator
from typing import List

from generate import TextToSpeechGenerator

class TextToSpeechRequest(BaseModel):
    """Request model for text-to-speech conversion."""
    text: str
    name: str

    @field_validator('name')
    @classmethod
    def validate_voice_name(cls, v: str) -> str:
        """Validate that the voice name is one of the available voices."""
        if v not in TextToSpeechGenerator.AVAILABLE_VOICES:
            raise ValueError(
                f"Invalid voice name. Must be one of: {', '.join(TextToSpeechGenerator.AVAILABLE_VOICES)}"
            )
        return v

class AudioResponse:
    """Helper class for creating audio responses."""
    MEDIA_TYPE = "audio/mpeg"
    FILENAME = "speech.mp3"

    @classmethod
    def create(cls, audio_content: bytes, generation_time: float) -> Response:
        """Create a Response object with audio content and metadata."""
        return Response(
            content=audio_content,
            media_type=cls.MEDIA_TYPE,
            headers={
                "X-Generation-Time": f"{generation_time:.2f}",
                "Content-Disposition": f"attachment; filename={cls.FILENAME}"
            }
        )

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Text-to-Speech API",
        description="API for converting text to speech using Google Cloud TTS",
        version="1.0.0"
    )
    
    tts_generator = TextToSpeechGenerator()

    @app.get("/voices", response_model=List[str])
    async def list_voices() -> List[str]:
        """List all available voice names."""
        return tts_generator.get_available_voices()

    @app.post("/generate-audio")
    async def generate_audio(request: TextToSpeechRequest) -> Response:
        """Generate audio from text using specified voice."""
        try:
            audio_content, generation_time = await tts_generator.generate(
                request.text, 
                request.name
            )
            return AudioResponse.create(audio_content, generation_time)
            
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/healthz")
    async def health_check():
        """Health check endpoint."""
        return {"status": "ok"}

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8989,
        reload=True,
        workers=4
    )
