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


class MeasureUnity(models.Model):
    description = models.CharField('Descrição da Medida', max_length=255, unique=True)

    def __str__(self):
        return self.description

class Measure(models.Model):    
    measure_unity = models.ForeignKey(MeasureUnity, verbose_name='Unidade de Medida', related_name='measure_unity', on_delete=models.CASCADE, blank=True, null=True)
    weight = models.DecimalField('Quantidade', default=100.00, decimal_places=2, max_digits=8)
    food = models.ForeignKey(Food, verbose_name='Alimento', related_name='measure_food', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.weight

class MealItem(models.Model):
    BREAKFAST = 'CAFÉ DA MANHÃ'
    SNACK_I = 'LANCHE I'
    LUNCH = 'ALMOÇO'
    SNACK_II = 'LANCHE II'
    DINNER = 'JANTAR'
    SUPPER = 'CEIA'
    MEAL_CHOICES = ((BREAKFAST, 'Café da Manhã'),(SNACK_I, 'Lanche I'),(LUNCH, 'Almoço'),(SNACK_II, 'Lanche II'),(DINNER, 'Jantar'),(SUPPER, 'Ceia'))
    meal = models.CharField('Refeição', max_length=40, choices=MEAL_CHOICES, default=None, blank=False, null=True)
    home_measure = models.CharField('Medida Caseira', max_length=255, blank=True)
    original_food = models.ForeignKey(Food, verbose_name='Alimento', related_name='meal_food', on_delete=models.CASCADE, blank=True, null=True)
    measure_unity  = models.ForeignKey(MeasureUnity, verbose_name='Unidade de Medida', related_name='meal_unity', on_delete=models.CASCADE, blank=True, null=True)
    #PESO DO MICRONUTRIENTE = peso_micro_original  * peso_refeição / 100
    #Infos
    weight = models.DecimalField('Quantidade', default=100.00, decimal_places=2, max_digits=8)

    #cardapio
    food_analysis = models.ForeignKey(FoodAnalysis, verbose_name='Cardápio', related_name='meal_analysis', on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.meal + " - " + str(self.original_food)

    #Retorna os micro calculados
    def measure(self):
        #print(measure)
        measure = Measure.objects.get(measure_unity=self.measure_unity, food=self.original_food)
        return measure

    def energy(self):
        if self.measure_unity == None:
            return (self.original_food.energy * self.weight) / self.original_food.weight
        else:
            return (self.original_food.energy * (self.measure().weight * self.weight)) / self.original_food.weight
    def carbohydrates(self):
        if self.measure_unity == None:
            return (self.original_food.carbohydrates * self.weight) / self.original_food.weight
        else:
            return (self.original_food.carbohydrates * (self.measure().weight * self.weight)) / self.original_food.weight
    def total_fat(self):
        if self.measure_unity == None:
            return (self.original_food.total_fat * self.weight) / self.original_food.weight
        else:
            return (self.original_food.total_fat * (self.measure().weight * self.weight)) / self.original_food.weight
    def poly_fat(self):
        if self.measure_unity == None:
            return (self.original_food.poly_fat * self.weight) / self.original_food.weight
        else:
            return (self.original_food.poly_fat * (self.measure().weight * self.weight)) / self.original_food.weight
    def mono_fat(self):
        if self.measure_unity == None:
            return (self.original_food.mono_fat * self.weight) / self.original_food.weight
        else:
            return (self.original_food.mono_fat * (self.measure().weight * self.weight)) / self.original_food.weight
    def sat_fat(self):
        if self.measure_unity == None:
            return (self.original_food.sat_fat * self.weight) / self.original_food.weight
        else:
            return (self.original_food.sat_fat * (self.measure().weight * self.weight)) / self.original_food.weight
    def protein(self):
        if self.measure_unity == None:
            return (self.original_food.protein * self.weight) / self.original_food.weight
        else:
            return (self.original_food.protein * (self.measure().weight * self.weight)) / self.original_food.weight
    def total_fibers(self):
        if self.measure_unity == None:
            return (self.original_food.total_fibers * self.weight) / self.original_food.weight
        else:
            return (self.original_food.total_fibers * (self.measure().weight * self.weight)) / self.original_food.weight
    def sol_fibers(self):
        if self.measure_unity == None:
            return (self.original_food.sol_fibers *self.weight) / self.original_food.weight
        else:
            return (self.original_food.sol_fibers * (self.measure().weight * self.weight)) / self.original_food.weight            
    def insol_fibers(self):
        if self.measure_unity == None:
            return (self.original_food.insol_fibers * self.weight) / self.original_food.weight
        else:
            return (self.original_food.insol_fibers * (self.measure().weight * self.weight)) / self.original_food.weight
    def cholesterol(self):
        if self.measure_unity == None:
            return (self.original_food.cholesterol * self.weight) / self.original_food.weight
        else:
            return (self.original_food.cholesterol * (self.measure().weight * self.weight)) / self.original_food.weight
    def retinol(self):
        if self.measure_unity == None:
            return (self.original_food.retinol * self.weight) / self.original_food.weight
        else:
            return (self.original_food.retinol * (self.measure().weight * self.weight)) / self.original_food.weight
    def ac_ascorbic(self):
        if self.measure_unity == None:
            return (self.original_food.ac_ascorbic * self.weight) / self.original_food.weight
        else:
            return (self.original_food.ac_ascorbic * (self.measure().weight * self.weight)) / self.original_food.weight
    def tiamine (self):
        if self.measure_unity == None:
            return (self.original_food.tiamine * self.weight) / self.original_food.weight
        else:
            return (self.original_food.tiamine * (self.measure().weight * self.weight)) / self.original_food.weight
    def riboflavin(self):
        if self.measure_unity == None:
            return (self.original_food.riboflavin * self.weight) / self.original_food.weight
        else:
            return (self.original_food.riboflavin * (self.measure().weight * self.weight)) / self.original_food.weight
    def pyridoxine(self):
        if self.measure_unity == None:
            return (self.original_food.pyridoxine * self.weight) / self.original_food.weight
        else:
            return (self.original_food.pyridoxine * (self.measure().weight * self.weight)) / self.original_food.weight
    def cobalamin(self):
        if self.measure_unity == None:
            return (self.original_food.cobalamin * self.weight) / self.original_food.weight
        else:
            return (self.original_food.cobalamin * (self.measure().weight * self.weight)) / self.original_food.weight
    def dvitamin(self):
        if self.measure_unity == None:
            return (self.original_food.dvitamin * self.weight) / self.original_food.weight
        else:
            return (self.original_food.dvitamin * (self.measure().weight * self.weight)) / self.original_food.weight
    def niacin(self):
        if self.measure_unity == None:
            return (self.original_food.niacin * self.weight) / self.original_food.weight
        else:
            return (self.original_food.niacin * (self.measure().weight * self.weight)) / self.original_food.weight
    def ac_folic(self):
        if self.measure_unity == None:
            return (self.original_food.ac_folic * self.weight) / self.original_food.weight
        else:
            return (self.original_food.ac_folic * (self.measure().weight * self.weight)) / self.original_food.weight
    def ac_pant(self):
        if self.measure_unity == None:
            return (self.original_food.ac_pant * self.weight) / self.original_food.weight
        else:
            return (self.original_food.ac_pant * (self.measure().weight * self.weight)) / self.original_food.weight
    def tocopherol(self):
        if self.measure_unity == None:
            return (self.original_food.tocopherol * self.weight) / self.original_food.weight
        else:
            return (self.original_food.tocopherol * (self.measure().weight * self.weight)) / self.original_food.weight
    def iodine(self):
        if self.measure_unity == None:
            return (self.original_food.iodine * self.weight) / self.original_food.weight
        else:
            return (self.original_food.iodine * (self.measure().weight * self.weight)) / self.original_food.weight
    def sodium(self):
        if self.measure_unity == None:
            return (self.original_food.sodium * self.weight) / self.original_food.weight
        else:
            return (self.original_food.sodium * (self.measure().weight * self.weight)) / self.original_food.weight
    def calcium(self):
        if self.measure_unity == None:
            return (self.original_food.calcium * self.weight) / self.original_food.weight
        else:
            return (self.original_food.calcium * (self.measure().weight * self.weight)) / self.original_food.weight
    def magnesium(self):
        if self.measure_unity == None:
            return (self.original_food.magnesium * self.weight) / self.original_food.weight
        else:
            return (self.original_food.magnesium * (self.measure().weight * self.weight)) / self.original_food.weight
    def zinc(self):
        if self.measure_unity == None:
            return (self.original_food.zinc * self.weight) / self.original_food.weight
        else:
            return (self.original_food.zinc * (self.measure().weight * self.weight)) / self.original_food.weight
    def manganese(self):
        if self.measure_unity == None:
            return (self.original_food.manganese * self.weight) / self.original_food.weight
        else:
            return (self.original_food.manganese * (self.measure().weight * self.weight)) / self.original_food.weight
    def potassium(self):
        if self.measure_unity == None:
            return (self.original_food.potassium * self.weight) / self.original_food.weight
        else:
            return (self.original_food.potassium * (self.measure().weight * self.weight)) / self.original_food.weight
    def phosphor(self):
        if self.measure_unity == None:
            return (self.original_food.phosphor * self.weight) / self.original_food.weight
        else:
            return (self.original_food.phosphor * (self.measure().weight * self.weight)) / self.original_food.weight
    def iron(self):
        if self.measure_unity == None:
            return (self.original_food.iron * self.weight) / self.original_food.weight
        else:
            return (self.original_food.iron * (self.measure().weight * self.weight)) / self.original_food.weight
    def copper(self):
        if self.measure_unity == None:
            return (self.original_food.copper * self.weight) / self.original_food.weight
        else:
            return (self.original_food.copper * (self.measure().weight * self.weight)) / self.original_food.weight
    def selenium(self):
        if self.measure_unity == None:
            return (self.original_food.selenium * self.weight) / self.original_food.weight
        else:
            return (self.original_food.selenium * (self.measure().weight * self.weight)) / self.original_food.weight


class SubstituteItem(models.Model):
    food_substitute = models.ForeignKey(Food, verbose_name='Alimento', related_name='substitute_food', on_delete=models.CASCADE, blank=True, null=True)
    unity_substitute  = models.ForeignKey(MeasureUnity, verbose_name='Unidade de Medida', related_name='substitute_unity', on_delete=models.CASCADE, blank=True, null=True)

    weight_substitute = models.DecimalField('Quantidade', default=100.00, decimal_places=2, max_digits=8)

    meal_substitute = models.ForeignKey(MealItem, verbose_name='Refeição', related_name='substitute_meal', on_delete=models.CASCADE,null=True, blank=True)
    food_analysis_substitute = models.ForeignKey(FoodAnalysis, verbose_name='Cardápio', related_name='substitute_analysis', on_delete=models.CASCADE,null=True)

    #Retorna os micro calculados

    #Retorna os micro calculados
    def measure(self):
        #print(measure)
        measure = Measure.objects.get(measure_unity=self.measure_unity, food=self.food_substitute)
        return measure

    def energy(self):
        if self.measure_unity == None:
            return (self.food_substitute.energy * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.energy * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def carbohydrates(self):
        if self.measure_unity == None:
            return (self.food_substitute.carbohydrates * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.carbohydrates * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def total_fat(self):
        if self.measure_unity == None:
            return (self.food_substitute.total_fat * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.total_fat * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def poly_fat(self):
        if self.measure_unity == None:
            return (self.food_substitute.poly_fat * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.poly_fat * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def mono_fat(self):
        if self.measure_unity == None:
            return (self.food_substitute.mono_fat * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.mono_fat * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def sat_fat(self):
        if self.measure_unity == None:
            return (self.food_substitute.sat_fat * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.sat_fat * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def protein(self):
        if self.measure_unity == None:
            return (self.food_substitute.protein * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.protein * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def total_fibers(self):
        if self.measure_unity == None:
            return (self.food_substitute.total_fibers * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.total_fibers * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def sol_fibers(self):
        if self.measure_unity == None:
            return (self.food_substitute.sol_fibers *self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.sol_fibers * (self.measure().weight * self.weight)) / self.food_substitute.weight            
    def insol_fibers(self):
        if self.measure_unity == None:
            return (self.food_substitute.insol_fibers * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.insol_fibers * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def cholesterol(self):
        if self.measure_unity == None:
            return (self.food_substitute.cholesterol * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.cholesterol * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def retinol(self):
        if self.measure_unity == None:
            return (self.food_substitute.retinol * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.retinol * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def ac_ascorbic(self):
        if self.measure_unity == None:
            return (self.food_substitute.ac_ascorbic * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.ac_ascorbic * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def tiamine (self):
        if self.measure_unity == None:
            return (self.food_substitute.tiamine * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.tiamine * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def riboflavin(self):
        if self.measure_unity == None:
            return (self.food_substitute.riboflavin * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.riboflavin * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def pyridoxine(self):
        if self.measure_unity == None:
            return (self.food_substitute.pyridoxine * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.pyridoxine * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def cobalamin(self):
        if self.measure_unity == None:
            return (self.food_substitute.cobalamin * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.cobalamin * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def dvitamin(self):
        if self.measure_unity == None:
            return (self.food_substitute.dvitamin * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.dvitamin * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def niacin(self):
        if self.measure_unity == None:
            return (self.food_substitute.niacin * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.niacin * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def ac_folic(self):
        if self.measure_unity == None:
            return (self.food_substitute.ac_folic * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.ac_folic * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def ac_pant(self):
        if self.measure_unity == None:
            return (self.food_substitute.ac_pant * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.ac_pant * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def tocopherol(self):
        if self.measure_unity == None:
            return (self.food_substitute.tocopherol * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.tocopherol * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def iodine(self):
        if self.measure_unity == None:
            return (self.food_substitute.iodine * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.iodine * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def sodium(self):
        if self.measure_unity == None:
            return (self.food_substitute.sodium * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.sodium * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def calcium(self):
        if self.measure_unity == None:
            return (self.food_substitute.calcium * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.calcium * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def magnesium(self):
        if self.measure_unity == None:
            return (self.food_substitute.magnesium * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.magnesium * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def zinc(self):
        if self.measure_unity == None:
            return (self.food_substitute.zinc * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.zinc * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def manganese(self):
        if self.measure_unity == None:
            return (self.food_substitute.manganese * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.manganese * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def potassium(self):
        if self.measure_unity == None:
            return (self.food_substitute.potassium * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.potassium * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def phosphor(self):
        if self.measure_unity == None:
            return (self.food_substitute.phosphor * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.phosphor * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def iron(self):
        if self.measure_unity == None:
            return (self.food_substitute.iron * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.iron * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def copper(self):
        if self.measure_unity == None:
            return (self.food_substitute.copper * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.copper * (self.measure().weight * self.weight)) / self.food_substitute.weight
    def selenium(self):
        if self.measure_unity == None:
            return (self.food_substitute.selenium * self.weight) / self.food_substitute.weight
        else:
            return (self.food_substitute.selenium * (self.measure().weight * self.weight)) / self.food_substitute.weight