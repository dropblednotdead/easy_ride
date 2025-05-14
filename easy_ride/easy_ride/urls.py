from django.contrib import admin
from django.urls import path

from easy_ride import views

urlpatterns = [
    path('main/', views.main_page, name='main'),
    path('registration/', views.RegistrationUser.as_view(), name='registration'),
    path('authorization/', views.AuthorizationUser.as_view(), name='authorization'),
    path('logout/', views.logout_user, name='logout'),
    path('user/', views.user_profile_view, name='user'),
    path('categories/', views.CategoriesPage.as_view(), name='categories'),
    path('category/<int:category>/', views.CategoryPage.as_view(), name='category'),
    path('rent/<int:pk>/', views.rent_car, name='rent'),
    path('my_rents/', views.MyRentsPage.as_view(), name='my_rents'),
    path('sales/', views.SalesPage.as_view(), name='sales'),
    path('review/', views.create_review, name='review'),
]