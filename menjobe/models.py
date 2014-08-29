from django.db import models

class DistributionPoint(models.Model) :
	"""Groceries Distribution Point"""


class Product(models.Model) :
	name = models.CharField(max_length=200)



