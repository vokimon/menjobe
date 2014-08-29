from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'devsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^json/allproducts$', 'menjobe.views.allProducts'),
    url(r'^json/productretailers/([0-9]+)$', 'menjobe.views.retailersForProduct'),
    url(r'^admin/', include(admin.site.urls)),
)

