from django.contrib import admin

# Register your models here.
from .models import Category, Item, Profile, Cart

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Profile)
admin.site.register(Cart)