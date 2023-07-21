from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Category, Item, Profile, Cart,ItemReview
from django.contrib.auth.models import User
from django.db.models import Q, Sum

from.forms import SignUpForm, ProfileForm, AddItemForm, RateReviewForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg

# Create your views here.
def home(request):
   
    categories = Category.objects.all()
    items = Item.objects.all()
    cart = Cart.objects.all()
    total_price = cart.aggregate(total_price=Sum('item__price'))['total_price'] or 0
    average_rating = {item.id: item.average_rating() for item in items}
    
    return render(request,'home.html',{'items':items,'categories':categories, 'cart':cart, 'total_price':total_price,'average_rating':average_rating})

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
        average_rating = {item.id: item.average_rating() for item in items}
        categories = Category.objects.filter(items__in=items).distinct()
        return render(request, 'searched.html', {'searched': searched, 'items': items, 'categories': categories,'average_rating':average_rating})
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
    if request.user.is_authenticated:
        user = get_object_or_404(User, username=username)
        profile = Profile.objects.get(user=user)
        return render(request, 'user_profile.html', {'user': user, 'profile': profile})
    else:
        messages.success(request, ("You must be logged in to view this page!"))
        return redirect('home')	
    
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


def dashboard(request, username):
    if request.user.is_authenticated:
        user = request.user
        items = Item.objects.filter(created_by=user)
        average_rating = {item.id: item.average_rating() for item in items}
        

        # Paginate the items to show 8 items per page
        paginator = Paginator(items, 2)
        page = request.GET.get('page')
        try:
            items_page = paginator.page(page)
        except PageNotAnInteger:
            items_page = paginator.page(1)
        except EmptyPage:
            items_page = paginator.page(paginator.num_pages)

        cart = Cart.objects.all()
        total_price = cart.aggregate(total_price=Sum('item__price'))['total_price'] or 0
        user = get_object_or_404(User, username=username)
        profile = Profile.objects.get(user=user)
        return render(request, 'dashboard.html', {'user': user, 'profile': profile, 'cart': cart, 'items_page': items_page,'average_rating':average_rating})
    else:
        messages.success(request, "You must be logged in to view this page!")
        return redirect('home')
    
    
@login_required
def add_item(request):
    if request.method == 'POST':
        form = AddItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user  # Set the current user as the creator
            item.save()
            return redirect('home')
    else:
        form = AddItemForm()

    return render(request, 'add_item.html', {'form': form})

    
@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.user == item.created_by:
        if request.method == 'POST':
            form = AddItemForm(request.POST, request.FILES, instance=item)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = AddItemForm(instance=item)
    else:
        messages.success(request, ("You Don't Own That ITEM!!"))
        return redirect('home')

    return render(request, 'edit_item.html', {'form': form, 'item': item})


@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.user == item.created_by:
        item.delete()
        return redirect('home')
    else:
        messages.success(request, ("You Don't Own That ITEM!!"))
        return redirect('home')


def item_details(request, item_id):
    item = get_object_or_404(Item, id=item_id)
   
    # Get all reviews for this item with the related user and review date
    item_reviews = item.user_review_details()
   
    authors = item.by_user()
   
    return render(request, 'item_details.html', {'item': item, 'item_reviews': item_reviews, 'authors': authors})




@login_required
def rate_review_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.method == 'POST':
        form = RateReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            review = form.cleaned_data['review']
           
            # Check if the user has already rated this item
            if ItemReview.objects.filter(item=item, user=request.user).exists():
                # Handle the case when the user has already rated this item
                # You can show an error message or redirect the user to a different page
                return redirect('item_details', item_id=item_id)
           
            # Save the rating and review for the item
            item_review = ItemReview.objects.create(item=item, user=request.user, rating=rating, review=review)
            # Calculate the average rating for the item
            average_rating = item.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
            item.rating = average_rating
            item.save()
            return redirect('item_details', item_id=item_id)
    else:
        form = RateReviewForm()

    return render(request, 'rate_review_item.html', {'form': form, 'item': item})

