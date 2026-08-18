from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    # Auth & Profile
    path("login/", views.DashboardLoginView.as_view(), name="login"),
    path("logout/", views.DashboardLogoutView.as_view(), name="logout"),
    path("profile/", views.DashboardProfileView.as_view(), name="profile"),
    path("", views.DashboardOverviewView.as_view(), name="overview"),

    # Projects
    path("projects/", views.ProjectListView.as_view(), name="projects_list"),
    path("projects/create/", views.ProjectCreateView.as_view(), name="projects_create"),
    path("projects/<int:pk>/edit/", views.ProjectUpdateView.as_view(), name="projects_edit"),
    path("projects/<int:pk>/delete/", views.ProjectDeleteView.as_view(), name="projects_delete"),
    path("projects/categories/", views.ProjectCategoryManageView.as_view(), name="projects_categories"),
    path("projects/images/<int:pk>/delete/", views.ProjectGalleryImageDeleteView.as_view(), name="projects_image_delete"),

    # News & Articles
    path("news/", views.NewsListView.as_view(), name="news_list"),
    path("news/create/", views.NewsCreateView.as_view(), name="news_create"),
    path("news/<int:pk>/edit/", views.NewsUpdateView.as_view(), name="news_edit"),
    path("news/<int:pk>/delete/", views.NewsDeleteView.as_view(), name="news_delete"),
    path("news/categories/", views.NewsCategoryManageView.as_view(), name="news_categories"),

    # Recruitment & Careers
    path("careers/jobs/", views.JobOpeningListView.as_view(), name="careers_jobs"),
    path("careers/jobs/create/", views.JobOpeningCreateView.as_view(), name="careers_jobs_create"),
    path("careers/jobs/<int:pk>/edit/", views.JobOpeningUpdateView.as_view(), name="careers_jobs_edit"),
    path("careers/jobs/<int:pk>/delete/", views.JobOpeningDeleteView.as_view(), name="careers_jobs_delete"),
    path("careers/jobs/<int:pk>/toggle-status/", views.JobOpeningQuickStatusView.as_view(), name="careers_jobs_toggle"),
    path("careers/departments/", views.JobDepartmentManageView.as_view(), name="careers_departments"),
    path("careers/applications/", views.JobApplicationListView.as_view(), name="careers_applications"),
    path("careers/applications/<int:pk>/", views.JobApplicationDetailView.as_view(), name="careers_application_detail"),
    path("careers/applications/<int:pk>/status/", views.JobApplicationQuickStatusView.as_view(), name="careers_application_status"),
    path("careers/applications/<int:pk>/delete/", views.JobApplicationDeleteView.as_view(), name="careers_application_delete"),
    path("careers/applications/<int:pk>/cv/", views.ProtectedResumeDownloadView.as_view(), name="careers_application_cv"),
    path("careers/applications/export/csv/", views.ExportApplicationsCsvView.as_view(), name="careers_applications_csv"),

    # Inquiries & Tenders
    path("inquiries/", views.InquiriesListView.as_view(), name="inquiries_list"),
    path("inquiries/<int:pk>/", views.InquiryDetailView.as_view(), name="inquiry_detail"),
    path("inquiries/<int:pk>/status/", views.InquiryQuickStatusView.as_view(), name="inquiry_status"),
    path("inquiries/<int:pk>/delete/", views.InquiryDeleteView.as_view(), name="inquiry_delete"),
    path("inquiries/export/csv/", views.ExportInquiriesCsvView.as_view(), name="inquiries_csv"),

    # Page CMS Editors (In-context)
    path("content/home/", views.HomeContentManageView.as_view(), name="content_home"),
    path("content/about/", views.AboutPageManageView.as_view(), name="content_about"),
    path("content/careers/", views.CareersPageManageView.as_view(), name="content_careers"),

    # Social Proof & Leadership
    path("partners/", views.PartnersManageView.as_view(), name="partners_manage"),
    path("team/", views.TeamManageView.as_view(), name="team_manage"),

    # Settings & Page Heroes
    path("settings/general/", views.SiteSettingsEditView.as_view(), name="settings_general"),
    path("heroes/<int:pk>/edit/", views.PageHeroEditView.as_view(), name="hero_edit"),

    # Staff & User Management (Superuser Only)
    path("users/", views.StaffUserListView.as_view(), name="users_list"),
    path("users/create/", views.StaffUserCreateView.as_view(), name="users_create"),
    path("users/<int:pk>/edit/", views.StaffUserUpdateView.as_view(), name="users_edit"),
    path("users/<int:pk>/toggle-status/", views.StaffUserToggleStatusView.as_view(), name="users_toggle"),
]
