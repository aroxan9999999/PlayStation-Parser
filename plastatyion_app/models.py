from django.db import models

class Product(models.Model):
    photo_url = models.URLField(max_length=5000, verbose_name="Image URL")
    product_url = models.URLField(max_length=5000, verbose_name="Product URL")
    name = models.CharField(max_length=555, verbose_name="Product Name")
    current_price = models.DecimalField(max_digits=100, decimal_places=2, verbose_name="Current Price")
    old_price = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True, verbose_name="Old Price")
    discount = models.CharField(max_length=50, null=True, blank=True, verbose_name="Discount")
    offer_end_date = models.DateField(null=True, blank=True, verbose_name="Offer End Date")

    def __str__(self):
        return f"{self.name} ({self.current_price} TL)"

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"