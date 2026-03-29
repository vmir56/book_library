# books/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_page, name='start_page'),
    path('api/reviews/<int:book_id>/', views.get_reviews, name='get_reviews'),
]