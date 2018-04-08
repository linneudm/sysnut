# -*- coding: utf8 -*-
from django.forms import ModelForm
from django import forms
from django.forms.utils import ErrorList
from .models import Food, UploadSheet, Measure
from dal import autocomplete

class FoodForm(ModelForm):

	class Meta:
		model = Food
		fields = '__all__'
MeasureFormSet = forms.inlineformset_factory(Food, Measure, fields=('measure_unity','weight'),extra=1)

class UploadSheetForm(ModelForm):

	class Meta:
		model = UploadSheet
		exclude = ['created_at']

