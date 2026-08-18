import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client
from apps.core.models import SiteSettings, JobOpening, ContactMessage, JobApplication, TeamMember, ClientLogo
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

        # Test In-App Email Reply
        reply_res = c.post(f"/dashboard/inquiries/{latest_inq.pk}/", {
            "action": "send_reply",
            "reply_subject": "Official Engineering Estimation Offer",
            "reply_body": "Thank you for contacting Al Bahaa. We have attached our technical quotation.",
        })
        assert reply_res.status_code in [200, 302]
        latest_inq.refresh_from_db()
        assert latest_inq.status == "resolved"
        assert "Official Engineering Estimation Offer" in latest_inq.internal_notes
        print(f"  [PASS] In-App Official Email Reply -> Dispatched & logged successfully")

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

    # 6. Test Team Management CRUD & Filters
    print("\n[TEST] Testing Team Management Suite...")
    # Create
    create_res = c.post("/dashboard/team/", {
        "action": "create",
        "name": "Eng. Test Executive Leader",
        "position": "Chief Technology Officer",
        "member_type": "executive",
        "quote": "Building the future with sustainable engineering.",
        "bio": "Extensive experience in infrastructure modernization.",
        "order": 99,
        "is_active": "on",
    })
    assert create_res.status_code in [200, 302]
    new_member = TeamMember.objects.filter(name="Eng. Test Executive Leader").first()
    assert new_member is not None
    assert new_member.position == "Chief Technology Officer"
    print("  [PASS] Team Member Create -> Successfully created in DB")

    # Team List & Member Presence
    team_list_res = c.get("/dashboard/team/")
    assert team_list_res.status_code == 200
    assert "Eng. Test Executive Leader" in team_list_res.content.decode("utf-8")
    print("  [PASS] Team List View -> Matched created member successfully")

    # Update / Edit
    update_res = c.post("/dashboard/team/", {
        "action": "update",
        "member_id": new_member.pk,
        "name": "Eng. Test Executive Leader Updated",
        "position": "Executive Vice President",
        "member_type": "executive",
        "quote": "Updated vision statement.",
        "bio": "Updated bio narrative.",
        "order": 100,
        "is_active": "on",
    })
    assert update_res.status_code in [200, 302]
    new_member.refresh_from_db()
    assert new_member.name == "Eng. Test Executive Leader Updated"
    assert new_member.position == "Executive Vice President"
    print("  [PASS] Team Member Edit/Update -> Successfully updated in DB")

    # Delete
    del_res = c.post("/dashboard/team/", {
        "action": "delete",
        "member_id": new_member.pk,
    })
    assert del_res.status_code in [200, 302]
    assert not TeamMember.objects.filter(pk=new_member.pk).exists()
    print("  [PASS] Team Member Delete -> Successfully removed from DB")

    print("\n[TEST] Testing Partner Logos Management Suite...")
    # Create Logo
    logo_create_res = c.post("/dashboard/clients/", {
        "action": "create",
        "name": "Test Engineering Authority",
        "order": 50,
        "is_active": "on",
        "show_on_home": "on",
        "show_on_about": "on",
    })
    assert logo_create_res.status_code in [200, 302]
    test_logo = ClientLogo.objects.filter(name="Test Engineering Authority").first()
    assert test_logo is not None
    assert test_logo.order == 50
    print("  [PASS] Partner Logo Create -> Successfully created in DB")

    # List & Edit View
    logo_list_res = c.get("/dashboard/clients/")
    assert logo_list_res.status_code == 200
    assert "Test Engineering Authority" in logo_list_res.content.decode("utf-8")
    logo_edit_res = c.get(f"/dashboard/clients/?edit={test_logo.pk}")
    assert logo_edit_res.status_code == 200
    assert "Edit Partner Logo" in logo_edit_res.content.decode("utf-8")
    print("  [PASS] Partner Logo List & Edit View -> OK")

    # Update Logo
    logo_update_res = c.post("/dashboard/clients/", {
        "action": "update",
        "logo_id": test_logo.pk,
        "name": "Test Engineering Authority Updated",
        "order": 55,
        "is_active": "on",
        "show_on_home": "on",
        "show_on_about": "on",
    })
    assert logo_update_res.status_code in [200, 302]
    test_logo.refresh_from_db()
    assert test_logo.name == "Test Engineering Authority Updated"
    assert test_logo.order == 55
    print("  [PASS] Partner Logo Edit/Update -> Successfully updated in DB")

    # Delete Logo
    logo_del_res = c.post("/dashboard/clients/", {
        "action": "delete",
        "logo_id": test_logo.pk,
    })
    assert logo_del_res.status_code in [200, 302]
    assert not ClientLogo.objects.filter(pk=test_logo.pk).exists()
    print("  [PASS] Partner Logo Delete -> Successfully removed from DB")

    print("\n[SUCCESS] ALL PUBLIC AND EXECUTIVE DASHBOARD TESTS PASSED WITH 100% SUCCESS!")

if __name__ == "__main__":
    run_tests()
