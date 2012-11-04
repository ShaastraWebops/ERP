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
from erp.department.models import *
from django.core.urlresolvers import reverse
from datetime import date
from django.utils.safestring import mark_safe

def read(request, request_id):
    curr_userprofile=userprofile.objects.get(user=request.user)
    department = curr_userprofile.department
    if department.is_event:
        if is_coord(request.user):
            curr_request=Request.objects.get(id=request_id)
            if curr_request.read_status==False:
                curr_request.read_status=True
                curr_request.save()
                return HttpResponseRedirect(reverse('erp.finance.views.advance', kwargs={'dept': '0',}))
            

def advance(request, dept):
    feedback_tab=True
    finance_core=False
    total_amount1=0
    curr_userprofile=userprofile.objects.get(user=request.user)
    page_owner = get_page_owner (request, owner_name=request.user)
    qms_dept=False
    events_core=False
    advance=False	
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
    
	#Check if instance of open portal present. Otherwise make one.                
    openportal=OpenBudgetPortal.objects.filter(id=1)
    if openportal:
        curr_portal=OpenBudgetPortal.objects.get(id=1)
    else:
        curr_portal=OpenBudgetPortal(opened=False)
        curr_portal.save()

    curr_user=request.user
    event=False
    finance=False
    event_chosen=False
        
    if (department.is_event):
        event=True
        if is_core(request.user):
            events_core=True 
        """
        if is_core(request.user):
            events_core=True 
            item_exist=False
            submitted = False
            plans = Budget.objects.filter(department=department)
            items = Item.objects.filter(department=department)
            if items:
                item_exist=True
                if curr_portal.opened == True:
                    budgets = plans.exclude(name='F')
                if curr_portal.opened == False:
                    plan_finance = Budget.objects.get(name='F',department=department)
                    if plan_finance.submitted == True:
                        submitted = True
                    budgets = plans.exclude(name='F') 
                return render_to_response('finance/event_core_view.html',locals(),context_instance=global_context(request))        
            else:
                return render_to_response('finance/event_core_view.html',locals(),context_instance=global_context(request)) 
        """                   
                          

        if curr_portal.opened==False:
            items=Item.objects.all()
            curr_plans = Budget.objects.filter(department=department)
            if curr_plans:
                item_exist=True
                plan_finance=Budget.objects.get(name='F',department=department)
                if plan_finance.submitted == True:
                    
                    submitted=True 
                    """
                    Create an instance of request model associated with each item in the
                    finance department approved plan
                    """
                    advance=True
                    curr_items = Item.objects.filter(budget=plan_finance,department=department)
                    request_items = Request.objects.filter(department=department)
                    for item in curr_items:
                        request_item1=Request.objects.filter(item=item)
                        if not request_item1:
                            new_request=Request(request_amount=0.0, granted_amount=0.0, balance_amount=item.original_amount, item=item, department=department)
                            new_request.save() 
                    request_items = Request.objects.filter(department=department)
                        
                    
                    """ADVANCE PORTAL FORM"""
                    if request.method == 'POST':
                        request_error=False
                        requested_amount = request.POST['request']
                        if requested_amount:
                            try:
                                requested_amount1=float(requested_amount)
                                curr_request = Request.objects.get(id=request.POST['id'])
                                curr_request.request_amount=requested_amount
                                curr_request.request_status=True
                                curr_request.granted_status=False
                                curr_request.read_status=False
                                curr_request.history = str(curr_request.history) + 'requested: '+str(requested_amount)+' on '+str(datetime.date.today())+'<br>'
                                curr_request.save()
                            except:
                                request_error=True
                        else:
                            request_error=True
                        #return HttpResponseRedirect(reverse('erp.finance.views.advance', kwargs={'dept': dept,}))
                        #check for error                                              
                        request_items = Request.objects.filter(department=department)
        return render_to_response('finance/advance_portal.html',locals(),context_instance=global_context(request))    
        
    elif str(department) == "Finance":
        no_request=False
        finance=True
        event=False
        departments=Department.objects.filter(is_event=True).order_by('Dept_Name')
        has_perms = False
        
        """
        Checking is the finance coord logged in has permission
        to update plan from finance department.
        """
        finance_coords=Permission.objects.all()
        for eachcoord in finance_coords:
            if curr_userprofile.name == eachcoord.coord:        
                if eachcoord.budget_sanction==True:
                    has_perms = True
              
        if is_core(request.user):
            has_perms=True 
            
        """
        Make a list of all the budget plans which have already been
        approved. Note that this happens only when the portal is 
        closed.
        """    
            
        if curr_portal.opened == False: 
            plans = Budget.objects.all()
            if plans:
                submitted_plans=Budget.objects.filter(name='F', submitted=True)
                if submitted_plans:
                    advance=True
                    pending_approval = []                    
                    if dept!='0':
                        for plan in submitted_plans:
                            if str(plan.department.id)==dept:
                                event_chosen = True
           
                    request_items = Request.objects.all() 
                    if request_items:
                        for req in request_items:
                            if req.request_status:
                                pending_approval.append(req.department.Dept_Name)
                    if event_chosen:
                        event_name = Department.objects.get(id=dept)
                        plan_finance = Budget.objects.get(name='F',department=event_name)
                        items=Item.objects.filter(department=event_name)
                        curr_items = Item.objects.filter(budget=plan_finance,department=event_name)
                        request_items = Request.objects.filter(department=event_name)
                        if request_items:
                            if request.method == 'POST':
                                approved_error=False
                                approved_amount = request.POST['request']
                                if approved_amount:
                                    try:
                                        approved_amount1=float(approved_amount)
                                        curr_request = Request.objects.get(id=request.POST['id'])
                                        curr_request.granted_amount=approved_amount
                                        curr_request.balance_amount=float(curr_request.balance_amount)-float(curr_request.granted_amount)
                                        curr_request.request_status=False
                                        curr_request.granted_status=True
                                        curr_request.read_status=False
                                        #new line not happening?
                                        curr_request.history = str(curr_request.history)+'approved: '+str(approved_amount)+' on '+str(date.today())+ '<br>'       
                                        curr_request.save()
                                        #if Response Redirect is not given then the history will be lagging
                                        #return HttpResponseRedirect(reverse('erp.finance.views.advance', kwargs={'dept': dept,}))
                                    except:
                                            approved_error=True
                                else:
                                    approved_error=True
                        else:
                            no_request=True    

                        request_items = Request.objects.filter(department=event_name)   
                        if request_items:
                            pending_approval = []
                            for req in request_items:
                                if req.request_status:
                                    pending_approval.append(req.department.Dept_Name)                                                      
        return render_to_response('finance/advance_portal.html',locals(),context_instance=global_context(request))
    
    if qms_dept:
        if curr_portal.opened == False: 
            plans = Budget.objects.all()
            if plans:
                submitted_plans=Budget.objects.filter(name='F', submitted=True)
                if submitted_plans:
                    advance=True
                    if dept!='0':
                        for plan in submitted_plans:
                            if str(plan.department.id)==dept:
                                event_chosen = True
           
                    request_items = Request.objects.all() 
                    if request_items:
                        pending_approval = []
                        for req in request_items:
                            if req.request_status:
                                pending_approval.append(req.department.Dept_Name)                                

        if event_chosen:
            event_name = Department.objects.get(id=dept)
            plan_finance = Budget.objects.get(name='F',department=event_name) 
            request_items = Request.objects.filter(department=event_name)  
            items=Item.objects.all()
        return render_to_response('finance/advance_portal.html',locals(),context_instance=global_context(request))
         
    """
    If user is part of QMS department then, he/she has the pemission to
    view all plans from all departments, like a finance coord without
    permission.
       	        
    if qms_dept:
        departments=Department.objects.filter(is_event=True).order_by('Dept_Name')
    	has_perms=False
        if curr_portal.opened == False: 
            submittedplans = []
            plans = Budget.objects.all()
            if plans:
                for dept in departments:
                    curr_plans = Budget.objects.filter(department=dept)
                    if curr_plans:
                        plan_finance=Budget.objects.get(name='F',department=dept)
                        if plan_finance.submitted == True:
                            submittedplans.append(dept.Dept_Name)
                                	
        return render_to_response('finance/finance_base_portal.html',locals(),context_instance=global_context(request))
       
    else:
        raise Http404  
    """
    

