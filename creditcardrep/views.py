from django.shortcuts import render
import openpyxl, datetime
dt = datetime.datetime

# Create your views here.
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from .models import UploadedFile, CreditCard
# Imaginary function to handle an uploaded file.

def credit_card_upload(request):
    form = UploadFileForm()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = UploadedFile(file=request.FILES['file'])
            new_file.save()

            fp = new_file.file.path
            data = list(openpyxl.load_workbook(fp).active.iter_rows(values_only=True))

            for i, row in enumerate(data):
                if is_code(str(row[0])):
                    if row[3]:
                        code = str(row[0])
                        account = str(row[13])
                        last_four = get_last_four(row[15])
                        user = str(row[22])
                        vendor_id = str(row[25])
                        if row[28]:
                            amount = str_to_float(row[28])
                            amount = -abs(amount)
                        else:
                            amount = remove_par(row[31])
                            amount = str_to_float(amount)
                    else:
                        row = data[i + 1]
                        code = str(row[0])
                        account = str(row[13])
                        last_four = get_last_four(row[15])
                        user = str(row[22])
                        vendor_id = str(row[25])
                        if row[28]:
                            amount = str_to_float(row[28])
                            amount = -abs(amount)
                        else:
                            amount = remove_par(row[31])
                            amount = str_to_float(amount)

                    new_data_entry = CreditCard(
                        code = code,
                        account = account,
                        last_four = last_four,
                        user = user,
                        vendor_id = vendor_id,
                        amount = amount,
            		)

                    new_data_entry.save()

    data = CreditCard.objects.all()

    context = {
    	'form': form,
        'data': data,
    }

    return render(request, 'credit_card_upload.html', context)

def is_code(code):
    if code[0] in ('A', 'D', 'M', 'V'):
        return True
    else:
        return False

def get_last_four(num):
    num = num[3:]
    num = remove_par(num)
    num = str(num)
    return num

def remove_par(num):
    num = num[1:].replace(')', '')
    num = str(num)
    return num

def str_to_float(amount):
    amount = amount[1:]
    amount = float(amount)
    return amount