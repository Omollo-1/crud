from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProgramListView.as_view(), name='program_list'),
    path('<int:pk>/', views.ProgramDetailView.as_view(), name='program_detail'),
    path('slug/<slug:slug>/', views.ProgramBySlugView.as_view(), name='program_by_slug'),
    path('summary/', views.ProgramSummaryView.as_view(), name='program_summary'),
    path('categories/', views.ProgramCategoryListView.as_view(), name='program_categories'),
    path('<int:program_id>/updates/', views.ProgramUpdateListView.as_view(), name='program_updates'),
    path('<int:program_id>/beneficiaries/', views.ProgramBeneficiaryListView.as_view(), name='program_beneficiaries'),
]