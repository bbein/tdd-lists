"""
Account app views.
"""

from django.shortcuts import redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib import auth
from django.core.urlresolvers import reverse

from accounts.models import Token

def send_login_email(request):
    """
    view that sends the login email
    """
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        f'{reverse("login")}?token={token.uid}')
    message_body = f'Use this link to log in:\n\n{url}'
    send_mail(
        'Your login link for Superlists',
        message_body,
        'noreply@superlists.com',
        [email]
    )
    messages.success(request,
                     "Check your email, we've sent you a link tou can use to log in")
    return redirect('/')

def login(request):
    """
    view that is displayed after the login
    """
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')
