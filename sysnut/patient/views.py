# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .forms import *
#DJANGO IMPORTS
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.core.urlresolvers import  reverse, reverse_lazy
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import logout
from django.db.models import Q
from dal import autocomplete
import decimal
# Create your views here.

class PatologyAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		# Don't forget to filter out results depending on the visitor !

		qs = Patology.objects.all()

		# Pesquisa pela Descrição
		if self.q:
			qs = qs.filter(Q(description__icontains=self.q))

		return qs



# CRUD Patient

@method_decorator(login_required, name='dispatch')
class PatientCreate(CreateView):

	model = Patient
	template_name = 'patient/new.html'
	form_class = PatientForm
	second_form_class = AddressForm

	def get(self, request, *args, **kwargs):
		self.object = None
		form = self.form_class
		address_form = self.second_form_class
		return self.render_to_response(
			self.get_context_data(
				form=form,
				address_form=address_form
			)
		)

	def post(self, request, *args, **kwargs):
		self.object = None
		address_form = self.second_form_class(self.request.POST)
		form = self.form_class(self.request.POST)

		if form.is_valid() and address_form.is_valid():
			messages.add_message(request, messages.SUCCESS, 'Paciente adicionado com sucesso!')
			return self.form_valid(form, address_form)
		else:
			return self.form_invalid(form, address_form)

	def form_valid(self, form, address_form):
		self.object = address_form.save()
		patient = form.save(commit=False)
		patient.address = self.object
		patient.user = self.request.user
		patient.save()
		return HttpResponseRedirect(self.get_success_url())

	def form_invalid(self, form, address_form):
		return self.render_to_response(
			self.get_context_data(
					form=form,
                    address_form=address_form
			)
		)

	def get_success_url(self):
		return reverse('patient:list')

@method_decorator(login_required, name='dispatch')
class PatientUpdate(UpdateView):

	model = Patient
	template_name = 'patient/new.html'
	form_class = PatientForm
	second_form_class = AddressForm

	def get_context_data(self, **kwargs):
		self.object = self.get_object()
		context = super(PatientUpdate, self).get_context_data(**kwargs)
		if self.request.POST:
			context['address_form'] = self.second_form_class(self.request.POST, instance=self.object)
			context['form'] = self.form_class(self.request.POST, instance=self.object.address)
		else:
			context['address_form'] = self.second_form_class(instance=self.object.address)
			context['form'] = self.form_class(instance=self.object)

		return context

	def get(self, request, *args, **kwargs):
		super(PatientUpdate, self).get(request, *args, **kwargs)
		form = self.form_class
		address_form = self.second_form_class
		return self.render_to_response(
			self.get_context_data(
				object=self.object,
				form=form,
				address_form=address_form
			)
		)

	def post(self, request, *args, **kwargs):

		self.object = self.get_object()
		form = self.form_class(self.request.POST, instance=self.object)
		address_form = self.second_form_class(self.request.POST, instance=self.object.address)

		if form.is_valid() and address_form.is_valid():
			return self.form_valid(form, address_form)
		else:
			return self.form_invalid(form, address_form)

	def form_valid(self, form, address_form):
		self.object = address_form.save()
		patient = form.save(commit=False)
		patient.address = self.object
		patient.user = self.request.user
		patient.save()
		return HttpResponseRedirect(self.get_success_url())

	def form_invalid(self, form, address_form):
		return self.render_to_response(
			self.get_context_data(
					form=form,
                    address_form=address_form
			)
		)

	def get_success_url(self):
		return reverse('patient:list')

