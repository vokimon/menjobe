from django.test import TestCase

from .models import Product

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

	def test_name_unique(self) :
		p = Product(name="Tomato")
		p.save()
		p2 = Product(name="Tomato")
		with self.assertRaises(IntegrityError) as cm :
			p2.save()
		self.assertEqual(str(cm.exception),
			"UNIQUE constraint failed: menjobe_product.name")

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

	def test_name_nullRaises(self) :
		r = RetailPoint()
		with self.assertRaises(IntegrityError) as cm :
			r.save()
		self.assertEquals(str(cm.exception),
			"NOT NULL constraint failed: menjobe_retailpoint.name")

	def test_name_unique(self) :
		r = RetailPoint(name="Can Xavi")
		r.save()
		r2 = RetailPoint(name="Can Xavi")
		with self.assertRaises(IntegrityError) as cm :
			r2.save()
		self.assertEqual(str(cm.exception),
			"UNIQUE constraint failed: menjobe_retailpoint.name")

class ProductsInRetailPoints_Test(TestCase) :
	def collect(self, iterable) :
		return "".join("{}\n".format(o) for o in iterable)

	def test_collect(self) :
		rows = [1,2,3,4]
		self.assertEqual(self.collect(rows),
			"1\n"
			"2\n"
			"3\n"
			"4\n"
		)

	def test_productList_whenEmpty(self) :
		r = RetailPoint(name="a retail point")
		r.save()

		self.assertEqual(
			self.collect(r.retailedProducts.all()),
			"")

	def test_productList_whenOne(self) :
		r = RetailPoint(name="a retail point")
		p = Product(name="Product 1")
		for a in r, p : a.save()

		r.retailedProducts.add(p)

		self.assertEqual(
			self.collect(r.retailedProducts.all()),
			"Product 1\n"
			"")

	def test_productList_whenMany(self) :
		r = RetailPoint(name="a retail point")
		p1 = Product(name="Product 1")
		p2 = Product(name="Product 2")
		for a in r, p1, p2 : a.save()

		r.retailedProducts.add(p1, p2)

		self.assertEqual(
			self.collect(r.retailedProducts.all()),
			"Product 1\n"
			"Product 2\n"
			"")

	def test_productRetailPoints_noRetailers(self) :
		p = Product(name="a product")
		p.save()
		self.assertEqual(
			self.collect(p.retailpoint_set.all()),
			"")

	def test_productRetailPoints_oneRetailer(self) :
		r = RetailPoint(name="Retailer 1")
		p = Product(name="a product")
		for a in p, r: a.save()

		r.retailedProducts.add(p)

		self.assertEqual(
			self.collect(p.retailpoint_set.all()),
			"Retailer 1\n"
			"")

	def test_productRetailPoints_manyRetailers(self) :
		r1 = RetailPoint(name="Retailer 1")
		r2 = RetailPoint(name="Retailer 2")
		p = Product(name="a product")
		for a in p, r1, r2 : a.save()

		r1.retailedProducts.add(p)
		r2.retailedProducts.add(p)

		self.assertEqual(
			self.collect(p.retailpoint_set.all()),
			"Retailer 1\n"
			"Retailer 2\n"
			"")






