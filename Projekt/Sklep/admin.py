
from django.contrib import admin
from .models import Category, Tag, Product, Order, OrderItem

admin.site.register(Category)
admin.site.register(Tag)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock_quantity']
    list_filter = ['category', 'tags']
    search_fields = ['name', 'category__name', 'tags__name']

    def display_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    display_tags.short_description = 'Tagi'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  
    autocomplete_fields = ['product'] 
    fields = ['product', 'quantity', 'price', 'line_total']
    readonly_fields = ['line_total'] 

    def line_total(self, instance):
        if instance.pk:
            return f"{instance.get_cost()} PLN"
        return "-"
    line_total.short_description = "Suma"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'created_at', 'order_total']
    list_filter = ['status', 'created_at']
    inlines = [OrderItemInline]
    search_fields = ['user__username', 'id']
    
    
    inlines = [OrderItemInline]
    
    autocomplete_fields = ['user']

    def order_total(self, obj):
        
        return f"{obj.get_total_cost()} PLN"
    order_total.short_description = "Wartość zamówienia"