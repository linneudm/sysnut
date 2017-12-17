# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from .forms import *
from django.contrib import messages




@login_required
def edit(request):
	template_name = "edit.html"
	context = {}
	if request.method == "POST":
		form = EditAccountForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, "Os dados da conta foram alterados com sucesso")
			return redirect("core:index")
	else:
		form = EditAccountForm(instance=request.user)

	context['form'] = form
	return render(request, template_name, context)
