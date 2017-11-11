# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db.models import signals
from django.shortcuts import render
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
import datetime
from datetime import date
from django.core.urlresolvers import reverse
from sysnut.patient.models import FoodAnalysis

class UploadSheet(models.Model):
    description = models.CharField('Descrição da Tabela', max_length=255)
    created_at = models.DateTimeField(u'Criado em', auto_now_add=True)
    path = models.FileField(u'Tabela', upload_to='upload/table', blank=True, null=True)

class Food(models.Model):
    #Micro nutrientes
    description = models.CharField('Descrição', max_length=255)
    weight = models.DecimalField('Peso líquido (ml ou g)', default=100.00, decimal_places=2, max_digits=8)
    energy = models.DecimalField('Energia (kcal)', default=0.00, decimal_places=2, max_digits=8)
    carbohydrates = models.DecimalField('Carboidratos (g)', default=0.00, decimal_places=2, max_digits=8)
    total_fat = models.DecimalField('Gorduras Totais (g)', default=0.00, decimal_places=2, max_digits=8)
    poly_fat = models.DecimalField('Gorduras Poli (g)', default=0.00, decimal_places=2, max_digits=8)
    mono_fat = models.DecimalField('Gorduras Mono (g)', default=0.00, decimal_places=2, max_digits=8)
    sat_fat = models.DecimalField('Gorduras Saturadas (g)', default=0.00, decimal_places=2, max_digits=8)
    protein = models.DecimalField('Proteínas (g)', default=0.00, decimal_places=2, max_digits=8)
    total_fibers = models.DecimalField('Fibras Totais (g)', default=0.00, decimal_places=2, max_digits=8)
    sol_fibers = models.DecimalField('Fibras Solúveis (g)', default=0.00, decimal_places=2, max_digits=8)
    insol_fibers = models.DecimalField('Fibras Insolúveis (g)', default=0.00, decimal_places=2, max_digits=8)
    cholesterol = models.DecimalField('Colesterol (mg)', default=0.00, decimal_places=2, max_digits=8)
    retinol = models.DecimalField('Retinol (Vit A) (mg)', default=0.00, decimal_places=2, max_digits=8)
    ac_ascorbic = models.DecimalField('Ácido Ascórbico (Vit C) (mg)', default=0.00, decimal_places=2, max_digits=8)
    tiamine = models.DecimalField('Tiamina (Vit B1) (mg)', default=0.00, decimal_places=2, max_digits=8)
    riboflavin = models.DecimalField('Riboflavina (Vit B2) (mg)', default=0.00, decimal_places=2, max_digits=8)
    pyridoxine = models.DecimalField('Piridoxina (Vit B6) (mg)', default=0.00, decimal_places=2, max_digits=8)
    cobalamin = models.DecimalField('Cobalamina (Vit B12) (mcg)', default=0.00, decimal_places=2, max_digits=8)
    dvitamin = models.DecimalField('Vitamina D (mcg)', default=0.00, decimal_places=2, max_digits=8)
    niacin = models.DecimalField('Niacina (Vit B3)(mg)', default=0.00, decimal_places=2, max_digits=8)
    ac_folic = models.DecimalField('Ácido fólico (Vit B9)(mcg)', default=0.00, decimal_places=2, max_digits=8)
    ac_pant = models.DecimalField('Ácido pantotênico (Vit B5)(mg)', default=0.00, decimal_places=2, max_digits=8)
    tocopherol = models.DecimalField('Tocoferol (Vit E)(mg)', default=0.00, decimal_places=2, max_digits=8)
    iodine = models.DecimalField('Iodo (mcg)', default=0.00, decimal_places=2, max_digits=8)
    sodium = models.DecimalField('Sódio (mg)', default=0.00, decimal_places=2, max_digits=8)
    calcium = models.DecimalField('Cálcio (mg)', default=0.00, decimal_places=2, max_digits=8)
    magnesium = models.DecimalField('Magnésio (mg)', default=0.00, decimal_places=2, max_digits=8)
    zinc = models.DecimalField('Zinco (mg)', default=0.00, decimal_places=2, max_digits=8)
    manganese = models.DecimalField('Manganês (mg)', default=0.00, decimal_places=2, max_digits=8)
    potassium = models.DecimalField('Potássio (mg)', default=0.00, decimal_places=2, max_digits=8)
    phosphor = models.DecimalField('Fósforo (mg)', default=0.00, decimal_places=2, max_digits=8)
    iron = models.DecimalField('Ferro (mg)', default=0.00, decimal_places=2, max_digits=8)
    copper = models.DecimalField('Cobre (mg)', default=0.00, decimal_places=2, max_digits=8)
    selenium = models.DecimalField('Selênio (mcg)', default=0.00, decimal_places=2, max_digits=8)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('food:list')

    class Meta:
        verbose_name = 'Alimento'
        verbose_name_plural = 'Alimentos'

