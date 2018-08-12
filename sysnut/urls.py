"""sysnut URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
#Import urls
from sysnut.core import urls as core_urls
from sysnut.account import urls as account_urls
from sysnut.nutritionist import urls as nutritionist_urls
from sysnut.patient import urls as patient_urls
from sysnut.food import urls as food_urls

from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^messages/', include('django_messages.urls')),
    url(r'^', include(core_urls, namespace='core')),
    url(r'^account/', include(account_urls, namespace='account')),
    url(r'^nutritionist/', include(nutritionist_urls, namespace='nutritionist')),
    url(r'^patient/', include(patient_urls, namespace='patient')),
    url(r'^food/', include(food_urls, namespace='food')),
]

if settings.DEBUG:
	urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
