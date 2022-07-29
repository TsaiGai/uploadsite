from django.shortcuts import render
import openpyxl, datetime
dt = datetime.datetime

# Create your views here.
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from .models import UploadedFile, TaxRecapSummary
# Imaginary function to handle an uploaded file.

def tax_recap_upload(request):
    form = UploadFileForm()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = UploadedFile(file=request.FILES['file'])
            new_file.save()

            fp = new_file.file.path
            data = list(openpyxl.load_workbook(fp).active.iter_rows(values_only=True))
            for i, row in enumerate(data):
            	if is_date(row[0]):
            		date = dt.strptime(row[0], '%d-%b')
            		if row[2]:
            			revenue = str_to_float(row[2])
            			octxci = str_to_float(row[4])
            			octxst = str_to_float(row[6])
            			saletx = str_to_float(row[8])
            		else:
            			row = data[i + 1]
            			revenue = str_to_float(row[2])
            			octxci = str_to_float(row[4])
            			octxst = str_to_float(row[6])
            			saletx = str_to_float(row[8])
            		
            		new_data_entry = TaxRecapSummary(
            			date = date,
            			revenue = revenue,
            			octxci = octxci,
            			octxst = octxst,
            			saletx = saletx,
            		)
            		new_data_entry.save()
    context = {
    	'form': form
    }

    return render(request, 'tax_recap_upload.html', context)

def is_date(date):
	if type(date) == str:
		date = date.split('-')
		if date[0].isnumeric() and len(date[1])==3:
			return True
		else:
			return False

def str_to_float(amount):	
	amount = amount[1:].replace(',', '')
	amount = float(amount)
	return amount