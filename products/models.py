from django.db import models
from profiles.models import UserProfile
from datetime import datetime   
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

class Review(models.Model):
    date = models.DateTimeField(default=datetime.now, blank=True)
    user=models.ForeignKey(UserProfile, on_delete=models.CASCADE)  
    product = models.ForeignKey('Product', null=True, blank=True, on_delete=models.SET_NULL)
    stars=models.IntegerField()
    comment=models.CharField(max_length=512, null=True, blank=True)

class Comments(models.Model):
    date = models.DateTimeField(default=datetime.now, blank=True)
    user=models.ForeignKey(UserProfile, on_delete=models.CASCADE)        
    product = models.ForeignKey('Product', null=True, blank=True, on_delete=models.SET_NULL)
    comment=models.TextField(blank=False)


class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    reviews = models.TextField()
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name