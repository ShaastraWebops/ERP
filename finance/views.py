# Create your views here.
from django.template import *
from django.http import *
from django.shortcuts import *
from finance.forms import *
from erp.misc.helper import is_core, is_coord, is_supercoord, get_page_owner
from django.forms.formsets import formset_factory

def budget_portal(request):
	
	page_owner = get_page_owner (request, owner_name=None)
	budgetclaimform=BudgetClaimForm()
	ItemFormset=formset_factory(ItemForm,extra=5)
	itemformset=ItemFormset()
	return render_to_response('finance/finance_portal.html',locals(),context_instance=RequestContext(request))
