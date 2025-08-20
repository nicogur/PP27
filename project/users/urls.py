
from django.urls import path
from .views import RegisterView, ContactView, ProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