@method_decorator(login_required, name='dispatch')
class PatientList(ListView):

	model = Patient
	http_method_names = ['get']
	template_name = 'patient/list.html'
	context_object_name = 'patient'
	paginate_by = 25

	def get_queryset(self):
		self.queryset = super(PatientList, self).get_queryset()
		if self.request.GET.get('search_box', False):
			self.queryset=self.queryset.filter(name__icontains = self.request.GET['search_box'])
		return self.queryset

	def get_context_data(self, **kwargs):
		_super = super(PatientList, self)
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
class PatientDetail(DetailView):
	model = Patient
	template_name = 'patient/details.html'

	def get_context_data(self,**kwargs): 
		if Consultation.objects.count() > 0:
			context = super(PatientDetail, self).get_context_data(**kwargs)
			context['consultation'] = []
			#Adiciona a consulta do paciente a uma lista
			for cons in self.object.patient_consultation.all():
				if(cons.patient.id == self.object.id):
					context['consultation'].append(cons)
			return context
		else:
			return 0

@method_decorator(login_required, name='dispatch')
class PatientReport(DetailView):
	model = Patient
	template_name = 'patient/report.html'

	def get_context_data(self,**kwargs): 
		if Consultation.objects.count() > 0:
			context = super(PatientReport, self).get_context_data(**kwargs)
			context['consultation'] = []
			#Adiciona a consulta do paciente a uma lista
			for cons in self.object.patient_consultation.all():
				if(cons.patient.id == self.object.id):
					context['consultation'].append(cons)
			return context
		else:
			return 0


@method_decorator(login_required, name='dispatch')
class PatientDelete(DeleteView):
	model = Patient
	success_url = reverse_lazy('patient:list')

#End CRUD Patient


# CRUD Consultation
@method_decorator(login_required, name='dispatch')
class ConsultationCreate(CreateView):
	model = Consultation
	template_name = 'consultation/new.html'
	form_class = ConsultationForm
	second_form_class = BodyCircunferenceForm
	third_form_class = EnergyCalcForm
	fourth_form_class = SkinFoldForm

	def get(self, request, *args, **kwargs):
		self.object = None
		self.exam_formset = ExamFormSet()
		form = self.form_class
		bodycirc_form = self.second_form_class
		energycalc_form = self.third_form_class
		skinfold_form = self.fourth_form_class
		return self.render_to_response(
			self.get_context_data(
				form=form,
				bodycirc_form=bodycirc_form,
				energycalc_form=energycalc_form,
				skinfold_form=skinfold_form
			)
		)


	def post(self, request, *args, **kwargs):
		self.object = None
		bodycirc_form = self.second_form_class(self.request.POST)
		energycalc_form = self.third_form_class(self.request.POST)
		skinfold_form = self.fourth_form_class(self.request.POST)
		form = self.get_form()
		self.exam_formset = ExamFormSet(self.request.POST, self.request.FILES)
		if form.is_valid() and bodycirc_form.is_valid() and energycalc_form.is_valid() and skinfold_form.is_valid() and self.exam_formset.is_valid():
			return self.form_valid(form, bodycirc_form, energycalc_form, skinfold_form)
		else:
			return self.form_invalid(form, bodycirc_form, energycalc_form, skinfold_form)

	def form_valid(self, form, bodycirc_form, energycalc_form, skinfold_form):
		self.object = form.save(commit=False)
		self.object.patient = Patient.objects.get(id = self.kwargs['patient'])
		self.object.bodycirc = bodycirc_form.save()
		self.object.energycalc = energycalc_form.save()
		self.object.skinfold = skinfold_form.save()
		self.object.save()
		self.exam_formset.instance = self.object
		self.exam_formset.save()
		return HttpResponseRedirect(reverse('patient:consultation_list', kwargs={'patient':self.kwargs['patient']}))

	def form_invalid(self, form, bodycirc_form, energycalc_form, skinfold_form):
		return self.render_to_response(
			self.get_context_data(
					form=form,
                    bodycirc_form=bodycirc_form,
					energycalc_form=energycalc_form,
					skinfold_form=skinfold_form
			)
		)

	def get_context_data(self, **kwargs):
		context = super(ConsultationCreate,self).get_context_data(**kwargs)
		context['exam_formset'] = self.exam_formset
		context['patient_id'] = self.kwargs['patient']
		context['patient'] = Patient.objects.get(id = self.kwargs['patient'])
		return context


