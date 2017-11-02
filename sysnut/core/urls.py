from django.conf.urls import url
from .views import *

urlpatterns = [
	# Home
    url(r'^$', index, name='index'),
]
