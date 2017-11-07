# -*- coding: utf-8 -*-

from django.forms import ModelForm
from django import forms
from .models import *
from sysnut.food.models import Meal
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
	patology = forms.ModelChoiceField(
			queryset=Patology.objects.all(),
			widget = autocomplete.ModelSelect2(url='patient:patology_autocomplete')
		)
	class Meta:
		model = Consultation
		exclude = ['bodycirc', 'energycalc', 'skinfold']
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
	class Meta:
		model = Meal
		fields = ['original_food', 'meal', 'weight', 'home_measure']