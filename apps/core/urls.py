from django.urls import path

from .views import AboutView, CareersView, ContactView, HomeView, JobDetailView

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("careers/", CareersView.as_view(), name="careers"),
    path("careers/<slug:slug>/", JobDetailView.as_view(), name="job_detail"),
    path("contact/", ContactView.as_view(), name="contact"),
]

