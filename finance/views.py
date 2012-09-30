# Create your views here.
from django.template import *
from django.http import *
from django.shortcuts import *
from erp.finance.forms import *
from erp.misc.util import *
from erp.misc.helper import is_core, is_coord, is_supercoord, get_page_owner
from django.forms.models import modelformset_factory
from django.contrib.auth.models import User
from erp.users.models import *

def toggle(request):
    page_owner = get_page_owner (request, owner_name=request.user)
    department = page_owner.get_profile ().department 
    if is_core(request.user) and str(department) == "Finance":
        openportal=OpenBudgetPortal.objects.filter(id=1)
        if openportal:
            curr_portal=OpenBudgetPortal.objects.get(id=1)
        else:
            curr_portal=OpenBudgetPortal(opened=False)
            curr_portal.save()
            
        if curr_portal.opened==False:
            curr_portal.opened=True
            curr_portal.save() 
            return redirect('erp.finance.views.display', )
    
        if curr_portal.opened==True:
            curr_portal.opened=False
            curr_portal.save()
            return redirect('erp.finance.views.display', )        
    else:
        raise Http404  
        
def permissions(request):
    page_owner = get_page_owner (request, owner_name=request.user)
    #Get Department Members' image thumbnails
    department = page_owner.get_profile ().department      
    dept_cores_list = User.objects.filter (
        groups__name = 'Cores',
        userprofile__department = department)
    dept_supercoords_list = User.objects.filter (
        groups__name = 'Supercoords',
        userprofile__department = department)
    dept_coords_list = User.objects.filter (
        groups__name = 'Coords',
        userprofile__department = department)

    #To display Add Tasks and Feedback options
    if is_core(request.user):
        is_core1=True
        is_visitor1=False  
        if str(department) == "QMS":
            qms_core=True
            qms_dept=True
        if str(department) == "Finance":
            finance_core=True    

    if is_supercoord(request.user):
        user_supercoord=True
        if str(department) == "QMS":
            qms_supercoord=True
            qms_dept=True             
    
    if is_coord(request.user):
        user_coord=True
        if str(department) == "QMS":
            qms_coord=True
            qms_dept=True 
            
    if is_core(request.user) and str(department) == "Finance":
        coords=Permission.objects.filter(budget_sanction=False)
        if coords:
            print 'coords exist'
            finance_coords=Permission.objects.all()
        else:
            finance_coords=userprofile.objects.filter(department=department)
            for eachcoord in finance_coords:
                if is_coord(eachcoord.user):
                    curr_coord=Permission(coord=eachcoord)
                    curr_coord.save()               
                               
                
        PermissionFormset=modelformset_factory(Permission, extra=0, form=PermissionForm) 
        qset = Permission.objects.all()
        print qset.count()
        if request.method == 'POST':
            permissionformset=PermissionFormset(request.POST, queryset=qset)            
            if permissionformset.is_valid():
                for form in permissionformset.forms:
                    if form.has_changed():
                        form.save()
                    qset = Permission.objects.all() 
                    permissionformset=PermissionFormset(queryset=qset)               
                    return render_to_response('finance/budget_portal.html',locals(),context_instance=RequestContext(request))
        else:
            permissionformset=PermissionFormset(queryset=qset)
                
    else:
        raise Http404 
    return render_to_response('finance/permissions.html',locals(),context_instance=RequestContext(request))
        
def budget_portal(request, plan):
    page_owner = get_page_owner (request, owner_name=request.user)

    #Get Department Members' image thumbnails
    department = page_owner.get_profile ().department      
    dept_cores_list = User.objects.filter (
        groups__name = 'Cores',
        userprofile__department = department)
    dept_supercoords_list = User.objects.filter (
        groups__name = 'Supercoords',
        userprofile__department = department)
    dept_coords_list = User.objects.filter (
        groups__name = 'Coords',
        userprofile__department = department)

    #To display Add Tasks and Feedback options
    if is_core(request.user):
        is_core1=True
        is_visitor1=False  
        if str(department) == "QMS":
            qms_core=True
            qms_dept=True
        if str(department) == "Finance":
            finance_core=True    

    if is_supercoord(request.user):
        user_supercoord=True
        if str(department) == "QMS":
            qms_supercoord=True
            qms_dept=True             
    
    if is_coord(request.user):
        user_coord=True
        if str(department) == "QMS":
            qms_coord=True
            qms_dept=True 
                    
    openportal=OpenBudgetPortal.objects.filter(id=1)
    if openportal:
        curr_portal=OpenBudgetPortal.objects.get(id=1)
    else:
        curr_portal=OpenBudgetPortal(opened=False)
        curr_portal.save()
                
    if curr_portal.opened==True:
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
                    
            #modelformset_factory has the option for a custom queryset        
            ItemFormset=modelformset_factory(Item, fields=('name', 'description', 'original_amount'),extra=2, can_delete=True) 
            qset = Item.objects.filter(department=department, budget=curr_plan)
            if request.method == 'POST':
                budgetclaimform=BudgetClaimForm(request.POST, instance=curr_plan) 
                itemformset=ItemFormset(request.POST, queryset=qset)            
                form_saved = False
                if itemformset.is_valid():
                    for form in itemformset.forms:
                        if form.has_changed():
                            if not form in itemformset.deleted_forms:
                                tempform = form.save(commit=False)
                                tempform.department=department
                                tempform.budget=curr_plan
                                tempform.save()
                        if form in itemformset.deleted_forms:
                            curr_item = Item.objects.get(id=form.instance.id)
                            curr_item.delete()
                if budgetclaimform.is_valid():
                    budgetclaimform.save()
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

    #Get Department Members' image thumbnails
    department = page_owner.get_profile ().department      
    dept_cores_list = User.objects.filter (
        groups__name = 'Cores',
        userprofile__department = department)
    dept_supercoords_list = User.objects.filter (
        groups__name = 'Supercoords',
        userprofile__department = department)
    dept_coords_list = User.objects.filter (
        groups__name = 'Coords',
        userprofile__department = department)

    #To display Add Tasks and Feedback options
    if is_core(request.user):
        is_core1=True
        is_visitor1=False  
        if str(department) == "QMS":
            qms_core=True
            qms_dept=True

    if is_supercoord(request.user):
        user_supercoord=True
        if str(department) == "QMS":
            qms_supercoord=True
            qms_dept=True             
    
    if is_coord(request.user):
        user_coord=True
        if str(department) == "QMS":
            qms_coord=True
            qms_dept=True     
    
    budgets = Budget.objects.filter(department=department)
    items = Item.objects.filter()
    return render_to_response('finance/display.html',locals(),context_instance=RequestContext(request))
    
    
