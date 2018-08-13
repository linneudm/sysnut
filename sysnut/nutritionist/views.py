# -*- coding: utf-8 -*-

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
from django.contrib.auth.models import Permission
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.forms import formset_factory
from datetime import date, datetime
from sysnut.account.models import Nutritionist, Address, User
from .forms import NutritionistForm, AddressForm, GuidanceForm, LogoForm
from dal import autocomplete
#from .decorators import odontology_required, Nutritionist_show_required
from django.template.response import TemplateResponse
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse_lazy
from sysnut.patient.models import Guidance

#is_nutritionist = user_passes_test(
#    lambda u: u.has_perm('patient.add_patients'), login_url=reverse_lazy('account:login'))

#Guidance Autocomplete
class GuidanceAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		# Don't forget to filter out results depending on the visitor !

		qs = Guidance.objects.all()

		# Pesquisa pela Descrição
		if self.q:
			qs = qs.filter(Q(description__icontains=self.q))

		return qs

# Autocomplete Nutritionist na consulta
class NutritionistAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		# Don't forget to filter out results depending on the visitor !

		qs = Nutritionist.objects.all()

		if self.q:
			qs = qs.filter(name__istartswith=self.q)

		return qs

# Signup nutritionist ---------------------------------------------------------------------------------#


class NutritionistCreate(CreateView):
	model = Nutritionist
	template_name = 'nutritionist/new.html'
	form_class = NutritionistForm
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
			return self.form_valid(form, address_form)
		else:
			return self.form_invalid(form, address_form)

	def form_valid(self, form, address_form):
		self.object = address_form.save()
		nutritionist = form.save(commit=False)
		nutritionist.address = self.object
		#nutritionist.is_staff = True
		permission_list = []
		permission = Permission.objects.get(codename='add_patient')
		permission_list.append(permission)
		permission = Permission.objects.get(codename='add_patology')
		permission_list.append(permission)
		permission = Permission.objects.get(codename='add_food')
		permission_list.append(permission)
		nutritionist.save()
		nutritionist.user_permissions.set(permission_list)
		return HttpResponseRedirect(self.get_success_url())

	def form_invalid(self, form, address_form):
		return self.render_to_response(
			self.get_context_data(
					form=form,
                    address_form=address_form
			)
		)

	def get_success_url(self):
		return reverse('account:login')

@method_decorator(login_required, name='dispatch')
class NutritionistUpdate(UpdateView):

	model = Nutritionist
	template_name = 'nutritionist/new.html'
	form_class = NutritionistForm
	second_form_class = AddressForm

	def get_context_data(self, **kwargs):
		self.object = self.get_object()
		context = super(NutritionistUpdate, self).get_context_data(**kwargs)
		if self.request.POST:
			context['address_form'] = self.second_form_class(self.request.POST, instance=self.object)
			context['form'] = self.form_class(self.request.POST, instance=self.object.address)
		else:
			context['address_form'] = self.second_form_class(instance=self.object.address)
			context['form'] = self.form_class(instance=self.object)

		return context

	def get(self, request, *args, **kwargs):
		super(NutritionistUpdate, self).get(request, *args, **kwargs)
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
		nutritionist = form.save(commit=False)
		nutritionist.address = self.object
		permission_list = []
		permission = Permission.objects.get(codename='add_patient')
		permission_list.append(permission)
		permission = Permission.objects.get(codename='add_patology')
		permission_list.append(permission)
		permission = Permission.objects.get(codename='add_food')
		permission_list.append(permission)
		nutritionist.user_permissions.set(permission_list)
		nutritionist.save()
		return HttpResponseRedirect(self.get_success_url())

	def form_invalid(self, form, address_form):
		return self.render_to_response(
			self.get_context_data(
					form=form,
                    address_form=address_form
			)
		)

	def get_success_url(self):
		return reverse('account:login')

@method_decorator(login_required, name='dispatch')
class NutritionistLogo(UpdateView):
	model = Nutritionist
	template_name = 'nutritionist/new.html'
	form_class = LogoForm

	def form_valid(self, form):
		form.save()
		return HttpResponseRedirect(self.get_success_url())

	def form_invalid(self, form):
		return self.render_to_response(
			self.get_context_data(
				form=form
			)
		)

	def get_success_url(self):
		return reverse('core:index')

@method_decorator(login_required, name='dispatch')
class NutritionistList(ListView):

	model = Nutritionist
	http_method_names = ['get']
	template_name = 'nutritionist/list.html'
	context_object_name = 'nutritionist'
	paginate_by = 25

	def get_queryset(self):
		self.queryset = super(NutritionistList, self).get_queryset()
		if self.request.GET.get('search_box', False):
			self.queryset=self.queryset.filter(first_name__icontains = self.request.GET['search_box'])
		return self.queryset

	def get_context_data(self, **kwargs):
		_super = super(NutritionistList, self)
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
class NutritionistDetail(DetailView):
	model = Nutritionist
	template_name = 'nutritionist/details.html'

@method_decorator(login_required, name='dispatch')
class NutritionistDelete(DeleteView):
	model = Nutritionist
	success_url = reverse_lazy('nutritionist:list')

#End CRUD Nutritionist

# Guidance CRUD
@method_decorator(login_required, name='dispatch')
class GuidanceList(ListView):

	model = Guidance
	http_method_names = ['get']
	template_name = 'guidance/list.html'
	context_object_name = 'guidance'
	paginate_by = 25

	def get_queryset(self):
		self.queryset = super(GuidanceList, self).get_queryset()
		if self.request.GET.get('search_box', False):
			self.queryset=self.queryset.filter(description__icontains = self.request.GET['search_box'])
		return self.queryset

	def get_context_data(self, **kwargs):
		_super = super(GuidanceList, self)
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
class GuidanceDetail(DetailView):
	model = Guidance
	template_name = 'guidance/details.html'

@method_decorator(login_required, name='dispatch')
class GuidanceCreate(CreateView):
	model = Guidance
	template_name = 'guidance/new.html'
	form_class = GuidanceForm

	def get(self, request, *args, **kwargs):
		self.object = None
		form = self.form_class
		return self.render_to_response(
			self.get_context_data(
				form=form,
			)
		)

	def post(self, request, *args, **kwargs):
		self.object = None
		form = self.form_class(self.request.POST)

		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)


	def form_valid(self, form):
		guidance = form.save(commit=False)
		guidance.nut = self.request.user
		guidance.save()
		return HttpResponseRedirect(self.get_success_url())

	def form_invalid(self, form, address_form):
		return self.render_to_response(
			self.get_context_data(
					form=form,
                    address_form=address_form
			)
		)

	def get_success_url(self):
		return reverse('nutritionist:guidance_list')

@method_decorator(login_required, name='dispatch')
class GuidanceUpdate(UpdateView):
	model = Guidance
	template_name = 'guidance/new.html'
	form_class = GuidanceForm
	success_url = reverse_lazy('nutritionist:guidance_list')

@method_decorator(login_required, name='dispatch')
class GuidanceDelete(DeleteView):
	model = Guidance
	success_url = reverse_lazy('nutritionist:guidance_list')

# End Guidance

