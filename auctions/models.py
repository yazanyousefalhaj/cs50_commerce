from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField("Auction", related_name="intrested_buyers",blank=True)


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name



class Auction(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    starting_bid = models.DecimalField(decimal_places=2, max_digits=20)
    image = models.URLField(null=True)
    categories = models.ManyToManyField(Category, related_name="auctions")
    is_active = models.BooleanField(default=True)
    is_closed = models.BooleanField(default=False)
    winner = models.ForeignKey(User, related_name="winnings",null=True, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.title} for {self.owner}"

    @property
    def highest_bid(self):
        if self.bids.all():
            return max([bid for bid in self.bids.all()], key=lambda bid: bid.value)
        else:
            return None

    
    @property
    def highest_bid_value(self):
        return self.highest_bid.value if self.highest_bid else self.starting_bid


    def close(self):
        if self.highest_bid:
            self.winner = self.highest_bid.bidder
        self.is_closed = True
        self.save()


class Bid(models.Model):
    value = models.DecimalField(decimal_places=2, max_digits=20)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")

    def __str__(self) -> str:
        return f"{self.bidder} bid {self.value} on [{self.auction}]"


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, related_name="comments", on_delete=models.CASCADE)