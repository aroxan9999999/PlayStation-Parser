# Generated by Django 5.1.4 on 2024-12-23 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plastatyion_app', '0002_alter_product_offer_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='offer_end_date',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Discount'),
        ),
    ]