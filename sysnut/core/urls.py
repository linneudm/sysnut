from django.conf.urls import url
from .views import *

urlpatterns = [
	# Home
    url(r'^$', index, name='index'),
    url(r'instructions/$', instructions, name='instructions'),
    url(r'about/$', about, name='about'),
]
