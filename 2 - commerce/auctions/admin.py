from django.contrib import admin
from .models import Bid, Comment, Item, User, Category
# Register your models here.

admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Item)
admin.site.register(User)
admin.site.register(Category)
