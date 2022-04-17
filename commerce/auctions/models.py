from pyexpat import model
from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Category name")

    class Meta:
        verbose_name_plural = "Categories"
        verbose_name = "Category"
    
    def __str__(self):
        return self.name
        

class Listing(models.Model):
    title = models.CharField(max_length=200, verbose_name="Name")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    description = models.TextField(verbose_name="Description")
    starting_bid = models.IntegerField(verbose_name="Starting bid (euro)")
    image = models.ImageField(upload_to="upload/", blank=True, verbose_name="Image")
    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True)


class Bid(models.Model):
    value = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    text = models.TextField()
