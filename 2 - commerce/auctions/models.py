from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    def __str__(self):
        return self.name



class Item(models.Model):
    id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=64)
    item_description = models.CharField(max_length=4000)
    min_bid = models.FloatField(default=1.0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_owner")
    image = models.URLField(max_length=200)
    categories = models.ManyToManyField(Category)
    users_watching = models.ManyToManyField(User, related_name="user_watchlist", blank=True)
    is_active = models.BooleanField(verbose_name="Item active", default=True)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.id}) Item {self.item_name} onwed by {self.owner} Categories: {self.categories}"

    def max_bid(self):
        bids = Bid.objects.filter(item_id=self.id)

        if len(bids) is 0:
            return self.min_bid

        max_bid: int = 0

        for bid in bids:
            if bid.ammount > max_bid:
                max_bid = bid.ammount

        return max_bid

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    bidder = models.ForeignKey(User,  null=False, on_delete=models.CASCADE)
    item = models.ForeignKey(Item,  null=False, on_delete=models.CASCADE)
    ammount = models.FloatField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}: {self.bidder} bid {self.ammount} for {self.item}"

    def get_user(self):
        return self.bidder

class Comment (models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, null=False, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=4000)

    def __str__(self):
        return f"{self.user} on {self.date} in {self.item}"

