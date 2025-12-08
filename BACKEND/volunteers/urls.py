from django.urls import path
from . import views

urlpatterns = [
    path('', views.VolunteerListView.as_view(), name='volunteer_list'),
    path('<int:pk>/', views.VolunteerDetailView.as_view(), name='volunteer_detail'),
    path('my-application/', views.MyVolunteerApplicationView.as_view(), name='my_volunteer_application'),
    path('<int:pk>/update-status/', views.UpdateVolunteerStatusView.as_view(), name='update_volunteer_status'),
    path('summary/', views.VolunteerSummaryView.as_view(), name='volunteer_summary'),
    path('assignments/', views.VolunteerAssignmentListView.as_view(), name='volunteer_assignment_list'),
    path('assignments/<int:pk>/', views.VolunteerAssignmentDetailView.as_view(), name='volunteer_assignment_detail'),
]