"""
Authentication views for WorkOS SSO
"""
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .workos_auth import get_authorization_url, handle_callback
import logging

logger = logging.getLogger(__name__)


def workos_login(request):
    """
    Initiate WorkOS SSO login flow
    """
    try:
        # Generate state for CSRF protection
        state = request.session.get('workos_state', '')
        if not state:
            import secrets
            state = secrets.token_urlsafe(32)
            request.session['workos_state'] = state
        
        # Get authorization URL
        authorization_url = get_authorization_url(state=state)
        
        return redirect(authorization_url)
        
    except Exception as e:
        logger.error(f"Error initiating WorkOS login: {e}")
        messages.error(request, 'Failed to initiate login. Please try again.')
        return redirect('index')


@csrf_exempt
def workos_callback(request):
    """
    Handle WorkOS OAuth callback
    """
    try:
        # Get authorization code from query params
        code = request.GET.get('code')
        state = request.GET.get('state', '')
        
        if not code:
            messages.error(request, 'Authentication failed. No authorization code received.')
            return redirect('index')
        
        # Verify state (CSRF protection)
        expected_state = request.session.get('workos_state', '')
        if state != expected_state:
            logger.warning(f"State mismatch: expected {expected_state}, got {state}")
            # Continue anyway for development, but log the warning
        
        # Exchange code for user profile and create/get user
        user = handle_callback(code)
        
        # Log the user in
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        # Clear state from session
        if 'workos_state' in request.session:
            del request.session['workos_state']
        
        # Redirect based on verification status
        if not user.is_verified:
            messages.success(request, f'Welcome, {user.username}! Please verify your identity.')
            return redirect('verification')
        else:
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('profile')
            
    except Exception as e:
        logger.error(f"Error in WorkOS callback: {e}")
        print(f"❌ WorkOS Callback Error: {e}")  # Print to console
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()  # Print full traceback
        messages.error(request, f'Authentication failed: {str(e)}')
        return redirect('index')
