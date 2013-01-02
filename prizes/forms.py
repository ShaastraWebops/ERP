from django.db import models
from django.forms import ModelForm
from models import *
from django import forms
from chosen import forms as chosenforms
from erp.prizes.models import *
from department.models import *
from django.contrib.auth.models import User
from django.forms.util import ErrorList

#from chosen import widgets as chosenwidgets

# Get Shaastra IDS
    
class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='Max. 2.5 MB'
    )
    
class BarcodeForm (ModelForm):
    shaastra_id=forms.CharField(required=True)
   
    def save(self,commit=True):
        try:
            shid=self.cleaned_data['shaastra_id']  
            barcode=self.cleaned_data['barcode']  
            instance=Participant.objects.filter(shaastra_id=shid)[0]
            self.instance.shaastra_id=instance        
            return super(BarcodeForm, self).save()
        except KeyError:
            return True
        except:
            msg='ShaastraID not found. Recheck this ID or remove it to save other entries.'
            self._errors['shaastra_id'] = ErrorList([msg])
            return False
            
    class Meta: 
        model=BarcodeMap
        exclude=('shaastra_id')    
		
    def __init__(self, *args, **kwargs):
        super(BarcodeForm, self).__init__(*args, **kwargs)
        self.fields['shaastra_id'].label = "Shaastra ID"
        self.fields['shaastra_id'].widget.attrs['data-provide'] = "typeahead"
        self.fields['shaastra_id'].widget.attrs['data-items'] = "10"
        #ids = [str(elem.shaastra_id) for elem in Participant.objects.all()]
        self.fields['shaastra_id'].widget.attrs['data-source']= ''

        
class PrizeForm (ModelForm):
    barcode=forms.CharField(required=False)
    class Meta:
        model=Prize
        widgets = {'participant':chosenforms.widgets.ChosenSelect()}  
        exclude=('event','user','cheque')

        
class ChequeForm (ModelForm):
    class Meta:
        model=Prize
        widgets = {'participant':chosenforms.widgets.ChosenSelect()}  
        exclude=('event','user','details','position')
