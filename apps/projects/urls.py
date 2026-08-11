from django.urls import path

from .views import ProjectFoundationView

app_name = "projects"

urlpatterns = [
    path("", ProjectFoundationView.as_view(), name="list"),
    path("<slug:slug>/", ProjectFoundationView.as_view(), name="detail"),
]
