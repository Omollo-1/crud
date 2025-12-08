from django.test import TestCase

# Create your tests here.
# donations/tests.py
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Donation

class DonationTestCase(APITestCase):
    def setUp(self):
        self.donation_data = {
            'donor_name': 'Test Donor',
            'donor_email': 'test@example.com',
            'amount': 100.00,
            'payment_method': 'credit_card',
            'donation_type': 'one_time'
        }
    
    def test_create_donation(self):
        response = self.client.post('/api/donations/', self.donation_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Donation.objects.count(), 1)
        self.assertEqual(Donation.objects.get().donor_name, 'Test Donor')