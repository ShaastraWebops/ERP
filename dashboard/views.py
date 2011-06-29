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
from erp.department.models import *
from erp.users.models import *
from erp.users.views import *
from erp.tasks.views import *
from erp.misc.util import *
from erp.settings import *
import sha,random,datetime
from erp.dashboard.forms import *
from erp.users.forms import *
import os # upload files
from django.conf import settings
import csv # invite coords
#import stringlib
# Create your views here.

# def delete_otherdetails(request):
#     print "came"
#     if request.method=='GET':
#         if "d" in request.GET:
#             number=request.GET['d']
#             query=OtherContactDetails(id=number)
#             query.delete()
#             print "deleted"
#             success_message="deleted"
#         else :
#             print "problem"
#     return details()

def display_contacts (request):
    """
    Display all contacts (listed by Department).
    """
    dept_names = [name for name, description in DEP_CHOICES]
    contacts = []
    # Create a list of tuples
    # (Dept Name, List of Core profiles, List of Coord profiles)
    # for each department
    for name in dept_names:
        core_profiles = userprofile.objects.filter (department__Dept_Name = name,
                                                    user__groups__name = 'Cores')
        coord_profiles = userprofile.objects.filter (department__Dept_Name = name,
                                                     user__groups__name = 'Coords')
        contacts.append ((name, core_profiles, coord_profiles))
    return render_to_response('dashboard/documents.html',locals() ,context_instance = global_context(request))


# old_details view:
#     if request.method=='GET':
# 	pass
#     else:
#         pass
#     other_contactform=OtherContactDetails_form(initial={'email_id':"Can be left blank"})
#     if request.method=='POST':
#         data=request.POST.copy()
#         form=OtherContactDetails_form(data)
        
#         if form.is_valid():
#             print "cool"
#             name=form.cleaned_data['name']
#             number=form.cleaned_data['number']
#             email_id=form.cleaned_data['email_id']
#             if (email_id=="Can be left blank"):
#                 print "cool then"
#                 email_id=""
            
#             addcontact=OtherContactDetails     (user=request.user,
#                                                 name=name,
#                                                 number=number,
#                                                 email_id=email_id,
#                                                 )
#             try :
#                 addcontact.save()
# 		success_message="The contact details has been saved"
#             except:
#                 print "lite maama"
#         else :
#             print "fool"

#this function creates the directory
def create_dir(file_name ,user_name , method=1):
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
    
    return (save_path , file_path)



#this function writes the file
def write_file(save_path ,f ,method=1):
    fout=open(save_path,'wb+')
    for chunk in f.chunks():
        fout.write(chunk)
    fout.close()



    
    
# this function is used for uploading csv files also(for inviting coords)
def upload_file(request):
    users_documents=upload_documents.objects.filter(user=request.user)       
    if request.method=='POST':
        print "post"
        form=UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            
            file_name=request.FILES['file'].name

            user_name=request.user.username

            save_path ,file_path = create_dir(file_name ,user_name)#passing to the fuction to make directories if not made         
            
            date=datetime.datetime.now()

            try:
                file_present=upload_documents.objects.get(user=request.user,file_name=file_name)
                message="File with this name exists.please change name  of the file"
            except:
                f=request.FILES['file']
                write_file(save_path ,f)
                file_object=upload_documents(user=request.user , file_name=file_name,file_path=save_path, url=file_path ,topic="hello",date=date)#to change topic
                file_object.save()
                print "SAVED"
            
        else:
            file_name=request.FILES['file'].name
            print "done"

    else:
        print "not post"
        form=UploadFileForm(initial={'title':"Enter the title" , 'short_description':"you may write anything here"})


    return render_to_response('dashboard/upload.html',locals() ,context_instance = global_context(request))





def upload_invite_coords(request):
    form=InviteForm()
    CsvForm=UploadFileForm(initial={'title':"Enter the title" , 'short_description':"you may write anything here"})
    if request.method=='POST':
        print "post"
        form=UploadFileForm(request.POST,request.FILES)
        if True : #form.is_valid(): yet to check the file            
            file_name=request.FILES['file'].name

            user_name=request.user.username

            save_path ,file_path = create_dir(file_name ,user_name)#passing to the fuction to make directories if not made         
            
            date=datetime.datetime.now()

            try:
                file_present=upload_documents.objects.get(user=request.user,file_name=file_name)
                message="There is a file already with this name .please change the name of the file"
            except:
                f=request.FILES['file']
                write_file(save_path ,f)
                file_object=upload_documents(user=request.user , file_name=file_name,file_path=file_path, url=file_path ,topic="invitation to coords",date=date)#to change topic
                file_object.save()


            message="done"
            """ from here the the csv file is opened and the the coords are invited """
            
            reader=csv.reader(open(save_path,'rb'),delimiter=' ')
            string=[]
            for field in reader:
                string=string+[field]
            final_string=[]
            for field in string:
        
                splits=field[0].split(';')#; is just temprorary
                final_string=final_string+[splits]
            print final_string
        
        
        else:
            print "not valid"

    else:
        print "not post"
        
    return render_to_response('dashboard/invite.html',locals() ,context_instance = global_context(request))




   
        

def change_profile_pic(request):
    if request.method == 'POST':
        form=change_pic(request.POST,request.FILES)      
        print "cool"
        if form.is_valid():
            print "form valid"
            file_name="PROFILE_PIC_OF_THE_USER"
            user_name=request.user.username

            save_path ,file_path = create_dir(file_name ,user_name)#passing to the fuction to make directories if not made         
            
            photo=userphoto(name =request.user)
            
            print "here only"
            f=request.FILES['file']
            write_file(save_path ,f)
	    print save_path
            shoto_path=settings.MEDIA_URL+"/upload_files/images/PROFILE_PIC_OF_THE_USER"
	    if os.path.isfile(save_path):
		print "file path is there"
		delete_object=userphoto.objects.filter(name=request.user)
		delete_object.delete()
	    else :
		print "not there"
            try:
                image_object=userphoto(name=request.user ,photo_path=file_path )
                image_object.save()
                print "save"
            except:
                print "not saved"
                pass
            return contact_details(request)    
	else:
	    print "not valid"
            
    pic_form=change_pic()
    
    return render_to_response('users/change_profile_pic.html',locals(),context_instance = global_context(request))






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
    

"""
another feature required is by mistake if the user clicks shout two times or refreshes the page,
the comment is passes twice,we can remove it by comparing it with the latest update in the database 

"""
# def shout(request):
#     if request.method=="POST":
#         form=shout_box_form(request.POST.copy)
#         if form.is_valid:
#             print "ya da.."
#             print form.is_valid
#             time=datetime.datetime.now() 
#             #comments=form.cleaned_data['comments']#here some error is there 
#             #number=form.cleaned_data['number']          
#             #print comments
#             user=userprofile.objects.get(user=request.user)
#             nickname=user.nickname
#             shout_object=shout_box(user=request.user,nickname=nickname,comments="cool",time_stamp=time)#change the comments part da comments=comments
#             shout_object.save()
            
        
#     print "at last"
#     return display_department_portal(request)
#     pass
