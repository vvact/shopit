from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import PaymentCreateSerializer
from .models import Payment

class CODPaymentView(APIView):
    permission_classes = [permissions.AllowAny]  # You can restrict to authenticated later

    def post(self, request):
        serializer = PaymentCreateSerializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save(status='pending')  # COD always starts as pending
            return Response({'message': 'COD payment created successfully.', 'payment_id': payment.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

