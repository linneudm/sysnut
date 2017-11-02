from django.conf.urls import url
from .views import *


urlpatterns = [
    # Autocomplete
    url(r'^patology-autocomplete/$', PatologyAutocomplete.as_view(create_field='description'), name='patology_autocomplete'),
    # Patient
    url(r'^add/$', PatientCreate.as_view(), name='create'),
    url(r'^edit/(?P<pk>[0-9]+)/$', PatientUpdate.as_view(), name='edit'),
    # Duplicar item, ver tratamento no HTML "new.html"
    url(r'^duplicate/(?P<pk>[0-9]+)/$', PatientUpdate.as_view(), name='duplicate'),
	url(r'^list/$', PatientList.as_view(), name='list'),
    url(r'^details/(?P<pk>[0-9]+)/$', PatientDetail.as_view(), name='details'),
    url(r'^delete/(?P<pk>[0-9]+)/$',PatientDelete.as_view(), name='delete'),

    #Consultation
    url(r'^consultation/add/$', ConsultationCreate.as_view(), name='consultation_create'),
    url(r'^consultation/edit/(?P<pk>[0-9]+)/$', ConsultationUpdate.as_view(), name='consultation_edit'),
    url(r'^consultation/duplicate/(?P<pk>[0-9]+)/$', ConsultationUpdate.as_view(), name='consultation_duplicate'),
	url(r'^consultation/list/$', ConsultationList.as_view(), name='consultation_list'),
    url(r'^consultation/details/(?P<pk>[0-9]+)/$', ConsultationDetail.as_view(), name='consultation_details'),
    url(r'^consultation/delete/(?P<pk>[0-9]+)/$',ConsultationDelete.as_view(), name='consultation_delete'),

    #FoodAnalysis
    url(r'^analysis/add/$', FoodAnalysisCreate.as_view(), name='analysis_create'),
    url(r'^analysis/edit/(?P<pk>[0-9]+)/$', FoodAnalysisUpdate.as_view(), name='analysis_edit'),
    url(r'^analysis/duplicate/(?P<pk>[0-9]+)/$', FoodAnalysisUpdate.as_view(), name='analysis_duplicate'),
    url(r'^analysis/list/$', FoodAnalysisList.as_view(), name='analysis_list'),
    url(r'^analysis/details/(?P<pk>[0-9]+)/$', FoodAnalysisDetail.as_view(), name='analysis_details'),
    url(r'^analysis/delete/(?P<pk>[0-9]+)/$',FoodAnalysisDelete.as_view(), name='analysis_delete')

    ]
