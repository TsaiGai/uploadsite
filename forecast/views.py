from django.shortcuts import render
import openpyxl, datetime
dt = datetime.datetime

# Create your views here.
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from .models import UploadedFile, Forecast

# this function handles the uploaded file and saves its various data 
def forecast_upload(request):
    # the uploaded file is saved as a variable
    form = UploadFileForm()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        # saves file if not null
        if form.is_valid():
            new_file = UploadedFile(file=request.FILES['file'])
            new_file.save()

            # sets the file path as a variable
            fp = new_file.file.path
            # converts the uploaded (excel) file to a mutable table of values
            data = list(openpyxl.load_workbook(fp).active.iter_rows(values_only=True))
            
            # iterates through every row of the table
            for i, row in enumerate(data):
            	if is_date(row[0]):
                    # convert date to datetime field
            		date = dt.strptime(row[0], '%m/%d/%Y')
                    # converts the variables to ints
            		ooi = int(row[4])
            		lts = int(row[30])
                    # converts the variables to floats
            		trr = str_to_float(row[35])
            		rod = str_to_float(row[37])
            		
            		new_data_entry = Forecast(
                        # creates and saves the data entry (row)
            			date = date,
            			ooi = ooi,
            			lts = lts,
            			trr = trr,
            			rod = rod,
            		)

            		new_data_entry.save()
                    
    # constructs an element to display in the html
    data = Forecast.objects.all()

    # constructs the context to hold the uploaded file
    context = {
    	'form': form,
        'data': data,
    }

    return render(request, 'forecast_upload.html', context)

# this function verifies if the input given is a date
def is_date(date):
    if type(date) == str:
        # the date has a / in the second character of the string
        if date[1] == '/':
            return True
        else:
            return False

# this function converts a string to a float
def str_to_float(amount):	
    # removes the comma
    amount = amount[1:].replace(',', '')
    amount = float(amount)
    return amount