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

            if is_date(data[1][0]):
                date = get_date(data[1][0])
                date = dt.strptime(date, '%m/%d/%Y')
            
            curr_date = date

            # iterates through each row of the table
            for i, row in enumerate(data):
                if '-' in str(row[1]):
                    prop_id = str(row[1])
                    ult_prop_id = prop_id[:5]

                # verifies if the first data value is a code
                if is_code(str(row[1])) and row[4]:
                    ''' Some of the rows of the excel file have its data on different lines.
                    Therefore, if a row is missing data, the data on the next line is
                    processed instead.'''
                    # converts the variables to strings
                    code = str(row[1])
                    account = str(row[19])
                    # grabs the last four digits of the card number
                    last_four = get_last_four(row[22])
                    # converts the variables to strings
                    user = str(row[33])
                    vendor_id = vendor_exists(row[38])
                    ''' For the amount, a positive or negative float is returned
                    depending on the column its placed in.
                    '''
                    if row[40]:
                        amount = str_to_float(row[40])
                    elif row[41]:
                        amount = str_to_float(row[41])
                    elif row[44]:
                        amount = str_to_float(row[44])
                    elif row[45]:
                        amount = str_to_float(row[45])

                    # creates and saves the entry (row)
                    new_data_entry = CreditCard(
                        date = curr_date,
                        prop_id = ult_prop_id,
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

def is_date(date):
    if date:
        date = date.split()
        return date[0] == "Credit"

def get_date(string):
    string = string.split()
    if string[4] == string[6]:
        string = string[4]

    return string

# this function verifies if the input given is a code
def is_code(code):
    # a code begins with an A, D M, or V
    return code[0] in ('A', 'D', 'M', 'V')

# this function selects the last four digits of the card number
def get_last_four(string):
    string = str(string)
    string = string.split()
    for num in string:
        remove_par(num)
        if num.isdigit():
            # converts the input to a string
            num = str(remove_par(num))

    return num

def vendor_exists(string):
    if string:
        return str(string)
    else:
        return ""

# this function removes parenthesis from the input
def remove_par(string):
    string = str(string)
    string = string[1:].replace(')', '')

    return str(string)

# this function converts a string to a float
def str_to_float(amount):
    amount = str(amount)

    if ',' in amount:
        amount = amount.replace(',', '')

    # removes the $ sign
    if '$' in amount:
        amount = amount.replace('$', '')

    if amount[0] == '(':
        amount = remove_par(amount)
        amount = float(amount)
    else:
        amount = float(amount)
        amount = -abs(amount)

    return amount