from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="avatars/", null=True, blank=True)
    realname = models.CharField(max_length=20, null=True, blank=True)
    biography = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.user)

    @property
    def name(self):
        return self.realname if self.realname else self.user.username

    @property
    def avatar(self):
        return self.image.url if self.image else static("images/avatar.png")
