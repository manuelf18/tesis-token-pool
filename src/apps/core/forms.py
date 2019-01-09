from django.forms import ModelForm, CheckboxInput
from django import forms


class BootstrapBaseForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            if self.fields[field].widget.__class__.__name__ != CheckboxInput().__class__.__name__:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })


class BootstrapModelForm(BootstrapBaseForm, ModelForm):
    pass


class BootstrapForm(BootstrapBaseForm, forms.Form):
    pass
