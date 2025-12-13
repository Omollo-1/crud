"""
URL configuration for BACKEND project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from donations.views import DonationViewSet, DonorViewSet, CampaignViewSet, DashboardStatsView
from payments.views import PaymentViewSet, mpesa_callback


def api_root(request):
    """API root endpoint showing available endpoints"""
    return JsonResponse({
        'message': 'Welcome to Charitize API',
        'endpoints': {
            'admin': '/admin/',
            'api': '/api/',
            'donations': '/api/donations/',
            'donors': '/api/donors/',
            'campaigns': '/api/campaigns/',
            'volunteers': '/api/volunteers/',
            'contact': '/api/contact/',
            'users': '/api/users/',
            'auth': {
                'login': '/api/users/login/',
                'register': '/api/users/register/',
                'social_login': '/accounts/<provider>/login/',
            },
            'payments': {
                'stk_push': '/api/payments/stk-push/',
                'status': '/api/payments/status/<checkout_id>/',
            },
            'dashboard': '/api/dashboard/stats/',
        }
    })


router = DefaultRouter()
router.register(r'donations', DonationViewSet)
router.register(r'donors', DonorViewSet)
router.register(r'campaigns', CampaignViewSet)
router.register(r'payments', PaymentViewSet, basename='payments')

urlpatterns = [
    path('', api_root, name='api-root'),  # Root URL showing API endpoints
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')),
    path('api/contact/', include('contact.urls')),
    path('api/volunteers/', include('volunteers.urls')),
    path('api/users/', include('users.urls')),
    path('api/dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('api/payments/callback/', mpesa_callback, name='mpesa-callback'),
    path('api/payments/stk-push/', PaymentViewSet.as_view({'post': 'initiate_stk_push'}), name='stk-push'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)