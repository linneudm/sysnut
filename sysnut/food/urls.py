# -*- coding: utf8 -*-
from django.conf.urls import url
from .views import *

urlpatterns = [
	# Home
    url(r'^importar/$', import_sheet, name='import_sheet'),
	# Food
    url(r'^food-autocomplete/$', FoodAutocomplete.as_view(), name='food_autocomplete'),
	url(r'^list/$', permission_required('food:list', raise_exception=True)(FoodList.as_view()), name='list'),
	url(r'^add/$', permission_required('food:add', raise_exception=True)(FoodCreate.as_view()), name='add'),
	url(r'^details/(?P<pk>[0-9]+)/$', permission_required('food:details', raise_exception=True)(FoodDetail.as_view()), name='details'),
	url(r'^edit/(?P<pk>[0-9]+)/$', permission_required('food:edit', raise_exception=True)(FoodUpdate.as_view()), name='edit'),
	url(r'^delete/(?P<pk>[0-9]+)/$', permission_required('food:delete', raise_exception=True)(FoodDelete.as_view()), name='delete'),
    #Meal
	url(r'^meal/list/$', permission_required('food:meal_list', raise_exception=True)(MealList.as_view()), name='meal_list'),
	url(r'^meal/add/$', permission_required('food:meal_add', raise_exception=True)(MealCreate.as_view()), name='meal_add'),
	url(r'^meal/details/(?P<pk>[0-9]+)/$', permission_required('food:meal_details', raise_exception=True)(MealDetail.as_view()), name='meal_details'),
	url(r'^meal/edit/(?P<pk>[0-9]+)/$', permission_required('food:meal_edit', raise_exception=True)(MealUpdate.as_view()), name='meal_edit'),
	url(r'^meal/delete/(?P<pk>[0-9]+)/$', permission_required('food:meal_delete', raise_exception=True)(MealDelete.as_view()), name='meal_delete'),
]
