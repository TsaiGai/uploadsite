from django.shortcuts import render
import openpyxl, datetime
dt = datetime.datetime

# Create your views here.
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from .models import UploadedFile, CreditCard

# this function handles the uploaded file and saves its various data
def credit_card_upload(request):
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

            # iterates through each row of the table
            for i, row in enumerate(data):
                # verifies if the first data value is a code
                if is_code(str(row[0])):
                    ''' Some of the rows of the excel file have its data on different lines.
                    Therefore, if a row is missing data, the data on the next line is
                    processed instead.'''
                    if row[3]:
                        # converts the variables to strings
                        code = str(row[0])
                        account = str(row[13])
                        # grabs the last four digits of the card number
                        last_four = get_last_four(row[15])
                        # converts the variables to strings
                        user = str(row[22])
                        vendor_id = str(row[25])
                        ''' For the amount, a positive or negative float is returned
                        depending on the column its placed in.
                        '''
                        # negative amount
                        if row[28]:
                            amount = str_to_float(row[28])
                            amount = -abs(amount)
                        # positive amount
                        else:
                            amount = remove_par(row[31])
                            amount = str_to_float(amount)
                    else:
                        # grabs the data from the row below
                        row = data[i + 1]
                        # converts variables to strings
                        code = str(row[0])
                        account = str(row[13])
                        # last four of card number
                        last_four = get_last_four(row[15])
                        # variables to strings
                        user = str(row[22])
                        vendor_id = str(row[25])
                        # negative amount
                        if row[28]:
                            amount = str_to_float(row[28])
                            amount = -abs(amount)
                        # positive amount
                        else:
                            amount = remove_par(row[31])
                            amount = str_to_float(amount)

                    # creates and saves the entry (row)
                    new_data_entry = CreditCard(
                        code = code,
                        account = account,
                        last_four = last_four,
                        user = user,
                        vendor_id = vendor_id,
                        amount = amount,
            		)

                    new_data_entry.save()

    # constructs an elemet to display in the html
    data = CreditCard.objects.all()

    # constructs the context to hold the uploaded file
    context = {
    	'form': form,
        'data': data,
    }

    return render(request, 'credit_card_upload.html', context)

# this function verifies if the input given is a code
def is_code(code):
    # a code begins with an A, D M, or V
    if code[0] in ('A', 'D', 'M', 'V'):
        return True
    else:
        return False

# this function selects the last four digits of the card number
def get_last_four(num):
    # removes everything before the digits
    num = num[3:]
    # removes parenthesis
    num = remove_par(num)
    # converts the input to a string
    num = str(num)
    return num

# this function removes parenthesis from the input
def remove_par(num):
    num = num[1:].replace(')', '')
    num = str(num)
    return num

# this function converts a string to a float
def str_to_float(amount):
    # removes the $ sign
    amount = amount[1:]
    amount = float(amount)
    return amount