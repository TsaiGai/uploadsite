from django.contrib import admin

# Register your models here.
from .models import UploadedFile
from .models import CreditCard
from .models import CreditCardReport

admin.site.register(UploadedFile)
admin.site.register(CreditCard)
admin.site.register(CreditCardReport)