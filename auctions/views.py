from django.http.response import HttpResponseBadRequest, HttpResponseForbidden
from auctions.forms import NewAuctionForm, NewBidForm, NewCommentFrom
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Auction, Bid, Category, Comment, User


def index(request):
    return render(
        request,
        "auctions/index.html",
        {"auctions": Auction.objects.filter(is_closed=False)},
    )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_auction(request):
    if request.method == "POST":
        auction = Auction(owner=request.user)
        form = NewAuctionForm(
            request.POST, instance=auction, action=reverse("create_auction")
        )

        if form.is_valid():
            form.save()
            return redirect(reverse("index"))
        else:
            print(form.errors)
    else:
        form = NewAuctionForm(action="create_auction")

    return render(
        request,
        "auctions/create_auction.html",
        {
            "form": form,
        },
    )


def edit_auction(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)
    if auction.owner != request.user:
        return HttpResponseForbidden("You are not allowed to edit this auction")
    form = NewAuctionForm(
        request.POST or None,
        instance=auction,
        action=reverse("edit_auction", kwargs={"auction_id": auction_id}),
    )

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(reverse("auction_index", kwargs={"auction_id": auction_id}))

    return render(
        request,
        "auctions/create_auction.html",
        {
            "form": form,
        },
    )


@login_required
def auction_index(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)
    is_in_watchlist = auction in request.user.watchlist.all()
    form_action = "remove_from_watchlist" if is_in_watchlist else "add_to_watchlist"
    return render(
        request,
        "auctions/auction.html",
        {
            "auction": auction,
            "is_in_watchlist": is_in_watchlist,
            "form_action": reverse(form_action, kwargs={"auction_id": auction_id}),
            "can_close_auction": request.user == auction.owner,
            "bid_form": NewBidForm(
                bid_price=auction.highest_bid_value,
                action=reverse("create_bid", kwargs={"auction_id": auction.id}),
            ),
            "comment_form": NewCommentFrom(action=reverse("create_comment", kwargs={"auction_id": auction.id})),
            "comments": auction.comments.all(),
            "is_winner": auction.winner == request.user,
        },
    )


@login_required
def watchlist(request):
    return render(
        request,
        "auctions/index.html",
        {"auctions": request.user.watchlist.filter(is_closed=False)},
    )


@login_required
def add_to_watchlist(request, auction_id):
    if request.method == "POST":
        auction = get_object_or_404(Auction, pk=auction_id)
        if auction not in request.user.watchlist.all():
            request.user.watchlist.add(auction)
        return redirect(reverse("auction_index", kwargs={"auction_id": auction_id}))
    else:
        return HttpResponseBadRequest("Invalid method used")


@login_required
def remove_from_watchlist(request, auction_id):
    if request.method == "POST":
        auction = get_object_or_404(Auction, pk=auction_id)
        if auction in request.user.watchlist.all():
            request.user.watchlist.remove(auction)
        return redirect(reverse("auction_index", kwargs={"auction_id": auction_id}))
    else:
        return HttpResponseBadRequest("Invalid method used")


@login_required
def close_auction(request, auction_id):
    if request.method == "POST":
        auction = get_object_or_404(Auction, pk=auction_id)
        if auction.owner == request.user:
            auction.close()
            return redirect(reverse("index"))
        else:
            return HttpResponseForbidden("Only auction owner can close this auction")
    else:
        return HttpResponseBadRequest("Invalid method used")


@login_required
def create_bid(request, auction_id):
    if request.method == "POST":
        auction = get_object_or_404(Auction, pk=auction_id)
        bid = Bid(auction=auction, bidder=request.user)
        bid_form = NewBidForm(request.POST, instance=bid)
        if bid_form.is_valid():
            bid_form.save()
            return redirect(reverse("auction_index", kwargs={"auction_id": auction_id}))
        else:
            print(bid_form.errors)
            return redirect(
                reverse(
                    "auction_index",
                    kwargs={
                        "auction_id": auction_id,
                    },
                )
            )
    else:
        return HttpResponseBadRequest("Invalid method used")


@login_required
def create_comment(request, auction_id):
    if request.method == "POST":
        auction = get_object_or_404(Auction, pk=auction_id)
        comment = Comment(auction=auction, author=request.user)
        comment_form = NewCommentFrom(request.POST, instance=comment)
        if comment_form.is_valid():
            comment_form.save()
            return redirect(reverse("auction_index", kwargs={"auction_id": auction_id}))
        else:
            print(comment_form.errors)
            return redirect(
                reverse(
                    "auction_index",
                    kwargs={
                        "auction_id": auction_id,
                    },
                ),
            )
    else:
        return HttpResponseBadRequest("Invalid method used")


def categories(request):
    return render(
        request,
        "auctions/categories.html",
        {
            "categories": Category.objects.all(),
        },
    )


def category_auctions(request, category_id):
    return render(
        request,
        "auctions/index.html",
        {
            "auctions": Auction.objects.filter(
                categories__id=category_id, is_closed=False
            )
        },
    )

