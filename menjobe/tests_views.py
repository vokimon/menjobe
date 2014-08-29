from django.test import TestCase
from .views import allProducts
from .views import retailersForProduct
from django.test import RequestFactory
from .models import Product
from .models import RetailPoint
import json

class View_Test(TestCase) :
	def setUp(self):
		self.factory = RequestFactory()

	def test_json_allProducts(self) :

		Product(name="Product 1").save()
		Product(name="Product 2").save()

		request = self.factory.get("/booo")
		response = allProducts(request)

		self.assertJSONEqual(response.content.decode("utf-8"),
			json.dumps( [
				[1, 'Product 1'],
				[2, 'Product 2'],
			]))

	def test_json_retailersForProduct(self) :

		p1 = Product(name="Product 1")
		p2 = Product(name="Product 2")
		r1 = RetailPoint(name="Retailer 1")
		for a in p1, p2, r1 : a.save()

		r1.sells(p1)

		request = self.factory.get("/booo")
		response = retailersForProduct(request, p1.id)

		self.assertJSONEqual(response.content.decode("utf-8"),
			json.dumps( [
				[1,"Retailer 1"],
			]))



