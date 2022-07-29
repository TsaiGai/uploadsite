from django.contrib import admin

# Register your models here.
from .models import UploadedFile
from .models import TaxRecapSummary

admin.site.register(UploadedFile)
admin.site.register(TaxRecapSummary)