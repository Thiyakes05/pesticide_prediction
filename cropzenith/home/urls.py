# home/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Login page
    path('', views.login_view, name='login'),

    # Homepage
    path('home/', views.homepage_view, name='homepage'),

    # Profile view page
    path('home/profile/', views.profile_view, name='profile_view'),

    # Profile edit page
    path('home/profile/edit/', views.profile_edit, name='profile_edit'),

    # Crop information page
    path('home/crop-information/', views.crop_information_view, name='crop_information'),

    # Prediction page (uncomment if needed)
    # path('home/predict/', views.predict_view, name='predict'),
]
