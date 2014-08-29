from django.test import TestCase

from .models import Product
#from .models import DistributionPoint

from django.db.utils import IntegrityError

class Product_Test(TestCase) :
	def test_name(self) :
		p = Product(name="Tomato")
		self.assertEqual(p.name, "Tomato")
		self.assertEqual(p.id, None)
		p.save()
		self.assertEqual(p.id, 1)

	def test_str(self) :
		p = Product(name="Tomato")
		self.assertEqual(str(p), "Tomato")

	def test_notName_raisesIntegrity(self) :
		p = Product()
		with self.assertRaises(IntegrityError) as cm :
			p.save()
		self.assertEquals(str(cm.exception),
			"NOT NULL constraint failed: menjobe_product.name")

from .models import RetailPoint

class RetailPoint_Test(TestCase) :

	def test_withName(self) :
		r = RetailPoint(name="Can Xavi")
		self.assertEqual(r.name, "Can Xavi")
		r.save()
		self.assertNotEqual(r.id, None)

	def test_str(self) :
		r = RetailPoint(name="Can Xavi")
		self.assertEqual(str(r), "Can Xavi")
		r.save()
		self.assertNotEqual(r.id, None)





