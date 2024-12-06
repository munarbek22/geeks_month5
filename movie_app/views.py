from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from .models import Movie, Director, Review
from .serializers import DirectorSerializer, ReviewSerializer,MovieSerializer


@api_view(['GET'])
def director_list_api_view(request):
    directors = Director.objects.all()
    serializers = DirectorSerializer(instance=directors, many=True)
    return Response(data=serializers.data, status=HTTP_200_OK)

@api_view(['GET'])
def director_detail_api_view(request, id):
    try:
        director = Director.object.all(id=id)
    except Director.DoesNotExist:
        return Response(data={'error': 'Director not found!'},
                        status=HTTP_404_NOT_FOUND)
    serializer = DirectorSerializer(instance=director)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def movie_list_api_view(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(instance=movies, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Movie not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = MovieSerializer(instance=movie)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(instance=reviews, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = ReviewSerializer(instance=review)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


