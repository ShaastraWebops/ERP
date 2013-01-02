from django.db import models
from django.forms import ModelForm
from models import *
from django import forms
from chosen import forms as chosenforms
from erp.prizes.models import *
from department.models import *
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
        if(event is not None):
            if(event.find("Workshop") == -1):
                self.fields['certificate_nos'].widget = self.fields['certificate_nos'].hidden_widget()   
