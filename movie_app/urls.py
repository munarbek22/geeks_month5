from django.urls import path
from . import views

urlpatterns = [
    path('directors/', views.director_list_api_view, name='director_view'),
    path('directors/<int:id>/', views.director_detail_api_view, name='director_detail'),
    path('movies/', views.movie_list_api_view, name='movie_list'),
    path('movies/<int:id>/', views.movie_detail_api_view, name='movie_detail'),
    path('reviews/', views.review_list_api_view, name='review_list'),
    path('reviews/<int:id>/', views.review_detail_api_view, name='review_detail')
]