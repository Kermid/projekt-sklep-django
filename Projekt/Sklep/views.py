from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout , authenticate
from django.contrib import messages
from .models import Product

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
    return render(request, 'Rejestracja/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Sprawdzenie czy użytkownik istnieje w MySQL
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Witaj {username}! Zostałeś zalogowany.")
                return redirect('product_list') # Przekierowanie na stronę główną
            else:
                messages.error(request, "Nieprawidłowy login lub hasło.")
        else:
            messages.error(request, "Błędne dane logowania.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'shop/login.html', {'login_form': form})

def logout_user(request):
    logout(request)
    messages.info(request, "Wylogowano pomyślnie.")
    return redirect('product_list')