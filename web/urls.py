"""
URL configuration for web app
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transactions/', views.transactions, name='transactions'),
    path('transactions/add/', views.add_transaction, name='add_transaction'),
    path('analytics/', views.analytics, name='analytics'),
]

