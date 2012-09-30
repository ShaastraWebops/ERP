# Create your views here.
from django.template import *
from django.http import *
from django.shortcuts import *
from erp.finance.forms import *
from erp.misc.util import *
from erp.misc.helper import is_core, is_coord, is_supercoord, get_page_owner
from django.forms.models import modelformset_factory
from erp.department.models import *

def budget_portal(request, plan):
    curr_userprofile=userprofile.objects.get(user=request.user)
    page_owner = get_page_owner (request, owner_name=request.user)
    curr_user=request.user
    if is_core(curr_user):
        is_core1=True
        is_visitor1=False
    department = page_owner.get_profile ().department
    event=False
    finance=False
    if(department.is_event):
        event=True    
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
            curr_plan = Budget(name='F', total_amount=0, department=department)
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
    	     
    	    qset = Item.objects.filter(department=department, budget=curr_plan)
            if len(qset)<7:
                extra1=7-len(qset)
            else:
                extra1=2
            ItemFormset=modelformset_factory(Item, fields=('name', 'description', 'original_amount'),extra=extra1)
    	    if request.method == 'POST':
    	        budgetclaimform=BudgetClaimForm(request.POST, instance=curr_plan) 
    	        itemformset=ItemFormset(request.POST, queryset=qset)            
    	        form_saved = False
    	        if budgetclaimform.is_valid():
    	            budgetclaimform.save()
                else:
                    error=True
    	        if itemformset.is_valid():
    	            for form in itemformset.forms:
    	                if form.has_changed():
    	                    tempform = form.save(commit=False)
    	                    tempform.department=department
    	                    tempform.budget=curr_plan
    	                    tempform.save()
    	            form_saved = True 
    	            qset = Item.objects.filter(department=department, budget=curr_plan) 
                    if len(qset)<7:
                        extra1=7-len(qset)
                    else:
                        extra1=2
                    ItemFormset=modelformset_factory(Item, fields=('name', 'description', 'original_amount'),extra=extra1)
    	            itemformset=ItemFormset(queryset=qset)               
    	            return render_to_response('finance/budget_portal.html',locals(),context_instance=RequestContext(request))
                else:
                    error=True
    	    else:
    	        budgetclaimform=BudgetClaimForm(instance=curr_plan)
    	        itemformset=ItemFormset(queryset=qset)                                      
	
    	return render_to_response('finance/budget_portal.html',locals(),context_instance=RequestContext(request))

    elif str(curr_userprofile.department) == "Finance":
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
            curr_plan = Budget(name='F', total_amount=0, department=department)
    	    curr_plan.save()
    	    plans = Budget.objects.filter(department=department)
        finance=True
        event=False
        departments=Department.objects.filter(is_event=True)
        return render_to_response('finance/budget_portal.html',locals(),context_instance=RequestContext(request))
    else:
        raise Http404
		

def display(request, event_name):
    """
    Display the plans and items.
    """
    finance=False
    curr_userprofile=userprofile.objects.get(user=request.user)
    page_owner = get_page_owner (request, owner_name=request.user)
    curr_user=request.user
    if is_core(curr_user):
        is_core1=True
        is_visitor1=False
    department = page_owner.get_profile ().department
    if(department.is_event):
        budgets = Budget.objects.filter(department=department)
        items = Item.objects.filter()
        return render_to_response('finance/display.html',locals(),context_instance=RequestContext(request))
    elif str(curr_userprofile.department) == "Finance":
        
        finance=True
        event1=Department.objects.get(Dept_Name=event_name)
        plans = Budget.objects.filter(department=event1)
        if plans:
            print "plans exist"
        else: 
            curr_plan = Budget(name='A', total_amount=0, department=event1)
            curr_plan.save() 
            curr_plan = Budget(name='B', total_amount=0, department=event1)
            curr_plan.save() 
            curr_plan = Budget(name='C', total_amount=0, department=event1)
            curr_plan.save()
            curr_plan = Budget(name='F', total_amount=0, department=event1)
            curr_plan.save()
            plans = Budget.objects.filter(department=event1)
        budgets=Budget.objects.filter(department=event1)
        items = Item.objects.filter()
        plan_finance=Budget.objects.get(name='F',department=event1)
        qset = Item.objects.filter(department=event1, budget=plan_finance) 
        if len(qset)<7:
            extra1=7-len(qset)
        else:
            extra1=2
        ItemFormset=modelformset_factory(Item, fields=('name', 'description', 'original_amount'),extra=extra1)
        if request.method== "POST":
            budgetclaimform=BudgetClaimForm(request.POST, instance=plan_finance) 
    	    itemformset=ItemFormset(request.POST, queryset=qset)            
    	    form_saved = False
    	    if budgetclaimform.is_valid():
    	        budgetclaimform.save()
            else:
                error=True
    	    if itemformset.is_valid():
    	        for form in itemformset.forms:
    	            if form.has_changed():
    	                tempform = form.save(commit=False)
    	                tempform.department=event1
    	                tempform.budget=plan_finance
    	                tempform.save()
    	        form_saved = True 
    	        qset = Item.objects.filter(department=event1, budget=plan_finance) 
                if len(qset)<7:
                    extra1=7-len(qset)
                else:
                    extra1=2
                ItemFormset=modelformset_factory(Item, fields=('name', 'description', 'original_amount'),extra=extra1)
    	        itemformset=ItemFormset(queryset=qset)  
            else:
                error=True
        else:
            budgetclaimform=BudgetClaimForm(instance=plan_finance)
            itemformset=ItemFormset(queryset=qset)
        return render_to_response('finance/display.html',locals(),context_instance=RequestContext(request))
    else:
        raise Http404


