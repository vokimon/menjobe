from django.test import TestCase
from .views import allProducts
from .views import retailersForProduct
from .views import retailerDetails
from .views import productsForRetailer
from django.test import RequestFactory
from .models import Product
from .models import RetailPoint
import json

class View_Test(TestCase) :
	def setUp(self):
		self.factory = RequestFactory()

	def assertJSONResponseEqual(self, response, data) :
		self.assertJSONEqual(
			response.content.decode("utf-8"),
			json.dumps( data))

	def test_json_allProducts(self) :

		Product(name="Product 1").save()
		Product(name="Product 2").save()

		request = self.factory.get("/booo")
		response = allProducts(request)

		self.assertJSONResponseEqual(response,
			[
				dict(id=1,name="Product 1"),
				dict(id=2,name="Product 2"),
			])

	def test_json_retailersForProduct(self) :

		p1 = Product(name="Product 1")
		p2 = Product(name="Product 2")
		r1 = RetailPoint(name="Retailer 1")
		for a in p1, p2, r1 : a.save()

		r1.sells(p1)

		request = self.factory.get("/booo")
		response = retailersForProduct(request, p1.id)

		self.assertJSONResponseEqual(response,
			[
				dict(id=1,name="Retailer 1"),
			])


	def test_json_productsForRetailer(self) :

		p1 = Product(name="Product 1")
		p2 = Product(name="Product 2")
		r1 = RetailPoint(name="Retailer 1")
		for a in p1, p2, r1 : a.save()

		r1.sells(p1)

		request = self.factory.get("/booo")
		response = productsForRetailer(request, p1.id)

		self.assertJSONResponseEqual(response,
			[
				dict(id=1,name="Product 1"),
			])


	def test_json_retailerDetails(self) :
		r1 = RetailPoint(
			name="Retailer 1",
			description="A nice retailer",
			)
		r1.save()

		request = self.factory.get("/booo")
		response = retailerDetails(request, r1.id)

		self.assertJSONResponseEqual(response,
				dict(
					id=1,
					name="Retailer 1",
					description="A nice retailer",
					descriptionHtml = "<p>A nice retailer</p>",
					address = None,
			))


