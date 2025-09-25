from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from .forms import SignupForm, LoginForm
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.http import JsonResponse
from .models import Product
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem
from .models import Cart, CartItem, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .models import Contact

def home(request):
    return render(request, 'index.html')

User = get_user_model()

def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)  # password ko hash karna zaroori hai
        )
        login(request, user)
        return redirect('product_list')
    return render(request, 'signup.html')
# Login
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# Logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Profile
@login_required
def profile_view(request):
    return render(request, "profile.html", {"user": request.user})

def product_list(request):
    category_slug = request.GET.get('category', None)
    current_category = None

    if category_slug and category_slug != 'all':
        products = Product.objects.filter(category__slug=category_slug)
        current_category = category_slug
    else:
        products = Product.objects.all()

    categories = Category.objects.all()

    return render(request, 'index.html', {
        'products': products,
        'categories': categories,
        'current_category': current_category,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    images = product.images.all()  # multiple images
    return render(request, "product_detail.html", {
        "product": product,
        "images": images
    })

def api_products(request):
    products = Product.objects.prefetch_related('images').all()
    data = []
    for p in products:
        data.append({
            'id': p.id,
            'name': p.name,
            'price': str(p.price),
            'category': p.category.name if p.category else '',
            'image': p.get_first_image(),
        })
    return JsonResponse(data, safe=False)

@login_required
def add_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += 1
        cart_item.save()

        return JsonResponse({
            "cart_count": sum(item.quantity for item in cart.items.all()),
            "product_quantity": cart_item.quantity
        })

    return JsonResponse({"error": "Invalid request"}, status=400)



@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {
        'cart': cart,
        'cart_items': cart.items.all(),
    }
    return render(request, 'cart_details.html', context)


@login_required
def update_cart_item(request, item_id):
    if request.method == "POST":
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart_details')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart_details')

@login_required
def cart_details(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, "cart_details.html", {"cart": cart})


def checkout(request):
    # yahan tum cart ka data fetch kar ke template ko bhej sakte ho
    cart = None
    if request.user.is_authenticated:
        cart = getattr(request.user, 'cart', None)

    return render(request, 'checkout.html', {'cart': cart})

def confirm_order(request):
    if request.method == "POST":
        # User ka cart lo
        cart = get_object_or_404(Cart, user=request.user)

        # Order banao
        order = Order.objects.create(
            user=request.user,
            total_price=cart.total_price(),
            payment_method=request.POST.get('payment_method', 'cod')  # optional
        )

        # Cart ke items ko Order me shift karo
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price  # price at order time
            )

        # Cart empty kar do
        cart.items.all().delete()

        # Redirect to confirmation page
        return redirect('order_confirmed', order_id=order.id)



def order_confirmed(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_confirmed.html', {'order': order})

def get_user_cart(request):
    if not request.user.is_authenticated:
        return None
    cart, _ = Cart.objects.get_or_create(user=request.user)
    # compute properties used in templates
    items = cart.items.select_related('product').all()
    cart.total_items = sum(i.quantity for i in items)
    cart.total_price = sum(i.quantity * i.product.price for i in items)
    return cart

def contact(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        Contact.objects.create(name=name, email=email, message=message)

        return JsonResponse({'message': 'Your message has been sent successfully!'})
    return render(request, 'index.html')