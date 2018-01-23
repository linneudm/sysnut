# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.urlresolvers import  reverse, reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from .models import MeasureUnity, Measure
#from sysnut.patient.views import StaffRequiredMixin
from django.shortcuts import render
from os.path import join, dirname, abspath
import xlrd
from .models import Food, MealItem, UploadSheet
from dal import autocomplete
import os

# Create your views here.

#@method_decorator(login_required, name='dispatch')

@login_required
def remove_all_units(request):
    food = Food.objects.all().delete()
    return HttpResponseRedirect(reverse('food:list'))

def create_measures_unity(request):
    MeasureUnity.objects.get_or_create(description="COL S CH")
    MeasureUnity.objects.get_or_create(description="COL S R")

    MeasureUnity.objects.get_or_create(description="COL SOB CH")
    MeasureUnity.objects.get_or_create(description="COL SOB R")

    MeasureUnity.objects.get_or_create(description="COL S CH PICADO")
    MeasureUnity.objects.get_or_create(description="COL S R PICADO")

    MeasureUnity.objects.get_or_create(description="PIRES CH PICADO")

    MeasureUnity.objects.get_or_create(description="COL CAFÉ CH")   
    MeasureUnity.objects.get_or_create(description="COL CAFÉ R")

    MeasureUnity.objects.get_or_create(description="COL CHÁ CH")
    MeasureUnity.objects.get_or_create(description="COL CHÁ R")

    MeasureUnity.objects.get_or_create(description="COL PAU M CH")
    MeasureUnity.objects.get_or_create(description="COL PAU P CH")
    MeasureUnity.objects.get_or_create(description="COL PAU P R")

    MeasureUnity.objects.get_or_create(description="COL A CH PICADO")
    MeasureUnity.objects.get_or_create(description="COL A R PICADO")

    MeasureUnity.objects.get_or_create(description="ESC M CH PICADO")
    MeasureUnity.objects.get_or_create(description="ESC M R PICADO")

    MeasureUnity.objects.get_or_create(description="COPO D N")
    MeasureUnity.objects.get_or_create(description="COPO P N")

    MeasureUnity.objects.get_or_create(description="X CAFÉ CH")
    MeasureUnity.objects.get_or_create(description="X CHÁ CH")

    MeasureUnity.objects.get_or_create(description="COPO D CH")
    MeasureUnity.objects.get_or_create(description="COPO P CH")

    MeasureUnity.objects.get_or_create(description="UND COMERCIAL")

    MeasureUnity.objects.get_or_create(description="COPO D CH PICADO")
    MeasureUnity.objects.get_or_create(description="COPO P CH PICADO")

    MeasureUnity.objects.get_or_create(description="PT F PICADO")
    MeasureUnity.objects.get_or_create(description="PT R PICADO")
    MeasureUnity.objects.get_or_create(description="PT R CH PICADO")
    MeasureUnity.objects.get_or_create(description="PT SOB CH PICADO")

    MeasureUnity.objects.get_or_create(description="UND G")
    MeasureUnity.objects.get_or_create(description="UND M")
    MeasureUnity.objects.get_or_create(description="UND P")

    MeasureUnity.objects.get_or_create(description="UND")    

    MeasureUnity.objects.get_or_create(description="FT G")
    MeasureUnity.objects.get_or_create(description="FT M")
    MeasureUnity.objects.get_or_create(description="FT P")

    MeasureUnity.objects.get_or_create(description="RAMO M")
    
    MeasureUnity.objects.get_or_create(description="FOLHA G")
    MeasureUnity.objects.get_or_create(description="FOLHA M")
    MeasureUnity.objects.get_or_create(description="FOLHA P")   


    messages.add_message(request, messages.SUCCESS, 'Unidades de medida criadas com sucesso!')
    return HttpResponseRedirect(reverse('food:list'))

def create_measures_excel(request):
        fname = join(dirname(dirname(abspath(__file__))), 'food', 'tabela-medidas.xlsx')#Pasta do App Food
        workbook = xlrd.open_workbook(fname)
        worksheet = workbook.sheet_by_name('Planilha1')
        worksheet = workbook.sheet_by_index(0)

        for row_num in range(worksheet.nrows):#le todas as linhas da planilha
    # cabeçalho
            if row_num == 0:
                continue
    # Lê as linhas
            row = worksheet.row_values(row_num)

            #print(row)
    # Salva no banco
            food, measure_unity, weight  = Food.objects.get(description=row[0]), MeasureUnity.objects.get(description=row[1]), row[2]
            if(Measure.objects.create(food=food,
                measure_unity=measure_unity,
                weight=weight)
            ):
                result = 1
            else:
                result = 0

        if(result == 1):
            messages.add_message(request, messages.SUCCESS, 'Medidas importadas com sucesso!')
        else:
            messages.add_message(request, messages.ERROR, 'Código 2! Algo de errado não está certo! Contate o administrador')
        return HttpResponseRedirect(reverse('food:list'))


