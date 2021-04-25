from crispy_forms.layout import Layout, Submit
from django.core.exceptions import ValidationError
from django.db.utils import ProgrammingError
from django.forms import ModelForm, fields, widgets

from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import StrictButton

from .models import Auction, Bid, Comment


class NewAuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ("title", "description", "image", "starting_bid", "categories")

    def __init__(self, *args, **kwargs):
        action = kwargs.pop("action")
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id_create_auction_form"
        self.helper.form_action = action
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Submit", css_class="col-2 offset-md-10"))
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-2"
        self.helper.field_class = "col-10"



class NewBidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ("value",)

    def __init__(self, *args, **kwargs):
        bid_price = kwargs.pop("bid_price", None)
        action = kwargs.pop("action", None)
        super().__init__(*args, **kwargs)
        # self.fields["value"].attrs.update({"placeholder": bid_price})
        self.helper = FormHelper()
        self.helper.form_id = "id_new_bid_form"
        self.helper.form_action = action
        self.helper.form_method = "post"
        self.helper.form_class = "form-inline"
        # self.helper.label_class = "col-4"
        # self.helper.field_class = "col-8"
        self.helper.layout = Layout(
            "value",
            Submit("submit", "Bid", css_class="btn btn-primary"),
        )

    
    def clean(self):
        print(self.instance)
        if not self.instance:
            raise ProgrammingError("There is no instance with this form")
        if self.cleaned_data["value"] <= self.instance.auction.highest_bid_value:
            raise ValidationError("Bid value is lower then the highest bid value")
        if self.instance.bidder == self.instance.auction.owner:
            raise ValidationError("You can't bid on your own auction")

        return super().clean()


class NewCommentFrom(ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)

    def __init__(self, *args, **kwargs):
        action = kwargs.pop("action", None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id_new_comment_form"
        self.helper.form_action = action
        self.helper.form_method = "post"

        self.helper.layout = Layout(
            "content",
            Submit("submit", "Comment", css_class="btn btn-primary"),
        )
