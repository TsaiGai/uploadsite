from django.db import models

# Create your models here.
class UploadedFile(models.Model):
	file = models.FileField(upload_to='')

class CreditCard(models.Model):
	code = models.CharField(max_length=2)
	account = models.CharField(max_length=10)
	last_four = models.CharField(max_length=4)
	user = models.CharField(max_length=8)
	vendor_id = models.CharField(max_length=8)
	amount = models.DecimalField(max_digits=6, decimal_places=2)