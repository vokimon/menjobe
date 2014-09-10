from django.test import TestCase
from unittest import skip

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

	def collect(self, iterable) :
		return "".join("{}\n".format(o) for o in iterable)

	def test_group(self) :
		p1 = Product(name="grandpa")
		p2 = Product(name="dad", group=p1)
		p3 = Product(name="oncle", group=p1)
		p4 = Product(name="me", group=p2)
		p5 = Product(name='sis', group=p2)
		p6 = Product(name='son', group=p4)
		p7 = Product(name='daughter', group=p4)

		for p in p1,p2,p3,p4,p5,p6,p7 : p.save()

		self.assertMultiLineEqual(self.collect(p2.get_descendants()),
			"me\n"
			"son\n"
			"daughter\n"
			"sis\n"
			)
		self.assertMultiLineEqual(self.collect(p2.get_descendants(include_self=True)),
			"dad\n"
			"me\n"
			"son\n"
			"daughter\n"
			"sis\n"
			)



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

	def test_description_defaultTrue(self) :
		r = RetailPoint(name="A retailer")
		r.save()
		self.assertMultiLineEqual(r.description, "")

	def test_description_blankRaises(self) :
		r = RetailPoint(name="A retailer", description=None)
		with self.assertRaises(IntegrityError) as cm :
			r.save()
		self.assertEqual(str(cm.exception),
			'NOT NULL constraint failed: menjobe_retailpoint.description')

	def test_description_set(self) :
		r = RetailPoint(name="A retailer", description="They\nretail")
		r.save()
		self.assertMultiLineEqual(r.description, "They\nretail")

	def test_descriptionHtml(self) :
		r = RetailPoint(name="A retailer", description="They\nretail")
		self.assertHTMLEqual(
			r.descriptionHtml(),
			"<p>They retail</p>")

	def test_address_defaultTrue(self) :
		r = RetailPoint(name="A retailer")
		r.save()
		self.assertEqual(r.address, None)

	@skip("Not working")
	def test_address_blankRaises(self) :
		r = RetailPoint(name="A retailer", address="")
		with self.assertRaises(IntegrityError) as cm :
			r.save()
		self.assertEqual(str(cm.exception),
			'NOT NULL constraint failed: menjobe_retailpoint.address')

	def test_address_set(self) :
		r = RetailPoint(name="A retailer", address="Percebe, 13, Baixos")
		r.save()
		self.assertEqual(r.address, "Percebe, 13, Baixos")



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

	def save(self, *args) :
		return [a.save() for a in args ]

	def test_productList_whenEmpty(self) :
		r = RetailPoint(name="a retail point")
		r.save()

		self.assertEqual(
			self.collect(r.products()),
			"")

	def test_productList_whenOne(self) :
		r = RetailPoint(name="a retail point")
		p = Product(name="Product 1")
		self.save( r, p )

		r.sells(p)

		self.assertEqual(
			self.collect(r.products()),
			"Product 1\n"
			"")

	def test_productList_whenMany(self) :
		r = RetailPoint(name="a retail point")
		p1 = Product(name="Product 1")
		p2 = Product(name="Product 2")
		self.save( r, p1, p2 )

		r.sells(p1, p2)

		self.assertEqual(
			self.collect(r.products()),
			"Product 1\n"
			"Product 2\n"
			"")

	def test_productRetailPoints_noRetailers(self) :
		p = Product(name="a product")
		p.save()
		self.assertEqual(
			self.collect(p.retailPoints()),
			"")

	def test_productRetailPoints_oneRetailer(self) :
		r = RetailPoint(name="Retailer 1")
		p = Product(name="a product")
		self.save( p, r)

		r.sells(p)

		self.assertEqual(
			self.collect(p.retailPoints()),
			"Retailer 1\n"
			"")

	def test_productRetailPoints_manyRetailers(self) :
		r1 = RetailPoint(name="Retailer 1")
		r2 = RetailPoint(name="Retailer 2")
		p = Product(name="a product")
		self.save(p, r1, r2)

		r1.sells(p)
		r2.sells(p)

		self.assertEqual(
			self.collect(p.retailPoints()),
			"Retailer 1\n"
			"Retailer 2\n"
			"")


	def test_productRetailPoints_withProductHierarchy(self) :
		r1  = RetailPoint(name="Retailer 1")
		r2  = RetailPoint(name="Retailer 2")
		r3  = RetailPoint(name="Retailer 3")
		pa  = Product(name="Product A")
		pb  = Product(name="Product B")
		paa = Product(name="Product A.a", group=pa)
		self.save(pa, pb, paa, r1, r2)

		r1.sells(pa)
		r2.sells(paa)

		self.assertEqual(
			self.collect(pa.retailPoints()),
			"Retailer 1\n"
			"Retailer 2\n"
			"")

	def test_productRetailPoints_withManyVarietiesAppearsOnce(self) :
		r1  = RetailPoint(name="Retailer 1")
		pa  = Product(name="Poma")
		paa = Product(name="Poma Golden", group=pa)
		pab = Product(name="Poma Reineta", group=pa)
		self.save(pa, paa, pab, r1)

		r1.sells(paa)
		r1.sells(pab)

		self.assertEqual(
			self.collect(pa.retailPoints()),
			"Retailer 1\n"
			"")






