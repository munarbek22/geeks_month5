from rest_framework import serializers
from .models import Director,Review, Movie
from rest_framework.exceptions import ValidationError

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "id text stars movie"

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class MovieReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    rating = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields = 'id title description duration director reviews rating'

    def get_rating(self, movie):
        if movie.reviews.exists():
            total_stars = sum(review.stars for review in movie.reviews.all())
            return round(total_stars / movie.reviews.count(), 2)
        return None

class DirectorCountSerializer(serializers.ModelSerializer):
    movies_count = serializers.IntegerField()

    class Meta:
        model = Director
        fields = 'id name movies_count'


class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, min_length=3, required=True)


class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, min_length=3, required=True)
    description = serializers.CharField(required=False)
    duration = serializers.IntegerField(min_value=1, required=True)
    director_id = serializers.IntegerField(required=True)

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError('Director does not exist!')
        return director_id


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(required=True)
    stars = serializers.IntegerField(min_value=1, max_value=5, required=True)
    movie_id = serializers.IntegerField(required=True)

    def validate_movie_id(self, movie_id):
        try:
            Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            raise ValidationError('Movie does not exist!')
        return movie_id


class MovieCreateSerializer(MovieValidateSerializer):
    def validate_title(self, title):
        if Movie.objects.filter(title__exact=title):
            raise ValidationError('Movie title already exists!')
        return title

class MovieUpdateSerializer(MovieValidateSerializer):
    def validate_title(self, title):
        product = self.context.get('product')
        if Movie.objects.filter(title__exact=title).exclude(id=movie.id):
            raise ValidationError('Movie title already exists!')
        return title