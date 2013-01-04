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

class DetailForm (ModelForm):
    shaastra_id=forms.CharField(max_length = 250)            
    class Meta: 
        model=BarcodeMap
        exclude=('shaastra_id')    
		
class ParticipantForm (ModelForm):
    barcode=forms.CharField(max_length = 250,required=False)
    college=forms.CharField(max_length = 250,required=False)
    college_roll=forms.CharField(max_length = 250,required=False)
    name=forms.CharField(max_length = 250,required=False)
    mobile_number=forms.CharField(max_length = 250,required=False)
    
    class Meta: 
        model=Participant  
        exclude=('events','college','college_roll','name','mobile_number')

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
    participant_1=forms.CharField(max_length = 250, required=False)
    participant_2=forms.CharField(max_length = 250, required=False)
    participant_3=forms.CharField(max_length = 250, required=False)
    participant_4=forms.CharField(max_length = 250, required=False)
    participant_5=forms.CharField(max_length = 250, required=False)
    participant_6=forms.CharField(max_length = 250, required=False)
    participant_7=forms.CharField(max_length = 250, required=False)
    
    def save(self,commit=True):
        try:
            shid = self.cleaned_data['participant_1']
            if shid:
                instance=Participant.objects.filter(shaastra_id=shid)[0]
                self.instance.participant_1 = instance
        except KeyError:
            return True
        except:
            msg='ShaastraID not found.'
            self._errors['participant_1'] = ErrorList([msg])
            return False
                    
        try:    
            shid = self.cleaned_data['participant_2']
            if shid:
                instance=Participant.objects.filter(shaastra_id=shid)[0]
                self.instance.participant_2 = instance
        except KeyError:
            return True
        except:
            msg='ShaastraID not found.'
            self._errors['participant_2'] = ErrorList([msg])
            return False
                        
        try:    
            shid = self.cleaned_data['participant_3']
            if shid:
                instance=Participant.objects.filter(shaastra_id=shid)[0]
                self.instance.participant_3 = instance
        except KeyError:
            return True
        except:
            msg='ShaastraID not found.'
            self._errors['participant_3'] = ErrorList([msg])
            return False
                        
        try:    
            shid = self.cleaned_data['participant_4']
            if shid:
                instance=Participant.objects.filter(shaastra_id=shid)[0]
                self.instance.participant_4 = instance
        except KeyError:
            return True
        except:
            msg='ShaastraID not found.'
            self._errors['participant_4'] = ErrorList([msg])
            return False
                        
        try:    
            shid = self.cleaned_data['participant_5']
            if shid:
                instance=Participant.objects.filter(shaastra_id=shid)[0]
                self.instance.participant_5 = instance                                                
        except KeyError:
            return True
        except:
            msg='ShaastraID not found.'
            self._errors['participant_5'] = ErrorList([msg])
            return False
                        
        try:    
            shid = self.cleaned_data['participant_6']
            if shid:
                instance=Participant.objects.filter(shaastra_id=shid)[0]
                self.instance.participant_6 = instance
        except KeyError:
            return True
        except:
            msg='ShaastraID not found.'
            self._errors['participant_6'] = ErrorList([msg])
            return False
                        
        try:    
            shid = self.cleaned_data['participant_7']
            if shid:
                instance=Participant.objects.filter(shaastra_id=shid)[0]
                self.instance.participant_7 = instance
         
            return super(PrizeForm, self).save()
        except KeyError:
            return True
        except:
            msg='ShaastraID not found.'
            self._errors['participant_7'] = ErrorList([msg])
            return False

    class Meta:
        model=Prize
        fields = ('details', 'cheque',)

    def __init__(self, eventdetails=None, position=None, instance=None, *args, **kwargs):
        kwargs['instance'] = instance
        super(PrizeForm, self).__init__(*args, **kwargs)
        
        self.fields['participant_1'].widget.attrs['class'] = "search"
        self.fields['participant_2'].widget.attrs['class'] = "search"
        self.fields['participant_3'].widget.attrs['class'] = "search"
        self.fields['participant_4'].widget.attrs['class'] = "search"
        self.fields['participant_5'].widget.attrs['class'] = "search"
        self.fields['participant_6'].widget.attrs['class'] = "search"
        self.fields['participant_7'].widget.attrs['class'] = "search"
        
        if isinstance(instance, Prize):
            if instance.participant_1:
                self.fields['participant_1'].widget.attrs['value'] = str(instance.participant_1.shaastra_id)
            if instance.participant_2:
                self.fields['participant_2'].widget.attrs['value'] = str(instance.participant_2.shaastra_id)
            if instance.participant_3:
                self.fields['participant_3'].widget.attrs['value'] = str(instance.participant_3.shaastra_id)
            if instance.participant_4:
                self.fields['participant_4'].widget.attrs['value'] = str(instance.participant_4.shaastra_id)
            if instance.participant_5:
                self.fields['participant_5'].widget.attrs['value'] = str(instance.participant_5.shaastra_id)
            if instance.participant_6:
                self.fields['participant_6'].widget.attrs['value'] = str(instance.participant_6.shaastra_id)
            if instance.participant_7:
                self.fields['participant_7'].widget.attrs['value'] = str(instance.participant_7.shaastra_id)
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
