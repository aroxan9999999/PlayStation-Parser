from django.shortcuts import render
from django.http import HttpResponse
import csv
import json
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def download_csv(request):
    products = Product.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Photo URL', 'Product URL', 'Current Price', 'Old Price', 'Discount', 'Offer End Date'])
    for product in products:
        writer.writerow([product.name, product.photo_url, product.product_url, product.current_price, product.old_price, product.discount, product.offer_end_date])

    return response

def download_json(request):
    products = Product.objects.all()
    data = []
    for product in products:
        data.append({
            'name': product.name,
            'photo_url': product.photo_url,
            'product_url': product.product_url,
            'current_price': str(product.current_price),
            'old_price': str(product.old_price) if product.old_price else None,
            'discount': product.discount,
            'offer_end_date': product.offer_end_date.strftime('%Y-%m-%d') if product.offer_end_date else None
        })

    response = HttpResponse(json.dumps(data, indent=4), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="products.json"'

    return response
