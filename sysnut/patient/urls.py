from django.conf.urls import url
from .views import *
from django.contrib.auth.decorators import permission_required

urlpatterns = [
    # Autocomplete
    url(r'^vitamin-autocomplete/$', VitaminAutocomplete.as_view(create_field='description'), name='vitamin_autocomplete'),
    #url(r'^supplement-autocomplete/$', SupplementAutocomplete.as_view(create_field='description'), name='supplement_autocomplete'),
    url(r'^patology-autocomplete/$', PatologyAutocomplete.as_view(create_field='description'), name='patology_autocomplete'),
    url(r'^biochemical-autocomplete/$', BiochemicalAutocomplete.as_view(create_field='description'), name='biochemical_autocomplete'),
    # Patient
    url(r'^add/$', permission_required('patient.add_patient', raise_exception=True)(PatientCreate.as_view()), name='create'),
    url(r'^edit/(?P<pk>[0-9]+)/$',permission_required('patient.add_patient', raise_exception=True)(PatientUpdate.as_view()), name='edit'),
    # Duplicar item, ver tratamento no HTML "new.html"
    url(r'^duplicate/(?P<pk>[0-9]+)/$', permission_required('patient.add_patient', raise_exception=True)(PatientUpdate.as_view()), name='duplicate'),
    url(r'^excel/$', permission_required('patient.add_patient', raise_exception=True)(excel_patient), name='excel_patient'),
    url(r'^pdf/$', permission_required('patient.add_patient', raise_exception=True)(pdf_patient), name='pdf_patient'),
	url(r'^list/$', permission_required('patient.add_patient', raise_exception=True)(PatientList.as_view()), name='list'),
    url(r'^details/(?P<pk>[0-9]+)/$', permission_required('patient.add_patient', raise_exception=True)(PatientDetail.as_view()), name='details'),
    url(r'^report/(?P<pk>[0-9]+)/$',PatientReport.as_view(), name='report'),
    url(r'^print/(?P<pk>[0-9]+)/$',PatientPrint.as_view(), name='print'),
    url(r'^delete/(?P<pk>[0-9]+)/$',permission_required('patient.add_patient', raise_exception=True)(PatientDelete.as_view()), name='delete'),

    #Consultation
    url(r'^consultation/excel/$', permission_required('patient.add_patient', raise_exception=True)(excel_consultation), name='excel_consultation'),
    url(r'^consultation/pdf/$', permission_required('patient.add_patient', raise_exception=True)(pdf_consultation), name='pdf_consultation'),
    url(r'^consultation/add/(?P<patient>[0-9]+)/$', permission_required('patient.add_patient', raise_exception=True)(ConsultationCreate.as_view()), name='consultation_create'),
    url(r'^consultation/edit/(?P<pk>[0-9]+)/$', permission_required('patient.add_patient', raise_exception=True)(ConsultationUpdate.as_view()), name='consultation_edit'),
    url(r'^consultation/duplicate/(?P<pk>[0-9]+)/$', permission_required('patient.add_patient', raise_exception=True)(ConsultationUpdate.as_view()), name='consultation_duplicate'),
	url(r'^consultation/list/(?P<patient>[0-9]+)/$', permission_required('patient.add_patient', raise_exception=True)(ConsultationList.as_view()), name='consultation_list'),
    url(r'^consultation/details/(?P<pk>[0-9]+)/$', permission_required('patient.add_patient', raise_exception=True)(ConsultationDetail.as_view()), name='consultation_details'),
    url(r'^consultation/delete/(?P<pk>[0-9]+)/$',permission_required('patient.add_patient', raise_exception=True)(ConsultationDelete.as_view()), name='consultation_delete'),
    url(r'^consultation/delete-biochemical/(?P<pk>[0-9]+)/$', permission_required('patient.add_patient', raise_exception=True)(biochemical_delete), name='biochemical_delete'),

    #FoodAnalysis
    url(r'^food-autocomplete/$', FoodAutocomplete.as_view(), name='food_autocomplete'),
    url(r'^guidanceaux-autocomplete/$', GuidanceAuxAutocomplete.as_view(), name='guidanceaux_autocomplete'),
    #url(r'^guidance-autocomplete/$', GuidanceAutocomplete.as_view(), name='guidance_autocomplete'),
    url(r'^guidance/upload/$', permission_required('patient.add_patient', raise_exception=True)(UploadGuidance.as_view()), name='upload_guidance'),
    url(r'^analysis/publish/(?P<pk>[0-9]+)/$', permission_required('patient.add_patient', raise_exception=True)(publish_analysis), name='publish_analysis'),
    url(r'^analysis/add/(?P<consultation>[0-9]+)/$', permission_required('patient.add_patient', raise_exception=True)(FoodAnalysisCreate.as_view()), name='analysis_create'),
    url(r'^analysis/edit/(?P<pk>[0-9]+)/$', permission_required('patient.add_patient', raise_exception=True)(FoodAnalysisUpdate.as_view()), name='analysis_edit'),
    url(r'^analysis/guidance/(?P<pk>[0-9]+)/$', permission_required('patient.add_patient', raise_exception=True)(FoodAnalysisGuidance.as_view()), name='analysis_guidance'),
    url(r'^analysis/duplicate/(?P<pk>[0-9]+)/$', permission_required('patient.add_patient', raise_exception=True)(FoodAnalysisUpdate.as_view()), name='analysis_duplicate'),
    url(r'^analysis/list/(?P<consultation>[0-9]+)/$', permission_required('patient.add_patient', raise_exception=True)(FoodAnalysisList.as_view()), name='analysis_list'),
    url(r'^analysis/details/(?P<pk>[0-9]+)/$',FoodAnalysisDetail.as_view(), name='analysis_details'),
    url(r'^analysis/print/(?P<pk>[0-9]+)/$',FoodAnalysisPrint.as_view(), name='analysis_print'),
    url(r'^analysis/delete/(?P<pk>[0-9]+)/$',permission_required('patient.add_patient', raise_exception=True)(FoodAnalysisDelete.as_view()), name='analysis_delete'),
    url(r'^analysis/delete-meal/(?P<pk>[0-9]+)/$', permission_required('patient.add_patient', raise_exception=True)(meal_delete), name='meal_delete'),
    url(r'^analysis/ajax_measure/$', permission_required('patient.add_patient', raise_exception=True)(load_measure), name='food_measure'),
    #Formula
    url(r'^formula/add/$', permission_required('nutritionist:delete', raise_exception=True)(FormulaCreate.as_view()), name='formula_create'),
    url(r'^formula/edit/(?P<pk>[0-9]+)/$', permission_required('nutritionist:delete', raise_exception=True)(FormulaUpdate.as_view()), name='formula_edit'),
    url(r'^formula/delete/(?P<pk>[0-9]+)/$',permission_required('nutritionist:delete', raise_exception=True)(FormulaDelete.as_view()), name='formula_delete'),
    url(r'^formula/list/$', permission_required('nutritionist:delete', raise_exception=True)(FormulaList.as_view()), name='formula_list'),
    url(r'^formula/ajax_activity/$', permission_required('patient.add_patient', raise_exception=True)(load_activity), name='formula_activity'),

]
