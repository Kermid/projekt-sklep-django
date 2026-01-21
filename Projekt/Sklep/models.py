from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, F

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)


    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    tags = models.ManyToManyField(Tag, related_name='products')
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    
    def __str__(self):
        tags_str = ", ".join([tag.name for tag in self.tags.all()])
        return f"{self.name} [{self.category.name}] ({tags_str}) - {self.price} PLN"

class Order(models.Model):
    STATUS_CHOICES = [('pending', 'Oczekujące'), ('paid', 'Opłacone'), ('shipped', 'Wysłane')]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    shipping_address = models.TextField()

    def get_total_cost(self):
        total = self.items.aggregate(
            total=Sum(F('price') * F('quantity'))
        )['total']
        return total if total else 0.00
    
    def __str__(self):
        return f"Zamówienie {self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        if not self.price and self.product:
            self.price = self.product.price
        super().save(*args, **kwargs)
        
    def get_cost(self):
        return self.price * self.quantity