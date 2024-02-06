from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Ad, Category, Author, Review
from .serializers import *
from .service import get_client_ip, AdFilter, Pagination
from django.db import models
from rest_framework import generics, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, parsers


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = Pagination


class AdListView(generics.ListAPIView):
    serializer_class = AdSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ['title', 'description']
    filterset_class = AdFilter
    ordering_fields = ['title', 'published_date', 'description']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = Pagination

    def get_queryset(self):
        ads = Ad.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return ads


class AdDetailView(generics.RetrieveAPIView):
    queryset = Ad.objects.filter(draft=False)
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AdCreateView(generics.CreateAPIView):
    serializer_class = AdSerializer


class AdUpdateView(generics.UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class AdDeleteView(generics.DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class AuthorUpdateView(generics.UpdateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorDetailView(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorViewSerializer


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer


class ReviewView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewViewSerializer
    pagination_class = Pagination


class ReviewUpdateView(generics.UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDeleteView(generics.DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class AddStarRatingView(generics.CreateAPIView):
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))
