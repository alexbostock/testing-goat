from django.contrib import auth, messages
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from accounts.models import Token
import superLists.settings as settings

def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + '?token=' + str(token.uid)
    )
    send_mail(
        'Sign in to SuperLists',
        f'Use this link to sign in:\n\n{url}',
        settings.EMAIL_HOST_USER,
        [email],
    )
    messages.success(
        request,
        'Check your email for your unique login link.'
    )
    return redirect('/')

def login(request):
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')
