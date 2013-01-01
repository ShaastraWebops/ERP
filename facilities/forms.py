from django import forms
from django.forms import ModelForm
from erp.facilities.models import *
from django import forms
from chosen import forms as chosenforms


class ApprovalForm(forms.Form):
    approved_number = forms.IntegerField()
    #comment = forms.CharField(max_length=100,widget=forms.Textarea)

class RoundForm(ModelForm):
    class Meta:
        model=EventRound
        exclude = ('number','department')
    

