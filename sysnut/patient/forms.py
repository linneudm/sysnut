# -*- coding: utf-8 -*-

from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm,UserChangeForm, PasswordResetForm
from sysnut.food.models import MealItem, SubstituteItem, Food
from datetime import datetime
from multiupload.fields import MultiFileField
from .widgets import ModelSelect2MultipleBootstrap, ModelSelect2Bootstrap
#from dal import autocomplete



class PasswordResetForm(PasswordResetForm):
	def clean_email(self):
		amount = get_user_model()._default_manager.filter(
            email__iexact=self.cleaned_data.get('email'), is_active=True).count()
		if(amount < 1):
			raise forms.ValidationError('Lamentamos, mas não reconhecemos esse endereço de e-mail.')
		return self.cleaned_data.get('email')

class FormulaForm(ModelForm):
	class Meta:
		model = Formula
		fields = '__all__'
FormulaFormSet = forms.inlineformset_factory(Formula, FormulaValue, fields=('name','value'),extra=1)

class PatientForm(UserCreationForm):
	def __init__(self, *args, **kwargs):
		super(PatientForm, self).__init__(*args, **kwargs)
		self.fields['first_name'].required = True
		self.fields['last_name'].required = True
		self.fields['email'].required = True
	class Meta:
		model = Patient
		fields = ['username', 'first_name', 'last_name', 'email', 'sex', 'birth_date', 'marital_status', 'phone', 'ocupation', 'observation', 'ethnicity']

class PatientEditForm(forms.ModelForm):
    

    def __init__(self, *args, **kwargs):
    	super(PatientEditForm, self).__init__(*args, **kwargs)
    	self.fields['first_name'].required = True
    	self.fields['last_name'].required = True
    	self.fields['email'].required = True
#'''
    def clean_birth_date(self):
    	my_date = self.cleaned_data['birth_date']
    	my_date = ('%s' % (my_date))
    	my_date = datetime.strptime(my_date, '%Y-%m-%d').date()
    	if my_date > date.today():
    		raise forms.ValidationError("Data inválida")
    	return my_date

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        # Valido o email para ser obrigatório
        if email == '':
        	raise forms.ValidationError('O endereço de email é obrigatório.')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('Este endereço de email já está em uso. Por favor, use um e-mail difrerente.')
        return email

    class Meta:
    	model = Patient
    	fields = ('username', 'first_name', 'last_name', 'email', 'sex', 'birth_date', 'marital_status', 'phone', 'ocupation', 'observation', 'ethnicity')

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
			'exam': ModelSelect2Bootstrap(url='patient:biochemical_autocomplete')
		}

class EnergyCalcForm(ModelForm):

	class Meta:
		model = EnergyCalc
		exclude = ['mbr', 'tee']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['activity_factor'].queryset = FormulaValue.objects.none()
		if 'formula' in self.data:
			try:
				formula_id = int(self.data.get('formula'))
				self.fields['activity_factor'].queryset = FormulaValue.objects.filter(formula_id=formula_id).order_by('name')
			except (ValueError, TypeError):
				pass  # invalid input from the client; ignore and fallback to empty City queryset
		elif self.instance.pk:
			if self.instance.formula != None:
				self.fields['activity_factor'].queryset = self.instance.formula.value_formula.order_by('name')

class SkinFoldForm(ModelForm):

	class Meta:
		model = SkinFold
		fields = '__all__'

class ConsultationForm(ModelForm):
	class Meta:
		model = Consultation
		exclude = ['patient', 'bodycirc', 'energycalc', 'skinfold', 'bioimpedance', 'bonediameter', 'biochemical']
		widgets = {
    		'patology': ModelSelect2MultipleBootstrap(url='patient:patology_autocomplete'),
    		'supplement': ModelSelect2MultipleBootstrap(url='patient:supplement_autocomplete'),
    		'vitamin': ModelSelect2MultipleBootstrap(url='patient:vitamin_autocomplete')
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

class FoodAnalysisGuidanceForm(ModelForm):
	class Meta:
		model = FoodAnalysis
		fields = ['guidance']
		widgets = {
			'guidance': ModelSelect2MultipleBootstrap(url='nutritionist:guidance_autocomplete'),
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
    		'original_food': ModelSelect2Bootstrap(url='patient:food_autocomplete'),
		}

class SubstituteMealForm(ModelForm):
	class Meta:
		model = SubstituteItem
		fields = ['weight_substitute', 'food_substitute', 'unity_substitute', 'meal_substitute']
		widgets = {
    		'food_substitute': ModelSelect2Bootstrap(url='patient:food_autocomplete'),
		}
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['meal_substitute'].queryset = MealItem.objects.exclude(original_food__isnull=True)
