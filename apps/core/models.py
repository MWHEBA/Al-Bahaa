import re
from django.db import models
from django.utils.html import escape, mark_safe


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # Enforce singleton persistence

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SiteSettings(SingletonModel):
    company_name = models.CharField(max_length=160, default="Al Bahaa Contracting (S.A.E)")
    header_logo = models.ImageField(upload_to="branding/", blank=True, help_text="Main navbar logo (SVG or Transparent PNG)")
    footer_logo = models.ImageField(upload_to="branding/", blank=True, help_text="Footer brand logo (Square SVG or PNG)")
    favicon = models.ImageField(upload_to="branding/", blank=True, help_text="Browser Favicon (.svg, .png, .ico, .webp)")

    phone_main = models.CharField(max_length=64, blank=True, default="+20 (2) 2389 9255")
    phone_tenders = models.CharField(max_length=64, blank=True, default="+20 (10) 0123 4567")
    phone_sale = models.CharField(max_length=64, blank=True)
    phone_support = models.CharField(max_length=64, blank=True)

    email_general = models.EmailField(blank=True, default="info@albahaacontracting.com")
    email_tenders = models.EmailField(blank=True, default="tenders@albahaacontracting.com")
    email_careers = models.EmailField(blank=True, default="careers@albahaacontracting.com")
    email_sale = models.EmailField(blank=True)
    email_support = models.EmailField(blank=True)

    address = models.TextField(blank=True, default="Central Hub, Units 213-217, First Settlement, New Cairo, Egypt")
    address_line1 = models.CharField(max_length=180, blank=True, default="Central Hub, Units 213-217")
    address_line2 = models.CharField(max_length=180, blank=True, default="First Settlement, New Cairo, Egypt")

    map_embed_url = models.TextField(
        blank=True,
        default="https://maps.google.com/maps?q=30.0633628,31.4215952+(Al+Bahaa+Contracting+-+Central+Hub)&t=&z=16&ie=UTF8&iwloc=&output=embed",
        help_text="Google Maps Embed URL or full <iframe> snippet (auto-sanitized)",
    )
    map_directions_url = models.URLField(
        blank=True,
        default="https://maps.app.goo.gl/wxBbUA5jU5uGwDTZ7",
        help_text="Direct link for Google Maps directions button",
    )
    map_url = models.URLField(blank=True)

    working_hours_weekdays = models.CharField(
        max_length=140, blank=True, default="Sunday – Thursday: 8:00 AM – 5:00 PM"
    )
    working_hours_emergencies = models.CharField(
        max_length=140, blank=True, default="Friday & Saturday: Site Emergencies Only"
    )

    linkedin_url = models.URLField(blank=True, default="https://linkedin.com", help_text="Official LinkedIn page URL")
    facebook_url = models.URLField(blank=True, default="https://facebook.com", help_text="Official Facebook page URL")
    instagram_url = models.URLField(blank=True, default="https://instagram.com", help_text="Official Instagram page URL")
    youtube_url = models.URLField(blank=True, default="https://youtube.com", help_text="Official YouTube channel URL")

    footer_quote = models.TextField(
        blank=True,
        default="Established in 1986, AlBahaa delivers integrated contracting, finishing, and construction solutions across Egypt.",
    )
    footer_quote_author = models.CharField(max_length=120, blank=True, default="Al Bahaa Contracting")
    copyright_text = models.CharField(
        max_length=160, blank=True, default="© 2026 ALBAHAA CONSTRUCTION. ALL RIGHTS RESERVED"
    )

    class Meta:
        verbose_name = "Site Settings & Identity"
        verbose_name_plural = "Site Settings & Identity"

    def __str__(self):
        return self.company_name or "Site Settings"

    @property
    def social_links(self):
        """Unified dictionary for backward-compatible template rendering."""
        return {
            "linkedin": self.linkedin_url or "",
            "facebook": self.facebook_url or "",
            "instagram": self.instagram_url or "",
            "youtube": self.youtube_url or "",
        }

    @property
    def safe_map_embed_url(self):
        """Auto-sanitizes raw iframe embed snippet if pasted by admin."""
        val = (self.map_embed_url or "").strip()
        if "<iframe" in val:
            match = re.search(r'src=["\']([^"\']+)["\']', val)
            if match:
                return match.group(1)
        return val


