from django.contrib import admin
from django.contrib.auth.forms import AdminPasswordChangeForm

from .models import *
# Register your models here.

admin.site.register(Auction)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(User)
admin.site.register(Comment)
