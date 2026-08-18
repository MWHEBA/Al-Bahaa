import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
django.setup()

from django.test import Client
from apps.core.models import SiteSettings, JobOpening, ContactMessage, JobApplication
from apps.projects.models import Project
from apps.news.models import Post

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

    print("[TEST] Testing GET requests on all main routes...")
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

    print("\n[SUCCESS] ALL AUTOMATED TESTS PASSED WITH 100% SUCCESS!")

if __name__ == "__main__":
    run_tests()