class PageHero(models.Model):
    PAGE_CHOICES = (
        ("home", "Home Page"),
        ("about", "About Us Page"),
        ("projects", "Projects Page"),
        ("news", "News Page"),
        ("careers", "Careers Page"),
        ("contact", "Contact Page"),
    )

    FALLBACK_HERO_IMAGES = {
        "home": "img/home/Rectangle 3.webp",
        "about": "img/about/Rectangle 21.webp",
        "projects": "img/projects/projects-hero-banner.webp",
        "news": "img/news/news-hero-banner.webp",
        "careers": "img/careers/careers-hero-banner.webp",
        "contact": "img/contact/contact-hero-recovered.webp",
    }

    page = models.CharField(max_length=30, choices=PAGE_CHOICES, unique=True)
    eyebrow = models.CharField(max_length=140, blank=True)
    title_line1 = models.CharField(max_length=160, blank=True, help_text="Architectural Title Line 1")
    title_line2 = models.CharField(max_length=160, blank=True, help_text="Architectural Title Line 2 (Optional)")
    description = models.TextField(blank=True)
    hero_image = models.ImageField(upload_to="heroes/", blank=True, help_text="Hero banner (Recommended: 1920x1080px, Max 2MB)")

    class Meta:
        verbose_name = "Page Hero Banner"
        verbose_name_plural = "Page Hero Banners"
        ordering = ["page"]

    def __str__(self):
        return f"{self.get_page_display()} Banner"

    @property
    def title_html(self):
        if self.title_line1 and self.title_line2:
            return mark_safe(f"{escape(self.title_line1)}<br>{escape(self.title_line2)}")
        if self.title_line1 or self.title_line2:
            return escape(self.title_line1 or self.title_line2)
        return ""

    @property
    def image_url(self):
        if self.hero_image:
            try:
                return self.hero_image.url
            except ValueError:
                pass
        fallback = self.FALLBACK_HERO_IMAGES.get(self.page, "img/home/Rectangle 3.png")
        return f"/static/{fallback}"


class HomeContent(SingletonModel):
    blueprints_eyebrow = models.CharField(max_length=120, blank=True, default="OUR SPECIALIZATION")
    blueprints_title_line1 = models.CharField(max_length=160, default="WE TURN BLUEPRINTS INTO")
    blueprints_title_line2 = models.CharField(max_length=160, default="ENDURING REALITY.")
    blueprints_description = models.TextField(
        default="With more than three decades of engineering leadership and active membership in the Egyptian Federation for Construction, Al Bahaa delivers turnkey civil, residential, and infrastructure landmarks on schedule, within budget, and to the highest QA/QC standards."
    )
    blueprints_btn_text = models.CharField(max_length=60, default="View More")
    blueprints_btn_url = models.CharField(max_length=120, default="/about/")
    blueprints_image = models.ImageField(upload_to="home/", blank=True, help_text="Blueprints section photo (Recommended: 700x900px)")

    class Meta:
        verbose_name = "Home Page Specific Content"
        verbose_name_plural = "Home Page Specific Content"

    def __str__(self):
        return "Home Page Content"


class SpecializationItem(models.Model):
    discipline = models.CharField(max_length=140, default="GRADE A INFRASTRUCTURE", help_text="Primary bold uppercase discipline heading")
    title = models.CharField(max_length=140, blank=True, help_text="Full discipline title")
    description = models.TextField(help_text="Detailed engineering capability description")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Specialization Slide"
        verbose_name_plural = "Specialization Slides (Home Slider)"

    def __str__(self):
        return f"{self.discipline} - {self.title or ''}"


class AboutContent(SingletonModel):
    who_we_are_title = models.CharField(max_length=120, default="WHO WE ARE")
    who_we_are_p1 = models.TextField(
        default="Albahaa Contracting is an Egyptian joint stock company (S.A.E) with more than 30 years of engineering and contracting experience. Established in 1986, Albahaa began its initial projects under the ownership of Engineer Mohamed Bahaa El Din Abdalla before formally transitioning into a joint stock company on December 14, 2000."
    )
    who_we_are_p2 = models.TextField(
        default="As an active member of the Egyptian Federation for Construction and Building Contractors since 1994, Albahaa holds the prestigious Grade A classification in water and sewage infrastructure networks, delivering turnkey civil, residential, and infrastructure landmarks on schedule and within budget."
    )

    cta_eyebrow = models.CharField(max_length=120, default="START A PROJECT")
    cta_title = models.CharField(max_length=160, default="Ready to build something iconic?")
    cta_description = models.TextField(
        default="Consult with our multidisciplinary engineering teams to bring technical precision and turnkey execution to your next landmark development."
    )
    cta_primary_btn_text = models.CharField(max_length=60, default="Contact Our Team")
    cta_primary_btn_url = models.CharField(max_length=120, default="/contact/")
    cta_secondary_btn_text = models.CharField(max_length=60, default="Explore Projects")
    cta_secondary_btn_url = models.CharField(max_length=120, default="/projects/")

    class Meta:
        verbose_name = "About Page Specific Content"
        verbose_name_plural = "About Page Specific Content"

    def __str__(self):
        return "About Page Content"


