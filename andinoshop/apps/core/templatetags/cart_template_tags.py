from django import template
from apps.store.models import Order, OrderProduct

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user = user, ordered = False)
        if qs.exists():
            this = qs[0]
            pro = OrderProduct.objects.filter(order = this.pk, save_later = False)
            return pro.count()
    return 0