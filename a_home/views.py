from django.http import HttpRequest
from django.shortcuts import redirect


def home_view(request: HttpRequest):
    return redirect("/blog")
