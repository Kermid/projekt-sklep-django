from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout , authenticate
from django.contrib import messages
from .models import Product, OrderItem, Order
from django.views.decorators.http import require_POST
from .cart import Cart
from django.db.models import Q
from django.contrib.auth.decorators import login_required

def product_list(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'Sklep/Panel_glowny.html', {'products': products})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('Panel_glowny')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Witaj {username}! Zostałeś zalogowany.")
                return redirect('Panel_glowny')
            else:
                messages.error(request, "Nieprawidłowy login lub hasło.")
        else:
            messages.error(request, "Błędne dane logowania.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.info(request, "Wylogowano pomyślnie.")
    return redirect('Panel_glowny')

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    # dodanie 1 sztuki
    cart.add(product=product, quantity=1)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})

def product_list(request):
    query = request.GET.get('q') # pobiera frazę z paska wyszukiwania
    products = Product.objects.filter(is_active=True)

    if query:
        # filtrowanie szuka w nazwie lub opisie
        products = products.filter(
            Q(name__icontains=query) | Q(category__name__icontains=query)
        )

    return render(request, 'Sklep/Panel_glowny.html', {'products': products})

@login_required
def user_orders(request):
    #pobiera zamówienia zalogowanego użytkownika 
    orders = Order.objects.filter(user=request.user).order_by('-created_at') 
    return render(request, 'Sklep/user_orders.html', {'orders': orders})

@login_required
def order_create(request):
    cart = Cart(request)
    
    # Zabezpieczenie pusty koszyk
    if len(cart) == 0:
        return redirect('cart_detail')

    if request.method == 'POST':
        #  Tworzymy zamówienie w bazie (przypisane do usera)
        order = Order.objects.create(
            user=request.user,
            shipping_address='Adres domyślny użytkownika', 
            status='paid' #uznajmy ze jest opłacone
        )

        #Produkty z koszyka do bazy danych
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )

        cart.clear()


        return redirect('user_orders')

    return redirect('cart_detail')