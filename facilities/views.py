# Create your views here.
from django.template import *
from django.http import *
from django.shortcuts import *
from django.template import *
from erp.misc.helper import is_core, is_coord, is_supercoord, get_page_owner
from erp.misc.util import *
from erp.facilities.models import *
from erp.facilities.forms import *
from django.forms.models import modelformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from erp.misc.helper import *
from erp.misc.util import *
from erp.facilities.forms import *
from settings import SITE_URL
from pdfGeneratingViews import generateOverallPDF
from pdfGeneratingViews import generateEventPDF
from erp.facilities.models import DATE_CHOICES
from erp.facilities.eventParticipationPDF import generateEventParticipationPDF

def test(request):
    facilities_tab = True
    return render_to_response('facilities/test.html',locals(),context_instance=global_context(request))  
  
def facilities_home(request):
    curr_userprofile=userprofile.objects.get(user=request.user)
    page_owner = get_page_owner (request, owner_name=request.user)
    department = page_owner.get_profile ().department      
    
    special_req_dept=Department.objects.get(id=58)
    '''if is_facilities_coord(request.user):
    	if is_core(request.user):
            return HttpResponseRedirect(SITE_URL + "erp/facilities/approval_portal/")
        if is_supercoord(request.user):
            return HttpResponseRedirect(SITE_URL + "erp/facilities/approval_portal/")
        if request.user.username == "ch10b090":
            return HttpResponseRedirect(SITE_URL + "erp/facilities/approval_portal/")
        if request.user.username == "ce10b084":
            return HttpResponseRedirect(SITE_URL + "erp/facilities/approval_portal/")

        
        
        return HttpResponseRedirect(SITE_URL + "erp/facilities/approval_portal/")'''
    # if department.Dept_Name=="QMS":
    #     return HttpResponseRedirect(SITE_URL + "erp/facilities/qms_visible_portal/")
    if request.user.username=="ee11b075":
        return HttpResponseRedirect(SITE_URL + "erp/facilities/approval_portal/")  
    if curr_userprofile.department.is_event:
        return HttpResponseRedirect(SITE_URL + "erp/facilities/round_home/"+str(curr_userprofile.department.id))         

    return HttpResponseRedirect(SITE_URL + "erp/facilities/approval_portal/")   

#Redundant
def portal(request,roundno):
    curr_userprofile=userprofile.objects.get(user=request.user)
    page_owner = get_page_owner (request, owner_name=request.user)
    department = page_owner.get_profile ().department 
    special_req_dept=Department.objects.get(id=58)
    
    if department.is_event:
        qset = FacilitiesObject.objects.filter(creator__department=curr_userprofile.department,roundno=roundno)
        if len(qset)<5:
            extra1=5-len(qset)
        else:
            extra1=2
        ItemFormset=modelformset_factory(FacilitiesObject, fields=('name','description','quantity'),extra=extra1, can_delete=True)
        if request.method=='POST':
            itemformset=ItemFormset(request.POST, queryset=qset)            
            form_saved = False
            if itemformset.is_valid():
                for form in itemformset.forms:
                    if form.has_changed():
                        if not form in itemformset.deleted_forms:
                            try:
                                curr_item = FacilitiesObject.objects.get(id=form.instance.id)
                                if curr_item.request_status ==0:
                                    tempform = form.save(commit=False)
                                    if tempform.quantity < 0:
                                        tempform.quantity=0
                                    tempform.roundno=roundno
                                    tempform.creator=curr_userprofile
                                    if form.instance.name.department == special_req_dept:
                                    	tempform.department=None
                                    else :
                                    	tempform.department=form.instance.name.department
                                    tempform.request_date = datetime.date.today()
                                    tempform.save()
                                    form_saved=True
                                elif curr_item.request_status==1:
                                    tempform = form.save(commit=False)
                                    tempform.creator=curr_userprofile
                                    tempform.request_date = datetime.date.today()
                                    if form.instance.name.department == special_req_dept:
                                    	tempform.department=None
                                    else :
                                    	tempform.department=form.instance.name.department
                                    tempform.department=form.instance.name.department
                                    tempform.roundno=roundno
                                    if tempform.quantity <= curr_item.approved_quantity:
                                        tempform.request_status=2
                                    tempform.save()
                                    form_saved=True
                                elif curr_item.request_status==2:
                                    tempform = form.save(commit=False)
                                    tempform.creator=curr_userprofile
                                    if form.instance.name.department == special_req_dept:
                                    	tempform.department=None
                                    else :
                                    	tempform.department=form.instance.name.department
                                    tempform.department=form.instance.name.department
                                    tempform.roundno=roundno
                                    tempform.request_date = datetime.date.today()
                                    if tempform.quantity > curr_item.approved_quantity:
                                        tempform.request_status=1
                                    tempform.save()
                                    form_saved=True   
                            except :
                                tempform = form.save(commit=False)
                                tempform.creator=curr_userprofile
                                if form.instance.name.department == special_req_dept:
                               	    tempform.department=None
                                else :
                                    tempform.department=form.instance.name.department
                                tempform.roundno=roundno
                                tempform.department=form.instance.name.department
                                tempform.request_date = datetime.date.today()
                                tempform.save()      
                                form_saved=True           
                        if form in itemformset.deleted_forms:
                            if FacilitiesObject.objects.filter(id=form.instance.id):
                                curr_item = FacilitiesObject.objects.get(id=form.instance.id)
                                if curr_item.request_status == 0:    
                                    curr_item.delete() 
                                    form_saved=True
                                else :
                                    error2 = 1
                      
                qset = FacilitiesObject.objects.filter(creator__department=curr_userprofile.department,roundno=roundno)
                #if 'add_more_items' in request.POST: 
                             
                if len(qset)<5:
                    extra1=5-len(qset)
                else:
                    extra1=2
               # else:
                #    if len(qset)<5:
                 #       extra1=5-len(qset)
                  #  else:
                   #     extra1=0
                ItemFormset=modelformset_factory(FacilitiesObject, fields=('name','description','quantity'),extra=extra1, can_delete=True)
                itemformset=ItemFormset(queryset=qset)  
            else:
                items=FacilitiesObject.objects.filter(roundno=roundno)
                error=True        
        else:            
            itemformset=ItemFormset(queryset=qset)

    return render_to_response('facilities/portal.html',locals(),context_instance=global_context(request))

