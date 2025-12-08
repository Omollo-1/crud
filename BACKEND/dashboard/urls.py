from django.urls import path
from . import views

urlpatterns = [
    path('summary/', views.DashboardSummaryView.as_view(), name='dashboard_summary'),
    path('stats/', views.DashboardStatsView.as_view(), name='dashboard_stats'),
    path('', views.DashboardSummaryView.as_view(), name='dashboard_index'),
]