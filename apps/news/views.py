from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView, TemplateView

from .models import NewsCategory, Post


DEMO_ARTICLES = [
    {
        "title": "Advancing Egypt's Water & Municipal Infrastructure Networks",
        "slug": "advancing-egypts-water-infrastructure-networks",
        "category_name": "Infrastructure",
        "category_slug": "infrastructure",
        "cover_image": "img/news/news-article1-recovered.png",
        "published_at": "October 15, 2026",
        "author": "Infrastructure Division",
        "excerpt": (
            "Al Bahaa continues to expand its Grade A infrastructure division, executing "
            "critical municipal water transmission lines and automated pumping station networks "
            "engineered to exacting national QA/QC benchmarks."
        ),
        "content": (
            "Across three decades of engineering leadership, Al Bahaa Contracting (S.A.E) has maintained "
            "an uncompromising commitment to executing Egypt's most critical civil and municipal infrastructure works. "
            "Our latest milestone encompasses the deployment of large-diameter ductile iron and HDPE water transmission mains, "
            "engineered with modern trenchless technology to minimize urban disruption while ensuring structural longevity.\n\n"
            "The engineering scope integrates multi-stage surge protection systems, cathodic protection against high-salinity "
            "subsurface conditions, and automated telemetry for real-time flow and pressure monitoring. "
            "With active Grade A classification from the Egyptian Federation for Construction, our teams adhere to the strictest "
            "quality assurance protocols from geotechnical excavation through to hydrostatic pressure testing."
        ),
        "highlights": [
            {"label": "Project Scope", "value": "42 km Municipal Transmission Main"},
            {"label": "Engineering Standard", "value": "Grade A Infrastructure Compliance"},
            {"label": "Technology", "value": "Trenchless Microtunneling & Automated Telemetry"},
            {"label": "QA/QC Benchmark", "value": "Zero-Defect Hydrostatic Testing"}
        ]
    },
    {
        "title": "Pioneering Quality Control & Structural Milestones in Civil Works",
        "slug": "pioneering-quality-control-structural-milestones",
        "category_name": "Civil Works",
        "category_slug": "civil-works",
        "cover_image": "img/news/news-article2-recovered.png",
        "published_at": "September 28, 2026",
        "author": "Technical Office & QA/QC",
        "excerpt": (
            "Achieving zero-defect concrete pours on high-capacity commercial and administrative "
            "structures through synchronized batch plant monitoring and thermal crack analysis."
        ),
        "content": (
            "Mass concrete placement in demanding climate conditions requires rigorous thermal management and continuous "
            "monitoring. Al Bahaa's technical office recently delivered a milestone 3,200 m³ continuous raft foundation pour, "
            "utilizing low-heat Portland cement formulations combined with embedded thermocouple sensors.\n\n"
            "By implementing strict pre-pour mockups, digital slump verification, and temperature-controlled curing regimes, "
            "our structural engineering teams prevented thermal differential cracking while achieving target compressive strength "
            "well within standard curing cycles. This disciplined execution reinforces our reputation as a trusted partner for prime developments."
        ),
        "highlights": [
            {"label": "Continuous Pour", "value": "3,200 m³ Structural Raft"},
            {"label": "Monitoring", "value": "Embedded Digital Thermal Sensors"},
            {"label": "Curing Regimen", "value": "Automated Moisture & Thermal Retention"},
            {"label": "Safety Milestone", "value": "500,000 Safe Working Hours"}
        ]
    },
    {
        "title": "Sustainable High-Performance Facade Engineering in Modern Developments",
        "slug": "sustainable-high-performance-facade-engineering",
        "category_name": "Architecture",
        "category_slug": "architecture",
        "cover_image": "img/news/news-article3-recovered.png",
        "published_at": "August 14, 2026",
        "author": "Architectural Engineering Team",
        "excerpt": (
            "Integrating climate-resilient envelope technologies and double-glazed curtain wall "
            "systems to optimize thermal performance across contemporary corporate headquarters."
        ),
        "content": (
            "Contemporary architectural landmarks demand a harmonious balance between expressive geometric design and high-efficiency "
            "energy performance. Al Bahaa's architectural division specializes in engineering unitized curtain wall facades, "
            "acoustic barrier envelopes, and bespoke solar-shading louvers tailored to the climatic demands of Egypt.\n\n"
            "Our engineering methodology encompasses precise 3D BIM coordination, wind tunnel simulation validation, "
            "and on-site air/water infiltration testing to guarantee enduring envelope integrity and occupant comfort."
        ),
        "highlights": [
            {"label": "Envelope Type", "value": "Unitized High-Efficiency Curtain Wall"},
            {"label": "Energy Performance", "value": "35% Reduction in Solar Heat Gain (SHGC)"},
            {"label": "BIM Integration", "value": "LOD 400 MEP & Structural Coordination"},
            {"label": "Testing", "value": "Dynamic Water Penetration & Wind Load Certified"}
        ]
    },
    {
        "title": "Turnkey Electromechanical & MEP Integration for Prime Landmarks",
        "slug": "turnkey-electromechanical-mep-integration",
        "category_name": "Electromechanical",
        "category_slug": "electromechanical",
        "cover_image": "img/news/news-article4-recovered.png",
        "published_at": "July 02, 2026",
        "author": "MEP Operations Division",
        "excerpt": (
            "Delivering integrated firefighting, HVAC, substation distribution, and building "
            "management systems (BMS) with seamless architectural coordination."
        ),
        "content": (
            "Complex landmark projects require seamless synchronization between heavy structural frameworks and sophisticated MEP systems. "
            "Al Bahaa provides comprehensive turnkey electromechanical solutions, from primary medium-voltage transformer stations "
            "and central chiller plants to intelligent automated building management systems (BMS).\n\n"
            "By coordinating multi-service containment corridors in BIM before field installation, our MEP teams eliminate on-site clashes, "
            "accelerate project schedules, and ensure long-term ease of maintenance for building operators."
        ),
        "highlights": [
            {"label": "Substation Capacity", "value": "Dual 11kV/0.4kV Transformers"},
            {"label": "HVAC Centralization", "value": "VAV Energy-Recovery Air Handlers"},
            {"label": "Automation", "value": "BACnet Integrated Building Management"},
            {"label": "Compliance", "value": "NFPA 13 & Civil Defense Certified"}
        ]
    },
]


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
        
        # Categories with count
        context["categories"] = NewsCategory.objects.annotate(
            posts_count=Count("post")
        )
        context["selected_category"] = self.request.GET.get("category", "all")
        context["total_posts_count"] = Post.objects.filter(is_published=True).count()

        # Hybrid fallback when database has no news posts
        if not db_posts:
            selected_cat = self.request.GET.get("category", "all")
            filtered_demo = DEMO_ARTICLES
            if selected_cat and selected_cat != "all":
                filtered_demo = [a for a in DEMO_ARTICLES if a["category_slug"] == selected_cat]
            
            # Map demo articles with reverse flag for alternating layout
            for idx, article in enumerate(filtered_demo):
                article["reverse"] = (idx % 2 == 1)

            context["articles"] = filtered_demo
            context["is_demo"] = True
            context["total_posts_count"] = len(DEMO_ARTICLES)
            context["demo_categories"] = [
                {"name": "Infrastructure", "slug": "infrastructure", "posts_count": 1},
                {"name": "Civil Works", "slug": "civil-works", "posts_count": 1},
                {"name": "Architecture", "slug": "architecture", "posts_count": 1},
                {"name": "Electromechanical", "slug": "electromechanical", "posts_count": 1},
            ]
        else:
            # Map DB posts with reverse flag
            for idx, post in enumerate(db_posts):
                post.reverse = (idx % 2 == 1)
            context["articles"] = db_posts
            context["is_demo"] = False

        return context


