"""
Audio service for text-to-speech using Coqui XTTS-v2
"""
import os
import uuid
import asyncio
from typing import Optional

from ..core.config import settings

try:
    from TTS.api import TTS
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    TTS = None

class AudioService:
    """Service for generating audio from text using Coqui TTS"""
    
    def __init__(self):
        self.tts = None
        self._initialize_tts()
    
    def _initialize_tts(self):
        """Initialize TTS model"""
        if not TTS_AVAILABLE:
            print("Warning: TTS package not available. Audio generation will be disabled.")
            self.tts = None
            return
            
        try:
            # Initialize TTS with XTTS-v2 model
            self.tts = TTS(model_name=settings.TTS_MODEL_NAME, progress_bar=False)
        except Exception as e:
            print(f"Warning: Could not initialize TTS model: {e}")
            self.tts = None
    
    async def generate_audio(self, text: str, story_id: str) -> Optional[str]:
        """Generate audio from text and return filename"""
        if not self.tts:
            print("TTS model not available, skipping audio generation")
            return None
        
        try:
            # Create unique filename
            audio_filename = f"{story_id}.wav"
            audio_path = os.path.join(settings.AUDIO_OUTPUT_DIR, audio_filename)
            
            # Ensure output directory exists
            os.makedirs(settings.AUDIO_OUTPUT_DIR, exist_ok=True)
            
            # Clean text for TTS
            clean_text = self._clean_text_for_tts(text)
            
            # Generate audio in a separate thread to avoid blocking
            await asyncio.get_event_loop().run_in_executor(
                None,
                self._generate_audio_sync,
                clean_text,
                audio_path
            )
            
            # Verify file was created
            if os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
                return audio_filename
            else:
                print(f"Audio file was not created or is empty: {audio_path}")
                return None
                
        except Exception as e:
            print(f"Error generating audio: {e}")
            return None
    
    def _generate_audio_sync(self, text: str, output_path: str):
        """Synchronous audio generation"""
        try:
            # Generate audio using TTS
            self.tts.tts_to_file(
                text=text,
                file_path=output_path,
                speaker_wav=None,  # Use default voice
                language="en"
            )
        except Exception as e:
            print(f"Error in TTS generation: {e}")
            raise
    
    def _clean_text_for_tts(self, text: str) -> str:
        """Clean text for better TTS output"""
        # Remove excessive newlines and whitespace
        text = ' '.join(text.split())
        
        # Limit text length to prevent very long audio files
        max_chars = 2000
        if len(text) > max_chars:
            # Find a good breaking point (end of sentence)
            truncated = text[:max_chars]
            last_period = truncated.rfind('.')
            last_exclamation = truncated.rfind('!')
            last_question = truncated.rfind('?')
            
            break_point = max(last_period, last_exclamation, last_question)
            if break_point > max_chars * 0.8:  # If we found a good break point
                text = text[:break_point + 1]
            else:
                text = truncated + "..."
        
        return text
    
    def delete_audio_file(self, filename: str) -> bool:
        """Delete an audio file"""
        try:
            file_path = os.path.join(settings.AUDIO_OUTPUT_DIR, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            print(f"Error deleting audio file {filename}: {e}")
            return False 