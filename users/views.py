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
from django.core.mail import send_mail,EmailMessage
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
        if is_multiple_user(request.user):
            multiple = userprofile.objects.all()
            for each in multiple:
                if (each.user.username.startswith(request.user.username.lower()) and each.user.username!=request.user.username):
                    image=userphoto.objects.get(name = each.user)
                    photo_path =image.photo_path
                    break

    profile = userprofile.objects.get(user=page_owner)
    group = str(page_owner.groups.all()[0])[:-1] #drop 's' from group name. Ex: 'Core' from 'Cores'
    print profile.nickname
    print profile.name

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

    curr_user=request.user
    curr_userprofile=userprofile.objects.get(user=request.user)    
    if is_core(curr_user):
		if str(curr_userprofile.department) == 'QMS':
			qms_core= True

    if is_supercoord(curr_user):
        if str(curr_userprofile.department) == 'QMS':
            qms_supercoord= True
            
    if is_coord(curr_user):
		if str(curr_userprofile.department) == 'QMS':
			qms_coord= True

    return render_to_response('users/view_profile.html',locals(),context_instance = global_context(request))
    	
@needs_authentication_multiple_user
def handle_profile (request, owner_name):
    print request.user.id , "is the id of the user"

    user = request.user
    profile = userprofile.objects.get(user=request.user)
    if request.method=='POST':
        try:
            supercores = request.user.get_profile().department.owner.all()     #check if the department has a supercore, else department.owner will be NULL, and go to except.
            supercore=supercores[0]
            for x in supercores:
                if request.user.username.startswith(x.username.lower()):
                    supercore = x
                    break
                    
            if request.user.username.startswith(supercore.username.lower()):                  #checking if the supercore is using one of his core accounts.
                profile = userprofile.objects.get(user = supercore)
                profile_form = userprofileForm (request.POST, instance = profile)
                if profile_form.is_valid():
                    profile_form.save ()
                departments = supercore.department_set.all()
                for dept in departments:
                    allUserProfiles = userprofile.objects.filter(department = dept)
                    for each in allUserProfiles:
                        if each.user.username.startswith(supercore.username.lower()):
                            profile_form = userprofileForm (request.POST, instance = each)
                            if profile_form.is_valid():
                                profile_form.save()
            else:                                                            
                department = request.user.get_profile().department
                if request.user.username.endswith(department.Dept_Name.replace(' ','').lower()):                #a multiple coord-associated acc.
                    allUserProfiles = userprofile.objects.all()
                    multiple_coord=request.user.username.split('_')[0]
                    for each in allUserProfiles:
                        if each.user.username.startswith(multiple_coord.lower()):
                            profile_form = userprofileForm (request.POST, instance = each)
                            if profile_form.is_valid():
                                profile_form.save()
                else:                                      #there may be an account in a department having a supercore, but is not a supercore-associated account, and isn't a multiple-coord-associated acc.
                    profile = userprofile.objects.get(user=request.user)
                    profile_form = userprofileForm (request.POST, instance = profile)
                    if profile_form.is_valid():
                        profile_form.save ()
                
        except:
            if is_multiple_user(request.user):                           #is a supercore/multiple-coord account
                allUserProfiles = userprofile.objects.all()
                for each in allUserProfiles:
                    if each.user.username.startswith(request.user.username.lower()):
                        profile_form = userprofileForm (request.POST, instance = each)
                        if profile_form.is_valid():
                            profile_form.save()
            else:                                        #multiple-coord-associated acc, in a dept without a supercore.
                department = request.user.get_profile().department
                if request.user.username.endswith(department.Dept_Name.replace(' ','').lower()):
                    allUserProfiles = userprofile.objects.all()
                    multiple_coord=request.user.username.split('_')[0]
                    print multiple_coord
                    for each in allUserProfiles:
                        if each.user.username.startswith(multiple_coord.lower()):
                            print each
                            profile_form = userprofileForm (request.POST, instance = each)
                            if profile_form.is_valid():
                                profile_form.save()
                else:
                    profile = userprofile.objects.get(user=request.user)
                    profile_form = userprofileForm (request.POST, instance = profile)
                    if profile_form.is_valid():
                        profile_form.save ()
            
        return redirect ('erp.users.views.view_profile', owner_name = request.user.username)
    print profile.hostel
    profile_form = userprofileForm (instance = profile)       
    print " default pic address http://localhost/django-media/upload_files/ee10b000/PROFILE_PIC_OF_THE_USER"
    try:
        image=userphoto.objects.get(name=request.user)
        photo_path =image.photo_path
        print photo_path
    except:
        photo_path=settings.MEDIA_URL+"/upload_files/ee10b000/PROFILE_PIC_OF_THE_USER"

    #Get Department Members' image thumbnails
    page_owner = get_page_owner (request, owner_name=None)
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

    curr_user=request.user
    curr_userprofile=userprofile.objects.get(user=request.user)    
    if is_core(curr_user):
		if str(curr_userprofile.department) == 'QMS':
			qms_core= True

    if is_supercoord(user):
        if str(curr_userprofile.department) == 'QMS':
            qms_supercoord= True
            
    if is_coord(curr_user):
		if str(curr_userprofile.department) == 'QMS':
			qms_coord= True

    return render_to_response('users/edit_profile.html',locals(),context_instance = global_context(request))
    
    

def change_password(request, owner_name=None):
    print "here"
    if (request.method=='POST'):
        old_pass=request.POST['old_pass']
        new_pass1=request.POST['new_pass1']
        new_pass2=request.POST['new_pass2']
        user = User.objects.get(username=request.user.username)
        if (user.check_password(old_pass)):
            if new_pass1==new_pass2 and user==request.user:
                user.set_password(new_pass1)
                user.save()
                changed=True  
            else:
                failed=True  
        else:            
            invalid=True
    return render_to_response('users/change_password.html', locals(), context_instance = global_context(request))            

