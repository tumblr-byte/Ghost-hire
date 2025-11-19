from PIL import Image
import requests
import os
import logging

logger = logging.getLogger(__name__)


# ============================================
# REVERSE IMAGE SEARCH
# ============================================

def check_image_online(image_path):
    """
    Check if image exists online using SerpAPI reverse image search.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        tuple: (exists_online: bool, sources: list)
    """
    api_key = os.environ.get('SERPAPI_KEY')
    
    if not api_key:
        logger.warning("SERPAPI_KEY not found. Skipping reverse image search.")
        return False, []
    
    try:
        # For SerpAPI, we need to upload the image or provide a URL
        # This is a simplified implementation
        # In production, you'd upload to a temporary hosting service
        
        # For now, we'll skip the actual API call and return False
        # You'll need to implement the actual SerpAPI integration
        logger.info("Reverse image search check (placeholder)")
        
        # Actual implementation would look like:
        # params = {
        #     'engine': 'google_reverse_image',
        #     'image_url': uploaded_image_url,
        #     'api_key': api_key
        # }
        # response = requests.get('https://serpapi.com/search', params=params)
        # data = response.json()
        # 
        # if 'image_results' in data and len(data['image_results']) > 0:
        #     return True, [result['source'] for result in data['image_results'][:3]]
        
        return False, []
        
    except Exception as e:
        logger.error(f"Error in reverse image search: {e}")
        return False, []


# ============================================
# DUPLICATE FACE DETECTION
# ============================================

def check_duplicate_face(uploaded_photo_path):
    """
    Compare uploaded photo with all existing users' verification photos.
    
    NOTE: PyTorch-based face detection disabled for production deployment.
    This feature is too resource-intensive for Railway's free tier.
    
    Args:
        uploaded_photo_path: Path to the uploaded photo
        
    Returns:
        tuple: (is_duplicate: bool, matched_username: str or None)
    """
    logger.info("Face duplicate detection disabled (PyTorch not available in production)")
    return False, None
