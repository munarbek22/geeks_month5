from django.urls import path
from . import views

urlpatterns = [
    path('/api/v1/directors/', views.DirectorListCreateAPIView.as_view(), name='director_view'),
    path('/api/v1/directors/<int:id>/', views.DirectorDetailAPIView.as_view(), name='director_detail'),
    path(' /api/v1/movies/', views.MovieListCreateAPIView.as_view(), name='movie_list'),
    path('/api/v1/movies/<int:id>/', views.MovieDetailAPIView.as_view(), name='movie_detail'),
    path('/api/v1/reviews/', views.ReviewListCreateAPIView, name='review_list'),
    path('/api/v1/reviews/<int:id>/', views.ReviewDetailAPIView.as_view(), name='review_detail'),
    path(' /api/v1/movies/reviews/', views.movie_reviews_list_api_view, name='movie_reviews_list'),
    path('/api/v1/directors/', views.director_list_count_api_view, name='directors')
]