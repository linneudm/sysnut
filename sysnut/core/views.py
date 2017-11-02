
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth import login

# Página inicial
def index(request):
	return render(request, 'index.html')