def approval_portal(request):
    date_list=[]
    date_list=range(5,len(DATE_CHOICES)+5)
    page_owner = get_page_owner (request, owner_name=request.user)
    curr_userprofile=userprofile.objects.get(user=request.user)
    department = page_owner.get_profile ().department
    departments=Department.objects.filter(is_event=True).order_by('Dept_Name')   
    changed_objects=[] 

    new_objects=[]
    exists_objects=[]
    special_req_dept=Department.objects.get(id=58)
    exist_dept=[]
    for dept in departments:
        a=EventRound.objects.filter(department=dept)
        if len(a)!=0:
            exist_dept.append(dept)
    '''for dept in departments:
        a=FacilitiesObject.objects.filter(creator__department=dept,department=curr_userprofile.department)
        b=FacilitiesObject.objects.filter(creator__department=dept,name__department=special_req_dept)
        if len(a.filter(request_status=0)) + len(b.filter(request_status=0)) != 0:       
            new_objects.append(dept.Dept_Name)   
        elif len(a.filter(request_status=1)) + len(b.filter(request_status=1)) != 0 :       
            changed_objects.append(dept.Dept_Name) 
        elif len(a) + len(b) !=0:
            exists_objects.append(dept.Dept_Name)'''
    
            
    return render_to_response('facilities/approval_portal.html',locals(),context_instance=global_context(request)) 

def qms_visible_portal(request):
    curr_userprofile=userprofile.objects.get(user=request.user)
    curr_user = request.user
    page_owner = get_page_owner (request, owner_name=request.user)
    department = page_owner.get_profile ().department
    departments=Department.objects.filter(is_event=True).order_by('Dept_Name')   
    changed_objects=[] 
    new_objects=[]
    exists_objects=[]
    
    ''''for dept in departments:
        a=FacilitiesObject.objects.filter(creator__department=dept)
        if len(a.filter(request_status=0)) != 0:       
            new_objects.append(dept.Dept_Name)   
        elif len(a.filter(request_status=1)) != 0 :       
            changed_objects.append(dept.Dept_Name) 
        elif len(a) !=0:
            exists_objects.append(dept.Dept_Name)'''
    
            
    return render_to_response('facilities/approval_portal.html',locals(),context_instance=global_context(request)) 
    
def round_home(request,event_id):
    dept = Department.objects.get(id = event_id)
    eventrounds=EventRound.objects.filter(department=dept)
    return render_to_response('facilities/round_home.html',locals(),context_instance=global_context(request))
 
def add_round(request,event_id):
    curr_userprofile=userprofile.objects.get(user=request.user)
    page_owner = get_page_owner (request, owner_name=request.user)
    department = Department.objects.get(id=event_id) 
    e=EventRound()
    try :
        print "c"
        exist = EventRound.objects.get(department=department,number=1)
        print "x"
        allround = EventRound.objects.filter(department=department).order_by('-number')
        print allround[0].number
        e.number = allround[0].number + 1
        e.department=department
        e.name = "Round " + str(e.number)
        p=e.id
        e.save()
        print "f"
    except:
        print "b"
        e.number=1
        e.department=department 
        e.name = "Round " + str(e.number)
        p=e.id
        e.save()
    items = ItemList.objects.all()
    for item in items:
        a=FacilitiesObject(department=department,event_round=e,name=item)
        a.save()
        
    return HttpResponseRedirect(SITE_URL + "erp/facilities/round_home/" + str(department.id))   

def delete_round(request,round_id):
    rounder = EventRound.objects.get(id=round_id)
    department=rounder.department
    try:
        rounder.delete()
    except:
        pass
    return HttpResponseRedirect(SITE_URL + "erp/facilities/round_home/" + str(department.id))
    

 
