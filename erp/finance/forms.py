from django.db import models
from django.forms import ModelForm
from erp.finance.models import *
from django import forms
from chosen import forms as chosenforms


class BudgetClaimForm(ModelForm):
	class Meta:
		model=Budget
		fields=('total_amount','comment')
        #widgets={'name':chosenforms.widgets.ChosenSelect()}
		
