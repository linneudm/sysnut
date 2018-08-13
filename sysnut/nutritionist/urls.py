from django.conf.urls import url
from .views import *


urlpatterns = [
    # Autocomplete
    #url(r'^patient-autocomplete/$', views.PatientAutocomplete.as_view(), name='patient-autocomplete'),
    # Nutritionist
    url(r'^add/$', NutritionistCreate.as_view(), name='create'),
    url(r'^edit/(?P<pk>[0-9]+)/$', permission_required('nutritionist:edit', raise_exception=True)(NutritionistUpdate.as_view()), name='edit'),
    url(r'^logo/(?P<pk>[0-9]+)/$', permission_required('patient.add_patient', raise_exception=True)(NutritionistLogo.as_view()), name='logo'),
	url(r'^list/$', permission_required('nutritionist:list', raise_exception=True)(NutritionistList.as_view()), name='list'),
    url(r'^details/(?P<pk>[0-9]+)/$', permission_required('nutritionist:details', raise_exception=True)(NutritionistDetail.as_view()), name='details'),
    url(r'^delete/(?P<pk>[0-9]+)/$', permission_required('nutritionist:delete', raise_exception=True)(NutritionistDelete.as_view()), name='delete'),

    #Guidance
    url(r'^guidance-autocomplete/$', GuidanceAutocomplete.as_view(), name='guidance_autocomplete'),
    url(r'^guidace/add/$', permission_required('patient.add_patient', raise_exception=True)(GuidanceCreate.as_view()), name='guidance_create'),
    url(r'^guidance/edit/(?P<pk>[0-9]+)/$', permission_required('patient.add_patient', raise_exception=True)(GuidanceUpdate.as_view()), name='guidance_edit'),
	url(r'^guidance/list/$', permission_required('patient.add_patient', raise_exception=True)(GuidanceList.as_view()), name='guidance_list'),
    url(r'^guidance/details/(?P<pk>[0-9]+)/$', permission_required('patient.add_patient', raise_exception=True)(GuidanceDetail.as_view()), name='guidance_details'),
    url(r'^guidance/delete/(?P<pk>[0-9]+)/$', permission_required('patient.add_patient', raise_exception=True)(GuidanceDelete.as_view()), name='guidance_delete'),


]
