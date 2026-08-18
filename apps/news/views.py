from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from .models import NewsCategory, Post


class NewsListView(ListView):
    model = Post
    template_name = "pages/news.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        queryset = Post.objects.select_related("category").filter(is_published=True)
        category_slug = self.request.GET.get("category")
        if category_slug and category_slug != "all":
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        db_posts = list(context["posts"])

        for idx, post in enumerate(db_posts):
            post.reverse = (idx % 2 == 1)

        context["articles"] = db_posts
        context["categories"] = NewsCategory.objects.annotate(
            posts_count=Count("post", filter=Q(post__is_published=True))
        )
        context["selected_category"] = self.request.GET.get("category", "all")
        context["total_posts_count"] = Post.objects.filter(is_published=True).count()

        # Build query string for pagination without 'page' param
        params = self.request.GET.copy()
        if "page" in params:
            params.pop("page")
        context["querystring_without_page"] = params.urlencode()

        return context


class NewsDetailView(DetailView):
    model = Post
    template_name = "pages/news_detail.html"
    context_object_name = "post"
    slug_url_kwarg = "slug"

    def get_object(self, queryset=None):
        return get_object_or_404(
            Post.objects.select_related("category"),
            slug=self.kwargs.get("slug"),
            is_published=True,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.object

        # Previous and Next articles navigation
        prev_post = (
            Post.objects.filter(is_published=True, order__lt=obj.order).order_by("-order", "-published_at").first()
            or Post.objects.filter(is_published=True, id__lt=obj.id).order_by("-id").first()
        )
        next_post = (
            Post.objects.filter(is_published=True, order__gt=obj.order).order_by("order", "published_at").first()
            or Post.objects.filter(is_published=True, id__gt=obj.id).order_by("id").first()
        )

        # Related articles (prioritize same category)
        related_qs = Post.objects.filter(is_published=True).exclude(id=obj.id).select_related("category")
        if obj.category:
            same_cat = list(related_qs.filter(category=obj.category)[:3])
            if len(same_cat) < 3:
                other_articles = list(related_qs.exclude(id__in=[p.id for p in same_cat])[: 3 - len(same_cat)])
                related_articles = same_cat + other_articles
            else:
                related_articles = same_cat
        else:
            related_articles = list(related_qs[:3])

        context["article"] = obj
        context["prev_post"] = prev_post
        context["next_post"] = next_post
        context["current_category_slug"] = obj.category.slug if obj.category else ""
        context["categories"] = NewsCategory.objects.annotate(
            posts_count=Count("post", filter=Q(post__is_published=True))
        )
        context["recent_articles"] = related_articles
        context["related_articles"] = related_articles

        return context
