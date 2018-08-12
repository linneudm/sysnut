# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
from django.shortcuts import render
#from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
import datetime
from datetime import date
from django.core.urlresolvers import reverse
import decimal
#from sysnut.account.models import Nutritionist
from django.contrib.auth.models import User
# Create your models here.

class Address(models.Model):
	zip_code = models.CharField('CEP', max_length=10, blank=True, null=True)
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
	    ('MA', 'Maranhão'),
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
	reference_point = models.CharField('Ponto de Referência', max_length=255, blank=True, null=True)
	neighborhood = models.CharField('Bairro', max_length=255, blank=True, null=True)
	country = models.CharField('País', max_length=255, default='Brasil')


class Patient(User):
	#name = models.CharField('Nome', max_length=150)
	MALE = 'M'
	FEMALE  = 'F'
	SEX_CHOICES = ((MALE, 'Masculino'), (FEMALE, 'Feminino'),)
	sex = models.CharField('Sexo', max_length=1, choices=SEX_CHOICES, default=MALE, blank=False)

	def is_upperclass(self):
		return self.sex in (self.MALE, self.FEMALE)

	MARRIED = 'CASADO(A)'
	SINGLE = 'SOLTEIRO(A)'
	SEPARATED = 'SEPARADO(A)'
	WINDOWER = 'VIUVO(A)'
	DIVORCED = 'DIVORCIADO(A)'
	MARITAL_STATUS_CHOICES = ((MARRIED, 'Casado(a)'), (SINGLE, 'Solteiro(a)'), (SEPARATED, 'Separado(a)'), (WINDOWER, 'Viuvo(a)'), (DIVORCED, 'Divorciado(a)'),)
	marital_status = models.CharField('Estado Cívil', max_length=30, choices=MARITAL_STATUS_CHOICES, default=SINGLE, blank=False, null=True)

	def is_upperclass(self):
		return self.marital_status in (self.MARRIED, self.SINGLE, self.SEPARATED, self.WINDOWER, self.DIVORCED)

	birth_date = models.DateField('Data de Nascimento')
	phone = models.CharField('Telefone', max_length=16)
	ocupation = models.CharField('Ocupação', max_length=16, blank=True, null=True)
	observation = models.CharField('Observação', max_length=200, blank=True, null=True)

	WHITE = 'BRANCO(A)'
	BLACK = 'NEGRO(A)'
	INDIGENOUS = 'INDÍGENA(A)'
	BROWN = 'PARDO(A)'
	MULATTO = 'MULATO(A)'
	OTHER = 'OUTRO'
	ETHNICITY_CHOICES = ((WHITE, 'Branco(a)'), (BLACK, 'Negro(a)'), (INDIGENOUS, 'Indígeno(a)'), (BROWN, 'Pardo(a)'), (MULATTO, 'Mulato(a)'), (OTHER, 'Outro'),)
	ethnicity = models.CharField('Etnia', max_length=20, choices=ETHNICITY_CHOICES, default=None, blank=False, null=False)
	#email = models.EmailField('E-mail', blank=True, null=True)
	address = models.ForeignKey(Address, verbose_name='Endereço', related_name='patient_address', on_delete=models.CASCADE, null=True)
	user = models.ForeignKey(User, verbose_name=u'Usuário', related_name='patient_users', on_delete=models.CASCADE)
	created_at = models.DateTimeField(u'Criado em', auto_now_add=True)
	update_at = models.DateTimeField(u'Atualizado em', auto_now_add=True)

	# calculating age
	def age(self):
		return self.created_at.year - self.birth_date.year

	def __str__(self):
		return self.first_name

	def get_absolute_url(self):
		return reverse('patient:list')

	class Meta:
		verbose_name = 'Paciente'
		verbose_name_plural = 'Pacientes'
		ordering = ['-created_at']

# Exclui o endereço depois que o paciente for excluido
def post_delete_patient(instance, **kwargs):
	address = Address.objects.get(pk=instance.address_id)
	address.delete()

models.signals.post_delete.connect(post_delete_patient, sender=Patient, dispatch_uid='post_delete_patient')

