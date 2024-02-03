from django.urls import path
from . import views


urlpatterns = [
    path("ad/", views.AdListView.as_view()),
    path("ad/<int:pk>/", views.AdDetailView.as_view()),
    path("create/", views.AdCreateView.as_view()),
    path("update/<int:pk>/", views.AdUpdateView.as_view()),
    path("delete/<int:pk>/", views.AdDeleteView.as_view()),
    path("review/", views.ReviewCreateView.as_view()),
    path("rating/", views.AddStarRatingView.as_view()),
    path("category/", views.CategoryListView.as_view()),
    path("category/<int:pk>/", views.CategoryListView.as_view()),
    path("author/<int:pk>/", views.AuthorDetailView.as_view()),
    path("author/update/<int:pk>/", views.AuthorUpdateView.as_view()),

]
