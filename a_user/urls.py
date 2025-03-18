from django.urls import path
from . import views


urlpatterns = [
    path("", views.profile_view, name="profile"),
    path("@<str:username>", views.profile_view, name="profile"),
    path("edit/", views.profile_edit_view, name="profile-edit"),
    path("onboarding/", views.profile_edit_view, name="profile-onboarding"),
    path("settings/", views.profile_settings_view, name="profile-settings"),
    path("delete/", views.profile_delete_view, name="profile-delete"),
    path("verify_email/", views.account_verify_email, name="verify-email"),
]
