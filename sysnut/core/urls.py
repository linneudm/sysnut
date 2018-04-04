from django.conf.urls import url
from .views import *
from django.contrib.auth.decorators import permission_required

urlpatterns = [
	# Home
    url(r'^$', index, name='index'),
    url(r'instructions/$', instructions, name='instructions'),
    url(r'about/$', about, name='about'),
    url(r'calculator/$', permission_required('patient.add_patient', raise_exception=True)(calculator), name='calculator'),
]
