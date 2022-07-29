from django.db import models

# Create your models here.
class UploadedFile(models.Model):
	file = models.FileField(upload_to='')

class Forecast(models.Model):
	date = models.DateTimeField()
	ooi = models.IntegerField()
	lts = models.IntegerField()
	trr = models.DecimalField(max_digits=7, decimal_places=2)
	rod = models.DecimalField(max_digits=5, decimal_places=2)
