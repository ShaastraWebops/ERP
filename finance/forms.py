from django.db import models
from django.forms import ModelForm
from erp.finance.models import *
from django import forms
from chosen import forms as chosenforms

class BudgetClaimForm(ModelForm):
	class Meta:
		model=Budget
		fields=('comment',)
        #widgets={'name':chosenforms.widgets.ChosenSelect()}
        
class ReimbForm(ModelForm):
    class Meta:
        model=Reimb
        fields=('amount',)
        
class ReimbForm1(ModelForm):
    class Meta:
        model=Reimb
        fields=('status','comment',)
        
class PermissionForm(ModelForm):
    class Meta:
        model = Permission

    def __init__(self, *args, **kwargs):
        super(PermissionForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.fields['coord'].widget.attrs['readonly'] = True
            
class DeadlineForm(ModelForm):
    class Meta:
        model=Deadline             
		
