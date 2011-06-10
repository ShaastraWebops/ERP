# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.template.loader import get_template
from django.template.context import Context, RequestContext
from django.utils.translation import ugettext as _
from django.core.mail import send_mail,EmailMessage,SMTPConnection
from django.contrib.sessions.models import Session
#from erp.dashboard import forms
from erp.dashboard.models import *
from erp.users.models import *
from erp.misc.util import *
from erp.settings import *
import sha,random,datetime
from erp.dashboard.forms import *
# Create your views here.
def home (request):
    redirected=session_get(request,"from_url")
    access_denied = session_get (request, "access_denied")
    logged_in = session_get (request, "logged_in")
    already_logged = session_get (request, "already_logged")
    return render_to_response('dashboard/home.html', locals(), context_instance= global_context(request)) 


def documents (request):
    events_dept=Department.objects.get(id=1)
    try:
        events_profile=userprofile.objects.filter(department=events_dept)
        print "done"
    except:
        print "events"#debugging

        
    qms_dept=Department.objects.get(id=2)
    try:
        qms_profile=userprofile.objects.filter(department=qms_dept)
    except:
        print "QMS"#debugging

        
    finance_dept=Department.objects.get(id=3)
    try:
        finance_profile=userprofile.objects.filter(department=finance_dept)
    except:
        print "finance"#debugging


        
    sponsorship_dept=Department.objects.get(id=4)
    try:
        sponsorship_profile=userprofile.objects.filter(department=sponsorship_dept)
    except:
        print "spons"#debugging


        
    evolve_dept=Department.objects.get(id=5)
    try:
        evolve_profile=userprofile.objects.filter(department=evolve_dept)
    except:
        print "evolve"#debugging


        
    facilities_dept=Department.objects.get(id=6)
    try:
        facilities_profile=userprofile.objects.filter(department=facilities_dept)
    except:
        print "facilities"#debugging


        
    webops_dept=Department.objects.get(id=7)
    try:
        webops_profile=userprofile.objects.filter(department=webops_dept)
    except:
        print "webops awesome"#debugging

        
    hospilatity_dept=Department.objects.get(id=8)
    try:
        hospitality_profile=userprofile.objects.filter(department=hospitality_dept)
    except:
        print "hospi"#debugging


        
    publicity_dept=Department.objects.get(id=9)
    try:
        publicity_profile=userprofile.objects.filter(department=publicity_dept)
    except:
        print "publicity"#debugging
    

    design_dept=Department.objects.get(id=10)
    try:
        design_profile=userprofile.objects.filter(department=design_dept)
    except:
        print "design"#debugging
    
        
    details=teamdetails.objects.all()#still to be filtered according to dept
    memberform=forms.add_team_member()
    return render_to_response('dashboard/documents.html',locals() ,context_instance = global_context(request))

def addteammember(request):
    events_profile=userprofile.objects.all(department_id=7)
    print "events"
    print events_profile
    memberform=forms.add_team_member()
    message="Hello"
    details=teamdetails.objects.all()#still to be filtered according to dept
    print details
    if request.method=='POST':
        print "here"
        data=request.POST.copy()
        form=forms.add_team_member(data)
        if form.is_valid():
            addmember=teamdetails(
            name=models.User.objects.get(username=form.cleaned_data['name']) ,
            email_id=form.cleaned_data['email_id'],
            mobile_number=form.cleaned_data['mobile_number'],
            department=Department.objects.get(Dept_Name=request.session['department']),
            )
        try:
            addmember.save()
            message="team member added"
            print "peace"

        except:
            #message="team member could not be added"
            print "problem"
            pass

    else:
        message="team member could not be added"
    return render_to_response('dashboard/documents.html',locals() ,context_instance = global_context(request))


def deleteteammember(request):
    memberform=forms.add_team_member()
    message = "could not delete the team member "
    details=teamdetails.objects.all()
    if "d" in request.GET:
        number=request.GET['d']
        delete=teamdetails.objects.get(id=number)
        print delete

        delete.delete();
        details=teamdetails.objects.all()
        message = "Team member deleted "
        print number
        print "yahoo"
        print delete



    return render_to_response('dashboard/documents.html',locals() ,context_instance = global_context(request))

"""
def editteammember(request):
    memberform=forms.add_team_member()
    message = "could not delete the team member "
    details=teamdetails.objects.all()
    button="Save"
        if "e" in request.GET:
            number=request.GET['e']
            edit=teamdetails.objects.filter(id=number)
    return render_to_response('dashboard/documents.html',locals() ,context_instance = global_context(request))
            
                
"""    

def upload_file(request):
    print "one"    
    if request.method=='POST':
        print "post"
        form=UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            print"valid"
            file_name=request.FIlES['file'].name
            user_name=request.user['username']
            destdir=os.path.join(settings.MEDIA_ROOT,user_name)
            if not os.path.isdir(destdir):
                os.makedirs(destdir,0775)
            filepath=os.path.join(destdir,os.path.basename(file_name))
            fout=open(filepath,'wb+')
            for chunk in f.chunks():
                fout.write(chunk)
            fout.close()
            date=datetime.datetime.now()
            file_object=upload_documents(user=request.user , file_name=file_name,file_path=filepath,topic=form.cleaned_data['short_description'],date=date)
            file_object.save()
            print "SAVED"
    else:
        print "not post"
        form=UploadFileForm(initial={'title':"Enter the title" , 'short_description':"you may write anything here"})

    return render_to_response('dashboard/upload.html',locals() ,context_instance = global_context(request))
            
    #return render_to_response('/dashboard/upload.html',locals(),context_instance=global_context(request)))
         
    
