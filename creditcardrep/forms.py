from django import forms

# creates a form for the file to be uploaded
class UploadFileForm(forms.Form):
    file = forms.FileField()