class Meal(models.Model):
    BREAKFAST = 'CAFÉ DA MANHÃ'
    SNACK_I = 'LANCHE I'
    LUNCH = 'ALMOÇO'
    SNACK_II = 'LANCHE II'
    DINNER = 'JANTAR'
    SUPPER = 'CEIA'
    MEAL_CHOICES = ((BREAKFAST, 'Café da Manhã'),(SNACK_I, 'Lanche I'),(LUNCH, 'Almoço'),(SNACK_II, 'Lanche II'),(DINNER, 'Jantar'),(SUPPER, 'Ceia'))
    meal = models.CharField('Refeição', max_length=40, choices=MEAL_CHOICES, default=None, blank=True, null=True)
    home_measure = models.CharField('Med. Caseira', max_length=255)
    #PESO DO MICRONUTRIENTE = peso_micro_original  * peso_refeição / 100
    original_food = models.ForeignKey(Food, verbose_name='Alimento', related_name='meal_food', on_delete=models.CASCADE)
    #Infos
    weight = models.DecimalField('Peso líquido (ml ou g)', default=100.00, decimal_places=2, max_digits=8)

    #cardapio
    food_analysis = models.ForeignKey(FoodAnalysis, verbose_name='Cardápio', related_name='meal_analysis', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('food:meal_list')
    
    #Retorna os micro calculados

    def energy(self):
        return (self.original_food.energy * self.weight) / self.original_food.weight
    def carbohydrates(self):
        return (self.original_food.carbohydrates * self.weight) / self.original_food.weight
    def total_fat(self):
        return (self.original_food.total_fat * self.weight) / self.original_food.weight
    def poly_fat(self):
        return (self.original_food.poly_fat * self.weight) / self.original_food.weight
    def mono_fat(self):
        return (self.original_food.mono_fat * self.weight) / self.original_food.weight
    def sat_fat(self):
        return (self.original_food.sat_fat * self.weight) / self.original_food.weight
    def protein(self):
        return (self.original_food.protein * self.weight) / self.original_food.weight
    def total_fibers(self):
        return (self.original_food.total_fibers * self.weight) / self.original_food.weight
    def sol_fibers(self):
        return (self.original_food.sol_fibers *self.weight) / self.original_food.weight
    def insol_fibers(self):
        return (self.original_food.insol_fibers * self.weight) / self.original_food.weight
    def cholesterol(self):
        return (self.original_food.cholesterol * self.weight) / self.original_food.weight
    def retinol(self):
        return (self.original_food.retinol * self.weight) / self.original_food.weight
    def ac_ascorbic(self):
        return (self.original_food.ac_ascorbic * self.weight) / self.original_food.weight
    def tiamine (self):
        return (self.original_food.tiamine * self.weight) / self.original_food.weight
    def riboflavin(self):
        return (self.original_food.riboflavin * self.weight) / self.original_food.weight
    def pyridoxine(self):
        return (self.original_food.pyridoxine * self.weight) / self.original_food.weight
    def cobalamin(self):
        return (self.original_food.cobalamin * self.weight) / self.original_food.weight
    def dvitamin(self):
        return (self.original_food.dvitamin * self.weight) / self.original_food.weight
    def niacin(self):
        return (self.original_food.niacin * self.weight) / self.original_food.weight
    def ac_folic(self):
        return (self.original_food.ac_folic * self.weight) / self.original_food.weight
    def ac_pant(self):
        return (self.original_food.ac_pant * self.weight) / self.original_food.weight
    def tocopherol(self):
        return (self.original_food.tocopherol * self.weight) / self.original_food.weight
    def iodine(self):
        return (self.original_food.iodine * self.weight) / self.original_food.weight
    def sodium(self):
        return (self.original_food.sodium * self.weight) / self.original_food.weight
    def calcium(self):
        return (self.original_food.calcium * self.weight) / self.original_food.weight
    def magnesium(self):
        return (self.original_food.magnesium * self.weight) / self.original_food.weight
    def zinc(self):
        return (self.original_food.zinc * self.weight) / self.original_food.weight
    def manganese(self):
        return (self.original_food.manganese * self.weight) / self.original_food.weight
    def potassium(self):
        return (self.original_food.potassium * self.weight) / self.original_food.weight
    def phosphor(self):
        return (self.original_food.phosphor * self.weight) / self.original_food.weight
    def iron(self):
        return (self.original_food.iron * self.weight) / self.original_food.weight
    def copper(self):
        return (self.original_food.copper * self.weight) / self.original_food.weight
    def selenium(self):
        return (self.original_food.selenium * self.weight) / self.original_food.weight