# -*- coding: utf8 -*-
from django.conf.urls import url
from .views import *

urlpatterns = [
	# Home
    url(r'^upload/$', UploadSheet.as_view(), name='upload'),
	#url(r'^food-autocomplete/$', FoodAutocomplete.as_view(), name='food_autocomplete'),
  	url(r'^list/$',FoodList.as_view(), name='list'),
    url(r'^add/$', FoodCreate.as_view(), name='add'),
	url(r'^remove/$', remove_all, name='remove_all'),
	url(r'^details/(?P<pk>[0-9]+)/$',FoodDetail.as_view(), name='details'),
	url(r'^edit/(?P<pk>[0-9]+)/$',FoodUpdate.as_view(), name='edit'),
	url(r'^delete/(?P<pk>[0-9]+)/$', FoodDelete.as_view(), name='delete'),
]
