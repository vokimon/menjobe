from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from . import views

urlpatterns = patterns('',
	url(r'^json/allproducts$',               views.allProducts),
	url(r'^json/productretailers/([0-9]+)$', views.retailersForProduct),
	url(r'^json/retailer/([0-9]+)$', views.retailerDetails),
	url(r'^json/retailer/([0-9]+)/products$', views.productsForRetailer),
	url(r'^$',
			TemplateView.as_view(template_name='menjobe/home.html')),
)
