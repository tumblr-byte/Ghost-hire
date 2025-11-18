"""
WorkOS Authentication Helper for Ghost Hire
"""
from workos import WorkOSClient
from django.conf import settings
from django.contrib.auth import get_user_model
import random
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

# Initialize WorkOS client
workos_client = WorkOSClient(
    api_key=settings.WORKOS_API_KEY,
    client_id=settings.WORKOS_CLIENT_ID,
)


def get_authorization_url(state=None):
    """
    Generate WorkOS authorization URL for Google OAuth
    
    Args:
        state: Optional state parameter for CSRF protection
        
    Returns:
        str: Authorization URL to redirect user to
    """
    # Use WorkOS SSO with Google OAuth provider
    authorization_url = workos_client.sso.get_authorization_url(
        provider='GoogleOAuth',
        redirect_uri=settings.WORKOS_REDIRECT_URI,
        state=state or '',
    )
    
    return authorization_url


def handle_callback(code):
    """
    Handle WorkOS OAuth callback and create/retrieve user
    
    Args:
        code: Authorization code from WorkOS callback
        
    Returns:
        User: Django user object
    """
    try:
        # Exchange code for profile using WorkOS SSO
        profile_and_token = workos_client.sso.get_profile_and_token(code)
        
        # Extract profile data
        profile = profile_and_token.profile
        
        # Extract user info
        workos_id = profile.id
        email = profile.email
        first_name = profile.first_name or ''
        last_name = profile.last_name or ''
        
        if not workos_id or not email:
            raise Exception("Missing user ID or email from WorkOS response")
        
        # Try to find existing user by workos_id (stored in google_id field)
        user = User.objects.filter(google_id=workos_id).first()
        
        if not user:
            # Try to find by email
            user = User.objects.filter(email=email).first()
            
            if user:
                # Update existing user with WorkOS ID
                user.google_id = workos_id
                user.save()
            else:
                # Create new user
                username = generate_unique_username()
                user = User.objects.create(
                    email=email,
                    username=username,
                    google_id=workos_id,
                )
                logger.info(f"Created new user: {username} with WorkOS ID: {workos_id}")
        
        return user
        
    except Exception as e:
        logger.error(f"Error handling WorkOS callback: {e}")
        print(f"❌ WorkOS Auth Error: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        raise


def generate_unique_username():
    """Generate a unique username in format ghost_XXXXX"""
    max_attempts = 10
    for _ in range(max_attempts):
        username = f"ghost_{random.randint(10000, 99999)}"
        if not User.objects.filter(username=username).exists():
            return username
    
    # Fallback: use timestamp if all random attempts fail
    import time
    return f"ghost_{int(time.time()) % 100000}"
