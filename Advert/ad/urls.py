from django.urls import path
from . import views


urlpatterns = [
    path("ad/", views.AdListView.as_view()),
    path("ad/<int:pk>/", views.AdDetailView.as_view()),
    path("review/", views.ReviewCreateView.as_view()),
    path("rating/", views.AddStarRatingView.as_view()),
    path("category/", views.CategoryListView.as_view()),
    path("category/<int:pk>/", views.CategoryListView.as_view()),

]
