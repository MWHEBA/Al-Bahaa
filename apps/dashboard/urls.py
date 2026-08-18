from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    # Auth & Profile
    path("login/", views.DashboardLoginView.as_view(), name="login"),
    path("logout/", views.DashboardLogoutView.as_view(), name="logout"),
    path("profile/", views.DashboardProfileView.as_view(), name="profile"),

    # Overview
    path("", views.DashboardOverviewView.as_view(), name="overview"),

    # Projects
    path("projects/", views.ProjectListView.as_view(), name="projects_list"),
    path("projects/create/", views.ProjectCreateView.as_view(), name="projects_create"),
    path("projects/<int:pk>/edit/", views.ProjectUpdateView.as_view(), name="projects_edit"),
    path("projects/<int:pk>/delete/", views.ProjectDeleteView.as_view(), name="projects_delete"),
    path("projects/gallery/<int:pk>/delete/", views.ProjectGalleryImageDeleteView.as_view(), name="projects_gallery_delete"),
    path("projects/categories/", views.ProjectCategoryManageView.as_view(), name="projects_categories"),

    # News
    path("news/", views.NewsListView.as_view(), name="news_list"),
    path("news/create/", views.NewsCreateView.as_view(), name="news_create"),
    path("news/<int:pk>/edit/", views.NewsUpdateView.as_view(), name="news_edit"),
    path("news/<int:pk>/delete/", views.NewsDeleteView.as_view(), name="news_delete"),

    # Careers & Recruitment
    path("careers/openings/", views.JobOpeningListView.as_view(), name="careers_jobs"),
    path("careers/openings/create/", views.JobOpeningCreateView.as_view(), name="careers_jobs_create"),
    path("careers/openings/<int:pk>/edit/", views.JobOpeningUpdateView.as_view(), name="careers_jobs_edit"),
    path("careers/openings/<int:pk>/delete/", views.JobOpeningDeleteView.as_view(), name="careers_jobs_delete"),
    path("careers/applications/", views.JobApplicationListView.as_view(), name="careers_applications"),
    path("careers/applications/<int:pk>/", views.JobApplicationDetailView.as_view(), name="careers_application_detail"),
    path("careers/applications/<int:pk>/status/", views.JobApplicationQuickStatusView.as_view(), name="careers_application_status"),
    path("careers/applications/export-csv/", views.ExportApplicationsCsvView.as_view(), name="careers_applications_export"),

    # Inquiries
    path("inquiries/", views.InquiriesListView.as_view(), name="inquiries_list"),
    path("inquiries/<int:pk>/", views.InquiryDetailView.as_view(), name="inquiry_detail"),
    path("inquiries/<int:pk>/status/", views.InquiryQuickStatusView.as_view(), name="inquiry_status"),
    path("inquiries/export-csv/", views.ExportInquiriesCsvView.as_view(), name="inquiries_export"),

    # Settings & Heroes
    path("settings/general/", views.SiteSettingsEditView.as_view(), name="settings_general"),
    path("settings/heroes/", views.PageHeroesManageView.as_view(), name="settings_heroes"),
    path("settings/heroes/<int:pk>/edit/", views.PageHeroEditView.as_view(), name="settings_hero_edit"),

    # Clients & Team
    path("clients/", views.ClientLogosManageView.as_view(), name="clients_manage"),
    path("clients/<int:pk>/edit/", views.ClientLogoEditView.as_view(), name="clients_edit"),
    path("team/", views.TeamManageView.as_view(), name="team_manage"),
    path("team/<int:pk>/edit/", views.TeamMemberEditView.as_view(), name="team_edit"),
]
