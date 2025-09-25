# store/context_processors.py
from types import SimpleNamespace
from .models import Cart

def cart_context(request):
    # If you require login to use cart, return empty for anonymous users
    if not request.user.is_authenticated:
        empty = SimpleNamespace(items=[], total_items=0, total_price=0)
        return {'cart': empty}

    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product').all()
    total_items = sum(i.quantity for i in items)
    total_price = sum(i.quantity * float(i.product.price) for i in items)

    # attach attrs so partial templates can use same API
    cart.total_items = total_items
    cart.total_price = total_price
    return {'cart': cart}
