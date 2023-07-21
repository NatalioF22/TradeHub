from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg

from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name
    
class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    quantity = models.IntegerField(default=1)
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    is_popupar = models.BooleanField(default=False)
    is_on_sale = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return self.name

    def average_rating(self):
        # Calculate the average rating for this item
        return self.reviews.aggregate(Avg('rating'))['rating__avg']

    def user_review_details(self):
        # Get all reviews for this item, along with the related user
        return ItemReview.objects.filter(item=self).select_related('user')

    def by_user(self):
        # Return a string representation of the user who created the item
        if self.created_by.first_name and self.created_by.last_name:
            return f"{self.created_by.first_name} {self.created_by.last_name}"
        else:
            return self.created_by.username

    def user_reviews(self):
        # Get all reviews for this item as a string
        reviews = self.reviews.all()
        
        return [f" {review.review}" for review in reviews]
    
class Profile(models.Model):
    STATE_CHOICES = (
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
)

    state = models.CharField(max_length=2, choices=STATE_CHOICES, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(null=True, blank=True, max_length=500)
    last_name = models.CharField(null=True, blank=True, max_length=500)
    profile_image = models.ImageField(upload_to='static', null=True, blank=True)
    profile_bio = models.CharField(max_length=500, null=True, blank=True)
    email = models.EmailField( max_length=500,null=True, blank=True)
    
    phone_number = models.CharField(max_length=100, null=True, blank=True)
    mobile_number = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    profession = models.CharField(max_length=100, null=True, blank=True)
   
    website_link = models.CharField(max_length=100, null=True, blank=True)
    facebook_link = models.CharField(max_length=100, null=True, blank=True)
    instagram_link = models.CharField(max_length=100, null=True, blank=True)
    linkedIn_link = models.CharField(max_length=100, null=True, blank=True)
    
	
    
    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return "Profile with no name"
        
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        user_profile = Profile(user=instance)
        user_profile.save()

    

def delete_user(user_id):
    try:
        user = User.objects.get(id=user_id)
        if user.profile:
            user.profile.delete()  # Delete the associated profile if it exists
        user.delete()  # Delete the user
        return True
    except User.DoesNotExist:
        return False

# Override the delete method of the User model
def user_delete(self, *args, **kwargs):
    if self.profile:
        self.profile.delete()  # Delete the associated profile if it exists
    super(User, self).delete(*args, **kwargs)

User.delete = user_delete  # Assign the overridden method to the User model

class Cart(models.Model):
    user = models.ForeignKey(User, related_name="carts", on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item,related_name='items', on_delete=models.CASCADE)
    def __str__(self):
        return F"{self.item.name}" if self.item else "Cart Empty"


class ItemReview(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically store the creation date and time
   
    class Meta:
        unique_together = ('item', 'user')

    def __str__(self):
        return f"Review for {self.item.name} by {self.user.username} {self.review}"
   
    def by_user(self):
        if self.user.first_name and self.user.last_name:
            return f" {self.user.first_name} {self.user.last_name}"
        else:
            return f" {self.user.username}"
           
    def user_reviews(self):
        return f" {self.review}"
    
    