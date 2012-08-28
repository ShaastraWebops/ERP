from django.db import models
from django.forms import ModelForm
from erp.feedback.models import *
from django import forms
from chosen import forms as chosenforms

class QuestionFormCoord (ModelForm):
    class Meta:
		model = Question
		fields= ('question','answered_by','departments',)
		widgets = {'answered_by':chosenforms.widgets.ChosenSelect(),'departments': chosenforms.widgets.ChosenSelectMultiple(overlay='')}

    def __init__(self, *args, **kwargs):
        super(QuestionFormCoord, self).__init__(*args, **kwargs)
        # Removing "Hold down "Control", or "Command" on a Mac, to select more than one."
        self.fields['departments'].help_text = ''

class QuestionFormCore (ModelForm):
    class Meta:
        model = Question
        fields= ('question','departments',)
        widgets = {'departments': chosenforms.widgets.ChosenSelectMultiple(overlay='')}
        
    def __init__(self, *args, **kwargs):
        super(QuestionFormCore, self).__init__(*args, **kwargs)
        # Removing "Hold down "Control", or "Command" on a Mac, to select more than one."
        self.fields['departments'].help_text = ''
