from datetime import date
from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class BlogPage(Page):
    body = RichTextField(blank=True)

    template = "a_blog/blog_page.html"
    content_panels = Page.content_panels + [FieldPanel("body")]

    def get_context(self, request, *args, **kwargs):
        articles = self.get_children().live().order_by("-first_published_at")
        context = super().get_context(request, *args, **kwargs)
        context["articles"] = articles
        return context


class ArticlePage(Page):
    intro = models.CharField(max_length=80)
    body = RichTextField(blank=True)
    date = models.DateField("Post date", default=date.today)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    caption = models.CharField(max_length=80, blank=True)

    template = "a_blog/article_page.html"
    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("image"),
        FieldPanel("caption"),
        FieldPanel("body"),
        FieldPanel("date"),
    ]
