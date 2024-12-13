from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from .models import Movie, Director, Review
from .serializers import DirectorSerializer, ReviewSerializer, MovieSerializer, MovieReviewsSerializer, \
    DirectorCountSerializer


@api_view(['GET', 'POST'])
def director_list_api_view(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        serializers = DirectorSerializer(instance=directors, many=True)
        return Response(data=serializers.data, status=HTTP_200_OK)
    elif request.method == 'POST':
        print(request.data)
        name = request.data.get('name', None)

        director = Director.objects.create(
            name=name
        )
        director.save()

        return Response(status=status.HTTP_201_CREATED,
                        data=DirectorSerializer(director).data)

@api_view(['GET', 'PUT', 'DELETE'])
def director_detail_api_view(request, id):
    try:
        director = Director.object.all(id=id)
    except Director.DoesNotExist:
        return Response(data={'error': 'Director not found!'},
                        status=HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = DirectorSerializer(instance=director)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        director.name = request.data.get('name')
        director.save()
        return Response(data=DirectorSerializer(director).data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def movie_list_api_view(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(instance=movies, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        print(request.data)
        title = request.data.get('title', None)
        description = request.data.get('description', 'no description')
        duration = request.data.get('duration', None)
        director = request.data.get('director', None)

        movie = Movie.objects.create(
            title=title,
            description=description,
            duration=duration,
            director=director
        )
        movie.save()

        return Response(status=status.HTTP_201_CREATED,
                        data=MovieSerializer(movie).data)




@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Movie not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = MovieSerializer(instance=movie)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        movie.title = request.data.get('title')
        movie.description = request.data.get('description')
        movie.duration = request.data.get('duration')
        movie.director_id = request.data.get('director_id')
        movie.save()
        return Response(data=MovieSerializer(movie).data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewSerializer(instance=reviews, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        text = request.data.get('text', 'no text')
        stars = request.data.get('stars', None)
        movie = request.data.get('movie', None)

        review = Review.objects.create(
            text=text,
            stars=stars,
            movie=movie
        )
        review.save()

        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewSerializer(review).data)


@api_view(['GET','PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ReviewSerializer(instance=review)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        review.text = request.data.get('text')
        review.stars = request.data.get('stars')
        review.movie_id = request.data.get('movie_id')
        review.save()
        return Response(data=ReviewSerializer(review).data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def movie_reviews_list_api_view(request):
    movies = Movie.objects.all()
    serializer = MovieReviewsSerializer(instance=movies, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

def director_list_count_api_view(request):
    directors = Director.objects.all()
    serializer = DirectorCountSerializer(instance=directors, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


