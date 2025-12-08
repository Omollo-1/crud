from django.urls import path
from . import views

urlpatterns = [
    path('', views.DonationListView.as_view(), name='donation_list'),
    path('<int:pk>/', views.DonationDetailView.as_view(), name='donation_detail'),
    path('my-donations/', views.MyDonationsView.as_view(), name='my_donations'),
    path('<int:pk>/update-status/', views.UpdatePaymentStatusView.as_view(), name='update_payment_status'),
    path('summary/', views.DonationSummaryView.as_view(), name='donation_summary'),
    path('recurring/', views.RecurringDonationListView.as_view(), name='recurring_donation_list'),
    path('recurring/<int:pk>/', views.RecurringDonationDetailView.as_view(), name='recurring_donation_detail'),
]