# Generated by Django 4.2.16 on 2024-10-08 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteapp', '0006_siteuser_isadmin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteuser',
            name='UserName',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
