from rest_framework import serializers, permissions

from .models import Ad, Review, Rating, Category, Author
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .service import *


class FilterReviewListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    permission_classes = [permissions.AllowAny]

    class Meta:
        model = Review
        fields = "__all__"


class ReviewViewSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)
    permission_classes = [permissions.AllowAny]

    class Meta:
        model = Review
        fields = ["text", "user", "draft", "ad", "children"]
        extra_kwargs = {
            'user': {'read_only': True},
        }


class UserReviewSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)
    permission_classes = [permissions.AllowAny]

    def get_queryset(self, request, *args, **kwargs):
        userpreviews = Preview.objects.filter(user=request.user).order_by('-id')
        return userpreviews

    class Meta:
        model = Review
        fields = "__all__"


class UserPreviewSerializer(serializers.ModelSerializer):
    review_user = UserReviewSerializer(many=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "date_joined", "review_user"]


class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Author
        fields = ["id", "user", "name", "image", "phone", "vk", "telegram", "whatsup"]
        read_only_fields = ('user',)


class UserSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "authors"]
        read_only_fields = ["email"]

    # def create(self, validated_data):
    #     authors = validated_data.pop('authors')
    #     user = User.objects.create(**validated_data)
    #     for author in authors:
    #         Author.objects.create(**author, user=user)
    #     return user

    def update(self, instance, validated_data):
        authors = validated_data.pop('authors')
        instance.username = validated_data.get("username", instance.username)
        instance.save()
        keep_authors = []
        for author in authors:
            if "id" in author.keys():
                if Author.objects.filter(id=author["id"]).exists():
                    c = Author.objects.get(id=author["id"])
                    c.username = author.get('username', c.username)
                    c.save()
                    keep_authors.append(c.id)
                else:
                    continue
            else:
                c = Author.objects.create(**author, user=instance)
                keep_authors.append(c.id)

        for author in instance.authors:
            if author.id not in keep_authors:
                author.delete()

        return instance


class AuthorViewSerializer(serializers.ModelSerializer):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    user = UserPreviewSerializer(read_only=True)

    class Meta:
        model = Author
        fields = ["image", "name", "phone", "vk", "telegram", "whatsup", "user"]


class CategorySerializer(serializers.ModelSerializer):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    class Meta:
        model = Category
        fields = ("id", "name", "image")


class AdSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    author = AuthorSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    class Meta:
        model = Ad
        fields = ("title", "category", "description", "author", "draft", "published_date", "created_date", "modified_date", "reviews")
        extra_kwargs = {
            'user': {'read_only': True}
        }


class CreateRatingSerializer(serializers.ModelSerializer):
    permission_classes = [permissions.AllowAny]

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
