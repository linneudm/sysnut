
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth import login
#from sysnut.settings import *

# Página inicial
def index(request):
	return render(request, 'index.html')

def about(request):
	return render(request, 'about.html')