from django import forms 
from. models import  Profile, Item,ItemReview
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#profile extras
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'profile_image', 'profile_bio', 'email', 'phone_number', 'mobile_number', 'address', 'city', 'state', 'profession', 'website_link', 'facebook_link', 'instagram_link', 'linkedIn_link']
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})  # Add Bootstrap class for instagram_link field
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})  # Add Bootstrap class for linkedIn_link field
        self.fields['profile_image'].widget.attrs.update({'class': 'form-control-file'})  # Add Bootstrap class for profile_image field
        self.fields['profile_bio'].widget.attrs.update({'class': 'form-control', 'rows': 4})  # Add Bootstrap class for profile_bio field and set rows
        self.fields['email'].widget.attrs.update({'class': 'form-control'})  # Add Bootstrap class for email field
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})  # Add Bootstrap class for phone_number field
        self.fields['mobile_number'].widget.attrs.update({'class': 'form-control'})  # Add Bootstrap class for mobile_number field
        self.fields['address'].widget.attrs.update({'class': 'form-control'})  # Add Bootstrap class for address field
        self.fields['city'].widget.attrs.update({'class': 'form-control'})  # Add Bootstrap class for city field
        self.fields['state'].widget.attrs.update({'class': 'form-control'})  # Add Bootstrap class for state field
        self.fields['profession'].widget.attrs.update({'class': 'form-control'})  # Add Bootstrap class for profession field
        self.fields['website_link'].widget.attrs.update({'class': 'form-control'})  # Add Bootstrap class for website_link field
        self.fields['facebook_link'].widget.attrs.update({'class': 'form-control'})  # Add Bootstrap class for facebook_link field
        self.fields['instagram_link'].widget.attrs.update({'class': 'form-control'})  # Add Bootstrap class for instagram_link field
        self.fields['linkedIn_link'].widget.attrs.update({'class': 'form-control'})  # Add Bootstrap class for linkedIn_link field
        
        
class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="",widget= forms.TextInput(attrs={'class':'form-control','placeholder':'Email Address'}),required=False)
    first_name = forms.CharField(label="",max_length=100,widget= forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),required=False)
    last_name = forms.CharField(label="",max_length=100,widget= forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),required=False)
    
    
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm,self).__init__(*args,**kwargs)
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Your User Name'
        self.fields['username'].label = ""
        self.fields['username'].help_text = "<span class='form-text text-muted'><small>Required. 150 character or fewer. Letters digits and symbols.</small></span>"
        
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ""
        self.fields['password1'].help_text = "<span class='form-text text-muted'><small>Your password must be at least 8 characters long. It must contains aty least 2 digits, 2 letters and 2 symbols</small></span>"
        
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Password Confirmation'
        self.fields['password2'].label = ""
        self.fields['password2'].help_text ="<span class='form-text text-muted'><small>Enter the same Password</small></span>"
        
    def clean_username(self):
        username = self.cleaned_data['username']
        current_user = self.instance
        if User.objects.exclude(pk=current_user.pk).filter(username=username).exists():
            raise forms.ValidationError("A user with this username already exists.")
        return username


class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['category', 'name', 'description', 'price', 'quantity', 'image', 'is_on_sale',]
    def __init__(self, *args, **kwargs):
        super(AddItemForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-control'})  
        self.fields['name'].widget.attrs.update({'class': 'form-control'})  
        self.fields['description'].widget.attrs.update({'class': 'form-control-file'})  
        self.fields['price'].widget.attrs.update({'class': 'form-control', 'rows': 4})  
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})  
        self.fields['image'].widget.attrs.update({'class': 'form-control'})  
       
       
   
   

class RateReviewForm(forms.Form):
    rating = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], widget=forms.RadioSelect)
    review = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))

    def save(self, user, item):
        rating = self.cleaned_data['rating']
        review_text = self.cleaned_data['review']
        ItemReview.objects.create(item=item, user=user, rating=rating, review=review_text)
        
    def __init__(self, *args, **kwargs):
        super(RateReviewForm, self).__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update({'type': 'checkbox'})  
        self.fields['review'].widget.attrs.update({'class': 'form-control'})  