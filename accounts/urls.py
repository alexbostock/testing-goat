from django.conf.urls import url
from accounts import views

urlpatterns = [
    url(r'^send-sign-in-email/$', views.send_sign_in_email, name='send_sign_in_email'),
    url(r'^sign-in/', views.sign_in, name='sign_in'),
    url(r'^sign-out/', views.sign_out, name='sign_out'),
]
