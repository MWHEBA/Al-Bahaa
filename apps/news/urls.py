from django.urls import path

from .views import NewsListView

app_name = "news"

urlpatterns = [
    path("", NewsListView.as_view(), name="list"),
]
