from django.http import HttpRequest
from django.shortcuts import render
from .models import ArticlePage


def articles_search_view(request: HttpRequest):
    articles = ArticlePage.objects.live().order_by("-first_published_at")
    search_query = request.GET.get("query", "").strip()
    if search_query:
        articles = articles.search(search_query)

    context = {"articles": articles, "search_query": search_query}
    return render(request, "a_blog/blog_page.html", context)
