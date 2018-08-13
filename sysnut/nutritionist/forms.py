# -*- coding: utf-8 -*-

from django.forms import ModelForm
from django import forms
from django.forms.utils import ErrorList
from django.contrib.auth.models import User
from sysnut.account.models import Nutritionist, Address, User
from dal import autocomplete
from django.contrib.auth.forms import UserCreationForm,PasswordResetForm
from django.contrib.auth import authenticate, get_user_model
from sysnut.patient.models import Guidance

class NutritionistForm(UserCreationForm):

	class Meta:
		model = Nutritionist
		fields = ['username', 'first_name', 'last_name', 'email', 'brand', 'sex', 'crn', 'birth_date', 'phone']

class LogoForm(ModelForm):
	class Meta:
		model = Nutritionist
		fields = ['brand']

class AddressForm(ModelForm):

	class Meta:
		model = Address
		fields = '__all__'


class GuidanceForm(ModelForm):
	class Meta:
		model = Guidance
		fields = ['description', 'message']
