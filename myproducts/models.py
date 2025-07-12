from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    productid = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    stock = models.CharField(max_length=100)
    sales = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/',blank=True,null=True)