'''
def create_measures(request):
    col_sch = MeasureUnity.objects.get(description="COL S CH PICADO")
    col_sr = MeasureUnity.objects.get(description="COL S R PICADO")

    col_ach = MeasureUnity.objects.get(description="COL A CH PICADO")
    col_ar = MeasureUnity.objects.get(description="COL A R PICADO")

    esc_mch = MeasureUnity.objects.get(description="ESC M CH PICADO")
    esc_mr = MeasureUnity.objects.get(description="ESC M R PICADO")

    copo_dch = MeasureUnity.objects.get(description="COPO D CH PICADO")
    copo_pch = MeasureUnity.objects.get(description="COPO P CH PICADO")

    pt_f = MeasureUnity.objects.get(description="PT F PICADO")
    pt_r = MeasureUnity.objects.get(description="PT R PICADO")

    und_g = MeasureUnity.objects.get(description="UND G")
    und_m = MeasureUnity.objects.get(description="UND M")
    und_p = MeasureUnity.objects.get(description="UND P")

    ft_g = MeasureUnity.objects.get(description="FT G")
    ft_m = MeasureUnity.objects.get(description="FT M")
    ft_p = MeasureUnity.objects.get(description="FT P")

    fol_g = MeasureUnity.objects.get(description="FOLHA G")
    fol_m = MeasureUnity.objects.get(description="FOLHA M")
    fol_p = MeasureUnity.objects.get(description="FOLHA P")


    #Unidades do Abacate
    Measure.objects.create(food=Food.objects.get(description="Abacate"),measure_unity=col_sch, weight=45.00)
    Measure.objects.create(food=Food.objects.get(description="Abacate"),measure_unity=copo_dch, weight=200.00)
    Measure.objects.create(food=Food.objects.get(description="Abacate"),measure_unity=copo_pch, weight=130.00)
    Measure.objects.create(food=Food.objects.get(description="Abacate"),measure_unity=pt_f, weight=450.00)
    Measure.objects.create(food=Food.objects.get(description="Abacate"),measure_unity=pt_r, weight=350.00)
    Measure.objects.create(food=Food.objects.get(description="Abacate"),measure_unity=und_g, weight=900.00)
    Measure.objects.create(food=Food.objects.get(description="Abacate"),measure_unity=und_m, weight=430.00)
    Measure.objects.create(food=Food.objects.get(description="Abacate"),measure_unity=und_p, weight=370.00)

    #Unidades do Abacaxi
    Measure.objects.create(food=Food.objects.get(description="Abacaxi"),measure_unity=ft_g, weight=190.00)
    Measure.objects.create(food=Food.objects.get(description="Abacaxi"),measure_unity=ft_m, weight=75.00)
    Measure.objects.create(food=Food.objects.get(description="Abacaxi"),measure_unity=ft_p, weight=50.00)
    Measure.objects.create(food=Food.objects.get(description="Abacaxi"),measure_unity=und_m, weight=750.00)
    Measure.objects.create(food=Food.objects.get(description="Abacaxi"),measure_unity=und_p, weight=480.00)

    #Abobrinha Cozida
    Measure.objects.create(food=Food.objects.get(description="Abobrinha (cozida)"),measure_unity=col_ach, weight=70.00)
    Measure.objects.create(food=Food.objects.get(description="Abobrinha (cozida)"),measure_unity=col_ar, weight=35.00)
    Measure.objects.create(food=Food.objects.get(description="Abobrinha (cozida)"),measure_unity=col_sch, weight=30.00)
    Measure.objects.create(food=Food.objects.get(description="Abobrinha (cozida)"),measure_unity=col_sr, weight=20.00)
    Measure.objects.create(food=Food.objects.get(description="Abobrinha (cozida)"),measure_unity=esc_mch, weight=90.00)
    Measure.objects.create(food=Food.objects.get(description="Abobrinha (cozida)"),measure_unity=esc_mr, weight=40.00)

    #Acarajé
    Measure.objects.create(food=Food.objects.get(description="Acarajé"),measure_unity=und_m, weight=100.00)

    #Acelga crua
    Measure.objects.create(food=Food.objects.get(description="Acelga (crua)"),measure_unity=col_ach, weight=10.00)
    Measure.objects.create(food=Food.objects.get(description="Acelga (crua)"),measure_unity=col_sch, weight=6.00)
    Measure.objects.create(food=Food.objects.get(description="Acelga (crua)"),measure_unity=fol_g, weight=20.00)
    Measure.objects.create(food=Food.objects.get(description="Acelga (crua)"),measure_unity=fol_m, weight=10.00)
    Measure.objects.create(food=Food.objects.get(description="Acelga (crua)"),measure_unity=fol_p, weight=3.00)
    Measure.objects.create(food=Food.objects.get(description="Acelga (crua)"),measure_unity=pt_r, weight=60.00)



    


    messages.add_message(request, messages.SUCCESS, 'Medidas criadas com sucesso!')
    return HttpResponseRedirect(reverse('food:list'))
'''

