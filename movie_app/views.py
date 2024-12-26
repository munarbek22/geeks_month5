from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from .models import Movie, Director, Review
from .serializers import (DirectorSerializer, ReviewSerializer,
                          MovieSerializer, MovieReviewsSerializer, DirectorCountSerializer,
                          DirectorValidateSerializer, MovieCreateSerializer, MovieUpdateSerializer,
                          ReviewValidateSerializer, )
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict

class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('total', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

class DirectorListCreateAPIView(ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    pagination_class = CustomPagination

class DirectorDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    lookup_field = 'id'

class MovieListCreateAPIView(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def create(self, request, *args, **kwargs):
        serializer = MovieCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        title = serializer.validated_data.get('title', None)
        description = serializer.validated_data.get('description', 'no description')
        duration = serializer.validated_data.get('duration', None)
        director = serializer.validated_data.get('director', None)

        movie = Movie.objects.create(
            title=title,
            description=description,
            duration=duration,
            director=director
        )
        movie.save()

        return Response(status=status.HTTP_201_CREATED,
                        data=MovieSerializer(movie).data)

class MovieDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'id'

class ReviewListCreateAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        text = serializer.validated_data.get('text', 'no text')
        stars = serializer.validated_data.get('stars', None)
        movie = serializer.validated_data.get('movie', None)

        review = Review.objects.create(
            text=text,
            stars=stars,
            movie=movie
        )
        review.save()

        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewSerializer(review).data)

class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'

@api_view(['GET', 'POST'])
def director_list_api_view(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        serializers = DirectorSerializer(instance=directors, many=True)
        return Response(data=serializers.data, status=HTTP_200_OK)
    elif request.method == 'POST':
        serializer = DirectorValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        director = Director.objects.create(**serializer.validated_data)
        return Response(data=DirectorSerializer(director).data, status=status.HTTP_201_CREATED)

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
        serializer = DirectorSerializer(data=request.data,
                                        context={'director': director})
        serializer.is_valid(raise_exception=True)
        director.name = serializer.validated_data.get('name')
        director.save()
        return Response(data=DirectorSerializer(director).data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def movie_list_api_view(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(instance=movies, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = MovieCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        title = serializer.validated_data.get('title', None)
        description = serializer.validated_data.get('description', 'no description')
        duration = serializer.validated_data.get('duration', None)
        director = serializer.validated_data.get('director', None)

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
        serializer = MovieUpdateSerializer(data=request.data,
                                             context={'movie': movie})
        serializer.is_valid(raise_exception=True)
        movie.title = serializer.validated_data.get('title')
        movie.description = serializer.validated_data.get('description')
        movie.duration = serializer.validated_data.get('duration')
        movie.director_id = serializer.validated_data.get('director_id')
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
    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        text = serializer.validated_data.get('text', 'no text')
        stars = serializer.validated_data.get('stars', None)
        movie = serializer.validated_data.get('movie', None)

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
        serializer = ReviewValidateSerializer(data=request.data,
                                              context = {'review': review})
        serializer.is_valid(raise_exception=True)
        review.text = serializer.validated_data.get('text')
        review.stars = serializer.validated_data.get('stars')
        review.movie_id = serializer.validated_data.get('movie_id')
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


