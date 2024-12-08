from rest_framework import serializers
from .models import Director,Review, Movie

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
