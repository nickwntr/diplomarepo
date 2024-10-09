from django.db import models
from django.db.models import Model
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.


class ProdModel(models.Model):
    brand = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True,upload_to='products/')
    desc = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.brand} {self.name}"

class SiteUser(models.Model):
    UserName = models.CharField(max_length=255,unique=True)
    EMail = models.CharField(max_length=255)
    Pass = models.CharField(max_length=255)
    isAdmin = models.BooleanField(default=False)
    def __str__(self):
        return self.UserName

class Orders(Model):
    OrderNum = models.IntegerField()
    User = models.ForeignKey(SiteUser,on_delete=models.CASCADE)
    Bought = models.ForeignKey(ProdModel,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return self.OrderNum

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(ProdModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MaxValueValidator(100),MinValueValidator(1)])

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def total_price(self):
        return self.quantity * self.product.price



