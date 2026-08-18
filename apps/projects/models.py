from django.db import models
from django.urls import reverse


class ProjectCategory(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "project categories"

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_ONGOING = "ongoing"
    STATUS_COMPLETED = "completed"
    STATUS_CHOICES = (
        (STATUS_ONGOING, "Ongoing"),
        (STATUS_COMPLETED, "Completed"),
    )

    FALLBACK_IMAGES = [
        "img/projects/projects-band-1-recovered.webp",
        "img/projects/projects-band-2-recovered.webp",
        "img/projects/projects-band-3-recovered.webp",
        "img/projects/projects-band-4-recovered.webp",
    ]

    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True, blank=True)
    cover_image = models.ImageField(upload_to="projects/", blank=True)
    short_description = models.TextField(blank=True)
    full_description = models.TextField(blank=True)
    client_name = models.CharField(max_length=160, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_COMPLETED)
    location = models.CharField(max_length=160, blank=True)
    date = models.DateField(null=True, blank=True)
    built_up_area = models.CharField(max_length=100, blank=True)
    scope_of_work = models.CharField(max_length=220, blank=True)
    architect_consultant = models.CharField(max_length=160, blank=True)
    engineering_highlights = models.TextField(blank=True, help_text="One highlight bullet per line")
    sustainability = models.CharField(max_length=220, blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-date", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("projects:detail", kwargs={"slug": self.slug})

    @property
    def image_url(self):
        """Unified property that returns valid URL for template rendering."""
        if self.cover_image:
            try:
                return self.cover_image.url
            except ValueError:
                pass
        fallback_idx = (self.pk or 1) % len(self.FALLBACK_IMAGES)
        return f"/static/{self.FALLBACK_IMAGES[fallback_idx]}"

    @property
    def cover_image_url(self):
        if self.cover_image:
            try:
                return self.cover_image.url
            except ValueError:
                return None
        return None

    @property
    def display_image(self):
        if self.cover_image:
            try:
                return {"url": self.cover_image.url, "is_static": False}
            except ValueError:
                pass
        fallback_idx = (self.pk or 1) % len(self.FALLBACK_IMAGES)
        return {"url": self.FALLBACK_IMAGES[fallback_idx], "is_static": True}

    @property
    def description_paragraphs(self):
        if self.full_description:
            paragraphs = [p.strip() for p in self.full_description.split("\n\n") if p.strip()]
            if paragraphs:
                return paragraphs
        if self.short_description:
            return [self.short_description]
        return [
            "The project delivers specialized construction and structural excellence tailored to modern durability, efficiency, and engineering standards."
        ]

    @property
    def highlights_list(self):
        if self.engineering_highlights:
            lines = [line.strip().lstrip("-•* ") for line in self.engineering_highlights.splitlines() if line.strip()]
            if lines:
                return lines
        return [
            "BIM 3D modeling and multidisciplinary MEP clash coordination prior to site execution.",
            "High-performance structural concrete and post-tensioned slab casting.",
            "Strict adherence to occupational health, safety, and environmental standards.",
        ]


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="projects/gallery/")
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.caption or f"{self.project} image"
