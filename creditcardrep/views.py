from django.shortcuts import render
import openpyxl, datetime
dt = datetime.datetime

# Create your views here.
from django.http import HttpResponseRedirect
from .forms import UploadFileForm, CreditCardReportForm
from .models import UploadedFile, CreditCard, CreditCardReport

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

            new_report = CreditCardReport(
                uploaded_file = new_file,
            )
            new_report.save()

            if is_multiprop(data[3][0]):
                # iterates through each row of the table
                for i, row in enumerate(data):
                    if '-' in str(row[1]):
                        prop_id = str(row[1])
                        ult_prop_id = prop_id[:5]

                    if is_date(str(row[1])):
                        date = str(row[1])
                        date = dt.strptime(date, '%m/%d/%Y')
                        curr_date = date

                    # verifies if the first data value is a code
                    if is_code(str(row[1])) and row[4]:
                        ''' Some of the rows of the excel file have its data on different lines.
                        Therefore, if a row is missing data, the data on the next line is
                        processed instead.'''
                        # converts the variables to strings
                        code_1 = None
                        code_2 = None
                        code = str(row[1])
                        if len(code) > 2:
                            code.split('\n')
                            code_1 = code[0]
                            code_2 = code[1]

                        if row[18]:
                            account = str(row[18])
                            if len(account) > 10:
                                account_1 = account[:10]
                                account_2 = account[10:]
                        else:
                            account = str(row[19])
                            if len(account) > 10:
                                account_1 = account[:10]
                                account_2 = account[10:]

                        # grabs the last four digits of the card number
                        for value in row[21:]:
                            if value: 
                                if str(value).count('(') < 2:
                                    last_four = get_last_four(value)
                                    break
                                else:
                                    last_fours = extract_last_four(str(value))
                                    last_four_1 = last_fours[0]
                                    last_four_2 = last_fours[1]
                                    break

                        # converts the variables to strings
                        for value in row[27:]:
                            if value and (('/') not in str(value)):
                                user = str(value)
                                break

                        for value in row[36:39]:
                            if value:
                                if len(str(value)) <= 9:
                                    vendor_id = vendor_exists(value)
                                else:
                                    value = str(value)
                                    vendor_id_1 = value[:8]
                                    vendor_id_2 = value[8:]

                        ''' For the amount, a positive or negative float is returned
                        depending on the column its placed in.
                        '''
                        for value in row[39:]:
                            if value and (('$') in str(value)):
                                if len(str(value)) <= 11:
                                    amount_1 = str_to_float(value)
                                else:
                                    amounts = extract_amounts(value)
                                    amount_1 = amounts[0]
                                    amount_2 = amounts[1]

                        if code_2:
                            new_data_entry = CreditCard(
                                date = curr_date,
                                prop_id = ult_prop_id,
                                code = code_1,
                                account = account_1,
                                last_four = last_four_1,
                                user = user,
                                vendor_id = vendor_id_1,
                                amount = amount_1,
                                report = new_report,
                            )
                            new_data_entry.save()

                            new_data_entry = CreditCard(
                                date = curr_date,
                                prop_id = ult_prop_id,
                                code = code_2,
                                account = account_2,
                                last_four = last_four_2,
                                user = user,
                                vendor_id = vendor_id_2,
                                amount = amount_2,
                                report = new_report,
                            )
                            new_data_entry.save()
                        else:
                            # creates and saves the entry (row)
                            new_data_entry = CreditCard(
                                date = curr_date,
                                prop_id = ult_prop_id,
                                code = code,
                                account = account,
                                last_four = last_four,
                                user = user,
                                vendor_id = vendor_id,
                                amount = amount_1,
                                report = new_report,
                            )
                            new_data_entry.save()               
            else:
                for i, row in reversed(list(enumerate(data))):
                    if '-' in str(row[0]):
                        prop_id = str(row[0])
                        ult_prop_id = prop_id[:5]
                        break

                for i, row in enumerate(data):
                    if is_date(str(row[0])):
                        date = str(row[0])
                        date = dt.strptime(date, '%m/%d/%Y')
                        curr_date = date

                    # verifies if the first data value is a code
                    if is_code(str(row[0])) and (row[3] or row[4]):
                        ''' Some of the rows of the excel file have its data on different lines.
                        Therefore, if a row is missing data, the data on the next line is
                        processed instead.'''
                        # converts the variables to strings
                        code_1 = None
                        code_2 = None
                        code = str(row[0])
                        if len(code) > 2:
                            code.split('\n')
                            code_1 = code[0]
                            code_2 = code[1]

                        for value in row[12:]:
                            if value:
                                account = str(value)
                                if len(account) > 11:
                                    account_1 = account[:10]
                                    account_2 = account[10:]
                                else:
                                    break

                        # grabs the last four digits of the card number
                        for value in row[14:]:
                            if value: 
                                if str(value).count('(') == 1:
                                    last_four = get_last_four(value)
                                    break
                                elif str(value).count('(') > 1:
                                    last_fours = extract_last_four(str(value))
                                    last_four_1 = last_fours[0]
                                    last_four_2 = last_fours[1]
                                    break

                        # converts the variables to strings
                        for value in row[21:]:
                            if value and (('/') not in str(value)):
                                user = str(value)
                                break

                        for value in row[24:]:
                            if value:
                                if ('/') not in str(value):
                                    if ('$') not in str(value):
                                        if ('/') not in str(row[row.index(value) - 3]):
                                            if len(str(value)) <= 9:
                                                vendor_id = vendor_exists(value)
                                                break
                                            else:
                                                value = str(value)
                                                vendor_id_1 = value[:8]
                                                vendor_id_2 = value[8:]
                                                break
                            else:
                                vendor_id = 'None'

                        ''' For the amount, a positive or negative float is returned
                        depending on the column its placed in.
                        '''
                        for value in row[27:]:
                            if value and (('$') in str(value)):
                                if len(str(value)) <= 11:
                                    amount = str_to_float(value)
                                    break
                                else:
                                    amounts = extract_amounts(value)
                                    amount_1 = amounts[0]
                                    amount_2 = amounts[1]

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
                            report = new_report,
                        )
                        new_data_entry.save()

                
    # constructs an element to display in the html
    data = CreditCard.objects.all()

    # constructs the context to hold the uploaded file
    context = {
        'form': form,
        'data': data,
    }

    return render(request, 'credit_card_upload.html', context)

