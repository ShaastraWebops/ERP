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
from erp.dashboard.models import *
from erp.users.models import *
from erp.misc.util import *
from erp.settings import *
import sha,random,datetime
from erp.dashboard.forms import *
from erp.users.forms import *
import os # upload files
import csv # invite coords
#import stringlib
# Create your views here.
def home (request):
    redirected=session_get(request,"from_url")
    access_denied = session_get (request, "access_denied")
    logged_in = session_get (request, "logged_in")
    already_logged = session_get (request, "already_logged")
    return render_to_response('dashboard/home.html', locals(), context_instance= global_context(request)) 

def delete_otherdetails(request):
    print "came"
    if request.method=='GET':
        if "d" in request.GET:
            number=request.GET['d']
            query=OtherContactDetails(id=number)
            query.delete()
            print "deleted"
            success_message="deleted"
        else :
            print "problem"
    return details()
def details(request):
    if request.method=='GET':
        success_message="came here"
    else:
        success_message="wow done it"
    other_contactform=OtherContactDetails_form(initial={'email_id':"Can be left blank"})
    if request.method=='POST':
        data=request.POST.copy()
        form=OtherContactDetails_form(data)
        
        if form.is_valid():
            print "cool"
            name=form.cleaned_data['name']
            number=form.cleaned_data['number']
            email_id=form.cleaned_data['email_id']
            if (email_id=="Can be left blank"):
                print "cool then"
                email_id=""
            
            addcontact=OtherContactDetails     (user=request.user,
                                                name=name,
                                                number=number,
                                                email_id=email_id,
                                                )
            try :
                addcontact.save()
            except:
                print "lite maama"
        else :
            print "fool"
            

    other_profile=OtherContactDetails.objects.filter(user=request.user)
    
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
    #memberform=forms.add_team_member() was causing somw probs
    return render_to_response('dashboard/documents.html',locals() ,context_instance = global_context(request))

   
# this function is used for uploading csv files also(for inviting coords)
def upload_file(request):
    users_documents=upload_documents.objects.filter(user=request.user)
    print "one"    
    if request.method=='POST':
        print "post"
        form=UploadFileForm(request.POST,request.FILES)
        if True : #form.is_valid():
            print"valid"
            file_name=request.FILES['file'].name
            user_name=request.user.username
            destdir_one=os.path.join(settings.MEDIA_ROOT,"upload_files")
            destdir=os.path.join(destdir_one,user_name)
            if not os.path.isdir(destdir):
                os.makedirs(destdir,0775)
            save_path=os.path.join(destdir,os.path.basename(file_name))

            
            destdir_one=os.path.join(settings.MEDIA_URL,"upload_files")
            destdir=os.path.join(destdir_one,user_name)
            if not os.path.isdir(destdir):
                os.makedirs(destdir,0775)
            file_path=os.path.join(destdir,os.path.basename(file_name))

            
            f=request.FILES['file']
            fout=open(save_path,'wb+')
            for chunk in f.chunks():
                fout.write(chunk)
            fout.close()
            date=datetime.datetime.now()
            try:
                try:
                    file_present=upload_documents.objects.get(user=request.user,file_name=file_name)
                    message="File with this name exists.please change name  of the file"
                except:
                    file_object=upload_documents(user=request.user , file_name=file_name,file_path=file_path, url=file_path ,topic="hello",date=date)#to change topic
                    file_object.save()
                    print "SAVED"
            except:
                print "duplicate name "
            
        else:
            file_name=request.FILES['file'].name
            print "done"

    else:
        print "not post"
        form=UploadFileForm(initial={'title':"Enter the title" , 'short_description':"you may write anything here"})

  # this part is used for invitingcoords 

    if "i" in request.POST:
        print "at last"
        print save_path
        message="done"
        form=InviteForm()
        CsvForm=UploadFileForm(initial={'title':"Enter the title" , 'short_description':"you may write anything here"})
        reader=csv.reader(open(save_path,'rb'),delimiter=' ')
        string=[]
        for field in reader:
            string=string+[field]
        final_string=[]
        for field in string:
        
            splits=field[0].split(';')#; is just temprorary
            final_string=final_string+[splits]
        print final_string
        
        return render_to_response('dashboard/invite.html',locals() ,context_instance = global_context(request))


  
    else :#debugging
        print "not done"

    # till here

    return render_to_response('dashboard/upload.html',locals() ,context_instance = global_context(request))



def delete_file(request):

    users_documents=upload_documents.objects.filter(user=request.user)
    
    if "d" in request.GET:
        number=request.GET['d']
        print number
        
    if "f" in request.GET:
        file_name=request.GET['f']
        print file_name


        user_name=request.user.username
        destdir_one=os.path.join(settings.MEDIA_ROOT,"upload_files")
        destdir=os.path.join(destdir_one,user_name)
        
        file_path=os.path.join(destdir,os.path.basename(file_name))
        print file_path
        print "harere"
        if os.path.isfile(file_path):
            print "cool"
            os.remove(file_path)
            message=file_name+" deleted"
        else:
            print "file not found"
    try:
        delete_file=upload_documents.objects.get(user=request.user , file_name=file_name)
        delete_file.delete()
    except:
        print "no file"
    form=UploadFileForm(initial={'title':"Enter the title" , 'short_description':"you may write anything here"})

    return render_to_response('dashboard/upload.html',locals() ,context_instance = global_context(request))
    
