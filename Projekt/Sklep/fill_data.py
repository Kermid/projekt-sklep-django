import random
from decimal import Decimal
from django.contrib.auth.models import User
# Zakładam, że Twoja aplikacja nazywa się 'Sklep' (tak widziałem w logach)
# Jeśli nazywa się inaczej, zmień 'Sklep' w poniższej linii:
from Sklep.models import Category, Tag, Product, Order, OrderItem

print("--- Rozpoczynam generowanie danych ---")

# 1. Tworzenie Kategorii
kategorie_nazwy = ['Elektronika', 'Ubrania', 'Dom i Ogród', 'Sport']
lista_kategorii = []

for nazwa in kategorie_nazwy:
    # get_or_create zapobiega błędom, jeśli uruchomisz skrypt 2 razy
    kat, created = Category.objects.get_or_create(
        name=nazwa, 
        defaults={'slug': nazwa.lower().replace(' ', '-')}
    )
    lista_kategorii.append(kat)
    if created:
        print(f"Dodano kategorię: {nazwa}")

# 2. Tworzenie Tagów
tagi_nazwy = ['Nowość', 'Promocja', 'Wyprzedaż', 'Bestseller']
lista_tagow = []

for nazwa in tagi_nazwy:
    tag, created = Tag.objects.get_or_create(
        name=nazwa,
        defaults={'slug': nazwa.lower()}
    )
    lista_tagow.append(tag)

# 3. Tworzenie Produktów
for i in range(1, 16): # Tworzymy 15 produktów
    kategoria = random.choice(lista_kategorii)
    cena = Decimal(random.randint(20, 500)) + Decimal('0.99')
    
    prod = Product.objects.create(
        category=kategoria,
        name=f"Produkt {kategoria.name} nr {i}",
        price=cena,
        stock_quantity=random.randint(0, 100),
        is_active=True
    )
    
    # Dodawanie losowych tagów (relacja ManyToMany wymaga .add())
    wylosowany_tag = random.choice(lista_tagow)
    prod.tags.add(wylosowany_tag)
    
    print(f"Stworzono: {prod.name} ({prod.price} PLN)")

# 4. Tworzenie Przykładowego Zamówienia (dla admina)
admin_user = User.objects.filter(username='admin').first()

if admin_user:
    # Tworzymy zamówienie
    zamowienie = Order.objects.create(
        user=admin_user,
        status='pending',
        shipping_address='ul. Testowa 1, 00-001 Warszawa'
    )
    
    # Dodajemy produkty do zamówienia (pobieramy 2 ostatnie produkty)
    ostatnie_produkty = Product.objects.all().order_by('-id')[:2]
    
    for p in ostatnie_produkty:
        OrderItem.objects.create(
            order=zamowienie,
            product=p,
            quantity=2,
            price=p.price # Cena w momencie zakupu
        )
    print(f"Stworzono przykładowe zamówienie dla użytkownika: {admin_user.username}")
else:
    print("Nie znaleziono użytkownika 'admin', pominięto tworzenie zamówienia.")

print("--- Zakończono sukcesem! ---")