from django.urls import path
from . import views


urlpatterns = [
    path("ad/", views.AdListView.as_view()),
    path("ad/<int:pk>/", views.AdDetailView.as_view()),
    path("ad/create/", views.AdCreateView.as_view()),
    path("ad/update/<int:pk>/", views.AdUpdateView.as_view()),
    path("ad/delete/<int:pk>/", views.AdDeleteView.as_view()),
    path("review/", views.ReviewView.as_view()),
    path("review/create/", views.ReviewCreateView.as_view()),
    path("review/<int:pk>/", views.ReviewView.as_view()),
    path("review/update/<int:pk>/", views.ReviewUpdateView.as_view()),
    path("review/delete/<int:pk>/", views.ReviewDeleteView.as_view()),
    path("rating/", views.AddStarRatingView.as_view()),
    path("category/", views.CategoryView.as_view()),
    path("author/<int:pk>/", views.AuthorDetailView.as_view()),
    path("author/update/<int:pk>/", views.AuthorUpdateView.as_view()),

]
