from django.conf.urls import url
from .views import *
from django.contrib.auth.decorators import permission_required

urlpatterns = [
    # Autocomplete
    url(r'^patology-autocomplete/$', PatologyAutocomplete.as_view(create_field='description'), name='patology_autocomplete'),
    url(r'^biochemical-autocomplete/$', BiochemicalAutocomplete.as_view(create_field='description'), name='biochemical_autocomplete'),
    # Patient
    url(r'^add/$', permission_required('patient.add_patient', raise_exception=True)(PatientCreate.as_view()), name='create'),
    url(r'^edit/(?P<pk>[0-9]+)/$',permission_required('patient.add_patient', raise_exception=True)(PatientUpdate.as_view()), name='edit'),
    # Duplicar item, ver tratamento no HTML "new.html"
    url(r'^duplicate/(?P<pk>[0-9]+)/$', permission_required('patient.add_patient', raise_exception=True)(PatientUpdate.as_view()), name='duplicate'),
	url(r'^list/$', permission_required('patient.add_patient', raise_exception=True)(PatientList.as_view()), name='list'),
    url(r'^details/(?P<pk>[0-9]+)/$', permission_required('patient.add_patient', raise_exception=True)(PatientDetail.as_view()), name='details'),
    url(r'^report/(?P<pk>[0-9]+)/$', permission_required('patient.add_patient', raise_exception=True)(PatientReport.as_view()), name='report'),
    url(r'^delete/(?P<pk>[0-9]+)/$',permission_required('patient.add_patient', raise_exception=True)(PatientDelete.as_view()), name='delete'),

    #Consultation
    url(r'^consultation/add/(?P<patient>[0-9]+)/$', ConsultationCreate.as_view(), name='consultation_create'),
    url(r'^consultation/edit/(?P<pk>[0-9]+)/$', ConsultationUpdate.as_view(), name='consultation_edit'),
    url(r'^consultation/duplicate/(?P<pk>[0-9]+)/$', ConsultationUpdate.as_view(), name='consultation_duplicate'),
	url(r'^consultation/list/(?P<patient>[0-9]+)/$', ConsultationList.as_view(), name='consultation_list'),
    url(r'^consultation/details/(?P<pk>[0-9]+)/$', ConsultationDetail.as_view(), name='consultation_details'),
    url(r'^consultation/delete/(?P<pk>[0-9]+)/$',ConsultationDelete.as_view(), name='consultation_delete'),
    url(r'^consultation/delete-biochemical/(?P<pk>[0-9]+)/$', biochemical_delete, name='biochemical_delete'),

    #FoodAnalysis
    url(r'^food-autocomplete/$', FoodAutocomplete.as_view(), name='food_autocomplete'),
    url(r'^analysis/publish/(?P<pk>[0-9]+)/$', publish_analysis, name='publish_analysis'),
    url(r'^analysis/add/(?P<consultation>[0-9]+)/$', FoodAnalysisCreate.as_view(), name='analysis_create'),
    url(r'^analysis/edit/(?P<pk>[0-9]+)/$', FoodAnalysisUpdate.as_view(), name='analysis_edit'),
    url(r'^analysis/duplicate/(?P<pk>[0-9]+)/$', FoodAnalysisUpdate.as_view(), name='analysis_duplicate'),
    url(r'^analysis/list/(?P<consultation>[0-9]+)/$', FoodAnalysisList.as_view(), name='analysis_list'),
    url(r'^analysis/details/(?P<pk>[0-9]+)/$', FoodAnalysisDetail.as_view(), name='analysis_details'),
    url(r'^analysis/delete/(?P<pk>[0-9]+)/$',FoodAnalysisDelete.as_view(), name='analysis_delete'),
    url(r'^analysis/delete-meal/(?P<pk>[0-9]+)/$', meal_delete, name='meal_delete')

    ]
