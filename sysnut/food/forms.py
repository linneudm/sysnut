# -*- coding: utf8 -*-
from django.forms import ModelForm
from django import forms
from django.forms.utils import ErrorList
from .models import Food, Meal
from dal import autocomplete

class FoodForm(ModelForm):

	class Meta:
		model = Food
		fields = '__all__'