class Bioimpedance(models.Model):
	fat_percentage = models.DecimalField('Percentual de Gordura', default=0.00, decimal_places=2, max_digits=8)
	bone_weight = models.DecimalField('Peso ósseo (kg)', default=0.00, decimal_places=2, max_digits=8)
	metabolic_age = models.IntegerField('Idade metabólica (anos)', default=0)

	lean_mass = models.DecimalField('Massa magra (kg)', default=0.00, decimal_places=2, max_digits=8)
	fat_free_mass = models.DecimalField('Massa livre de gordura (kg)', default=0.00, decimal_places=2, max_digits=8)
	total_body_water = models.DecimalField('Água corporal total (kg)', default=0.00, decimal_places=2, max_digits=8)

	visceral_fat = models.DecimalField('Gordura visceral (grau)', default=0.00, decimal_places=2, max_digits=8)


class BodyCircunference(models.Model):
	thorax_circ = models.DecimalField('Circ. do Tórax (cm)', default=0.00, decimal_places=2, max_digits=8)
	shoulder_circ = models.DecimalField('Circ. do Ombro (cm)', default=0.00, decimal_places=2, max_digits=8)
	relaxed_arm_circ = models.DecimalField('Circ. Braço Relaxado (cm)', default=0.00, decimal_places=2, max_digits=8)
	contracted_arm_circ = models.DecimalField('Circ. Braço Contraído (cm)', default=0.00, decimal_places=2, max_digits=8)

	forearm_circ = models.DecimalField('Circ. do Antebraço (cm)', default=0.00, decimal_places=2, max_digits=8)
	waist_circ = models.DecimalField('Circ. Cintura (cm)', default=0.00, decimal_places=2, max_digits=8)
	abdomen_circ = models.DecimalField('Circ. do Abdomen (cm)', default=0.00, decimal_places=2, max_digits=8)
	hip_circ = models.DecimalField('Circ. Quadril (cm)', default=0.00, decimal_places=2, max_digits=8)

	proximal_thigh_circ = models.DecimalField('Circ. Coxa Proximal (cm)', default=0.00, decimal_places=2, max_digits=8)
	medial_thigh_circ = models.DecimalField('Circ. Coxa Medial (cm)', default=0.00, decimal_places=2, max_digits=8)
	distal_thigh_circ = models.DecimalField('Circ. Coxa Distal (cm)', default=0.00, decimal_places=2, max_digits=8)
	calf_circ = models.DecimalField('Circ. Panturrilha (cm)', default=0.00, decimal_places=2, max_digits=8)

class SkinFold(models.Model):
	tricipital_fold = models.DecimalField('Dobra tricipital (mm)', default=0.00, decimal_places=2, max_digits=8)
	subscapular_fold = models.DecimalField('Dobra subescapular (mm)', default=0.00, decimal_places=2, max_digits=8)
	chest_fold = models.DecimalField('Dobra torácica (mm)', default=0.00, decimal_places=2, max_digits=8)
	bicipital_fold = models.DecimalField('Dobra bicipital (mm)', default=0.00, decimal_places=2, max_digits=8)
	mean_axillary_fold = models.DecimalField('Dobra axilar média (mm)', default=0.00, decimal_places=2, max_digits=8)
	suprailiathic_fold = models.DecimalField('Dobra suprailíaca (mm)', default=0.00, decimal_places=2, max_digits=8)
	abdominal_fold = models.DecimalField('Dobra abdominal (mm)', default=0.00, decimal_places=2, max_digits=8)
	thigh_fold = models.DecimalField('Dobra da coxa (mm)', default=0.00, decimal_places=2, max_digits=8)
	calf_fold = models.DecimalField('Dobra da panturrilha (mm)', default=0.00, decimal_places=2, max_digits=8)
	
class BoneDiameter(models.Model):
	humeros_diameter = models.DecimalField('Diâmetro do úmero (cm)', default=0.00, decimal_places=2, max_digits=8)
	wrist_diameter = models.DecimalField('Diâmetro do pulso (cm)', default=0.00, decimal_places=2, max_digits=8)
	femoral_diameter = models.DecimalField('Diâmetro do fêmur (cm)', default=0.00, decimal_places=2, max_digits=8)

