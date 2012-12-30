from django.db import models
from django.forms import ModelForm
from models import *
from django import forms
from chosen import forms as chosenforms
from erp.prizes.models import *
from django.contrib.auth.models import User
#from chosen import widgets as chosenwidgets

class BarcodeForm (ModelForm):
    class Meta:
        model=BarcodeMap
        widgets = {'shaastra_id':chosenforms.widgets.ChosenSelect()}
		
    def __init__(self, *args, **kwargs):
        super(BarcodeForm, self).__init__(*args, **kwargs)
        self.fields['shaastra_id'].label = "Shaastra ID"
        
class PrizeForm (ModelForm):
    barcode=forms.CharField(required=False)
    class Meta:
        model=Prize
        widgets = {'participant':chosenforms.widgets.ChosenSelect()}  
        exclude=('event','user','cheque')
              
