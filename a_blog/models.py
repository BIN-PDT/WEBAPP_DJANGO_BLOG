from datetime import date
from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager


class BlogPage(Page):
    body = RichTextField(blank=True)

    template = "a_blog/blog_page.html"
    content_panels = Page.content_panels + [FieldPanel("body")]

    def get_context(self, request, *args, **kwargs):
        tag = request.GET.get("tag")
        if tag:
            articles = (
                ArticlePage.objects.live()
                .filter(tags__name=tag)
                .order_by("-first_published_at")
            )
        else:
            articles = self.get_children().live().order_by("-first_published_at")

        context = super().get_context(request, *args, **kwargs)
        context["articles"] = articles
        context["tag"] = tag
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
    tags = ClusterTaggableManager(through="ArticleTag", blank=True)
    views = models.PositiveIntegerField(default=0, editable=False)

    def increase_view_count(self):
        self.views += 1
        self.save(update_fields=["views"])

    def serve(self, request, *args, **kwargs):
        session_key = f"article_viewd_{self.pk}"
        if not request.session.get(session_key, False):
            self.increase_view_count()
            request.session[session_key] = True

        return super().serve(request, *args, **kwargs)

    def image_url(self):
        return self.image.get_rendition("fill-1200x675|jpegquality-80").url

    def get_context(self, request):
        context = super().get_context(request)
        context["image_url"] = self.image_url()
        return context

    def get_tags(self):
        return ", ".join(tag.name for tag in self.tags.all())

    def get_author_realname(self):
        return self.owner.profile.realname

    def get_author_username(self):
        return self.owner.username

    template = "a_blog/article_page.html"
    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("image"),
        FieldPanel("caption"),
        FieldPanel("body"),
        FieldPanel("date"),
        FieldPanel("tags"),
    ]
    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
        index.SearchField("get_tags"),
        index.SearchField("get_author_realname"),
        index.SearchField("get_author_username"),
    ]


class ArticleTag(TaggedItemBase):
    content_object = ParentalKey(
        ArticlePage,
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )
