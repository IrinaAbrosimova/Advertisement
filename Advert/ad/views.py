from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Ad, Category
from .serializers import AdListSerializer, AdDetailSerializer, ReviewCreateSerializer, CreateRatingSerializer, \
    CategoryListSerializer, CategoryDetailSerializer
from .service import get_client_ip, AdFilter, PaginationAd
from django.db import models
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class CategoryListView(generics.ListAPIView):

    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


class AdListView(generics.ListAPIView):
    serializer_class = AdListSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ['title', 'description']
    filterset_class = AdFilter
    ordering_fields = ['title', 'published_date', 'description']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, permissions.IsAdminUser]
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
    permission_classes = [permissions.IsAuthenticated]


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class AddStarRatingView(generics.CreateAPIView):
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))