def budget_portal(request, plan="None"):
    feedback_tab=True
    finance_core=False
    total_amount1=0
    curr_userprofile=userprofile.objects.get(user=request.user)
    page_owner = get_page_owner (request, owner_name=request.user)
    qms_dept=False
    events_core=False
    advance=False	
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
    
	#Check if instance of open portal present. Otherwise make one.                
    openportal=OpenBudgetPortal.objects.filter(id=1)
    if openportal:
        curr_portal=OpenBudgetPortal.objects.get(id=1)
    else:
        curr_portal=OpenBudgetPortal(opened=False)
        curr_portal.save()

    curr_user=request.user
    event=False
    finance=False
    deadline=Deadline.objects.filter(id=1)
    if deadline:
        deadline=Deadline.objects.get(id=1)
    if not deadline:
        deadline=Deadline(budget_portal_deadline=date.today())
  
    if finance_core:
        deadlines=Deadline.objects.all()
        if not deadlines:
            deadline1=Deadline(budget_portal_deadline=date.today())
            deadline1.save()
        deadline=Deadline.objects.get(id=1)
        
    if (department.is_event):
        event=True
        if is_core(request.user):
            events_core=True 
            item_exist=False
            submitted = False
            plans = Budget.objects.filter(department=department)
            items = Item.objects.filter(department=department)
            if items:
                item_exist=True
                if curr_portal.opened == True:
                    budgets = plans.exclude(name='F')
                if curr_portal.opened == False:
                    plan_finance = Budget.objects.get(name='F',department=department)
                    if plan_finance.submitted == True:
                        submitted = True
                    budgets = plans.exclude(name='F') 
                return render_to_response('finance/event_core_view.html',locals(),context_instance=global_context(request))        
            else:
                return render_to_response('finance/event_core_view.html',locals(),context_instance=global_context(request))            
            
                           
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
                if len(qset)<5:
                    extra1=5-len(qset)
                else:
                    extra1=2
                ItemFormset=modelformset_factory(Item, fields=('name', 'description','quantity', 'original_amount'),extra=extra1, can_delete=True)
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
                                    if item.objects.filter(id=form.instance.id):
                                        curr_item = Item.objects.get(id=form.instance.id)
                                        curr_item.delete()   
                            form_saved = True 
                        qset = Item.objects.filter(department=department, budget=curr_plan)
                        if 'add_more_items' in request.POST: 
                         
                            if len(qset)<5:
                                extra1=5-len(qset)
                            else:
                                extra1=2
                        else:
                            if len(qset)<5:
                                extra1=5-len(qset)
                            else:
                                extra1=0
                        ItemFormset=modelformset_factory(Item, fields=('name', 'description','quantity','original_amount'),extra=extra1, can_delete=True)
                        itemformset=ItemFormset(queryset=qset)               
                        
                    else:
                        error=True
                    if budgetclaimform.is_valid():
    	                budgetclaimform1=budgetclaimform.save(commit=False)
    	                for qset1 in qset:
    	                    total_amount1+=qset1.original_amount
    	                budgetclaimform1.total_amount=float(total_amount1)
    	                budgetclaimform1.save()
    	            else:
                        error=True
    	        else:
    	            budgetclaimform=BudgetClaimForm(instance=curr_plan)
    	            itemformset=ItemFormset(queryset=qset)
                  
            
        else:
            items=Item.objects.all()
            curr_plans = Budget.objects.filter(department=department)
            if curr_plans:
                item_exist=True
                plan_finance=Budget.objects.get(name='F',department=department)
                if plan_finance.submitted == True:
                    
                    submitted=True            
                    """ADVANCE"""
                    """
                    Create an instance of request model associated with each item in the
                    finance department approved plan
                    """
                    advance=True
                    curr_items = Item.objects.filter(budget=plan_finance,department=department)
                    request_items = Request.objects.filter(department=department)
                    if not request_items:
                        for item in curr_items:
                            new_request=Request(request_amount=0.0, granted_amount=0.0, balance_amount=item.original_amount, item=item, department=department)
                            new_request.save() 
                        request_items = Request.objects.filter(department=department)
                        
                    
                    """ADVANCE PORTAL FORM"""
                    if request.method == 'POST':
                        requested_amount = request.POST['request']
                        if requested_amount:
                            try:
                                requested_amount1=float(requested_amount)
                                curr_request = Request.objects.get(id=request.POST['id'])
                                curr_request.request_amount=requested_amount
                                curr_request.request_status=True
                                #new line not happening?
                                curr_request.history = str(curr_request.history) + '\n' +'requested amount: '+str(requested_amount)+' on '+str(datetime.date.today())      
                                curr_request.save() 
                                #if Response Redirect is not given then the history will be lagging 
                                #return HttpResponseRedirect(reverse('erp.finance.views.budget_portal', kwargs={'plan': 'budget',}))
                            except:
                                request_error=True
                                              
                        request_items = Request.objects.filter(department=department)
        return render_to_response('finance/budget_portal.html',locals(),context_instance=global_context(request))    
        
    elif str(department) == "Finance":
        finance=True
        event=False
        departments=Department.objects.filter(is_event=True).order_by('Dept_Name')
        has_perms = False
        
        """
        Checking is the finance coord logged in has permission
        to update plan from finance department.
        """
        finance_coords=Permission.objects.all()
        for eachcoord in finance_coords:
            if curr_userprofile.name == eachcoord.coord:        
                if eachcoord.budget_sanction==True:
                    has_perms = True
              
        if is_core(request.user):
            has_perms=True 
            
        """
        Make a list of all the budget plans which have already been
        approved. Note that this happens only when the portal is 
        closed.
        """    
            
        if curr_portal.opened == False: 
            submittedplans = []
            plans = Budget.objects.all()
            if plans:
                for dept in departments:
                    curr_plans = Budget.objects.filter(department=dept)
                    if curr_plans:
                        plan_finance=Budget.objects.get(name='F',department=dept)
                        if plan_finance.submitted == True:
                            submittedplans.append(dept.Dept_Name)
                submitted_plans=Budget.objects.filter(name='F', submitted=True)
                if submitted_plans:
                    advance=True
                    curr_items = Item.objects.filter(budget=plan_finance,department=department)
                    request_items = Request.objects.filter(department=department)
                    if not request_items:
                        for item in curr_items:
                            new_request=Request(request_amount=0.0, granted_amount=0.0, balance_amount=item.original_amount, item=item, department=department)
                            new_request.save() 
                        request_items = Request.objects.filter(department=department)
                        
                    
                    """ADVANCE PORTAL FORM
                    if request.method == 'POST':
                        requested_amount = request.POST['request']
                        curr_request = Request.objects.get(id=request.POST['id'])
                        curr_request.request_amount=requested_amount
                        curr_request.request_status=True
                        #new line not happening?
                        curr_request.history = str(curr_request.history) + '\n' +'requested amount: '+str(requested_amount)+' on '+str(datetime.date.today())      
                        curr_request.save() 
                        #if Response Redirect is not given then the history will be lagging 
                        return HttpResponseRedirect(reverse('erp.finance.views.budget_portal', kwargs={'plan': 'budget',}))"""                                
                            
                            
        """
        Finance core has the option to set deadline.
        """                            
        if finance_core:
            form_saved=False                
            if request.method=='POST':
                deadlineform=DeadlineForm(request.POST,instance=deadline)
                if deadlineform.is_valid():
                    deadlineform.save()
                    form_saved=True
       
            else:
    	        deadlineform=DeadlineForm(instance=deadline)
    
        return render_to_response('finance/budget_portal.html',locals(),context_instance=global_context(request))
        
    """
    If user is part of QMS department then, he/she has the pemission to
    view all plans from all departments, like a finance coord without
    permission.
    """    	        
    if qms_dept or events_core:
        departments=Department.objects.filter(is_event=True).order_by('Dept_Name')
    	has_perms=False
        if curr_portal.opened == False: 
            submittedplans = []
            plans = Budget.objects.all()
            if plans:
                for dept in departments:
                    curr_plans = Budget.objects.filter(department=dept)
                    if curr_plans:
                        plan_finance=Budget.objects.get(name='F',department=dept)
                        if plan_finance.submitted == True:
                            submittedplans.append(dept.Dept_Name)
                                	
        return render_to_response('finance/budget_portal.html',locals(),context_instance=global_context(request))
    else:
        raise Http404 

