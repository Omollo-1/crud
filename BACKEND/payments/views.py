import requests
import base64
from datetime import datetime
from django.conf import settings
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from .models import MpesaPayment
from .serializers import MpesaPaymentSerializer, STKPushRequestSerializer
from donations.models import Donation
import logging

logger = logging.getLogger(__name__)


def get_mpesa_access_token():
    """
    Generate M-Pesa access token using OAuth
    """
    try:
        consumer_key = settings.MPESA_CONFIG['CONSUMER_KEY']
        consumer_secret = settings.MPESA_CONFIG['CONSUMER_SECRET']
        api_url = settings.MPESA_CONFIG.get('AUTH_URL', 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials')
        
        # Create base64 encoded string of consumer_key:consumer_secret
        credentials = f"{consumer_key}:{consumer_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {encoded_credentials}'
        }
        
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        
        json_response = response.json()
        return json_response.get('access_token')
    
    except Exception as e:
        logger.error(f"Error getting M-Pesa access token: {str(e)}")
        return None


def initiate_stk_push(phone_number, amount, account_reference="Donation", transaction_desc="Charitize Donation", donation_id=None):
    """
    Initiate STK Push to customer's phone
    """
    try:
        access_token = get_mpesa_access_token()
        if not access_token:
            return {'success': False, 'message': 'Failed to get access token'}
        
        # M-Pesa API endpoint
        api_url = settings.MPESA_CONFIG.get('STK_PUSH_URL', 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest')
        
        # Get configuration
        business_short_code = settings.MPESA_CONFIG['SHORTCODE']
        passkey = settings.MPESA_CONFIG['PASSKEY']
        callback_url = settings.MPESA_CONFIG['CALLBACK_URL']
        
        # Generate timestamp
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        
        # Generate password (Base64 encoded: Shortcode + Passkey + Timestamp)
        password_str = f"{business_short_code}{passkey}{timestamp}"
        password = base64.b64encode(password_str.encode()).decode()
        
        # Prepare request payload
        payload = {
            "BusinessShortCode": business_short_code,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),  # M-Pesa expects integer
            "PartyA": phone_number,  # Customer phone number
            "PartyB": business_short_code,
            "PhoneNumber": phone_number,
            "CallBackURL": callback_url,
            "AccountReference": account_reference,
            "TransactionDesc": transaction_desc
        }
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Make request
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        
        json_response = response.json()
        
        # Check if request was successful
        if json_response.get('ResponseCode') == '0':
            # Create payment record
            donation = None
            if donation_id:
                try:
                    donation = Donation.objects.get(id=donation_id)
                except Donation.DoesNotExist:
                    pass
            
            payment = MpesaPayment.objects.create(
                merchant_request_id=json_response.get('MerchantRequestID'),
                checkout_request_id=json_response.get('CheckoutRequestID'),
                phone_number=phone_number,
                amount=amount,
                account_reference=account_reference,
                transaction_desc=transaction_desc,
                status='pending',
                donation=donation
            )
            
            return {
                'success': True,
                'message': json_response.get('CustomerMessage', 'STK Push sent successfully'),
                'checkout_request_id': json_response.get('CheckoutRequestID'),
                'merchant_request_id': json_response.get('MerchantRequestID'),
                'payment_id': payment.id
            }
        else:
            return {
                'success': False,
                'message': json_response.get('errorMessage', 'Failed to initiate payment'),
                'response': json_response
            }
    
    except requests.exceptions.RequestException as e:
        logger.error(f"M-Pesa API request error: {str(e)}")
        return {'success': False, 'message': f'Network error: {str(e)}'}
    except Exception as e:
        logger.error(f"Error initiating STK push: {str(e)}")
        return {'success': False, 'message': f'Error: {str(e)}'}


class PaymentViewSet(viewsets.ViewSet):
    """
    ViewSet for M-Pesa payment operations
    """
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['post'])
    def initiate_stk_push(self, request):
        """
        Initiate STK Push payment
        POST /api/payments/stk-push/
        """
        serializer = STKPushRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'success': False, 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        validated_data = serializer.validated_data
        
        result = initiate_stk_push(
            phone_number=validated_data['phone_number'],
            amount=validated_data['amount'],
            account_reference=validated_data.get('account_reference', 'Donation'),
            transaction_desc=validated_data.get('transaction_desc', 'Charitize Donation'),
            donation_id=validated_data.get('donation_id')
        )
        
        if result['success']:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='status/(?P<checkout_id>[^/.]+)')
    def check_status(self, request, checkout_id=None):
        """
        Check payment status
        GET /api/payments/status/<checkout_request_id>/
        """
        try:
            payment = MpesaPayment.objects.get(checkout_request_id=checkout_id)
            serializer = MpesaPaymentSerializer(payment)
            return Response({
                'success': True,
                'payment': serializer.data
            })
        except MpesaPayment.DoesNotExist:
            return Response(
                {'success': False, 'message': 'Payment not found'},
                status=status.HTTP_404_NOT_FOUND
            )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def mpesa_callback(request):
    """
    Handle M-Pesa payment callback
    POST /api/payments/callback/
    """
    try:
        # Log the callback data
        logger.info(f"M-Pesa Callback received: {request.data}")
        
        # Extract callback data
        callback_data = request.data
        
        # Get the Body from the callback
        body = callback_data.get('Body', {})
        stk_callback = body.get('stkCallback', {})
        
        # Extract key information
        merchant_request_id = stk_callback.get('MerchantRequestID')
        checkout_request_id = stk_callback.get('CheckoutRequestID')
        result_code = stk_callback.get('ResultCode')
        result_desc = stk_callback.get('ResultDesc')
        
        # Find the payment record
        try:
            payment = MpesaPayment.objects.get(checkout_request_id=checkout_request_id)
        except MpesaPayment.DoesNotExist:
            logger.error(f"Payment not found for CheckoutRequestID: {checkout_request_id}")
            return Response({'ResultCode': 0, 'ResultDesc': 'Accepted'})
        
        # Update payment status
        payment.result_code = str(result_code)
        payment.result_desc = result_desc
        
        if result_code == 0:
            # Payment successful
            payment.status = 'completed'
            
            # Extract callback metadata
            callback_metadata = stk_callback.get('CallbackMetadata', {})
            items = callback_metadata.get('Item', [])
            
            for item in items:
                if item.get('Name') == 'MpesaReceiptNumber':
                    payment.mpesa_receipt_number = item.get('Value')
                elif item.get('Name') == 'TransactionDate':
                    # Convert timestamp to datetime
                    timestamp = str(item.get('Value'))
                    payment.transaction_date = datetime.strptime(timestamp, '%Y%m%d%H%M%S')
            
            # Update linked donation if exists
            if payment.donation:
                payment.donation.status = 'completed'
                payment.donation.save()
        else:
            # Payment failed
            payment.status = 'failed'
            
            # Update linked donation if exists
            if payment.donation:
                payment.donation.status = 'failed'
                payment.donation.save()
        
        payment.save()
        
        logger.info(f"Payment {checkout_request_id} updated: {payment.status}")
        
        # Respond to M-Pesa
        return Response({
            'ResultCode': 0,
            'ResultDesc': 'Accepted'
        })
    
    except Exception as e:
        logger.error(f"Error processing M-Pesa callback: {str(e)}")
        return Response({
            'ResultCode': 1,
            'ResultDesc': 'Failed'
        })
