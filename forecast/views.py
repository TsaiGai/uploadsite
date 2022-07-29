from django.shortcuts import render
import openpyxl, datetime
dt = datetime.datetime

# Create your views here.
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from .models import UploadedFile, Forecast
# Imaginary function to handle an uploaded file.

def forecast_upload(request):
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
            		date = dt.strptime(row[0], '%m/%d/%Y')
            		# if row[4]:
            		ooi = is_zero(row[4])
            		lts = int(row[30])
            		trr = str_to_float(row[35])
            		rod = str_to_float(row[37])
            		
            		new_data_entry = Forecast(
            			date = date,
            			ooi = ooi,
            			lts = lts,
            			trr = trr,
            			rod = rod,
            		)

            		new_data_entry.save()
                    
    data = Forecast.objects.all()

    context = {
    	'form': form,
        'data': data,
    }

    return render(request, 'forecast_upload.html', context)

def is_date(date):
	if type(date) == str:
		if date[1] == '/':
			return True
		else:
			return False

def is_zero(num):
    num = str(num)

    if int(num) == 0:
        return 0
    else:
        return int(num)

def str_to_float(amount):	
	amount = amount[1:].replace(',', '')
	amount = float(amount)
	return amount