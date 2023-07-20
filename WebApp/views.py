from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Category, Item, Profile, Cart
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404
from.forms import SignUpForm, ProfileForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
   
    categories = Category.objects.all()
    items = Item.objects.all()
    cart = Cart.objects.all()
    total_price = cart.aggregate(total_price=Sum('item__price'))['total_price'] or 0
    
    
    return render(request,'home.html',{'items':items,'categories':categories, 'cart':cart, 'total_price':total_price})

def login_user(request):
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "There was an error logging in. Please try again.")
            return redirect('login')
    else:
        return render(request, 'login.html', {})
    
    
def logout_user(request):
    logout(request)
    return redirect('home')

def add_to_cart(request, item_id):
    if request.method == 'POST':
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Get the item based on the item_id
            item = Item.objects.get(pk=item_id)
            # Check if the user already has a cart with this item
            cart, created = Cart.objects.get_or_create(user=request.user, item=item)
            return redirect('home')
        else:
            # If the user is not logged in, redirect to the login page
            return redirect('login')
def search_items(request):
    if request.method == "POST":
        searched = request.POST.get('searched', '')
        items = Item.objects.filter(
            Q(name__icontains=searched) |
            Q(category__name__icontains=searched) |  
            Q(price__icontains=searched) |
            Q(rating__icontains=searched) |
            Q(description__icontains=searched)
        )
        categories = Category.objects.filter(items__in=items).distinct()
        return render(request, 'searched.html', {'searched': searched, 'items': items, 'categories': categories})
    else:
        return render(request, 'searched.html', {'searched': ""})
    
from django.shortcuts import get_object_or_404

def category_items(request, category_id):
    if category_id == 0:
        # If category_id is 0, fetch all items without filtering by category
        items = Item.objects.all()
        category = None
    else:
        # If category_id is not 0, filter items by the selected category
        category = get_object_or_404(Category, id=category_id)
        items = Item.objects.filter(category=category)
    
    categories = Category.objects.all()  # Fetch all categories for the sidebar
    
    return render(request, 'category_items.html', {'category': category, 'items': items, 'categories': categories})

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    return render(request, 'user_profile.html', {'user': user, 'profile': profile})

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            
            #log in user
            user = authenticate(username = username, password = password)
            login(request,user)
            messages.success(request, ("You have successfully registered. Welcome!"))
            return redirect('edit_user_profile')
        
            
    return render(request, 'register_user.html', {'form':form})
@login_required
def edit_user_profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if profile_form.is_valid():
            profile_form.save()
            return redirect('home')  # Replace 'user_profile' with the URL name of the user profile page

    else:
        profile_form = ProfileForm(instance=profile)

    return render(request, 'edit_user_profile.html', {'profile_form': profile_form})
