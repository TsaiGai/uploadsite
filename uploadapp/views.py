from django.shortcuts import render
import openpyxl, datetime
# Setting datetime as a local variable
dt = datetime.datetime

# Create your views here.
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from .models import UploadedFile, TaxRecapSummary

# this function handles the uploaded file and saves its various data
def tax_recap_upload(request):
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
                ''' Some rows of the excel file have its data on different lines.
                Therefore, if a row is missing data, the data on the next line is
                processed instead.
                '''
                if is_date(row[0]):
                    # convert date to datetime field
                    date = dt.strptime(row[0], '%d-%b')
                    if row[2]:
                        # converts all the variables to floats
                        revenue = str_to_float(row[2])
                        octxci = str_to_float(row[4])
                        octxst = str_to_float(row[6])
                        saletx = str_to_float(row[8])
                    else:
                        # grabs the data from the row below
                        row = data[i + 1]
                        # converts all the variables to floats
                        revenue = str_to_float(row[2])
                        octxci = str_to_float(row[4])
                        octxst = str_to_float(row[6])
                        saletx = str_to_float(row[8])
            		
                    # creates and saves the entry (row)
                    new_data_entry = TaxRecapSummary(
                        date = date,
                        revenue = revenue,
                        octxci = octxci,
                        octxst = octxst,
                        saletx = saletx,
                    )
                    
                    new_data_entry.save()

    # creates context to hold the uploaded file
    context = {
    	'form': form
    }

    return render(request, 'tax_recap_upload.html', context)

# this function verifies if the string given is a viable date
def is_date(date):
			return True
    if type(date) == str:
        # removes the dash
        date = date.split('-')
        # the date should have a number followed by a three-letter string
        if date[0].isnumeric() and len(date[1])==3:
            return True
        else:
            return False

# this function converts a string to float
def str_to_float(amount):	
    # removes the comma
    amount = amount[1:].replace(',', '')
    amount = float(amount)
    return amount