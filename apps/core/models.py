from django.db import models


class SiteSettings(models.Model):
    phone_sale = models.CharField(max_length=64, blank=True)
    phone_support = models.CharField(max_length=64, blank=True)
    email_support = models.EmailField(blank=True)
    email_sale = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    map_url = models.URLField(blank=True)
    social_links = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return "Site settings"

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Testimonial(models.Model):
    client_name = models.CharField(max_length=120)
    position = models.CharField(max_length=120, blank=True)
    company = models.CharField(max_length=120, blank=True)
    quote = models.TextField()
    avatar = models.ImageField(upload_to="testimonials/", blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "client_name"]

    def __str__(self):
        return self.client_name


class ClientLogo(models.Model):
    name = models.CharField(max_length=120)
    logo_image = models.ImageField(upload_to="clients/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    name = models.CharField(max_length=120)
    position = models.CharField(max_length=120)
    photo = models.ImageField(upload_to="team/")
    quote = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class ServiceItem(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=80, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}>"


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
        return [r.strip() for r in self.requirements.splitlines() if r.strip()]

    @property
    def responsibilities_list(self):
        if not self.responsibilities:
            return []
        return [r.strip() for r in self.responsibilities.splitlines() if r.strip()]

    @property
    def benefits_list(self):
        if not self.benefits:
            return []
        return [b.strip() for b in self.benefits.splitlines() if b.strip()]


class JobApplication(models.Model):
    job = models.ForeignKey(JobOpening, on_delete=models.CASCADE, related_name="applications")
    full_name = models.CharField(max_length=140)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    cover_note = models.TextField(blank=True)
    resume = models.FileField(upload_to="resumes/", blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]
        verbose_name = "Job Application"
        verbose_name_plural = "Job Applications"

    def __str__(self):
        return f"{self.full_name} - {self.job.title}"

