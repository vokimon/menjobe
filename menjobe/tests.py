from django.test import TestCase

from .models import Product

class Product_Test(TestCase) :
	def test_name(self) :
		p = Product(name="Tomato")
		self.assertEqual(p.name, "Tomato")
		p.save()
		self.assertEqual(p.id, 1)






