from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name
    
class Bid(models.Model):
    bid = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_bid")

class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    image_url = models.URLField(max_length=1024)
    starting_bid = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bid_price")
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="listings")
    watch_listing = models.ManyToManyField(User, blank=True, null=True, related_name="watch_listing")

    def __str__(self):
        return self.title
    
class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_comment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listing_comment")
    message = models.CharField(max_length=2048)

    def __str__(self):
        return f"{self.author} comment on {self.listing}"
    