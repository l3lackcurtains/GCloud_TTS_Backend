from fastapi import FastAPI, HTTPException, Response, BackgroundTasks
from pydantic import BaseModel, field_validator  # Changed from validator to field_validator
from generate import TextToSpeechGenerator
from typing import List
import asyncio

app = FastAPI()
tts_generator = TextToSpeechGenerator()

class TextToSpeechRequest(BaseModel):
    text: str
    name: str

    @field_validator('name')  # Changed from @validator to @field_validator
    @classmethod  # Added @classmethod decorator as required by field_validator
    def validate_voice_name(cls, v):
        if v not in TextToSpeechGenerator.AVAILABLE_VOICES:
            raise ValueError(f"Invalid voice name. Must be one of: {', '.join(TextToSpeechGenerator.AVAILABLE_VOICES)}")
        return v

@app.get("/voices", response_model=List[str])
async def list_voices():
    """List all available voice names"""
    return tts_generator.get_available_voices()

@app.post("/generate-audio")
async def generate_audio(request: TextToSpeechRequest):
    try:
        audio_content, generation_time = await tts_generator.generate(request.text, request.name)
        
        response = Response(
            content=audio_content,
            media_type="audio/mpeg",
            headers={
                "X-Generation-Time": f"{generation_time:.2f}",
                "Content-Disposition": "attachment; filename=speech.mp3"
            }
        )
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",  # Changed to use import string
        host="0.0.0.0",
        port=8989,
        reload=True,  # Enable auto-reload during development
        workers=4
    )
