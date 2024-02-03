from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Ad, Category, Author
from .serializers import AdListSerializer, AdDetailSerializer, ReviewCreateSerializer, CreateRatingSerializer, \
    CategoryListSerializer, AdSerializer, AuthorSerializer
from .service import get_client_ip, AdFilter, PaginationAd
from django.db import models
from rest_framework import generics, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, parsers


class CategoryListView(generics.ListAPIView):

    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    pagination_class = PaginationAd


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class AdListView(generics.ListAPIView):
    serializer_class = AdListSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ['title', 'description']
    filterset_class = AdFilter
    ordering_fields = ['title', 'published_date', 'description']

    pagination_class = PaginationAd

    def get_queryset(self):
        ads = Ad.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return ads


class AdDetailView(generics.RetrieveAPIView):
    queryset = Ad.objects.filter(draft=False)
    serializer_class = AdDetailSerializer


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer


class AddStarRatingView(generics.CreateAPIView):
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


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
    serializer_class = AuthorSerializer
