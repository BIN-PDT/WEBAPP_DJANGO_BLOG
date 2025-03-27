from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.core.exceptions import ImmediateHttpResponse
from django.contrib import messages
from django.shortcuts import resolve_url, redirect


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_signup_redirect_url(self, request):
        return resolve_url("profile-onboarding")


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user = request.user
        email_addresses = [e.email for e in sociallogin.email_addresses]

        if user.is_authenticated:
            if sociallogin.is_existing:
                messages.error(request, "Social account is already in use!")
            else:
                if user.email in email_addresses:
                    sociallogin.connect(request, user)
                    email_address = EmailAddress.objects.get_primary(user=user)
                    if not email_address.verified:
                        email_address.verified = True
                        email_address.save()
                    messages.success(request, "Link social account successfully!")
                else:
                    messages.error(request, "Invalid social account!")
            raise ImmediateHttpResponse(redirect("profile-settings"))

        if not sociallogin.is_existing:
            if EmailAddress.objects.filter(email__in=email_addresses).exists():
                messages.error(request, "Email is already linked to another account!")
                raise ImmediateHttpResponse(redirect("account_login"))
