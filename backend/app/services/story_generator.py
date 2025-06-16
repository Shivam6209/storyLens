"""
Story generation service using Microsoft Kosmos-2 model
"""
import base64
import io
import requests
from PIL import Image
from typing import Optional

from ..core.config import settings

class StoryGeneratorService:
    """Service for generating stories from images using Kosmos-2"""
    
    def __init__(self):
        self.api_url = f"https://api-inference.huggingface.co/models/{settings.KOSMOS_MODEL_ID}"
        self.headers = {
            "Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
    
    def _prepare_image(self, image_bytes: bytes) -> str:
        """Prepare image for API request"""
        try:
            # Open and process image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize if too large (max 1024x1024 for better performance)
            max_size = 1024
            if max(image.size) > max_size:
                image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # Convert to base64
            buffer = io.BytesIO()
            image.save(buffer, format='JPEG', quality=85)
            image_b64 = base64.b64encode(buffer.getvalue()).decode()
            
            return image_b64
            
        except Exception as e:
            raise ValueError(f"Error processing image: {str(e)}")
    
    def _create_story_prompt(self, story_type: str = "story") -> str:
        """Create appropriate prompt based on story type"""
        if story_type.lower() == "poem":
            return "Write a creative and engaging poem inspired by this image. The poem should be vivid, emotional, and capture the essence of what you see. Make it between 8-16 lines."
        else:
            return "Write a creative and engaging short story inspired by this image. The story should be imaginative, descriptive, and capture the mood and details you observe. Make it 3-5 paragraphs long."
    
    async def generate_story(self, image_bytes: bytes, story_type: str = "story") -> str:
        """Generate a story from an image"""
        try:
            # Prepare image
            image_b64 = self._prepare_image(image_bytes)
            
            # Create prompt
            prompt = self._create_story_prompt(story_type)
            
            # Prepare payload for Kosmos-2
            payload = {
                "inputs": {
                    "image": image_b64,
                    "text": prompt
                },
                "parameters": {
                    "max_new_tokens": 500,
                    "temperature": 0.8,
                    "do_sample": True,
                    "top_p": 0.9
                }
            }
            
            # Make API request
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract generated text
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get("generated_text", "")
                elif isinstance(result, dict):
                    generated_text = result.get("generated_text", "")
                else:
                    generated_text = str(result)
                
                # Clean up the generated text
                story = self._clean_generated_text(generated_text, prompt)
                
                if not story.strip():
                    return self._get_fallback_story(story_type)
                
                return story
            
            elif response.status_code == 503:
                # Model is loading, return fallback
                return self._get_fallback_story(story_type)
            
            else:
                raise Exception(f"API request failed: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            # Network error, return fallback
            return self._get_fallback_story(story_type)
        except Exception as e:
            raise Exception(f"Error generating story: {str(e)}")
    
    def _clean_generated_text(self, text: str, prompt: str) -> str:
        """Clean and format the generated text"""
        # Remove the prompt from the beginning if it appears
        if text.startswith(prompt):
            text = text[len(prompt):].strip()
        
        # Remove common prefixes
        prefixes_to_remove = [
            "Here's a story:",
            "Here's a poem:",
            "Story:",
            "Poem:",
            "Generated text:",
        ]
        
        for prefix in prefixes_to_remove:
            if text.lower().startswith(prefix.lower()):
                text = text[len(prefix):].strip()
        
        # Clean up extra whitespace and newlines
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        text = '\n\n'.join(lines)
        
        return text
    
    def _get_fallback_story(self, story_type: str) -> str:
        """Return a fallback story when AI generation fails"""
        if story_type.lower() == "poem":
            return """A moment captured in time,
Frozen in this frame divine,
Stories whisper from each hue,
Memories both old and new.

Light and shadow dance as one,
Speaking of what's been and done,
In this image lies a tale,
Of moments that will never pale."""
        else:
            return """This image captures a moment filled with stories waiting to be told. Every detail holds significance, from the interplay of light and shadow to the subtle emotions conveyed through composition. 

There's something magical about frozen moments like these - they invite us to imagine the stories that led to this instant and wonder about what happened next. The colors, textures, and subjects all work together to create a narrative that speaks to the viewer's imagination.

In this single frame, we find a window into a world of possibilities, where every element contributes to a larger story that continues to unfold in the mind of anyone who takes the time to truly look and see.""" 