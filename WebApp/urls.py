from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("logout/", views.logout_user, name="logout_user"),
    path("login/", views.login_user, name="login_user"),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('search_items/',views.search_items, name = 'search_items'),
    path('category/<int:category_id>/', views.category_items, name='category_items'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('register/',views.register_user,name="register"),
    path('edit_user_profile/',views.edit_user_profile,name="edit_user_profile"),
]
