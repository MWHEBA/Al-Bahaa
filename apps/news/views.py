from django.views.generic import TemplateView


class NewsListView(TemplateView):
    template_name = "pages/news.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        excerpt = (
            "Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots "
            "in a piece of classical Latin literature from 45 BC, making it over 2000 years "
            "old. Richard McClintock, a Latin professor at Hampden-Sydney College in "
            "Virginia, looked up one of the more obscure Latin words, consectetur, from a "
            "Lorem Ipsum passage, and going through the cites of the word in classical"
        )
        context["articles"] = [
            {"title": "Have a Good Time", "excerpt": excerpt, "image": "img/news/news-article1-recovered.png"},
            {"title": "Have a Good Time", "excerpt": excerpt, "image": "img/news/news-article2-recovered.png", "reverse": True},
            {"title": "Have a Good Time", "excerpt": excerpt, "image": "img/news/news-article3-recovered.png"},
            {"title": "Have a Good Time", "excerpt": excerpt, "image": "img/news/news-article4-recovered.png", "reverse": True},
        ]
        context["pagination_items"] = ["1", "2", "3", "...", "8"]
        return context