@method_decorator(login_required, name='dispatch')
class ConsultationList(ListView):

	model = Consultation
	http_method_names = ['get']
	template_name = 'consultation/list.html'
	context_object_name = 'consultation'
	paginate_by = 25

	def get_queryset(self):
		self.queryset = super(ConsultationList, self).get_queryset()
		self.queryset = self.queryset.filter(patient = self.kwargs['patient'])
		if self.request.GET.get('search_box', False):
			self.queryset=self.queryset.filter(patient__name__icontains = self.request.GET['search_box'])
		return self.queryset

	def get_context_data(self, **kwargs):
		_super = super(ConsultationList, self)
		context = _super.get_context_data(**kwargs)
		adjacent_pages = 3
		page_number = context['page_obj'].number
		num_pages = context['paginator'].num_pages
		startPage = max(page_number - adjacent_pages, 1)
		#Define o ID da consulta para o Template.
		context['patient_id'] = self.kwargs['patient']
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
class ConsultationDetail(DetailView):
	model = Consultation
	template_name = 'consultation/details.html'

@method_decorator(login_required, name='dispatch')
class ConsultationUpdate(UpdateView):

	model = Consultation
	template_name = 'consultation/new.html'
	form_class = ConsultationForm
	second_form_class = BodyCircunferenceForm
	third_form_class = EnergyCalcForm
	fourth_form_class = SkinFoldForm

	def get_context_data(self, **kwargs):
		self.object = self.get_object()
		self.exam_formset = ExamFormSet(instance = self.object)
		context = super(ConsultationUpdate, self).get_context_data(**kwargs)
		context['exam_formset']=self.exam_formset
		context['patient_id'] = self.object.patient.id
		context['patient'] = Patient.objects.get(id = self.object.patient.id)
		if self.request.POST:
			context['skinfold_form'] = self.fourth_form_class(self.request.POST, instance=self.object)
			context['energycalc_form'] = self.third_form_class(self.request.POST, instance=self.object)
			context['bodycirc_form'] = self.second_form_class(self.request.POST, instance=self.object)
			context['form'] = self.form_class(self.request.POST, instance=self.object.bodycirc)
		else:
			context['skinfold_form'] = self.fourth_form_class(instance=self.object.skinfold)
			context['energycalc_form'] = self.third_form_class(instance=self.object.energycalc)
			context['bodycirc_form'] = self.second_form_class(instance=self.object.bodycirc)
			context['form'] = self.form_class(instance=self.object)

		return context

	def get(self, request, *args, **kwargs):
		super(ConsultationUpdate, self).get(request, *args, **kwargs)
		form = self.form_class
		bodycirc_form = self.second_form_class
		energycalc_form = self.third_form_class
		skinfold_form = self.fourth_form_class
		return self.render_to_response(
			self.get_context_data(
				object=self.object,
				form=form,
				bodycirc_form=bodycirc_form,
				energycalc_form=energycalc_form,
				skinfold_form=skinfold_form
			)
		)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.exam_formset = ExamFormSet(self.request.POST, self.request.FILES, instance=self.object)
		bodycirc_form = self.second_form_class(self.request.POST)
		energycalc_form = self.third_form_class(self.request.POST)
		skinfold_form = self.fourth_form_class(self.request.POST)
		form = self.get_form()
		if form.is_valid() and bodycirc_form.is_valid() and energycalc_form.is_valid() and skinfold_form.is_valid() and self.exam_formset.is_valid():
			return self.form_valid(form, bodycirc_form, energycalc_form, skinfold_form)
		else:
			return self.form_invalid(form, bodycirc_form), energycalc_form, skinfold_form

	def form_valid(self, form, bodycirc_form, energycalc_form, skinfold_form):
		self.object = form.save(commit=False)
		self.object.bodycirc = bodycirc_form.save()
		self.object.energycalc = energycalc_form.save(commit=False)
		self.object.energycalc.mbr = decimal.Decimal(self.object.mbr())
		self.object.energycalc = energycalc_form.save()
		self.object.skinfold = skinfold_form.save()
		self.object.save()
		self.exam_formset.instance = self.object
		self.exam_formset.save()
		return HttpResponseRedirect(self.get_success_url())

	def form_invalid(self, form, bodycirc_form, energycalc_form, skinfold_form):
		context = super(ConsultationUpdate,self).get_context_data(**kwargs)
		context['exam_formset']=self.exam_formset
		return self.render_to_response(
			self.get_context_data(
					form=form,
                    bodycirc_form=bodycirc_form,
                    energycalc_form=energycalc_form,
                    skinfold_form=skinfold_form
			)
		)

	success_url = reverse_lazy('patient:consultation_list')

