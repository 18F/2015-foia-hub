from django import forms

from foia_core.models import FOIARequest

class FOIARequestForm(forms.ModelForm):
    class Meta:
        #fields = ('name', 'description', 'project_type', 'active', 'private')
        model = FOIARequest