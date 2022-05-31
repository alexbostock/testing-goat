import uuid
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from accounts.models import Token

def send_sign_in_email(request):
    email = request.POST['email']
    uid = uuid.uuid4()
    Token.objects.create(email=email, uid=uid)
    url = request.build_absolute_uri(f'/accounts/sign-in?uid={uid}')
    print(email)
    print(url)
    send_mail(
        'Sign in to SuperLists',
        f'Use this link to sign in: {url}',
        settings.EMAIL_HOST_USER,
        [email]
    )
    return render(request, 'sign_in_email_sent.html')

def sign_in(request):
    uid = request.GET['uid']
    user = authenticate(uid=uid)
    if user is not None:
        auth_login(request, user)
    return redirect('/')

def sign_out(request):
    auth_logout(request)
    return redirect('/')
