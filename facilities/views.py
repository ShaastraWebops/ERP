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
from erp.misc.util import *
from erp.facilities.forms import *

def test(request):
    facilities_tab = True
    return render_to_response('facilities/test.html',locals(),context_instance=global_context(request))    

def portal(request):
    curr_userprofile=userprofile.objects.get(user=request.user)
    page_owner = get_page_owner (request, owner_name=request.user)
    department = page_owner.get_profile ().department      
    if is_facilities_coord(request.user):
        return HttpResponseRedirect("/erp/facilities/approval_portal")
    if department.Dept_Name=="QMS":
        return HttpResponseRedirect("/erp/facilities/qms_visible_portal")
    if department.is_event:
        qset = FacilitiesObject.objects.filter(creator__department=curr_userprofile.department)
        if len(qset)<5:
            extra1=5-len(qset)
        else:
            extra1=2
        ItemFormset=modelformset_factory(FacilitiesObject, fields=('name','description','quantity','department'),extra=extra1, can_delete=True)
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
                                    tempform.creator=curr_userprofile
                                    tempform.request_date = datetime.date.today()
                                    tempform.save()
                                    form_saved=True
                                elif curr_item.request_status==1:
                                    tempform = form.save(commit=False)
                                    tempform.creator=curr_userprofile
                                    tempform.request_date = datetime.date.today()
                                    if tempform.quantity <= curr_item.approved_quantity:
                                        tempform.request_status=2
                                    tempform.save()
                                    form_saved=True
                                elif curr_item.request_status==2:
                                    tempform = form.save(commit=False)
                                    tempform.creator=curr_userprofile
                                    tempform.request_date = datetime.date.today()
                                    if tempform.quantity > curr_item.approved_quantity:
                                        tempform.request_status=1
                                    tempform.save()
                                    form_saved=True   
                            except :
                                tempform = form.save(commit=False)
                                tempform.creator=curr_userprofile
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
                      
                qset = FacilitiesObject.objects.filter(creator__department=curr_userprofile.department)
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
                ItemFormset=modelformset_factory(FacilitiesObject, fields=('name','description','quantity','department'),extra=extra1, can_delete=True)
                itemformset=ItemFormset(queryset=qset)  
            else:
                items=FacilitiesObject.objects.all()
                error=True        
        else:            
            itemformset=ItemFormset(queryset=qset)

    return render_to_response('facilities/portal.html',locals(),context_instance=global_context(request))

def approval_portal(request):
    curr_userprofile=userprofile.objects.get(user=request.user)
    curr_user = request.user
    page_owner = get_page_owner (request, owner_name=request.user)
    department = page_owner.get_profile ().department
    departments=Department.objects.filter(is_event=True).order_by('Dept_Name')   
    changed_objects=[] 
    new_objects=[]
    exists_objects=[]
    for dept in departments:
        a=FacilitiesObject.objects.filter(creator__department=dept,department=curr_userprofile.department)
        if len(a.filter(request_status=0)) != 0:       
            new_objects.append(dept.Dept_Name)   
        elif len(a.filter(request_status=1)) != 0 :       
            changed_objects.append(dept.Dept_Name) 
        elif len(a) !=0:
            exists_objects.append(dept.Dept_Name)
            
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
    for dept in departments:
        a=FacilitiesObject.objects.filter(creator__department=dept)
        if len(a.filter(request_status=0)) != 0:       
            new_objects.append(dept.Dept_Name)   
        elif len(a.filter(request_status=1)) != 0 :       
            changed_objects.append(dept.Dept_Name) 
        elif len(a) !=0:
            exists_objects.append(dept.Dept_Name)
            
    return render_to_response('facilities/approval_portal.html',locals(),context_instance=global_context(request)) 
    
def display(request):
    curr_userprofile=userprofile.objects.get(user=request.user)
    page_owner = get_page_owner (request, owner_name=request.user)
    department = page_owner.get_profile ().department   
    items = FacilitiesObject.objects.filter(creator__department=curr_userprofile.department).order_by('request_date','request_status')
    number=0
    #number=Department.facilitiesitem_set.count()
    return render_to_response('facilities/display.html',locals(),context_instance=global_context(request))

def approve_event(request,event_name,form_saved=0,error=0):
    qms_coord=0
    dept=Department.objects.get(id=event_name)
    facilities_coord=0
    curr_userprofile=userprofile.objects.get(user=request.user)
    if is_facilities_coord(request.user):
        facilities_coord=1
        items = FacilitiesObject.objects.filter(creator__department=dept,department=curr_userprofile.department).order_by('request_status','request_date')
    elif curr_userprofile.department.Dept_Name == "QMS":
        qms_coord=1
        items = FacilitiesObject.objects.filter(creator__department=dept).order_by('request_status','request_date')
        
    

    request_form = ApprovalForm()
    return render_to_response('facilities/approve_event.html',locals(),context_instance=global_context(request))

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
            return HttpResponseRedirect('/erp/facilities/approve_event/%d/%d/%d/'%(item.creator.department.id,form_saved,error)) 
            
        else:
            error=1
    return HttpResponseRedirect('/erp/facilities/approve_event/%d/%d/%d/'%(item.creator.department.id,form_saved,error))
    