def display(request,roundno):
    curr_userprofile=userprofile.objects.get(user=request.user)
    page_owner = get_page_owner (request, owner_name=request.user)
    department = page_owner.get_profile ().department   
    items = FacilitiesObject.objects.filter(creator__department=curr_userprofile.department,roundno=roundno).order_by('name','request_status')
    
    return render_to_response('facilities/display.html',locals(),context_instance=global_context(request))

def approve_event(request,round_id,form_saved=0,error=0):
    curr_userprofile=userprofile.objects.get(user=request.user)
    qms_coord=0
    editable=0
    print "a"
    rounder = EventRound.objects.get(id = round_id)
    dept=rounder.department
    facilities_coord=0
    items = FacilitiesObject.objects.filter(event_round = rounder)
   
    if is_core(request.user) and is_facilities_coord(request.user):
        editable = 1
    if request.user.username == "ch10b090":
        editable = 1
    if request.user.username == "ce10b084":
        editable = 1
    if request.user.username == "ee11b075":
        editable = 1
    if curr_userprofile.department.id==57:
        editable = 1
    if curr_userprofile.department.id == dept.id:
        event_editable=1
    if curr_userprofile.department.Dept_Name =="QMS":
        event_editable=1
        
    form_saved
    if request.method == "POST":
        form_saved=0
        error=0
        try:        
            round_form=RoundForm(request.POST)
            form=round_form.save(commit=False)
            form.department=rounder.department
            form.number=rounder.number
            form.id=rounder.id
            form.save()
            form_saved=1
            
            rounder=form
        except:
            error=1
        return HttpResponseRedirect(SITE_URL + 'erp/facilities/approve_event/%d/%d/%d/'%(rounder.id,form_saved,error))
    round_form = RoundForm(instance=rounder)
    request_form=ApprovalForm()
    return render_to_response('facilities/approve_event.html',locals(),context_instance=global_context(request))  
       
    
    '''
    request_form = ApprovalForm()
    ItemFormset=modelformset_factory(EventRound, fields=('name','date','hour','minute'))
    qset=EventRound.objects.filter(id=round_id)
    if request.method=="POST":
        itemform=ItemFormset(request.POST, queryset=qset)            
        form_saved = False
        if itemform.is_valid():
            if itemform.has_changed():
                tempform = itemform.save(commit=False)
                tempform.number = rounder.number
                tempform.department = rounder.department
                tempform.save()
                form_saved=1
        else:
            error=1
    itemform=ItemFormset(queryset=qset)'''

    '''if is_facilities_coord(request.user):
        
    	if is_core(request.user):
    	    editable=1
    	    items = FacilitiesObject.objects.filter(creator__department=dept).order_by('-roundno','name','request_status')
    	if is_supercoord(request.user):
    	    editable=1
    	    items = FacilitiesObject.objects.filter(creator__department=dept).order_by('-roundno','name','request_status')
    	else:
            items = FacilitiesObject.objects.filter(creator__department=dept,department=curr_userprofile.department).order_by('-roundno','name','request_status','request_date')
    elif curr_userprofile.department.Dept_Name == "QMS":
        qms_coord=1
        editable=1
        items = FacilitiesObject.objects.filter(creator__department=dept).order_by('-roundno','name','request_status')'''

def submit_round(request,round_id):
    form_saved=0
    error=0
    rounder = EventRound.objects.get(id=round_id)
    if request.method== 'POST':
        round_form = RoundForm(request.POST)
        if round_form.is_valid():
            rounder.name
    
def submit_approval(request,item_id):
    form_saved=0
    error=0
    item = FacilitiesObject.objects.get(id=item_id)
    if request.method == 'POST':
        approval_form = ApprovalForm(request.POST)
        if approval_form.is_valid():    
            item.quantity = approval_form.cleaned_data['approved_number']
            try:
                item.save()
                form_saved=1
            except:
                error=1
        else:
            error=1
    return HttpResponseRedirect(SITE_URL + 'erp/facilities/approve_event/%d/%d/%d/'%(item.event_round.id,form_saved,error))        

'''
def submit_approval(request,item_id):

    item = FacilitiesObject.objects.get(id=item_id)
    error=form_saved=0
    if request.method == 'POST':
        approval_form = ApprovalForm(request.POST)
        if approval_form.is_valid():
            item.approved_quantity = approval_form.cleaned_data['approved_number']
            item.comment = approval_form.cleaned_data['comment']
            item.approved_by = str(request.user.get_profile().name + "(" + request.user.get_profile().department.Dept_Name + ")")
            if item.approved_quantity <= 0:              
                item.request_status = 0
                item.approved_quantity=0

            elif item.approved_quantity < item.quantity:                
                item.request_status = 1
            else:
                item.request_status = 2 
            item.save()
            form_saved=1
            return HttpResponseRedirect(SITE_URL + 'erp/facilities/approve_event/%d/%d/%d/'%(item.creator.department.id,form_saved,error)) 
            
        else:
            error=1
    return HttpResponseRedirect(SITE_URL + 'erp/facilities/approve_event/%d/%d/%d/'%(item.creator.department.id,form_saved,error))
'''

@login_required
def event_participation_pdf(request, dept_id):
    dept_id = int(dept_id)
    return generateEventParticipationPDF(dept_id)

