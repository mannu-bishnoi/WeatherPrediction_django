from django import forms 
from .models import cityname

class cityForm(forms.ModelForm):
    class Meta:
        model=cityname
        fields=["ticker"]