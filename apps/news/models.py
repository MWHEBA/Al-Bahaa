from django.db import models
from django.urls import reverse


class NewsCategory(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "news categories"

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL, null=True, blank=True)
    cover_image = models.ImageField(upload_to="news/", blank=True)
    author = models.CharField(max_length=120, blank=True, default="Technical Office & QA/QC")
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    published_at = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-published_at", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news:detail", kwargs={"slug": self.slug})

    @property
    def image_url(self):
        if self.cover_image:
            try:
                return self.cover_image.url
            except ValueError:
                pass
        return "/static/img/news/news-article1-recovered.webp"
