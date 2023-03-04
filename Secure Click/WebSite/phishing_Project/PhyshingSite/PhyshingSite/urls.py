"""PhyshingSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from PhyshingApp.views import home,URL,resultURL,SMSEMAIL,resultMasage,AboutUs,homeAR,URLAr,reseltURLAr,SMSEMAILAr,resultSMSEMAIAr,AboutUsAr

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', home, name='home'),
    path('Ar/', homeAR, name='homeAR'),

    path('URL/', URL, name='URL'),
    path('Ar/URLAr', URLAr, name='URLAr'),
    path('URLAr', URLAr, name='URLAr'),

    path('URL/resultURL/', resultURL, name='resultURL'),
    path('Ar/reseltURLAr/', reseltURLAr, name='reseltURLAr'),
    path('reseltURLAr/', reseltURLAr, name='reseltURLAr'),

    path('SMSEMAIL/', SMSEMAIL, name='SMSEMAIL'),
    path('Ar/SMSEMAILAr', SMSEMAILAr, name='SMSEMAILAr'),
    path('SMSEMAILAr', SMSEMAILAr, name='SMSEMAILAr'),

    path('SMSEMAIL/resultSMSEMAIL/', resultMasage, name='resultMasage'),
    path('Ar/resultSMSEMAIAr/', resultSMSEMAIAr, name='resultSMSEMAIAr.html'),
    path('resultSMSEMAIAr/', resultSMSEMAIAr, name='resultSMSEMAIAr.html'),

    path('AboutUs/', AboutUs, name='AboutUs'),
    path('AboutUsAr/', AboutUsAr, name='AboutUsAr'),
    path('Ar/AboutUsAr', AboutUsAr, name='AboutUsAr'),

]
