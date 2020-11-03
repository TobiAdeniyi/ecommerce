from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.contrib import admin
from . import views

urlpatterns = [
	path('', views.store, name="store"),

	path('basket/', views.basket, name="basket"),
	path('checkout/', views.checkout, name="checkout"),

    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),

	path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), 
        {'next_page': settings.LOGIN_REDIRECT_URL}, name="login"),
	path('logout/', auth_views.LogoutView.as_view(template_name='store/logout.html'), 
        {'next_page': settings.LOGOUT_REDIRECT_URL}, name="logout"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
]