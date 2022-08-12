from django import forms

# creates a form for the file to be uploaded
class UploadFileForm(forms.Form):
    file = forms.FileField()

class CreditCardReportForm(forms.Form):
    card_choices = [
        ['VI', 'Visa'], 
        ['DS', 'Discover'],
        ['MC', 'Mastercard'],
        ['AX', 'American Express'],
        ['', 'All Cards'],
    ]

    sr_choices = [
        [True, 'Sale'],
        [False, 'Refund'],
        ['', 'Both'],
    ]

    date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    prop_id = forms.CharField(max_length=5)
    card = forms.ChoiceField(choices=card_choices, required=False)
    positive = forms.ChoiceField(choices=sr_choices, required=False)
    vendor_id = forms.CharField(max_length=8, required=False)
    last_four = forms.CharField(max_length=4, required=False)
