import random
from decimal import Decimal
from django.contrib.auth.models import User
from Sklep.models import Category, Tag, Product, Order, OrderItem

print("--- Rozpoczynam generowanie danych ---")


kategorie_nazwy = ['Elektronika', 'Ubrania', 'Dom i Ogród', 'Sport']
lista_kategorii = []

for nazwa in kategorie_nazwy:
 
    kat, created = Category.objects.get_or_create(
        name=nazwa, 
        defaults={'slug': nazwa.lower().replace(' ', '-')}
    )
    lista_kategorii.append(kat)
    if created:
        print(f"Dodano kategorię: {nazwa}")


tagi_nazwy = ['Nowość', 'Promocja', 'Wyprzedaż', 'Bestseller']
lista_tagow = []

for nazwa in tagi_nazwy:
    tag, created = Tag.objects.get_or_create(
        name=nazwa,
        defaults={'slug': nazwa.lower()}
    )
    lista_tagow.append(tag)


for i in range(1, 16): 
    kategoria = random.choice(lista_kategorii)
    cena = Decimal(random.randint(20, 500)) + Decimal('0.99')
    
    prod = Product.objects.create(
        category=kategoria,
        name=f"Produkt {kategoria.name} nr {i}",
        price=cena,
        stock_quantity=random.randint(0, 100),
        is_active=True
    )
    
    
    wylosowany_tag = random.choice(lista_tagow)
    prod.tags.add(wylosowany_tag)
    
    print(f"Stworzono: {prod.name} ({prod.price} PLN)")


admin_user = User.objects.filter(username='admin').first()

if admin_user:
    
    zamowienie = Order.objects.create(
        user=admin_user,
        status='pending',
        shipping_address='ul. Testowa 1, 00-001 Warszawa'
    )
    
    
    ostatnie_produkty = Product.objects.all().order_by('-id')[:2]
    
    for p in ostatnie_produkty:
        OrderItem.objects.create(
            order=zamowienie,
            product=p,
            quantity=2,
            price=p.price 
        )
    print(f"Stworzono przykładowe zamówienie dla użytkownika: {admin_user.username}")
else:
    print("Nie znaleziono użytkownika 'admin', pominięto tworzenie zamówienia.")

print("--- Zakończono sukcesem! ---")