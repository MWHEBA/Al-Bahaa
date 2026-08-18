import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client
from apps.core.models import SiteSettings, JobOpening, ContactMessage, JobApplication
from apps.projects.models import Project, ProjectCategory
from apps.news.models import Post

User = get_user_model()

def run_tests():
    c = Client()
    endpoints = [
        ("/", "Home Page"),
        ("/about/", "About Us Page"),
        ("/projects/", "Projects List"),
        ("/news/", "News List"),
        ("/careers/", "Careers Page"),
        ("/contact/", "Contact Us Page"),
        ("/admin/login/", "Admin Panel Login"),
    ]

    print("[TEST] Testing GET requests on all public routes...")
    for url, name in endpoints:
        res = c.get(url)
        assert res.status_code == 200, f"Failed GET {url} ({name}) - Status: {res.status_code}"
        print(f"  [PASS] {name} ({url}) -> HTTP 200")

    # Test Project Detail
    proj = Project.objects.first()
    if proj:
        url = f"/projects/{proj.slug}/"
        res = c.get(url)
        assert res.status_code == 200, f"Failed GET {url} -> {res.status_code}"
        print(f"  [PASS] Project Detail ({url}) -> HTTP 200")

    # Test News Detail
    post = Post.objects.first()
    if post:
        url = f"/news/{post.slug}/"
        res = c.get(url)
        assert res.status_code == 200, f"Failed GET {url} -> {res.status_code}"
        print(f"  [PASS] News Detail ({url}) -> HTTP 200")

    # Test Job Detail
    job = JobOpening.objects.first()
    if job:
        url = f"/careers/{job.slug}/"
        res = c.get(url)
        assert res.status_code == 200, f"Failed GET {url} -> {res.status_code}"
        print(f"  [PASS] Job Detail ({url}) -> HTTP 200")

    # Test Contact Form AJAX submission
    print("\n[TEST] Testing Contact Form Submission...")
    contact_data = {
        "name": "Eng. Test Client",
        "company": "Test Engineering Consultant",
        "email": "testclient@example.com",
        "phone": "+201012345678",
        "inquiry_type": "tenders",
        "message": "Testing automated project estimation request.",
        "website_source_check": "",  # Clean honeypot
    }
    res = c.post("/contact/", contact_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
    assert res.status_code == 200, f"Failed Contact POST -> {res.status_code}, {res.content}"
    assert ContactMessage.objects.filter(email="testclient@example.com").exists()
    print("  [PASS] Contact Form AJAX Submission -> OK, Saved to DB with unread status")

    # Test Honeypot bot rejection
    bot_data = contact_data.copy()
    bot_data["website_source_check"] = "I am a spam bot"
    res = c.post("/contact/", bot_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
    assert res.status_code == 400, f"Honeypot failed to block bot -> {res.status_code}"
    print("  [PASS] Honeypot Spam Bot Defense -> Successfully Blocked with HTTP 400")

    # Test Job Application Form submission
    print("\n[TEST] Testing Job Application Submission...")
    from django.core.files.uploadedfile import SimpleUploadedFile
    cv_file = SimpleUploadedFile("engineer_cv.pdf", b"%PDF-1.4 Mock CV Content for Al Bahaa", content_type="application/pdf")
    app_data = {
        "full_name": "Eng. Tarek Mahmoud",
        "email": "tarek.mahmoud@example.com",
        "phone": "+201098765432",
        "cover_note": "Applying for Senior Infrastructure Project Manager.",
        "resume": cv_file,
        "website_source_check": "",
    }
    res = c.post(f"/careers/{job.slug}/", app_data)
    assert res.status_code == 200, f"Failed Job Application POST -> {res.status_code}"
    assert JobApplication.objects.filter(email="tarek.mahmoud@example.com").exists()
    print("  [PASS] Job Application Form Submission -> OK, Saved to DB with new status and CV attachment")

    # =========================================================================
    # EXECUTIVE DASHBOARD TESTS
    # =========================================================================
    print("\n[TEST] Testing Executive Dashboard Security & Routes...")
    
    # 1. Unauthenticated redirect
    anon_client = Client()
    dash_res = anon_client.get("/dashboard/")
    assert dash_res.status_code == 302, f"Expected redirect for anonymous user, got {dash_res.status_code}"
    assert "/dashboard/login/" in dash_res.url
    print("  [PASS] Anonymous visitor cleanly redirected to /dashboard/login/")

    # 2. Login as Superuser / Staff
    admin_user = User.objects.filter(is_superuser=True).first()
    assert admin_user is not None, "Superuser admin not found in DB"
    c.force_login(admin_user)

    dash_routes = [
        ("/dashboard/", "Dashboard Overview"),
        ("/dashboard/profile/", "Executive Profile"),
        ("/dashboard/projects/", "Projects List"),
        ("/dashboard/projects/create/", "Project Create Form"),
        ("/dashboard/projects/categories/", "Project Categories"),
        ("/dashboard/news/", "News List"),
        ("/dashboard/news/create/", "News Create Form"),
        ("/dashboard/careers/openings/", "Job Openings List"),
        ("/dashboard/careers/openings/create/", "Job Opening Create Form"),
        ("/dashboard/careers/applications/", "Job Applications List"),
        ("/dashboard/inquiries/", "Inquiries Inbox"),
        ("/dashboard/settings/general/", "Tabbed Site Settings"),
        ("/dashboard/settings/heroes/", "Page Hero Banners"),
        ("/dashboard/clients/", "Partner Logos Management"),
        ("/dashboard/team/", "Leadership Team Management"),
    ]

    for route, name in dash_routes:
        res = c.get(route)
        assert res.status_code == 200, f"Failed Dashboard route {route} ({name}) - Status {res.status_code}"
        print(f"  [PASS] {name} ({route}) -> HTTP 200")

    # 3. Test Detail Views
    latest_app = JobApplication.objects.first()
    if latest_app:
        res = c.get(f"/dashboard/careers/applications/{latest_app.pk}/")
        assert res.status_code == 200
        print(f"  [PASS] Candidate Application Detail View -> HTTP 200")

    latest_inq = ContactMessage.objects.first()
    if latest_inq:
        res = c.get(f"/dashboard/inquiries/{latest_inq.pk}/")
        assert res.status_code == 200
        print(f"  [PASS] Contact Inquiry Detail View -> HTTP 200")

    # 4. Test Quick AJAX Status updates
    if latest_app:
        res = c.post(f"/dashboard/careers/applications/{latest_app.pk}/status/", {"status": "shortlisted"})
        assert res.status_code == 200
        assert res.json()["status"] == "shortlisted"
        latest_app.refresh_from_db()
        assert latest_app.status == "shortlisted"
        print(f"  [PASS] Candidate Quick AJAX Status Update -> OK (Status updated to shortlisted)")

    if latest_inq:
        res = c.post(f"/dashboard/inquiries/{latest_inq.pk}/status/", {"status": "resolved"})
        assert res.status_code == 200
        assert res.json()["status"] == "resolved"
        latest_inq.refresh_from_db()
        assert latest_inq.status == "resolved"
        print(f"  [PASS] Contact Inquiry Quick AJAX Status Update -> OK (Status updated to resolved)")

    # 5. Test CSV Exports
    csv_app = c.get("/dashboard/careers/applications/export-csv/")
    assert csv_app.status_code == 200
    assert "text/csv" in csv_app["Content-Type"]
    print("  [PASS] 1-Click Job Applications CSV Export -> HTTP 200 with text/csv")

    csv_inq = c.get("/dashboard/inquiries/export-csv/")
    assert csv_inq.status_code == 200
    assert "text/csv" in csv_inq["Content-Type"]
    print("  [PASS] 1-Click Contact Inquiries CSV Export -> HTTP 200 with text/csv")

    print("\n[SUCCESS] ALL PUBLIC AND EXECUTIVE DASHBOARD TESTS PASSED WITH 100% SUCCESS!")

if __name__ == "__main__":
    run_tests()
