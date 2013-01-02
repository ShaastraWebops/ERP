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

class BarcodeForm (ModelForm):
    shaastra_id=forms.CharField(required=True)
   
    def save(self,commit=True):
        try:
            shid=self.cleaned_data['shaastra_id']
            instance=Participant.objects.filter(shaastra_id=shid)[0]
            self.instance.shaastra_id=instance        
            return super(BarcodeForm, self).save()
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
        self.fields['shaastra_id'].widget.attrs['data-source'] = '["Alpha","Mike","Foxtrot"]'
        #import pickle
        #f = open('ids.txt','rb')
        #ids = pickle.load(f)    
        #self.fields['shaastra_id'].widget.attrs['data-source']=  str(ids)

        
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
        
        
class EventDetailsForm (ModelForm):
    class Meta:
        model = EventDetails
        exclude=('event',)

    def __init__(self, event=None, *args, **kwargs):
        super(EventDetailsForm, self).__init__(*args, **kwargs)
        self.fields['team_nos'].label = "Number of Teams"
        self.fields['max_members'].label = "Maximum Members per Team"
        self.fields['winner_nos'].label = "Number of Places with Cash Prize and Cerificate (1st, 2nd, 3rd etc.)"
        self.fields['finalist_nos'].label = "Number of Finalist Teams (inclusive of the winners)"
        self.fields['certificate_nos'].label = "Number of Participant Certificates"
        if isinstance(event, Department):
            if(event.Dept_Name.find("Workshop") == -1):
                self.fields['certificate_nos'].widget = self.fields['certificate_nos'].hidden_widget()
        else:
            super(EventDetailsForm, self).__init__(event,*args, **kwargs)                  
