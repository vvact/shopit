from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import AllowPostAnyUser


class OrderCreateView(APIView):
    permission_classes = [AllowPostAnyUser]

    def post(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderListView(ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        request = self.request
        user = request.user if request.user.is_authenticated else None
        session_key = request.session.session_key

        if user:
            return Order.objects.filter(user=user).order_by('-created_at')
        return Order.objects.filter(session_key=session_key).order_by('-created_at')


class OrderDetailView(RetrieveAPIView):
    serializer_class = OrderSerializer
    lookup_field = 'id'

    def get_queryset(self):
        request = self.request
        user = request.user if request.user.is_authenticated else None
        session_key = request.session.session_key

        if user:
            return Order.objects.filter(user=user)
        return Order.objects.filter(session_key=session_key)
