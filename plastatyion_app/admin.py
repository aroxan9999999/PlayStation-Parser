from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'current_price', 'old_price', 'discount', 'offer_end_date')
    list_filter = ('discount', 'offer_end_date')
    search_fields = ('name', 'product_url')
    ordering = ('-current_price',)