@method_decorator(login_required, name='dispatch')
class UploadSheet(CreateView):
    model = UploadSheet
    template_name = 'uploadsheet/new.html'
    form_class = UploadSheetForm
    success_url = reverse_lazy('food:list')


    def form_valid(self, form):
        self.object = form.save(commit=False)
        #print(">>>>>> ", sheet.path)
        self.object.save()
        fname = join(dirname(abspath("media/" + str(self.object.path))),os.path.basename(str(self.object.path)))
        try:
            workbook = xlrd.open_workbook(fname)
        except:
            messages.add_message(self.request, messages.ERROR, 'Código 3! Formato de arquivo inválido!')
            return HttpResponseRedirect(reverse('food:upload'))
        worksheet = workbook.sheet_by_name('tabelaok')
        worksheet = workbook.sheet_by_index(0)

        for row_num in range(worksheet.nrows):#le todas as linhas da planilha
        #for row_num in range(10):#le apenas as 10 primeiras linhas
    # cabeçalho
            if row_num == 0:
                continue
    # Lê as linhas
            row = worksheet.row_values(row_num)
            #Verifica se todos os números nas colunas da planilha são válidos
            for col in range (34):
                if(col != 0): #coluna 0 fica a descricao, portanto nao deve ser considerada
                    if not(isinstance(row[col], float)) and not(isinstance(row[col], int)):
                        #print("Numero :", row[col])
                        #print("Tipo :", type(row[col]))
                        messages.add_message(request, messages.ERROR, 'Código 1! Algo de errado não está certo! Contate o administrador')
                        return HttpResponseRedirect(reverse('food:list'))

            #print(row)
    # Salva no banco
            if(Food.objects.create(description=row[0],
                weight=row[1],
                energy=row[2],
                carbohydrates=row[3],
                total_fat=row[4],
                poly_fat =row[5],
                mono_fat =row[6],
                sat_fat =row[7],
                protein =row[8],
                total_fibers =row[9],
                sol_fibers=row[10],
                insol_fibers=row[11],
                cholesterol =row[12],
                retinol =row[13],
                ac_ascorbic=row[14],
                tiamine =row[15],
                riboflavin=row[16],
                pyridoxine=row[17],
                cobalamin=row[18],
                dvitamin =row[19],
                niacin =row[20],
                ac_folic=row[21],
                ac_pant =row[22],
                tocopherol=row[23],
                iodine =row[24],
                sodium =row[25],
                calcium=row[26],
                magnesium=row[27],
                zinc =row[28],
                manganese=row[29],
                potassium=row[30],
                phosphor=row[31],
                iron=row[32],
                copper =row[33],
                selenium=row[34])
            ):
                result = 1
            else:
                result = 0

        if(result == 1):
            messages.add_message(self.request, messages.SUCCESS, 'Alimentos importados com sucesso!')
        else:
            messages.add_message(self.request, messages.ERROR, 'Código 2! Algo de errado não está certo! Contate o administrador')
        return HttpResponseRedirect(reverse('food:list'))
            #return reverse('food:list')

        return HttpResponseRedirect(self.get_success_url())

# Importação planilha com o tombamento e descrição
def import_sheet(request):
    fname = join(dirname(dirname(abspath(__file__))), 'food', 'tabela-essencial.xlsx')
    workbook = xlrd.open_workbook(fname)
    worksheet = workbook.sheet_by_name('tabelaok')
    worksheet = workbook.sheet_by_index(0)

    for row_num in range(worksheet.nrows):#le todas as linhas da planilha
# cabeçalho
        if row_num == 0:
            continue
# Lê as linhas
        row = worksheet.row_values(row_num)
        #Verifica se todos os números nas colunas da planilha são válidos
        for col in range (34):
            if(col != 0): #coluna 0 fica a descricao
                if not(isinstance(row[col], float)) and not(isinstance(row[col], int)):
                    #print("Numero :", row[col])
                    #print("Tipo :", type(row[col]))
                    messages.add_message(request, messages.ERROR, 'Código 1! Algo de errado não está certo! Contate o administrador')
                    return HttpResponseRedirect(reverse('food:list'))

        #print(row)
