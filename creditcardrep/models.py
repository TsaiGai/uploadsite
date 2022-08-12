from django.db import models

# Create your models here.

# creates a filefield model
class UploadedFile(models.Model):
	file = models.FileField(upload_to='')

class CreditCardReport(models.Model):
	uploaded_file = models.OneToOneField(
		UploadedFile, 
		on_delete=models.CASCADE,
		primary_key=True,
	)

# creates a model for the elements of a credit card report
class CreditCard(models.Model):
	date = models.DateField()
	prop_id = models.CharField(max_length=5)
	code = models.CharField(max_length=2)
	account = models.CharField(max_length=10)
	last_four = models.CharField(max_length=4)
	user = models.CharField(max_length=8)
	vendor_id = models.CharField(max_length=8)
	amount = models.DecimalField(max_digits=7, decimal_places=2)
	report = models.ForeignKey(
		CreditCardReport,
		on_delete=models.CASCADE,
	)