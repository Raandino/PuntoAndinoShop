from django import template
from apps.store.models import Order, OrderProduct, Usuario

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

@register.filter
def coins_count(user):
    if user.is_authenticated:
        usuario = user.usuario
        return usuario.coins
    return 0