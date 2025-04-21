from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, validator
from generate import TextToSpeechGenerator
from typing import List

app = FastAPI()
tts_generator = TextToSpeechGenerator()

class TextToSpeechRequest(BaseModel):
    text: str
    name: str

    @validator('name')
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
        audio_content, generation_time = tts_generator.generate(request.text, request.name)
        
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
    uvicorn.run(app, host="0.0.0.0", port=8989)
