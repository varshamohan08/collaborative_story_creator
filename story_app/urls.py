from django.urls import path
from .views import StoriesAPI

urlpatterns = [
    path('', StoriesAPI.as_view(), name=''),
]
