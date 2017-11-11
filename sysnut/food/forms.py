# -*- coding: utf8 -*-
from django.forms import ModelForm
from django import forms
from django.forms.utils import ErrorList
from .models import Food, Meal, UploadSheet
from dal import autocomplete

class FoodForm(ModelForm):

	class Meta:
		model = Food
		fields = '__all__'

class UploadSheetForm(ModelForm):

	class Meta:
		model = UploadSheet
		exclude = ['created_at']

