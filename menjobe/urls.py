from django.conf.urls import patterns, include, url
from django.views.generic import ListView

urlpatterns = patterns('',
    url(r'^json/allproducts$',               'menjobe.views.allProducts'),
    url(r'^json/productretailers/([0-9]+)$', 'menjobe.views.retailersForProduct'),
    url(r'^$',                               'menjobe.views.home'),
)