"""
To open or clode budget portal
"""        
def toggle(request):
    feedback_tab=True
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
            return HttpResponseRedirect(reverse('erp.finance.views.budget_portal', kwargs={'plan': 'budget',}))
    
        if curr_portal.opened==True:
            curr_portal.opened=False
            curr_portal.save()
            return HttpResponseRedirect(reverse('erp.finance.views.budget_portal', kwargs={'plan': 'budget',}))       
    else:
        raise Http404  
"""
To grant permissions to specific finance coords
"""        
def permissions(request):
    curr_userprofile=userprofile.objects.get(user=request.user)
    feedback_tab=True
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
            finance=True   

    if is_supercoord(request.user):
        user_supercoord=True
        if str(department) == "QMS":
            qms_supercoord=True
            qms_dept=True             
        if str(department) == "Finance":
            finance=True
                
    if is_coord(request.user):
        user_coord=True
        if str(department) == "QMS":
            qms_coord=True
            qms_dept=True 
        if str(department) == "Finance":
            finance=True            
            
    """
    Get instances already created of Permission model 
    create instances of Permission model with coord name and permission
    Note: There will be as many objects as finance coords.
    """ 
    if is_core(request.user) and str(department) == "Finance":
        coords=Permission.objects.all()
        if coords:
            print 'coords exist'
            finance_coords=Permission.objects.all()
        else:
            finance_coords=userprofile.objects.filter(department=department)
            for eachcoord in finance_coords:
                if is_coord(eachcoord.user):
                    curr_coord=Permission(coord=eachcoord.name)
                    curr_coord.save()               
                               
                
        PermissionFormset=modelformset_factory(Permission, extra=0, form=PermissionForm) 
        qset = Permission.objects.all()
        perms = False
        if request.method == 'POST':
            permissionformset=PermissionFormset(request.POST, queryset=qset)            
            if permissionformset.is_valid():
                for form in permissionformset.forms:
                    if form.has_changed:
                        form.save()
                qset = Permission.objects.all() 
                permissionformset=PermissionFormset(queryset=qset) 
                perms=True 
                return render_to_response('finance/permissions.html',locals(),context_instance=global_context(request))
        else:
            permissionformset=PermissionFormset(queryset=qset)
                
    else:
        raise Http404 
    return render_to_response('finance/permissions.html',locals(),context_instance=global_context(request))
        
