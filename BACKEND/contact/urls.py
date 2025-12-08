from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.ContactMessageListView.as_view(), name='contact_messages'),
    path('messages/<int:pk>/', views.ContactMessageDetailView.as_view(), name='contact_message_detail'),
    path('messages/<int:pk>/reply/', views.ReplyContactMessageView.as_view(), name='reply_contact_message'),
    path('newsletter/subscribe/', views.NewsletterSubscribeView.as_view(), name='newsletter_subscribe'),
    path('newsletter/unsubscribe/', views.NewsletterUnsubscribeView.as_view(), name='newsletter_unsubscribe'),
    path('newsletter/subscribers/', views.NewsletterSubscriberListView.as_view(), name='newsletter_subscribers'),
    path('configuration/', views.SiteConfigurationView.as_view(), name='site_configuration'),
    path('summary/', views.ContactSummaryView.as_view(), name='contact_summary'),
]