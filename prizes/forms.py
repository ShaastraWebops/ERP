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
        # This doesn't seem to work. Added in Meta instead
        # self.fields['shaastra_id'].widget = chosenforms.widgets.ChosenSelect()