def is_multiprop(string):
    string = str(string)
    string = string.split()
    return ('R') in string[0]

def is_date(date):
    date = str(date)
    has_two = False
    is_num = False

    if date.count('/') == 2:
        has_two = True
    if date.replace('/', '').isnumeric():
        is_num = True

    return has_two and is_num

# this function verifies if the input given is a code
def is_code(code):
    # a code begins with an A, D M, or V
    return code[0] in ('A', 'D', 'M', 'V')

# this function selects the last four digits of the card number
def get_last_four(string):
    string = str(string)
    paren_pos = string.find('(') + 1

    if paren_pos > 0:
        string = string[paren_pos:(paren_pos + 4)]
        return string
    else:
        if string.isnumeric() and len(string) == 4:
            return string
        else:
            return ""

def extract_last_four(value):
    first_par_i = str(value).find('(') + 1
    first_four = str(value)[first_par_i:(first_par_i + 4)]

    second_par_i = str(value).find('(', first_par_i) + 1
    second_four = str(value)[second_par_i:(second_par_i + 4)]

    return (first_four, second_four)

def vendor_exists(string):
    if string:
        return str(string)
    else:
        return ""

# this function converts a string to a float
def str_to_float(amount):
    amount = str(amount)

    if ',' in amount:
        amount = amount.replace(',', '')

    # removes the $ sign
    if '$' in amount:
        amount = amount.replace('$', '')

    if amount[0] == '(':
        amount = amount[1:].replace(')', '')
        amount = float(amount)
    else:
        amount = float(amount)
        amount = -abs(amount)

    return amount

def extract_amounts(value):
    # take off the 3rd value
    while str(value).count('$') > 2:
        if value.endswith(')'):
            value = value[:value.rfind('(')]
        else:
            value = value[:value.rfind('$')]

    if value.count('.') < 2:
        decimal_index = str(value).find('.') + 1
        value = value[:decimal_index + 2]
        first_amt = str_to_float(value)
        second_amt = None
        return (first_amt, second_amt)

    # both values are positive
    if value.startswith('(') and value.endswith(')'):
        first_amt_i = value.find('$')+1
        first_amt_i_end = value.find(')')
        first_amt = float(value[first_amt_i:first_amt_i_end].replace(',',''))
        second_amt_i = value.find('$', first_amt_i_end) + 1
        second_amt = float(value[second_amt_i:-1].replace(',',''))
        
    # first value is positive, second is negative
    elif ')$' in value:
        first_amt_i = value.find('$')+1
        first_amt_i_end = value.find(')')
        first_amt = float(value[first_amt_i:first_amt_i_end].replace(',',''))
        second_amt = -float(value[value.find('$',2):][1:].replace(',',''))
        
    # first value is negative, second is positive
    elif value.find('(', 2) != -1:
        first_amt = -float(value[:value.find('(')][1:].replace(',',''))
        second_amount_i = value.find('($')+2
        second_amt = float(value[second_amount_i:-1])
        
    # both values are negative
    else:
        (first_amt, second_amt) = tuple(-float(x.replace(',','')) for x in value.split('$')[1:])
        
    # return the values
    return (first_amt, second_amt)


def credit_card_search(request):
    form = CreditCardReportForm()
    form_errors = None
    qs = None

    if request.method == 'POST':
        form = CreditCardReportForm(request.POST)
        # saves file if not null
        if form.is_valid():
            form_data = form.cleaned_data

            qs = CreditCard.objects.filter(
                prop_id__exact=form_data['prop_id'],
                date__exact=form_data['date'],
            )

            if form_data['card'] != None:
                qs = qs.filter(code__exact=form_data['card'])

            if form_data['positive']:
                qs = qs.filter(amount__gt=0)
            elif form_data['positive'] == False:
                qs = qs.filter(amount__lt=0)

            if form_data['vendor_id']:
                qs = qs.filter(vendor_id__exact=form_data['vendor_id'])

        else:
            form_errors = form.errors

    context = {
        'form': form,
        'form_errors': form_errors,
        'qs': qs,
    }

    return render(request, 'credit_card_search.html', context)