from django.contrib import admin

# Register your models here.
from .models import Category, Item, Profile, Cart,ItemReview

admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(ItemReview)


class ItemReviewInline(admin.TabularInline):
    model = ItemReview
    extra = 0

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'average_rating')
    inlines = [ItemReviewInline]

admin.site.register(Item, ItemAdmin)


