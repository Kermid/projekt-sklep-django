from decimal import Decimal
from django.conf import settings
from .models import Product  # Zakładam, że Twój model produktu nazywa się Product

class Cart:
    def __init__(self, request):
        """Inicjalizacja koszyka."""
        self.session = request.session
        cart = self.session.get('cart_key')
        if not cart:
            # Zapisujemy pusty koszyk w sesji
            cart = self.session['cart_key'] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """Dodawanie produktu do koszyka lub zmiana jego ilości."""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Oznaczenie sesji jako zmodyfikowanej."""
        self.session.modified = True

    def remove(self, product):
        """Usunięcie produktu z koszyka."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Iterowanie po elementach koszyka i pobieranie produktów z bazy."""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def get_total_price(self):
        """Obliczanie całkowitej wartości koszyka."""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Wyczyszczenie koszyka (np. po zakupie)."""
        del self.session['cart_key']
        self.save()

    def __len__(self):
        """Zwracanie liczby pozycji w koszyku."""
        return sum(item['quantity'] for item in self.cart.values())