class AboutStatistic(models.Model):
    value = models.CharField(max_length=30, help_text="e.g. 30+, Grade A, 1994, S.A.E")
    label = models.CharField(max_length=140, help_text="e.g. Years of Industry Experience (Est. 1986)")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Company Credential & Stat"
        verbose_name_plural = "Company Credentials & Stats (About Page)"

    def __str__(self):
        return f"{self.value} - {self.label}"


class CompanyPillar(models.Model):
    number = models.CharField(max_length=10, default="01", help_text="e.g. 01, 02, 03")
    title = models.CharField(max_length=140)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Engineering Pillar"
        verbose_name_plural = "Engineering Pillars (About Page)"

    def __str__(self):
        return f"{self.number}. {self.title}"


class TeamMember(models.Model):
    MEMBER_TYPE_CHOICES = (
        ("founder", "Founding Heritage Card"),
        ("executive", "Executive Board Member"),
        ("general", "General Team Member"),
    )

    name = models.CharField(max_length=120)
    position = models.CharField(max_length=120)
    member_type = models.CharField(max_length=20, choices=MEMBER_TYPE_CHOICES, default="general")
    photo = models.ImageField(upload_to="team/", blank=True, help_text="Member photo (Recommended: 600x700px)")
    quote = models.TextField(blank=True, help_text="Executive quote or vision statement")
    bio = models.TextField(blank=True, help_text="Detailed biography (especially for founder)")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Leadership & Team Member"
        verbose_name_plural = "Leadership & Team Members"

    def __str__(self):
        return f"{self.name} ({self.get_member_type_display()})"

    @property
    def image_url(self):
        if self.photo:
            try:
                return self.photo.url
            except ValueError:
                pass
        return "/static/img/team/Rectangle 24.webp"


class ServiceItem(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=80, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "What We Do Item"
        verbose_name_plural = "What We Do Services (About Page)"

    def __str__(self):
        return self.title


class CareerSettings(SingletonModel):
    spontaneous_eyebrow = models.CharField(max_length=120, default="SPONTANEOUS APPLICATION")
    spontaneous_title = models.CharField(max_length=160, default="Didn't find the right role for you?")
    spontaneous_description = models.TextField(
        default="We are constantly seeking passionate engineers, BIM coordinators, and construction managers. Send your CV and portfolio directly to our recruitment team, and we will contact you when a fitting opportunity opens."
    )
    spontaneous_btn_text = models.CharField(max_length=60, default="Send Your CV")
    spontaneous_email = models.EmailField(default="careers@albahaacontracting.com")

    class Meta:
        verbose_name = "Careers Page Specific Settings"
        verbose_name_plural = "Careers Page Specific Settings"

    def __str__(self):
        return "Careers Page Settings"


class CareerPillar(models.Model):
    number = models.CharField(max_length=10, default="01", help_text="e.g. 01, 02, 03")
    title = models.CharField(max_length=140)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Culture & Value Pillar"
        verbose_name_plural = "Culture & Values Pillars (Careers Page)"

    def __str__(self):
        return f"{self.number}. {self.title}"


class Testimonial(models.Model):
    client_name = models.CharField(max_length=120)
    position = models.CharField(max_length=120, blank=True)
    company = models.CharField(max_length=120, blank=True)
    quote = models.TextField()
    avatar = models.ImageField(upload_to="testimonials/", blank=True)
    show_on_home = models.BooleanField(default=True)
    show_on_about = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_accent = models.BooleanField(default=False, help_text="Highlight card with dark background")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "client_name"]
        verbose_name = "Client Testimonial"
        verbose_name_plural = "Client Testimonials"

    def __str__(self):
        return f"{self.client_name} ({self.company or self.position})"


