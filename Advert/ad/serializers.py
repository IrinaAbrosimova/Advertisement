from rest_framework import serializers, permissions

from .models import Ad, Review, Rating, Category, Author


class FilterReviewListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ReviewCreateSerializer(serializers.ModelSerializer):
    permission_classes = [permissions.IsAuthenticated]

    class Meta:
        model = Review
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)
    permission_classes = [permissions.AllowAny]

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        exclude = ("draft",)


class AuthorSerializer(serializers.ModelSerializer):

    permission_classes = [permissions.IsAuthenticated]

    class Meta:
        model = Author
        fields = "__all__"


class CategoryListSerializer(serializers.ModelSerializer):
    permission_classes = [permissions.IsAuthenticated]

    class Meta:
        model = Category
        fields = ("id", "name", "image")


class AdListSerializer(serializers.ModelSerializer):
    permission_classes = [permissions.AllowAny]
    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()

    class Meta:
        model = Ad
        fields = ("id", "title", "category", "description", "author", "rating_user", "middle_star", "published_date")
        extra_kwargs = {
            'user': {'read_only': True}
        }


class AdSerializer(serializers.ModelSerializer):
    permission_classes = [permissions.IsAuthenticated]

    class Meta:
        model = Ad
        fields = ("title", "category", "description", "author", "draft", "published_date", "created_date", "modified_date")
        extra_kwargs = {
            'user': {'read_only': True}
        }


class AdDetailSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer(read_only=True)
    author = AuthorSerializer(read_only=True)
    reviews = ReviewSerializer(many=True)
    permission_classes = [permissions.AllowAny]

    class Meta:
        model = Ad
        fields = "__all__"


class CreateRatingSerializer(serializers.ModelSerializer):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    class Meta:
        model = Rating
        fields = ("star", "ad")

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            ad=validated_data.get('ad', None),
            defaults={'star': validated_data.get("star")}
        )
        return rating
