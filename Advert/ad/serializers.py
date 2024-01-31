from rest_framework import serializers

from .models import Ad, Review, Rating, Category


class FilterReviewListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "image")


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class AdListSerializer(serializers.ModelSerializer):
    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()

    class Meta:
        model = Ad
        fields = ("id", "title", "category", "description", "author", "rating_user", "middle_star", "published_date")
        extra_kwargs = {
            'user': {'read_only': True}
        }


class ReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        exclude = ("draft",)


class AdDetailSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer(read_only=True)
    author = serializers.SlugRelatedField(slug_field="name", read_only=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Ad
        exclude = ("draft", )


class CreateRatingSerializer(serializers.ModelSerializer):
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
