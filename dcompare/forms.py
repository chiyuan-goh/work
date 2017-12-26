from django import forms

class FileUploadForm(forms.Form):
    documents = forms.FileField(widget =
                                forms.ClearableFileInput(attrs={'multiple': True}))
