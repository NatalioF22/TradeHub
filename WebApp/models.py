from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1,6)], default=1)
    quantity = models.IntegerField(default=1)
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    is_popupar = models.BooleanField(default=False)
    is_on_sale = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

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