class Formula(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

    def calculator(self, sex, h, wa, lean_mass, a):
    	if(self.name == "HARRIS-BENEDICT(1919)"):
    		if(sex == "M"):
    			return (66 + decimal.Decimal('13.7') * (wa) + (5 * h) - (decimal.Decimal('6.8') * a))
    		else:
    			return (655 + decimal.Decimal('9.6') * wa) + (decimal.Decimal('1.8') * h) - (decimal.Decimal('4.7') * a)
    	elif(self.name == "HARRIS-BENEDICT(1984)"):
    		if(sex == "M"):
    			return (decimal.Decimal('88.362') + (decimal.Decimal('13.397') * wa) + (decimal.Decimal('4.799') * (h)) - (decimal.Decimal('5.677') * a))
    		else:
    			return (decimal.Decimal('447.593') + (decimal.Decimal('9.247') * wa) + (decimal.Decimal('3.098') * (h)) - (decimal.Decimal('4.330') * a))
    	elif(self.name == "CUNNINGHAN(1996)"):
    		return (370 + decimal.Decimal('21.6') * lean_mass)
    	else:
    		return 0

class FormulaValue(models.Model):
    formula = models.ForeignKey(Formula, verbose_name="Formula", related_name="value_formula", on_delete=models.CASCADE)
    name = models.CharField('Fator de Atividade',max_length=50)
    value = models.DecimalField('Valor', default=0.00, decimal_places=2, max_digits=8)
    
    def __str__(self):
        return self.name

class EnergyCalc(models.Model):
	calc_title = models.CharField('Título do Cálculo',max_length=255, blank=True, null=True, default="Calculo padrão")
	knee_height = models.DecimalField('Altura do Joelho (cm)', default=0.00, decimal_places=2, max_digits=8)
	#Formulas de calculo energetico, consultar a bibliografia
	#formula = models.CharField('Fórmula', max_length=30, choices=FORMULA_CHOICES, default=HARRIS_BENEDICT_OLD, blank=False, null=True)
	formula = models.ForeignKey(Formula,  verbose_name="Formula", on_delete=models.CASCADE, null=True, blank=True)
	activity_factor = models.ForeignKey(FormulaValue, verbose_name="Fator de Atividade", on_delete=models.CASCADE, null=True, blank=True)
	'''
	ACTIVITY_CHOICES = (
	    ('1.0', 'Repouso'),
	    ('1.5', 'Muito Leve'),
	    ('2.5', 'Leve'),
	    ('5.0', 'Moderada'),
	    ('7.0', 'Intensa'),
	    ('1.2', 'Acamado'),
	    ('1.25', 'Acamado + móvel'),
	    ('1.3', 'Ambulante')
	)
	'''
	#activity_factor = models.CharField('Fator de Atividade', max_length=30, choices=ACTIVITY_CHOICES, default='1.5', blank=False, null=True)
	mbr = models.CharField('Taxa Metabólica Basal',max_length=255, blank=True, null=True)
	tee = models.CharField('Gasto Energético Total',max_length=255, blank=True, null=True)

class Patology(models.Model):
	description = models.CharField('Descrição', max_length=255, blank=True, null=True)

	def __str__(self):
		return self.description

class Vitamin(models.Model):
	description = models.CharField('Descrição', max_length=255, blank=True, null=True)
	def __str__(self):
		return self.description

#class Supplement(models.Model):
#	description = models.CharField('Descrição', max_length=255, blank=True, null=True)

#	def __str__(self):
#		return self.description

class Consultation(models.Model):
	patient = models.ForeignKey(Patient, verbose_name='Paciente', related_name='patient_consultation', on_delete=models.CASCADE)
	weight = models.DecimalField('Peso (kg)', default=0.00, decimal_places=2, max_digits=8)
	height = models.DecimalField('Altura (Metros)', default=0.00, decimal_places=2, max_digits=8)
	objective = models.CharField('Objetivo',max_length=255)
	date = models.DateField('Data da consulta')
	patology = models.ManyToManyField(Patology, verbose_name='Patologia', related_name='consultation_patology', blank=True)
	#supplement = models.ManyToManyField(Supplement, verbose_name='Suplemento', related_name='consultation_supplement', blank=True)
	NUTRIENTS_CHOICES = (
		('OMS2008', 'OMS 2008'),
		('DRI2002', 'DRI 2002/2005')
	)
	nutrients = models.CharField('Adequação de Nutrientes', max_length=30, choices=NUTRIENTS_CHOICES, default='OMS2008', blank=False, null=False)
	vitamin = models.ManyToManyField(Vitamin, verbose_name='Deficiência Vitamínica', related_name='consultation_vitamin', blank=True)
	family_history = models.CharField('Histórico Familiar',max_length=255, blank=True)
	drugs = models.CharField('Fármacos',max_length=255, blank=True, null=True)
	life_style = models.CharField('Estilo de vida',max_length=255, blank=True, null=True)
	feed_preferences = models.CharField('Preferências Alimentares',max_length=255, blank=True, null=True)
	prognostic = models.CharField('Prognóstico',max_length=255, blank=True, null=True)
	evaluation = models.CharField('Avaliação',max_length=255, blank=True, null=True)
	observation = models.CharField('Observações gerais',max_length=255, blank=True, null=True)
	bodycirc = models.ForeignKey(BodyCircunference, verbose_name='Circunferência Corporal', related_name='consultation_bodycirc', on_delete=models.CASCADE)
	energycalc = models.ForeignKey(EnergyCalc, verbose_name='Calculos Energéticos', related_name='consultation_energcalc', on_delete=models.CASCADE,null=True, blank=True)
	skinfold = models.ForeignKey(SkinFold, verbose_name='Dobras Corporais', related_name='consultation_skinfold', on_delete=models.CASCADE)
	bioimpedance = models.ForeignKey(Bioimpedance, verbose_name='Bioimpedância', related_name='consultation_bioimpedance', on_delete=models.CASCADE)
	bonediameter = models.ForeignKey(BoneDiameter, verbose_name='Diâmetro ósseo', related_name='consultation_bone_diameter', on_delete=models.CASCADE)

	def imc(self):
		w = float(self.weight)
		h = float(self.height)
		result = "Nada cadastrado."
		tag="secondary"

		if w != 0 and h != 0:
			imc = w / (h * h)
			ideal = (h * h) * 24
			adjust = ideal
			if imc > 30:
				adjust = (w - ideal) * 0.25 + ideal
			if imc < 18:
				adjust = (ideal - w) * 0.25 + w
			if imc >= 16.0 and imc <= 16.9:
				result = "Muito abaixo do peso."
				tag = "danger"
			elif imc <= 18.4:
				result = "Abaixo do peso."
				tag = "warning"
			elif imc <= 24.9:
				result = "Peso normal."
				tag = "success"
			elif imc <= 29.9:
				result = "Acima do peso."
				tag = "warning"
			elif imc <= 34.9:
				result = "Obesidade Grau I."
				tag = "danger"
			elif imc <= 40.0:
				result = "Obesidade Grau II."
				tag = "danger"
			elif imc > 40:
				result = "Obesidade Grau III."
				tag = "danger"
			imc = {
				'val': imc,
				'result': result,
				'tag': tag,
				'ideal': ideal,
				'adjust': adjust
			}
		else:
			imc = {
			'val': 0,
			'result': result,
			}
		return imc
	#taxa metabolica basal (tmb)
	def mbr(self):
		w = (self.weight)#peso
		h = (self.height)#altura
		a = (self.patient.created_at.year - self.patient.birth_date.year)#idade
		lm = (self.bioimpedance.lean_mass)#massa livre
		sex = self.patient.sex
		ideal = 24 * (h * h)
		imc = w * (h * h)
		#Ajuste de peso de acordo com o IMC
		if imc > 30:
			wa = (w - ideal) * decimal.Decimal('0.25') + ideal
		elif imc < 18:
			wa = (ideal - w) * decimal.Decimal('0.25') + w
		else:
			wa = ideal 
		if self.energycalc.formula != None:
			#print(self.energycalc.formula.calculator(sex, h, wa, lm, a))
			return self.energycalc.formula.calculator(sex, h, wa, lm, a)
		else:
			return 0
	#gasto energetico total (get)
	def tee(self):
		if self.energycalc.activity_factor != None and self.mbr() != None:
			result = self.mbr() * decimal.Decimal(self.energycalc.activity_factor.value)
		else:
			result = 0
		return result
	#relacao cintura quadril (rcq)
	def whp(self):
		whp = 0
		result = "Nada cadastrado."
		tag="secondary"
		if self.bodycirc.waist_circ != 0 and self.bodycirc.hip_circ != 0:
			age = (self.patient.created_at.year - self.patient.birth_date.year)
			sex = self.patient.sex
			whp = self.bodycirc.waist_circ / self.bodycirc.hip_circ
			if age >= 50:
				if sex == 'M':
					if age < 60 and age >= 50:
						if whp < 0.9:
							result = "Baixo."
							tag = "info"
						elif whp <= 0.96:
							result = "Moderado."
							tag = "warning"
						elif whp <= 1.02:
							result = "Alto."
							tag = "danger"
						else:
							result = "Muito alto."
							tag = "danger"
					if age < 70 and age >= 60:
						if whp < 0.91:
							result = "Baixo."
							tag = "info"
						elif whp <= 0.98:
							result = "Moderado."
							tag = "warning"
						elif whp <= 1.03:
							result = "Alto."
							tag = "danger"
						else:
							result = "Muito alto."
							tag = "danger"
				else:
					if age < 60 and age >= 50:
						if whp < 0.74:
							result = "Baixo."
							tag = "info"
						elif whp <= 0.81:
							result = "Moderado."
							tag = "warning"
						elif whp <= 0.88:
							result = "Alto."
							tag = "danger"
						else:
							result = "Muito alto."
							tag = "danger"
					if age < 70 and age >= 60:
						if whp < 0.76:
							result = "Baixo."
							tag = "info"
						elif whp <= 0.83:
							result = "Moderado."
							tag = "warning"
						elif whp <= 0.90:
							result = "Alto."
							tag = "danger"
						else:
							result = "Muito alto."
							tag = "danger"
			else:
				result = "Não aplicável."
				tag = "secondary"
				whp = 0

		else:
			result = "Valores da Circ. da Cintura e/ou Circ. do Quadril não definidos."
		whp = {
			"val": whp,
			"result": result,
			"tag": tag,
		}
		return whp
	#relacao cintura altura
	def whr(self):
		whr = 0
		result = "Nada cadastrado."
		tag="secondary"
		if self.bodycirc.waist_circ != 0 and self.height != 0:
			sex = self.patient.sex
			whr = self.bodycirc.waist_circ / (self.height * 100)
			if sex == 'M':
				if whr > 0.52:
					result = "Aumentado."
					tag = "danger"
				else:
					result = "Normal."
					tag = "info"
			else:
				if whr > 0.53:
					result = "Aumentado."
					tag = "danger"
				else:
					result = "Normal."
					tag = "info"

		else:
			result = "Valores da Circ. da Cintura e/ou altura não definidos."
		whr = {
			"val": whr,
			"result": result,
			"tag": tag,
		}
		return whr

	def get_absolute_url(self):
		return reverse('patient:consultation_list', kwargs={'id': self.pk})

	def __str__(self):
		return self.patient.first_name

	class Meta:
		verbose_name = 'Consulta'
		verbose_name_plural = 'Consultas'
		ordering = ['-patient']

	def delete(self):
		for item in self.exam_consultation.all():
			item.path.delete()
		return super(Consultation, self).delete()

class Exam(models.Model):
	description = models.CharField('Descrição', max_length=255)
	path = models.FileField(u'Exame', upload_to='upload/exam', blank=True, null=True)
	consultation = models.ForeignKey(Consultation, verbose_name='Exame', related_name='exam_consultation', on_delete=models.CASCADE)

	def delete(self):
		self.path.delete()
		return super(Exam, self).delete()

class Biochemical(models.Model):
	description = models.CharField('Descricao',max_length=200, blank=True, null=True)

	def __str__(self):
		return self.description

class BiochemicalExam(models.Model):
	exam = models.ForeignKey(Biochemical, verbose_name='Descrição', related_name='value_biochemical', on_delete=models.CASCADE,blank=True, null=True)
	CONDICTION_CHOICES = (
	    ('Alto', 'Alto'),
	    ('Normal', 'Normal'),
	    ('Baixo', 'Baixo')
	)
	condiction = models.CharField('Condição', max_length=10, choices=CONDICTION_CHOICES, default=None)
	consultation = models.ForeignKey(Consultation, verbose_name='Exame Bioquímico', related_name='consultation_biochemical', on_delete=models.CASCADE)
	
class UploadGuidance(models.Model):
    description = models.CharField('Descrição da Tabela', max_length=255)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    path = models.FileField(u'Tabela', upload_to='upload/table', blank=True, null=True)

class Guidance(models.Model):
	#tabela com mensagens criadas pelo nutricionista
	nut = models.ForeignKey(User, verbose_name='Nutricionista', related_name='guidance_nut')
	description = models.CharField('Descrição', max_length=200, blank=False, null=False)
	message = models.TextField('Mensagem', max_length=200, blank=False, null=False)
	def __str__(self):
		return self.description


#class GuidanceAux(models.Model):
	#tabela com mensagens pre-definidas
#	description = models.CharField('Descrição', max_length=200, blank=False, null=False)
#	message = models.CharField('Mensagem', max_length=200, blank=False, null=False)
#	def __str__(self):
#		return self.description


class FoodAnalysis(models.Model):
	guidance = models.ManyToManyField(Guidance, verbose_name='Orientação', related_name='analysis_guidance', blank=True)
#	guidanceaux = models.ManyToManyField(GuidanceAux, verbose_name='Orientação pré-definida', related_name='analysis_guidanceaux', blank=True)
	consultation = models.ForeignKey(Consultation, verbose_name='Consulta', related_name='analysis_consultation', on_delete=models.CASCADE)
	description = models.CharField(u'Descrição', max_length=200, blank=False, null=False)
	created_at = models.DateTimeField(u'Criado em', auto_now_add=True)
	update_at = models.DateTimeField(u'Atualizado em', auto_now_add=True)
	published = models.BooleanField('Publicar?')

	def get_absolute_url(self):
		return reverse('patient:analysis_edit', kwargs={'id': self.pk})

	def __str__(self):
		return self.description

	def energy(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.energy()
		return total

	def result(self):
		tee = decimal.Decimal(self.consultation.tee())
		energy = decimal.Decimal(self.energy())
		percent = 0
		result = 2
		msg = "Nada cadastrado"
		if(energy > 0):
			percent = (energy * 100) / tee
			if (percent >= 90 and percent <= 110):
				result = 0
				msg = "Adequado."
			elif (percent < 90):
				result = -1
				msg = "Inadequado. Abaixo do recomendado."
			elif (percent > 100):
				result = 1
				msg = "Inadequado. Acima do recomendado."

		result = {
			'val': result,
			'percent': percent,
			'msg': msg
		}
		return result


	def carb(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.carbohydrates()
		return total
	def total_fat(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.total_fat()
		return total
	def poly_fat(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.poly_fat()
		return total
	def mono_fat(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.mono_fat()
		return total
	def sat_fat(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.sat_fat()
		return total
	def protein(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.protein()
		return total
	def total_fibers(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.total_fibers()
		return total
	def sol_fibers(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.sol_fibers()
		return total
	def insol_fibers(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.insol_fibers()
		return total
	def cholesterol(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.cholesterol()
		return total
	def retinol(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.retinol()
		return total
	def ac_ascorbic(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.ac_ascorbic()
		return total
	def tiamine (self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.tiamine()
		return total
	def riboflavin(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.riboflavin()
		return total
	def pyridoxine(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.pyridoxine()
		return total
	def cobalamin(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.cobalamin()
		return total
	def dvitamin(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.dvitamin()
		return total
	def niacin(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.niacin()
		return total
	def ac_folic(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.ac_folic()
		return total
	def ac_pant(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.ac_pant()
		return total
	def tocopherol(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.tocopherol()
		return total
	def iodine(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.iodine()
		return total
	def sodium(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.sodium()
		return total
	def calcium(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.calcium()
		return total
	def magnesium(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.magnesium()
		return total
	def zinc(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.zinc()
		return total
	def manganese(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.manganese()
		return total
	def potassium(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.potassium()
		return total
	def phosphor(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.phosphor()
		return total
	def iron(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.iron()
		return total
	def copper(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.copper()
		return total
	def selenium(self):
		total = 0
		for item in self.meal_analysis.all():
			total += item.selenium()
		return total