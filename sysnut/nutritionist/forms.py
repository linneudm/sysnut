# -*- coding: utf-8 -*-

from django.forms import ModelForm
from django import forms
from django.forms.utils import ErrorList
from django.contrib.auth.models import User
from sysnut.account.models import Nutritionist, Address, User
from dal import autocomplete
from django.contrib.auth.forms import UserCreationForm,PasswordResetForm
from django.contrib.auth import authenticate, get_user_model

class NutritionistForm(UserCreationForm):

	class Meta:
		model = Nutritionist
		fields = ['username', 'first_name', 'last_name', 'email', 'sex', 'crn', 'birth_date', 'phone']

class AddressForm(ModelForm):

	class Meta:
		model = Address
		fields = '__all__'
