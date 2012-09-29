# Create your views here.
from django.template import *
from django.http import *
from django.shortcuts import *
from erp.finance.forms import *
from erp.misc.util import *
from erp.misc.helper import is_core, is_coord, is_supercoord, get_page_owner
from django.forms.models import modelformset_factory

def budget_portal(request, plan):
    page_owner = get_page_owner (request, owner_name=request.user)
    department = page_owner.get_profile ().department
        
    """
    First check if plans exist in database for the particular department
    else create three plans.
    """
    plans = Budget.objects.filter(department=department)
    if plans:
        print "plans exist"
    else: 
        curr_plan = Budget(name='A', total_amount=0, department=department)
        curr_plan.save() 
        curr_plan = Budget(name='B', total_amount=0, department=department)
        curr_plan.save() 
        curr_plan = Budget(name='C', total_amount=0, department=department)
        curr_plan.save()
        plans = Budget.objects.filter(department=department)  
    description='Description'
    form_selected = False
    """
    Let the user choose the Plan to be updated and accordingly prepopulate 
    the form with the data.
    """    
    if plan=='A' or plan=='B' or plan=='C':
        for p in plans:
            if p.name == plan:
                curr_plan = Budget.objects.get(id=p.id)
                form_selected=True
        ItemFormset=modelformset_factory(Item, fields=('name', 'description', 'original_amount'),extra=2) 
        qset = Item.objects.filter(department=department, budget=curr_plan)
        if request.method == 'POST':
            budgetclaimform=BudgetClaimForm(request.POST, instance=curr_plan) 
            itemformset=ItemFormset(request.POST, queryset=qset)            
            form_saved = False
            if budgetclaimform.is_valid():
                budgetclaimform.save()
            if itemformset.is_valid():
                for form in itemformset.forms:
                    if form.has_changed():
                        tempform = form.save(commit=False)
                        tempform.department=department
                        tempform.budget=curr_plan
                        tempform.save()
                form_saved = True 
                qset = Item.objects.filter(department=department, budget=curr_plan) 
                itemformset=ItemFormset(queryset=qset)               
                return render_to_response('finance/budget_portal.html',locals(),context_instance=RequestContext(request))
        else:
            budgetclaimform=BudgetClaimForm(instance=curr_plan)
            itemformset=ItemFormset(queryset=qset)                                      

    return render_to_response('finance/budget_portal.html',locals(),context_instance=RequestContext(request))

def display(request):
    """
    Display the plans and items.
    """
    page_owner = get_page_owner (request, owner_name=request.user)
    department = page_owner.get_profile ().department
    budgets = Budget.objects.filter(department=department)
    items = Item.objects.filter()
    return render_to_response('finance/display.html',locals(),context_instance=RequestContext(request))
