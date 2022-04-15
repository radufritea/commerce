from pyexpat import model
from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Category name")

    class Meta:
        verbose_name_plural = "Categories"
        verbose_name = "Category"
    
    def __str__(self):
        return self.name
        
class Listing(models.Model):
    title = models.CharField(max_length=200, verbose_name="Name")
    description = models.TextField(verbose_name="Description")
    starting_bid = models.IntegerField(verbose_name="Starting bid")
    image = models.ImageField(upload_to="images/", blank=True, verbose_name="Image")
    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
# class Bid(models.Model):
#     pass

# class Comment(models.Model):
#     pass
class User(AbstractUser):
    watchlist = models.ManyToManyField(Listing, blank=True, related_name="watchers")