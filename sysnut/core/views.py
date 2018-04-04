
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth import login
#from sysnut.settings import *

# Página inicial
def index(request):
	return render(request, 'index.html')

def instructions(request):
	return render(request, 'instructions.html')

def about(request):
	return render(request, 'about.html')

def calculator(request):
	return render(request, 'calculator.html')

def page_not_found(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response