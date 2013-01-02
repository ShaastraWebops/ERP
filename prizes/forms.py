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
    shaastra_id=forms.CharField(max_length = 250)
   
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
        self.fields['shaastra_id'].widget.attrs['class'] = "search"
        #test = str([str(elem.shaastra_id) for elem in Participant.objects.all()])
        #print test
        #self.fields['shaastra_id'].widget.attrs['data-source'] = test
        #import pickle
        #f = open('ids.txt','rb')
        #ids = pickle.load(f)    
        #self.fields['shaastra_id'].widget.attrs['data-source']=  str(ids)


class EventRegnForm(BarcodeForm):
    def __init__(self, *args, **kwargs):
        super(EventRegnForm, self).__init__(*args, **kwargs)
        self.fields['team_id']=forms.ModelChoiceField(queryset=Team.objects.all())
        self.fields['team_id'].label = "Team ID"
        self.fields['team_id'].widget = chosenforms.widgets.ChosenSelect()


class PrizeForm (ModelForm):
    class Meta:
        model=Prize
        exclude=('event','user','position')
        widgets = {'participant_1':chosenforms.widgets.ChosenSelect(),
                  'participant_2':chosenforms.widgets.ChosenSelect(),
                  'participant_3':chosenforms.widgets.ChosenSelect(),
                  'participant_4':chosenforms.widgets.ChosenSelect(),
                  'participant_5':chosenforms.widgets.ChosenSelect(),
                  'participant_6':chosenforms.widgets.ChosenSelect(),
                  'participant_7':chosenforms.widgets.ChosenSelect(),
                  }

    def __init__(self, eventdetails=None, position=None, *args, **kwargs):
        super(PrizeForm, self).__init__(*args, **kwargs)
        if isinstance(eventdetails, EventDetails):
            if(int(position) > int(eventdetails.winner_nos)):
                self.fields['cheque'].widget = self.fields['cheque'].hidden_widget()
        else:
            super(PrizeForm, self).__init__(eventdetails,position,*args, **kwargs)  
        
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