def display(request, event_name):
    """
    Display the plans and items.
    """
    display=True
    finance=False
    feedback_tab=True
    form_saved=False
    total_amount1=0
    page_owner = get_page_owner (request, owner_name=request.user)
    curr_userprofile=userprofile.objects.get(user=request.user)
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
         
	#Check if instance of open portal present. Otherwise make one.                
    openportal=OpenBudgetPortal.objects.filter(id=1)
    if openportal:
        curr_portal=OpenBudgetPortal.objects.get(id=1)
    else:
        curr_portal=OpenBudgetPortal(opened=False)
        curr_portal.save()  

    if(department.is_event):
        event=True
        budgets = Budget.objects.filter(department=department)
        items = Item.objects.all()
        item_exist = False
        if items:
            item_exist = True
        return render_to_response('finance/budget_display.html',locals(),context_instance=global_context(request))
    
  
    first_time=False
    item_exist=False
    event1 = Department.objects.get(id=event_name)
    if str(department) == "Finance" or "QMS":
   
        finance_core=False
        if str(department) == "Finance":
            finance=True
        else:
            qms_dept=True    
        event1 = Department.objects.get(id=event_name)
        plans = Budget.objects.filter(department=event1)
        if plans:
            item_exist=True
            budgets=Budget.objects.filter(department=event1)
            items = Item.objects.all()
            planF = False
            has_perms = False
            if curr_portal.opened==False:
                finance_coords=Permission.objects.all()
                for eachcoord in finance_coords:
                    if curr_userprofile.name == eachcoord.coord:        
                        if eachcoord.budget_sanction==True:
                            has_perms = True
                        
                if is_core(request.user) and str(department) == "Finance":
                    has_perms=True                  
                    finance_core=True
                planF = True
                plan_finance=Budget.objects.get(name='F',department=event1)
                submitted = False
                
                if plan_finance.submitted ==False:
                    qset = Item.objects.filter(department=event1, budget=plan_finance)
                    for qset1 in qset:
    	                        total_amount1+=qset1.original_amount 
                    if len(qset)<5:
                        extra1=5-len(qset)
                    else:
                        extra1=0
                    ItemFormset=modelformset_factory(Item, fields=('name', 'description','quantity', 'original_amount'), extra=extra1, can_delete=True)
                    if request.method== "POST":
                        budgetclaimform=BudgetClaimForm(request.POST, instance=plan_finance) 
                        itemformset=ItemFormset(request.POST, queryset=qset)            
                        form_saved = False
                        if itemformset.is_valid():
                            for form in itemformset.forms:
                                if form.has_changed():
                                    if not form in itemformset.deleted_forms:
                                        tempform = form.save(commit=False)
                                        tempform.department=event1
                                        tempform.budget=plan_finance
                                        tempform.save()
                                    if form in itemformset.deleted_forms:
                                        if Item.objects.filter(id=form.instance.id):
                                            curr_item = Item.objects.get(id=form.instance.id)
                                            curr_item.delete()      	                
                                    form_saved = True 
                            qset = Item.objects.filter(department=event1, budget=plan_finance) 
                        else:
                            error=True
                        if budgetclaimform.is_valid():
                            total_amount1=0
    	                    budgetclaimform1=budgetclaimform.save(commit=False)
    	                    for qset1 in qset:
    	                        total_amount1+=qset1.original_amount
    	                    budgetclaimform1.total_amount=float(total_amount1)
    	                    budgetclaimform1.save()
    	                else:
                            error=True
                        if 'add_more_items' in request.POST: 
                            if len(qset)<5:
                                extra1=5-len(qset)
                            else:
                                extra1=2
                        else:
                            if len(qset)<5:
                                extra1=5-len(qset)
                            else:
                                extra1=0
                        ItemFormset=modelformset_factory(Item, fields=('name', 'description','quantity','original_amount'),extra=extra1, can_delete=True)
                        itemformset=ItemFormset(queryset=qset) 
                    else:
                        budgetclaimform=BudgetClaimForm(instance=plan_finance)
                        itemformset=ItemFormset(queryset=qset)
                    return render_to_response('finance/budget_display.html',locals(),context_instance=global_context(request))
                else:
                    submitted = True
                    return render_to_response('finance/budget_display.html',locals(),context_instance=global_context(request))               
            else:
                return render_to_response('finance/budget_display.html',locals(),context_instance=global_context(request))    
                        
        else:
            first_time = True
            return render_to_response('finance/budget_display.html',locals(),context_instance=global_context(request)) 
 
"""
Finance core can approve a plan from finance department
"""       
def submit(request, event):
    feedback_tab=True
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
            event1 = Department.objects.get(id=event)
            plans = Budget.objects.filter(department=event1)
            if plans:
                plan_finance=Budget.objects.get(name='F',department=event1)
                
                if plan_finance.submitted==False:
                    plan_finance.submitted=True
                    plan_finance.save()
                    return HttpResponseRedirect(reverse('erp.finance.views.display', kwargs={'event_name': event,}))
                if plan_finance.submitted==True:
                    plan_finance.submitted=False
                    plan_finance.save()
                    return HttpResponseRedirect(reverse('erp.finance.views.budget_portal', kwargs={'plan': 'budget',}))
    else:
        raise Http404
