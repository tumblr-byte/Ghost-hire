import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as T
from PIL import Image
import requests
import os
import logging

logger = logging.getLogger(__name__)

# ============================================
# SIAMESE NETWORK MODEL
# ============================================

class SiameseNetwork(nn.Module):
    """Siamese Network for face similarity detection"""
    
    def __init__(self):
        super(SiameseNetwork, self).__init__()
        self.feature_extraction = torch.hub.load(
            "pytorch/vision:v0.10.0", "resnet18", pretrained=True
        )
        self.fc1 = nn.Linear(1000, 512)
        self.fc2 = nn.Linear(512, 256)
        self.dropout = nn.Dropout(p=0.3)
        self.out = nn.Linear(256, 1)

    def forward_once(self, x):
        """Extract features from one image"""
        return self.feature_extraction(x)

    def forward(self, x1, x2):
        """Compare two images and return similarity score"""
        out1 = self.forward_once(x1)
        out2 = self.forward_once(x2)
        diff = torch.abs(out1 - out2)
        x = F.relu(self.fc1(diff))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.dropout(x)
        out = torch.sigmoid(self.out(x))
        return out


# Image preprocessing transform
transform = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor()
])

# Global model instance
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = None


def load_siamese_model():
    """Load the Siamese network model (lazy loading)"""
    global model
    if model is None:
        try:
            model = SiameseNetwork().to(device)
            model_path = os.path.join(os.path.dirname(__file__), '..', 'best_siamese_model.pth')
            if os.path.exists(model_path):
                model.load_state_dict(torch.load(model_path, map_location=device))
                model.eval()
                logger.info("Siamese model loaded successfully")
            else:
                logger.warning(f"Model file not found at {model_path}. Face duplicate detection will be skipped.")
                model = None
        except Exception as e:
            logger.error(f"Error loading Siamese model: {e}")
            model = None
    return model


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
    
    Args:
        uploaded_photo_path: Path to the uploaded photo
        
    Returns:
        tuple: (is_duplicate: bool, matched_username: str or None)
    """
    from haunted_profiles.models import User
    
    # Load model
    model = load_siamese_model()
    if model is None:
        logger.warning("Siamese model not available. Skipping duplicate face check.")
        return False, None
    
    try:
        # Load and preprocess uploaded image
        uploaded_img = transform(Image.open(uploaded_photo_path).convert("RGB")).unsqueeze(0).to(device)
        
        # Get all verified users with verification photos
        existing_users = User.objects.filter(is_verified=True).exclude(verification_photo='')
        
        with torch.no_grad():
            for user in existing_users:
                try:
                    existing_img_path = user.verification_photo.path
                    existing_img = transform(Image.open(existing_img_path).convert("RGB")).unsqueeze(0).to(device)
                    
                    # Calculate similarity score
                    similarity_score = model(uploaded_img, existing_img).item()
                    
                    logger.info(f"Similarity with {user.username}: {similarity_score}")
                    
                    # If similarity > 0.9, consider it a duplicate
                    if similarity_score > 0.9:
                        logger.warning(f"Duplicate face detected! Matches user: {user.username}")
                        return True, user.username
                        
                except Exception as e:
                    logger.error(f"Error comparing with user {user.username}: {e}")
                    continue
        
        return False, None
        
    except Exception as e:
        logger.error(f"Error in duplicate face detection: {e}")
        return False, None