@method_decorator(login_required, name='dispatch')
class ConsultationDelete(DeleteView):
	model = Consultation

	def delete(self, request, *args, **kwargs):
	    self.object = self.get_object()
	    id_return = self.object.patient.id
	    #print(">>>>>>>", id_return)
	    self.object.delete()
	    messages.add_message(request, messages.SUCCESS, 'Consulta removido com sucesso!')
	    return HttpResponseRedirect(reverse('patient:consultation_list', kwargs={'patient': id_return}))
class FoodAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		# Don't forget to filter out results depending on the visitor !

		qs = Food.objects.all()

		# Pesquisa pela Descrição
		if self.q:
			qs = qs.filter(Q(description__icontains=self.q))
		print(qs)
		return qs

# FoodAnalysis CRUD
@method_decorator(login_required, name='dispatch')
class FoodAnalysisList(ListView):

	model = FoodAnalysis
	http_method_names = ['get']
	template_name = 'analysis/list.html'
	context_object_name = 'analysis'
	paginate_by = 25

	def get_queryset(self):
		self.queryset = super(FoodAnalysisList, self).get_queryset()
		self.queryset = self.queryset.filter(consultation = self.kwargs['consultation'])
		if self.request.GET.get('search_box', False) :
			self.queryset=self.queryset.filter(title__icontains = self.request.GET['search_box'])
		return self.queryset

	def get_context_data(self, **kwargs):
		_super = super(FoodAnalysisList, self)
		context = _super.get_context_data(**kwargs)
		adjacent_pages = 3
		page_number = context['page_obj'].number
		num_pages = context['paginator'].num_pages
		startPage = max(page_number - adjacent_pages, 1)
		#Define o ID da consulta para o Template.
		context['consultation_id'] = self.kwargs['consultation']
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

#@method_decorator(login_required, name='dispatch')
class FoodAnalysisDetail(DetailView):
	model = FoodAnalysis
	template_name = 'analysis/details.html'

@method_decorator(login_required, name='dispatch')
class FoodAnalysisCreate(CreateView):
	model = FoodAnalysis
	template_name = 'analysis/new.html'
	form_class = FoodAnalysisForm
	second_form_class = MealForm

	def get(self, request, *args, **kwargs):
		self.object = None
		self.consultation = Consultation.objects.get(id = self.kwargs['consultation'])
		form = self.form_class
		meal_form = self.second_form_class
		return self.render_to_response(
			self.get_context_data(
				form=form,
				meal_form=meal_form
			)
		)

	def post(self, request, *args, **kwargs):
		self.object = None
		meal_form = self.second_form_class(self.request.POST)
		form = self.form_class(self.request.POST)

		if form.is_valid() and meal_form.is_valid():
			messages.add_message(request, messages.SUCCESS, 'Cardápio adicionado com sucesso!')
			return self.form_valid(form, meal_form)
		else:
			return self.form_invalid(form, meal_form)

	def form_valid(self, form, meal_form):
		self.object = meal_form.save(commit=False)
		analysis = form.save(commit=False)
		analysis.consultation = Consultation.objects.get(id = self.kwargs['consultation'])
		analysis.save()
		self.object.food_analysis = analysis
		self.object.save()
		return HttpResponseRedirect(reverse('patient:analysis_edit', kwargs={'pk':analysis.pk}))

	def form_invalid(self, form, meal_form):
		return self.render_to_response(
			self.get_context_data(
					form=form,
                    meal_form=meal_form
			)
		)

	def get_context_data(self, **kwargs):
		context = super(FoodAnalysisCreate,self).get_context_data(**kwargs)
		context['consultation_id'] = self.kwargs['consultation']
		context['consultation'] = Consultation.objects.get(id = self.kwargs['consultation'])
		return context

