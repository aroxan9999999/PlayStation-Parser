from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('download/csv/', views.download_csv, name='download_csv'),
    path('download/json/', views.download_json, name='download_json'),
]
