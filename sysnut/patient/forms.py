# -*- coding: utf-8 -*-

from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm,PasswordResetForm
from sysnut.food.models import MealItem, SubstituteItem, Food
from multiupload.fields import MultiFileField
from dal import autocomplete



class PatientForm(UserCreationForm):

	class Meta:
		model = Patient
		fields = ['username', 'first_name', 'last_name', 'email', 'sex', 'birth_date', 'marital_status', 'phone', 'ocupation', 'observation', 'ethnicity']

class AddressForm(ModelForm):

	class Meta:
		model = Address
		exclude = ['content_type','content_object','object_id']

class BodyCircunferenceForm(ModelForm):

	class Meta:
		model = BodyCircunference
		fields = '__all__'

class BoneDiameterForm(ModelForm):

	class Meta:
		model = BoneDiameter
		fields = '__all__'

class BioimpedanceForm(ModelForm):

	class Meta:
		model = Bioimpedance
		fields = '__all__'

class BiochemicalForm(ModelForm):

	class Meta:
		model = BiochemicalExam
		exclude = ['consultation']
		widgets = {
			'exam': autocomplete.ModelSelect2(url='patient:biochemical_autocomplete')
		}

class EnergyCalcForm(ModelForm):

	class Meta:
		model = EnergyCalc
		exclude = ['mbr', 'tee']

class SkinFoldForm(ModelForm):

	class Meta:
		model = SkinFold
		fields = '__all__'

def get_my_choices():
	MY_CHOICES = (
	    ('1', 'Option 1'),
	    ('2', 'Option 2'),
	    ('3', 'Option 3'),
	)
	return MY_CHOICES

class ConsultationForm(ModelForm):
	class Meta:
		model = Consultation
		exclude = ['patient', 'bodycirc', 'energycalc', 'skinfold', 'bioimpedance', 'bonediameter', 'biochemical']
		widgets = {
    		'patology': autocomplete.ModelSelect2Multiple(url='patient:patology_autocomplete'),
    		#'supplement': autocomplete.ModelSelect2Multiple(url='patient:supplement_autocomplete'),
    		'vitamin': autocomplete.ModelSelect2Multiple(url='patient:vitamin_autocomplete')
		}
ExamFormSet = forms.inlineformset_factory(Consultation, Exam, fields=('description','path'),extra=1)

class PatologyForm(ModelForm):
	class Meta:
		model = Patology
		fields = '__all__'

class FoodAnalysisForm(ModelForm):
	class Meta:
		model = FoodAnalysis
		fields = ['description', 'published', 'guidance']
		widgets = {
    		'guidance': autocomplete.ModelSelect2Multiple(url='nutritionist:guidance_autocomplete')
    		#'guidanceaux': autocomplete.ModelSelect2Multiple(url='patient:guidanceaux_autocomplete')
		}

class UploadGuidanceForm(ModelForm):
	class Meta:
		model = UploadGuidance
		exclude = ['created_at']	


class MealForm(ModelForm):

	class Meta:
		model = MealItem
		fields = ['meal', 'weight', 'original_food', 'home_measure', 'measure_unity']
		widgets = {
    		'original_food': autocomplete.ModelSelect2(url='patient:food_autocomplete'),
		}

class SubstituteMealForm(ModelForm):
	class Meta:
		model = SubstituteItem
		fields = ['weight_substitute', 'food_substitute', 'unity_substitute', 'meal_substitute']
		widgets = {
    		'food_substitute': autocomplete.ModelSelect2(url='patient:food_autocomplete'),
		}
