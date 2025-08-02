from orders.models import OrderItem

def user_has_purchased(user, product):
    return OrderItem.objects.filter(
        order__user=user,
        product=product,
        order__status='delivered'  # Assuming this means a completed purchase
    ).exists()
