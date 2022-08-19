from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField(max_length=300)
    price = models.IntegerField()
    qty = models.IntegerField()




