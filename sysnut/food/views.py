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
from django.shortcuts import render
from os.path import join, dirname, abspath
import xlrd
from .models import Food, Meal, UploadSheet
from dal import autocomplete
import os

# Create your views here.

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

        #for row_num in range(worksheet.nrows):#le todas as linhas da planilha
        for row_num in range(10):#le apenas as 10 primeiras linhas
    # cabeçalho
            if row_num == 0:
                continue
    # Lê as linhas
            row = worksheet.row_values(row_num)
            #Verifica se todos os números nas colunas da planilha são válidos
            for col in range (34):
                if(col != 0): #coluna 0 fica a descricao, portanto nao deve ser considerada
                    if not(isinstance(row[col], float)) and not(isinstance(row[col], int)):
                        print("Numero :", row[col])
                        print("Tipo :", type(row[col]))
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
                    print("Numero :", row[col])
                    print("Tipo :", type(row[col]))
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
class FoodAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !

        qs = Food.objects.all()

        # Pesquisa pela Descrição
        if self.q:
            qs = qs.filter(Q(description__icontains=self.q))

        return qs


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

@method_decorator(login_required, name='dispatch')
class FoodUpdate(UpdateView):
	model = Food
	template_name = 'food/new.html'
	form_class = FoodForm
	success_url = reverse_lazy('food:list')

@method_decorator(login_required, name='dispatch')
class FoodDelete(DeleteView):
	model = Food
	success_url = reverse_lazy('food:list')

# End Food
