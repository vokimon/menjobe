from django.db import models


class Product(models.Model) :
	name = models.CharField(max_length=200, default=None)

	def __str__(self) :
		return self.name

class RetailPoint(models.Model) :
	name = models.CharField(max_length=200, default=None)
#	retailedProducts = models.ManyToMany(Product)

	def __str__(self) :
		return self.name

