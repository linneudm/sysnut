from django.conf.urls import url
from .views import *


urlpatterns = [
    # Autocomplete
    #url(r'^patient-autocomplete/$', views.PatientAutocomplete.as_view(), name='patient-autocomplete'),
    # Nutritionist
    url(r'^add/$', permission_required('nutritionist:list', raise_exception=True)(NutritionistCreate.as_view()), name='create'),
    url(r'^edit/(?P<pk>[0-9]+)/$', permission_required('nutritionist:list', raise_exception=True)(NutritionistUpdate.as_view()), name='edit'),
	url(r'^list/$', permission_required('nutritionist:list', raise_exception=True)(NutritionistList.as_view()), name='list'),
    url(r'^details/(?P<pk>[0-9]+)/$', permission_required('nutritionist:list', raise_exception=True)(NutritionistDetail.as_view()), name='details'),
    url(r'^delete/(?P<pk>[0-9]+)/$', permission_required('nutritionist:delete', raise_exception=True)(NutritionistDelete.as_view()), name='delete'),


]
