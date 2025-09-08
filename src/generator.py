import os
import sys
from config.paths import cow_image_path, uploaded_image_path, artifacts_path
from utils.logger import get_logger
from utils.custom_exception import CustomException

from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FALLBACK_GEMINI_API_KEY = os.getenv("FALLBACK_GEMINI_API_KEY")

logger = get_logger(__name__)

# Create a default client with your API key
default_client = genai.Client(api_key=GEMINI_API_KEY or FALLBACK_GEMINI_API_KEY)

def generate_image(user_api_key=None):
    """
    Uses Gemini model to generate an image of a human in the style of the Holy Cow image.
    
    Args:
        user_api_key (str, optional): User's own API key. If provided, it will be used instead of the default API key.
    """
    try:
        # Use user's API key if provided, otherwise use the default client
        if user_api_key:
            client = genai.Client(api_key=user_api_key)
            logger.info("Using user-provided API key")
        else:
            client = default_client
            logger.info("Using default API key")
            
        prompt = (
            "Using the first image of the cow generate a new image where Instead of the cow's head, use the zoomed head "
            "of the person from the second picture, adjust the person's head pose and face just like the cow from the first image, also include the glasses, keep the red background style, "
            "dont inlcude the person's photo below the neck so only the head and neck is seen in the image where the person is posing with the head upwards and the pov of the photo captures the person from a sideview exactly like the cow, "
            "then change the colour and style of the person's face like the cow's, the final output image should be in 1:1 ratio"
        )
        cow_image = Image.open(cow_image_path)
        user_image = Image.open(uploaded_image_path)

        with BytesIO() as cow_buf, BytesIO() as user_buf:
            cow_image.save(cow_buf, format="PNG")
            user_image.save(user_buf, format="PNG")
            cow_bytes = cow_buf.getvalue()
            user_bytes = user_buf.getvalue()

        # Compose inputs: prompt + encoded images
        contents = [
            prompt,
            types.Part.from_bytes(data=cow_bytes, mime_type="image/png"),
            types.Part.from_bytes(data=user_bytes, mime_type="image/png")
        ]

        response = client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=contents
        )

        for part in response.candidates[0].content.parts:
            if hasattr(part, "text") and part.text is not None:
                logger.info(f"Generated text: {part.text}")
            elif hasattr(part, "inline_data") and part.inline_data is not None:
                image = Image.open(BytesIO(part.inline_data.data))
                output_path = artifacts_path / "generated_image.png"
                image.save(output_path)
                logger.info(f"Generated image saved to: {output_path}")
                return output_path

        raise CustomException("No image data received from the model", sys)
    except Exception as e:
        error_str = str(e).lower()
        logger.error(f"Error in generate_image: {str(e)}")
        
        # Check for specific API errors and provide more user-friendly messages
        if any(keyword in error_str for keyword in ['429', 'quota', 'rate limit', 'exceeded', 'resource_exhausted', 'resource has been exhausted']):
            raise CustomException("API quota exceeded. Please try again later or use your own API key.", sys)
        elif any(keyword in error_str for keyword in ['unauthorized', 'authentication', 'invalid key', 'forbidden', '401', '403']):
            raise CustomException("API authentication failed. Please check your API key or try again later.", sys)
        elif any(keyword in error_str for keyword in ['service unavailable', 'timeout', 'connection', '503', '504']):
            raise CustomException("API service temporarily unavailable. Please try again later.", sys)
        elif 'permission' in error_str:
            raise CustomException("API permission denied. Please use your own API key.", sys)
        else:
            raise CustomException(f"Failed to generate image: {str(e)}", sys)
