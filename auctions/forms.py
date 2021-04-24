from django.core.exceptions import ValidationError
from django.db.utils import ProgrammingError
from django.forms import ModelForm, fields

from .models import Auction, Bid


class NewAuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ("title", "description", "image", "starting_bid", "categories")


class NewBidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ("value",)

    
    def clean(self):
        print(self.instance)
        if not self.instance:
            raise ProgrammingError("There is no instance with this form")
        if self.cleaned_data["value"] <= self.instance.auction.highest_bid_value:
            raise ValidationError("Bid value is lower then the highest bid value")
        if self.instance.bidder == self.instance.auction.owner:
            raise ValidationError("You can't bid on your own auction")

        return super().clean()