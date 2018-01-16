from django.conf.urls import url
from .views import *

urlpatterns = [
	# Home
    url(r'^$', index, name='index'),
    url(r'welcome/$', welcome, name='welcome'),
    url(r'about/$', about, name='about'),
]
