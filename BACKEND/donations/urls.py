from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'donations', views.DonationViewSet, basename='donation')
router.register(r'donors', views.DonorViewSet, basename='donor')
router.register(r'campaigns', views.CampaignViewSet, basename='campaign')

urlpatterns = [
    path('', include(router.urls)),
    # Custom views that don't fit into the router can remain as specific paths if needed, 
    # but based on views.py, most are covered or can be actions.
    # Dashboard stats is a GenericAPIView, so it needs a specific path:
    path('dashboard/stats/', views.DashboardStatsView.as_view(), name='dashboard_stats'),
]