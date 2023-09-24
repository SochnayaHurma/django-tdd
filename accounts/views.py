from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.contrib import messages
from django.urls import reverse
from django.contrib import auth

from accounts.models import Token
from accounts.utils import add_get_params


def send_login_email(request: HttpRequest) -> HttpResponse:
    email = request.POST.get("email")
    if email and len(email.split("@")) == 2:
        token = Token.objects.create(email=email)
        url = request.build_absolute_uri(
            add_get_params(
                url=reverse("accounts:login"),
                token=token.uid
            )
        )
        send_mail(
            'Your login link for Superlists',
            f'Your login link for Superlists {url}',
            settings.EMAIL_HOST_USER,
            [email]
        )
        messages.success(request, "Check your email")

    return redirect("/")


def login(request: HttpRequest) -> HttpResponse:
    """
    Представление входа в систему
    """
    token = request.GET.get("token")
    user = auth.authenticate(uid=token)
    if user:
        auth.login(request, user)
    return redirect("/")
