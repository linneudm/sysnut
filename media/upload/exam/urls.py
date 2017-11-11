# -*- coding: utf8 -*-
from django.conf.urls import url
from .views import *

urlpatterns = [
	# Home
    url(r'^upload/$', permission_required('food:upload', raise_exception=True)(UploadSheet.as_view()), name='upload'),
	#url(r'^food-autocomplete/$', FoodAutocomplete.as_view(), name='food_autocomplete'),
  	url(r'^list/$', permission_required('food:list', raise_exception=True)(FoodList.as_view()), name='list'),
	url(r'^add/$', permission_required('food:add', raise_exception=True)(FoodCreate.as_view()), name='add'),
	url(r'^details/(?P<pk>[0-9]+)/$', permission_required('food:details', raise_exception=True)(FoodDetail.as_view()), name='details'),
	url(r'^edit/(?P<pk>[0-9]+)/$', permission_required('food:edit', raise_exception=True)(FoodUpdate.as_view()), name='edit'),
	url(r'^delete/(?P<pk>[0-9]+)/$', permission_required('food:delete', raise_exception=True)(FoodDelete.as_view()), name='delete'),
]
