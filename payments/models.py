from django.db import models

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('mpesa_stk', 'M-Pesa STK Push'),
        ('mpesa_manual', 'M-Pesa Manual Paybill'),
        ('cash_on_delivery', 'Cash on Delivery'),
        # You can add 'card' later if needed
    )

    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )

    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='payment')
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order.id} - {self.payment_method} - {self.status}"

