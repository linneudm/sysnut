# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib.auth.views import *
from django.contrib.auth import views
from .views import *
from .forms import PasswordResetForm



urlpatterns = [
    # Reset Password
    url(r'^password_change/$', password_change, { 'template_name': 'password_change.html', 'post_change_redirect': 'account:password_change_done'}, name='password_change'),
	url(r'^password_change/done/$', password_change_done, { 'template_name': 'password_change_done.html'}, name='password_change_done'),
 	url(r'^password_reset/$', password_reset, { 'from_email': 'Nome <linneu.dm@gmail.com>',
 		 'template_name': 'password_reset.html',
 		 'html_email_template_name': 'password_reset_email.html',
 		 'email_template_name': 'password_reset_email.txt', # Template padrao sem formatação
 		 'post_reset_redirect': 'account:password_reset_done',
 		 'password_reset_form':PasswordResetForm}, name='password_reset'),
 	url(r'^password_reset/done/$', password_reset_done, { 'template_name': 'account/password_reset_done.html'}, name='password_reset_done'),
 	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
 		password_reset_confirm, { 'template_name': 'account/password_reset_confirm.html', 'post_reset_redirect' : 'account:login'}, name='password_reset_confirm'),
 	url(r'^reset/done/$', password_reset_complete, { 'template_name': 'account/password_reset_complete.html'}, name='password_reset_complete'),
    # Login
    url(r'^logout/$', logout_then_login, { 'login_url': '/account/login/' }, name='logout'),
    url(r'^login/$', views.login, {'template_name': 'login.html'}, name='login'),

    #Account
    url(r'^account/edit/$', edit, name='edit'),

]
