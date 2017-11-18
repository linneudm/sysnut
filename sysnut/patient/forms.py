# -*- coding: utf-8 -*-

from django.forms import ModelForm
from django import forms
from .models import *
from sysnut.food.models import Meal, Food
from multiupload.fields import MultiFileField
from dal import autocomplete


class PatientForm(ModelForm):

	class Meta:
		model = Patient
		exclude = ['address', 'user']

class AddressForm(ModelForm):

	class Meta:
		model = Address
		exclude = ['content_type','content_object','object_id']

class BodyCircunferenceForm(ModelForm):

	class Meta:
		model = BodyCircunference
		fields = '__all__'

class EnergyCalcForm(ModelForm):

	class Meta:
		model = EnergyCalc
		exclude = ['mbr']

class SkinFoldForm(ModelForm):

	class Meta:
		model = SkinFold
		fields = '__all__'

class ConsultationForm(ModelForm):
	class Meta:
		model = Consultation
		exclude = ['patient', 'bodycirc', 'energycalc', 'skinfold']
		widgets = {
    		'patology': autocomplete.ModelSelect2Multiple(url='patient:patology_autocomplete')
		}
ExamFormSet = forms.inlineformset_factory(Consultation, Exam, fields=('description','path'),extra=1)

class PatologyForm(ModelForm):
	class Meta:
		model = Patology
		fields = '__all__'

class FoodAnalysisForm(ModelForm):
	class Meta:
		model = FoodAnalysis
		fields = ['description', 'published']


class MealForm(ModelForm):
	original_food = forms.ModelChoiceField(
			queryset=Food.objects.all(),
			widget = autocomplete.ModelSelect2(url='patient:food_autocomplete')
		)
	class Meta:
		model = Meal
		fields = ['meal', 'weight', 'home_measure', 'original_food']