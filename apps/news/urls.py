from django.urls import path

from .views import NewsFoundationView

app_name = "news"

urlpatterns = [
    path("", NewsFoundationView.as_view(), name="list"),
]
