# Create your views here.
from django.shortcuts import render_to_response, redirect
# from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.template.context import Context, RequestContext
from forms import * 
from django import forms
from erp.users.models import *
from erp.misc.util import *
from erp.misc.helper import *
from erp.department.models import *
from erp.dashboard.forms import *			
from django.contrib.auth.models import Group,Permission
import sha,random,datetime
from erp.users.forms import *
from django.core.mail import send_mail,EmailMessage,SMTPConnection
from django.conf import settings
import os


def register_user(request, dept_name="Events", owner_name = None):
    """
    for test phase the default dept is Events
    """
    print "this is the deptname user belongs to ",dept_name
    department=Department.objects.filter(Dept_Name = dept_name)
    user_form = AddUserForm ()
    profile_form = userprofileForm ()
    if request.method=='POST':
        user_form = AddUserForm (request.POST)

        if user_form.is_valid():
            # Create the User
            new_user = User.objects.create_user(
                username = user_form.cleaned_data['username'],
                email = user_form.cleaned_data['email'],
                password = user_form.cleaned_data['password'],
                )    
            # Save his profile - mainly his dept name
            #here if must be changed to try
	    if True:
	        department=Department.objects.get(Dept_Name = dept_name)
		profile=userprofile.objects.create(user=new_user ,department=department)
                profile.save()
                #creating a folder for the user
		print "user profile saved"
		
                print "trying to craete a folder for the user and assigning a default profile pic"
                file_name="PROFILE_PIC_OF_THE_USER"
                savepath ,file_path=create_dir(file_name  , user_form.cleaned_data['username'])
                image_object=userphoto(name=new_user ,photo_path="http://localhost/django-media/upload_files/ee10b000/PROFILE_PIC_OF_THE_USER")
                image_object.save()
                print "created folder and given default user_profil_pic"
	    else:
		print "userprofile not saved ,check out"
            # Make the user a Coord
            new_user.groups.add (Group.objects.get (name = 'Coords'))
            new_user.is_active=True #took from userportal
            new_user.save()
            registered_successfully = True
            request.session['just_registered'] = True
            return redirect ('erp.home.views.login')
	else:
	    print "the user form is not valid the errors are :"
	    print user_form.errors
            return render_to_response('users/register.html' , locals() ,context_instance = global_context(request))
    else:
        return render_to_response('users/register.html' , locals() ,context_instance = global_context(request))

        
      


# WTH is this?

# def register_invite(request,dept_name="none" ,username="none" ,rollno="ee0b000"):
#     print "deptname :" ,dept_name
#     user_form = AddUserForm (initial={'username':rollno},)
#     return render_to_response('users/register.html' , locals() ,context_instance = global_context(request))


@needs_authentication
def invite(request ,owner_name):
    CsvForm=UploadFileForm(initial={'title':"Enter the name" , 'short_description':"you may write anything here"})
    message=[]
    message+=["start"]
    User=request.user
    user_dept = str(User.userprofile_set.all()[0].department)
    print user_dept
    success_message="" 
    if request.method=='POST':
        form=InviteForm(request.POST)
        if form.is_valid():
            message+=["form valid "]
            name=form.cleaned_data['invitee']
            emailid=form.cleaned_data['email_id']
            roll_no=form.cleaned_data['roll_no']
            

            # print settings.SITE_URL+"/users/register_invite/"+user_dept+"/"+name+"/"+roll_no+"/"
            invite_details=invitation(
            core=request.user,
            invitee=name,
            email_id=emailid,
            time=datetime.datetime.now(),
            )#this stores the information of invitation
            try:
                #here the essential mail details are assigned
                hyperlink=settings.SITE_URL+"/users/register_invite/"+user_dept+"/"+name+"/"+roll_no+"/"
                mail_header="Invitaiton from the core to join ERP"
                mail=[emailid,]
		print mail
                #sending mail here
                print "came till the function part"
                success_message=mail_coord(hyperlink ,mail_header ,name ,"users/emailcoords.html" ,mail ) 
               
            except:
                message+=["mail could not be sent "]
                success_message=["mail could not be sent may be wrong details"]
                print "mail not sent."
                pass

		

    else:
        message+=["form not valid"]
    form=InviteForm()
    return render_to_response('dashboard/invite.html',locals(),context_instance = global_context(request))



"""
this part yet to be done
"""
@needs_authentication
def invite_inbulk(request ,self):
    CsvForm=UploadFileForm(initial={'title':"Enter the title" , 'short_description':"you may write anything here"})
    form=InviteForm()
    if request.method=='POST':
        pass



            
@profile_authentication
def view_profile(request, owner_name=None):
    page_owner = get_page_owner (request, owner_name)
    try:
        image=userphoto.objects.get(name=page_owner)
        photo_path =image.photo_path
    except:
        photo_path=settings.MEDIA_URL+"/upload_files/ee10b000/PROFILE_PIC_OF_THE_USER"
    profile = userprofile.objects.get(user=page_owner)
    print profile.nickname
    print profile.name
    return render_to_response('users/view_profile.html',locals(),context_instance = global_context(request))
    	


@needs_authentication
def handle_profile (request  , owner_name):
    print request.user.id , "is the id of the user"

    user = request.user
    profile = userprofile.objects.get(user=request.user)
    if request.method=='POST' :
        profile_form = userprofileForm (request.POST, instance = profile)
        if profile_form.is_valid ():
            profile_form.save ()
            # Should this just redirect to the dashboard?
	    return view_profile(request ,request.user.username)
    print profile.hostel
    profile_form = userprofileForm (instance = profile)       
    print " default pic address http://localhost/django-media/upload_files/ee10b000/PROFILE_PIC_OF_THE_USER"
    try:
        image=userphoto.objects.get(name=request.user)
        photo_path =image.photo_path
        print photo_path
    except:
        photo_path=settings.MEDIA_URL+"/upload_files/ee10b000/PROFILE_PIC_OF_THE_USER"
    return render_to_response('users/edit_profile.html',locals(),context_instance = global_context(request))

