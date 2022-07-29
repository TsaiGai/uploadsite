from django.contrib import admin

# Register your models here.
from .models import UploadedFile
from .models import CreditCard

admin.site.register(UploadedFile)
admin.site.register(CreditCard)