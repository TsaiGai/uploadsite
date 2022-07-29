from django.db import models

# Create your models here.
class UploadedFile(models.Model):
	file = models.FileField(upload_to='')

class TaxRecapSummary(models.Model):
	date = models.DateTimeField()
	revenue = models.DecimalField(max_digits=7, decimal_places=2)
	octxci = models.DecimalField(max_digits=6, decimal_places=2)
	octxst = models.DecimalField(max_digits=6, decimal_places=2)
	saletx = models.DecimalField(max_digits=5, decimal_places=2)