@method_decorator(login_required, name='dispatch')
class FoodAnalysisUpdate(UpdateView):
	model = FoodAnalysis
	template_name = 'analysis/new.html'
	form_class = FoodAnalysisForm
	second_form_class = MealForm

	def get_context_data(self, **kwargs):
		self.object = self.get_object()
		context = super(FoodAnalysisUpdate, self).get_context_data(**kwargs)
		context['consultation_id'] = self.object.consultation.id
		context['consultation'] = Consultation.objects.get(id = self.object.consultation.id)
		if self.request.POST:
			#context['meal_form'] = self.second_form_class(self.request.POST, instance=self.object)
			context['form'] = self.form_class(self.request.POST, instance=self.object)
		else:
			#context['meal_form'] = self.second_form_class(instance=self.object)
			context['form'] = self.form_class(instance=self.object)

		return context



	def get(self, request, *args, **kwargs):
		super(FoodAnalysisUpdate, self).get(request, *args, **kwargs)
		form = self.form_class
		meal_form = self.second_form_class
		return self.render_to_response(
			self.get_context_data(
				object=self.object,
				form=form,
				meal_form=meal_form
			)
		)

		return self.render_to_response(self.get_context_data())

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		meal_form = self.second_form_class(self.request.POST)
		form = self.form_class(self.request.POST, instance=self.object)

		if form.is_valid() and meal_form.is_valid():
			return self.form_valid(form, meal_form)
		else:
			return self.form_invalid(form, meal_form)

	def form_valid(self, form, meal_form):
		self.object = meal_form.save(commit=False)
		analysis = form.save(commit=False)
#		analysis.consultation = Consultation.objects.get(id = self.kwargs['consultation'])
		analysis.save()
		self.object.food_analysis = analysis
		self.object.save()
		return HttpResponseRedirect(reverse('patient:analysis_edit', kwargs={'pk':analysis.pk}))

	def form_invalid(self, form, meal_form):
		return self.render_to_response(
			self.get_context_data(
					form=form,
                    meal_form=meal_form
			)
		)

	def get_success_url(self):
		return HttpResponseRedirect(reverse('patient:analysis_list', kwargs={'consultation': id_return}))

@method_decorator(login_required, name='dispatch')
class FoodAnalysisDelete(DeleteView):
	model = FoodAnalysis
	#success_url = reverse_lazy('patient:analysis_list')

	def delete(self, request, *args, **kwargs):
	    self.object = self.get_object()
	    id_return = self.object.consultation.id
	    #print(">>>>>>>", id_return)
	    self.object.delete()
	    messages.add_message(request, messages.SUCCESS, 'Cardápio removido com sucesso!')
	    return HttpResponseRedirect(reverse('patient:analysis_list', kwargs={'consultation': id_return}))

def meal_delete(request, pk):
	meal = get_object_or_404(Meal,id=pk)
	id_return = meal.food_analysis.id
	success_url = reverse('patient:analysis_edit', kwargs={'pk': id_return})

	if not request.user.is_superuser:
		messages.add_message(request, messages.INFO, 'Você precisa ser administrador para realizar esta ação.')
	else:
		meal.delete()
		messages.add_message(request, messages.SUCCESS, 'Refeição removida com sucesso!')
	return HttpResponseRedirect(success_url)

# End FoodAnalysis CRUD

