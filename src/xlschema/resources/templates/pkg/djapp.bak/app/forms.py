from django import forms
from .models import ${classname}


class ${classname}Form(forms.ModelForm):

    class Meta:
        model = ${classname}
        # exclude = (,)

    def __init__(self, *args, **kwargs):
        set_crispy(self, '${name}-form')
        super(${classname}Form, self).__init__(*args, **kwargs)

    def set_readonly(self):
        for field in self.fields:
            self.fields[field].required = False
            self.fields[field].widget.attrs['disabled'] = 'disabled'
