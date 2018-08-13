# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
import datetime
from datetime import date

# Create your models here.

class AuditModel(models.Model):
	# Audit Fields
	created_on = models.DateTimeField('Criado em', auto_now_add=True)
	updated_on = models.DateTimeField('Autalizado em', auto_now=True)

	class Meta:
		abstract=True


class Address(models.Model):
	city = models.CharField('Cidade', max_length=255, blank=True, null=True)
	UF_CHOICES = (
	    ('AC', 'Acre'),
	    ('AL', 'Alagoas'),
	    ('AP', 'Amapá'),
	    ('BA', 'Bahia'),
	    ('CE', 'Ceará'),
	    ('DF', 'Distrito Federal'),
	    ('ES', 'Espírito Santo'),
	    ('GO', 'Goiás'),
	    ('MA', 'Maranão'),
	    ('MG', 'Minas Gerais'),
	    ('MS', 'Mato Grosso do Sul'),
	    ('MT', 'Mato Grosso'),
	    ('PA', 'Pará'),
	    ('PB', 'Paraíba'),
	    ('PE', 'Pernanbuco'),
	    ('PI', 'Piauí'),
	    ('PR', 'Paraná'),
	    ('RJ', 'Rio de Janeiro'),
	    ('RN', 'Rio Grande do Norte'),
	    ('RO', 'Rondônia'),
	    ('RR', 'Roraima'),
	    ('RS', 'Rio Grande do Sul'),
	    ('SC', 'Santa Catarina'),
	    ('SE', 'Sergipe'),
	    ('SP', 'São Paulo'),
	    ('TO', 'Tocantins')
	)
	state = models.CharField('UF', max_length=2, choices=UF_CHOICES, default='PI')
	street = models.CharField('Rua',max_length=255, blank=True, null=True)
	number = models.CharField('Número', max_length=20, blank=True, null=True)
	complement = models.CharField('Complemento', max_length=255, blank=True, null=True)
	zip_code = models.CharField('CEP', max_length=10, blank=True, null=True)
	reference_point = models.CharField('Ponto de Referência', max_length=255, blank=True, null=True)
	neighborhood = models.CharField('Bairro', max_length=255, blank=True, null=True)
	country = models.CharField('País', max_length=255, default='Brasil', blank=True, null=True)

#Nutritionist infos
class Nutritionist(User, AuditModel):


	MALE = 'M'
	FEMALE  = 'F'
	SEX_CHOICES = ((MALE, 'Masculino'), (FEMALE, 'Feminino'),)
	sex = models.CharField('Sexo', max_length=1, choices=SEX_CHOICES, default=FEMALE)

	def is_upperclass(self):
		return self.sex in (self.MALE, self.FEMALE)

	birth_date = models.DateField('Data Nascimento')
	brand = models.FileField(u'Logomarca (opcional)', upload_to='upload/brand', blank=True, null=True)
	crn = models.CharField('CRN', max_length=6, null=False,)
	phone = models.CharField('Telefone', max_length=16)
	address = models.ForeignKey(Address, verbose_name='Endereço', related_name='employees_address', on_delete=models.CASCADE, null=True)

	def __str__(self):
		return self.first_name
