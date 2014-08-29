from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Product

def allProducts(request) :
	data = [
		(p.id, str(p))
		for p in Product.objects.all()
	]
	return JsonResponse(data, safe=False)

def retailersForProduct(request, productId) :
	product = Product.objects.get(id=productId)
	data = [
		(r.id, str(r) )
		for r in product.retailPoints()
	]
	return JsonResponse(data, safe=False)


