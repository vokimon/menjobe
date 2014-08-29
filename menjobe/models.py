from django.db import models


class Product(models.Model) :
	name = models.CharField(
			max_length=200,
			default=None,
			unique=True,
			)

	def __str__(self) :
		return self.name

class RetailPoint(models.Model) :
	name = models.CharField(
			max_length=200,
			default=None,
			unique=True,
			)
	retailedProducts = models.ManyToManyField(Product)

	def __str__(self) :
		return self.name

	def sells(self, *products) :
		self.retailedProducts.add(*products)

	def products(self) :
		return self.retailedProducts.all()


