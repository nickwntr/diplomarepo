# Generated by Django 4.2.16 on 2024-10-08 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('siteapp', '0002_orders_quantity_alter_orders_ordernum'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Orders',
        ),
    ]