class ClientLogo(models.Model):
    FALLBACK_LOGOS = [
        "img/clients/Layer 1.webp",
        "img/clients/Layer 2.webp",
        "img/clients/Layer 3.webp",
        "img/clients/Layer 4.webp",
        "img/clients/Layer 5.webp",
        "img/clients/Layer 6.webp",
        "img/clients/l3.webp",
        "img/clients/logo_partner-3.webp",
        "img/clients/11.webp",
        "img/clients/logo_partner-8.webp",
        "img/clients/l4.webp",
        "img/clients/Layer 1 copy.webp",
    ]

    name = models.CharField(max_length=120)
    logo_image = models.ImageField(upload_to="clients/", blank=True, help_text="Partner Logo (Transparent PNG or SVG, 1:1 or 4:3)")
    show_on_home = models.BooleanField(default=True)
    show_on_about = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Client / Partner Logo"
        verbose_name_plural = "Client & Partner Logos"

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        if self.logo_image:
            try:
                return self.logo_image.url
            except ValueError:
                pass
        fallback_idx = (self.pk or 1) % len(self.FALLBACK_LOGOS)
        return f"/static/{self.FALLBACK_LOGOS[fallback_idx]}"


class ContactMessage(models.Model):
    INQUIRY_CHOICES = (
        ("tenders", "Tenders & Project Estimations"),
        ("procurement", "Subcontractors & Supplier Registration"),
        ("general", "General Inquiries & Client Relations"),
        ("consulting", "Engineering & Architectural Coordination"),
        ("other", "Other Inquiries"),
    )
    STATUS_CHOICES = (
        ("unread", "New / Unread"),
        ("read", "Reviewed"),
        ("resolved", "Resolved / Contacted"),
    )

    name = models.CharField(max_length=120)
    company = models.CharField(max_length=140, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    inquiry_type = models.CharField(max_length=60, choices=INQUIRY_CHOICES, default="general")
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="unread")
    is_read = models.BooleanField(default=False)
    internal_notes = models.TextField(blank=True, help_text="Private internal response notes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries Inbox"

    def __str__(self):
        return f"{self.name} <{self.email}> - {self.get_inquiry_type_display()}"


class JobDepartment(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Job Department"
        verbose_name_plural = "Job Departments"

    def __str__(self):
        return self.name


class JobOpening(models.Model):
    JOB_TYPE_CHOICES = (
        ("Full-Time", "Full-Time"),
        ("Part-Time", "Part-Time"),
        ("Contract", "Contract"),
    )

    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    department = models.ForeignKey(JobDepartment, on_delete=models.SET_NULL, null=True, blank=True, related_name="jobs")
    location = models.CharField(max_length=140, default="New Cairo, Egypt")
    job_type = models.CharField(max_length=40, choices=JOB_TYPE_CHOICES, default="Full-Time")
    experience = models.CharField(max_length=60, default="5-8 Years")
    summary = models.TextField()
    responsibilities = models.TextField(help_text="One bullet per line", blank=True)
    requirements = models.TextField(help_text="One bullet per line")
    benefits = models.TextField(help_text="One bullet per line", blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Job Opening"
        verbose_name_plural = "Job Openings"

    def __str__(self):
        return self.title

    @property
    def requirements_list(self):
        if not self.requirements:
            return []
        return [r.strip().lstrip("-•* ") for r in self.requirements.splitlines() if r.strip()]

    @property
    def responsibilities_list(self):
        if not self.responsibilities:
            return []
        return [r.strip().lstrip("-•* ") for r in self.responsibilities.splitlines() if r.strip()]

    @property
    def benefits_list(self):
        if not self.benefits:
            return []
        return [b.strip().lstrip("-•* ") for b in self.benefits.splitlines() if b.strip()]


class JobApplication(models.Model):
    STATUS_CHOICES = (
        ("new", "New Application"),
        ("reviewed", "Under Review"),
        ("shortlisted", "Shortlisted for Interview"),
        ("rejected", "Archived / Rejected"),
    )

    job = models.ForeignKey(JobOpening, on_delete=models.CASCADE, related_name="applications")
    full_name = models.CharField(max_length=140)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    cover_note = models.TextField(blank=True)
    resume = models.FileField(upload_to="resumes/%Y/%m/", blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    internal_notes = models.TextField(blank=True, help_text="Internal HR evaluation notes")
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]
        verbose_name = "Job Application"
        verbose_name_plural = "Job Applications Inbox"

    def __str__(self):
        return f"{self.full_name} - {self.job.title}"
