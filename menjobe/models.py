from django.db import models
from mptt.models import MPTTModel, TreeForeignKey



class Product(MPTTModel) :
	name = models.CharField(
		max_length=200,
		default=None,
		unique=True,
		)

	group = TreeForeignKey('self',
		null=True,
		blank=True,
		related_name='subgroups',
		default=None,
		)

	class MPTTMeta:
		parent_attr = 'group'

	def __str__(self) :
		return self.name

	def retailPoints(self) :
		descendantsIds = list(self
			.get_descendants(include_self=True)
			.values_list("id", flat=True)
			)
		return RetailPoint.objects.filter(
			retailedProducts__id__in = descendantsIds
			).distinct()

class RetailPoint(models.Model) :
	name = models.CharField(
			max_length=200,
			default=None,
			unique=True,
			)
	description = models.TextField(default="")
	address = models.TextField(default=None, null=True, blank=False)
	retailedProducts = models.ManyToManyField(Product, blank=True, null=False)

	def descriptionHtml(self) :
		import markdown
		return markdown.markdown(self.description)

	def __str__(self) :
		return self.name

	def sells(self, *products) :
		self.retailedProducts.add(*products)

	def products(self) :
		return self.retailedProducts.all()