class NewsDetailView(DetailView):
    model = Post
    template_name = "pages/news_detail.html"
    context_object_name = "post"
    slug_url_kwarg = "slug"

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        # Check DB first
        if Post.objects.filter(slug=slug, is_published=True).exists():
            return Post.objects.select_related("category").get(slug=slug, is_published=True)
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        obj = self.object

        if obj is None:
            # Look up in demo articles
            matching = next((a for a in DEMO_ARTICLES if a["slug"] == slug), DEMO_ARTICLES[0])
            context["article"] = matching
            context["is_demo"] = True
            context["current_category_slug"] = matching.get("category_slug", "")
            context["categories"] = [
                {"name": "Infrastructure", "slug": "infrastructure", "posts_count": 1},
                {"name": "Civil Works", "slug": "civil-works", "posts_count": 1},
                {"name": "Architecture", "slug": "architecture", "posts_count": 1},
                {"name": "Electromechanical", "slug": "electromechanical", "posts_count": 1},
            ]
            context["recent_articles"] = [a for a in DEMO_ARTICLES if a["slug"] != matching["slug"]][:3]
            context["related_articles"] = context["recent_articles"]
        else:
            context["article"] = obj
            context["is_demo"] = False
            context["current_category_slug"] = obj.category.slug if obj.category else ""
            context["categories"] = Category.objects.filter(is_active=True).annotate(
                posts_count=Count("posts", filter=Q(posts__is_published=True))
            )
            context["recent_articles"] = Post.objects.filter(
                is_published=True
            ).exclude(id=obj.id).select_related("category")[:3]
            context["related_articles"] = context["recent_articles"]

        return context