# Salva no banco
        if(Food.objects.create(description=row[0],
            weight=row[1],
            energy=row[2],
            carbohydrates=row[3],
            total_fat=row[4],
            poly_fat =row[5],
            mono_fat =row[6],
            sat_fat =row[7],
            protein =row[8],
            total_fibers =row[9],
            sol_fibers=row[10],
            insol_fibers=row[11],
            cholesterol =row[12],
            retinol =row[13],
            ac_ascorbic=row[14],
            tiamine =row[15],
            riboflavin=row[16],
            pyridoxine=row[17],
            cobalamin=row[18],
            dvitamin =row[19],
            niacin =row[20],
            ac_folic=row[21],
            ac_pant =row[22],
            tocopherol=row[23],
            iodine =row[24],
            sodium =row[25],
            calcium=row[26],
            magnesium=row[27],
            zinc =row[28],
            manganese=row[29],
            potassium=row[30],
            phosphor=row[31],
            iron=row[32],
            copper =row[33],
            selenium=row[34])):
            result = 1
        else:
            result = 0

    if(result == 1):
        messages.add_message(request, messages.SUCCESS, 'Alimentos importados com sucesso!')
    else:
        messages.add_message(request, messages.ERROR, 'Código 2! Algo de errado não está certo! Contate o administrador')
    return HttpResponseRedirect(reverse('food:list'))
        #return reverse('food:list')

# Food CRUD


@method_decorator(login_required, name='dispatch')
class FoodList(ListView):

	model = Food
	http_method_names = ['get']
	template_name = 'food/list.html'
	context_object_name = 'food'
	paginate_by = 10

	def get_queryset(self):
		self.queryset = super(FoodList, self).get_queryset().order_by('description')
		if self.request.GET.get('search_box', False):
			self.queryset=self.queryset.filter(description__icontains = self.request.GET['search_box'])
		return self.queryset

	def get_context_data(self, **kwargs):
		_super = super(FoodList, self)
		context = _super.get_context_data(**kwargs)
		adjacent_pages = 3
		page_number = context['page_obj'].number
		num_pages = context['paginator'].num_pages
		startPage = max(page_number - adjacent_pages, 1)
		if startPage <= 5:
		    startPage = 1
		endPage = page_number + adjacent_pages + 1
		if endPage >= num_pages - 1:
		    endPage = num_pages + 1
		page_numbers = [n for n in range(startPage, endPage) \
				if n > 0 and n <= num_pages]
		context.update({
			'page_numbers': page_numbers,
			'show_first': 1 not in page_numbers,
			'show_last': num_pages not in page_numbers,
		    })
		return context

@method_decorator(login_required, name='dispatch')
class FoodDetail(DetailView):
	model = Food
	template_name = 'food/details.html'

@method_decorator(login_required, name='dispatch')
class FoodCreate(CreateView):
    model = Food
    template_name = 'food/new.html'
    form_class = FoodForm

    def get(self, request, *args, **kwargs):
        self.object = None
        self.measure_formset = MeasureFormSet()
        form = self.form_class
        return self.render_to_response(
            self.get_context_data(
                form=form,
                )
            )
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        self.measure_formset = MeasureFormSet(self.request.POST)
        if form.is_valid() and self.measure_formset.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        self.measure_formset.instance = self.object
        self.measure_formset.save()
        #messages.add_message(self.request, messages.SUCCESS, 'Alimento adicionado com sucesso!')
        return HttpResponseRedirect(reverse('food:list'))

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                )
            )

    def get_context_data(self, **kwargs):
        context = super(FoodCreate,self).get_context_data(**kwargs)
        context['measure_formset'] = self.measure_formset
        return context


@method_decorator(login_required, name='dispatch')
class FoodUpdate(UpdateView):
    model = Food
    template_name = 'food/new.html'
    form_class = FoodForm
    success_url = reverse_lazy('food:list')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        super(FoodUpdate, self).get(request, *args, **kwargs)
        #self.measure_formset = MeasureFormSet()
        form = self.form_class
        return self.render_to_response(
            self.get_context_data(
                form=form,
            )
        )
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        self.measure_formset = MeasureFormSet(self.request.POST, instance=self.object)
        if form.is_valid() and self.measure_formset.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        self.measure_formset.instance = self.object
        self.measure_formset.save()
        #messages.add_message(self.request, messages.SUCCESS, 'Alimento adicionado com sucesso!')
        return HttpResponseRedirect(reverse('food:list'))

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                )
            )

    def get_context_data(self, **kwargs):
        self.measure_formset = MeasureFormSet(instance = self.object)
        context = super(FoodUpdate,self).get_context_data(**kwargs)
        context['measure_formset'] = self.measure_formset
        if self.request.POST:
            context['form'] = self.form_class(self.request.POST, instance=self.object)
        else:
            context['form'] = self.form_class(instance=self.object)
        return context

@method_decorator(login_required, name='dispatch')
class FoodDelete(DeleteView):
	model = Food
	success_url = reverse_lazy('food:list')

@login_required
def remove_all(request):
    food = Food.objects.all().delete()
    return HttpResponseRedirect(reverse('food:list'))


# End Food
