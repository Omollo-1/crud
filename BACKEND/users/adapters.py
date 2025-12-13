from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        """Redirect to frontend after login"""
        return settings.LOGIN_REDIRECT_URL if hasattr(settings, 'LOGIN_REDIRECT_URL') else '/'


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_connect_redirect_url(self, request, socialaccount):
        """Redirect to frontend after social account connection"""
        return settings.LOGIN_REDIRECT_URL if hasattr(settings, 'LOGIN_REDIRECT_URL') else '/'
    
    def populate_user(self, request, sociallogin, data):
        """Populate user instance with data from social provider"""
        user = super().populate_user(request, sociallogin, data)
        
        # Extract additional data from provider
        if sociallogin.account.provider == 'google':
            user.first_name = data.get('given_name', '')
            user.last_name = data.get('family_name', '')
        elif sociallogin.account.provider == 'facebook':
            user.first_name = data.get('first_name', '')
            user.last_name = data.get('last_name', '')
        elif sociallogin.account.provider == 'twitter':
            # Twitter provides name as a single field
            name = data.get('name', '').split(' ', 1)
            user.first_name = name[0] if len(name) > 0 else ''
            user.last_name = name[1] if len(name) > 1 else ''
        
        return user
