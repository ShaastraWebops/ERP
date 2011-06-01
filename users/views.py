# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.template.loader import get_template
from django.template.context import Context, RequestContext
from forms import * 
from django import forms
from erp.users import *
from erp.misc.util import *
from erp.department.models import *
from erp.users import models
from django.contrib.auth.models import Group,Permission
import sha,random,datetime
from erp.users.forms import *
from django.core.mail import send_mail,EmailMessage,SMTPConnection


#author :vivek kumar bagaria
#description in short
#we take the details from the user
#store it in user profile
#please check if i have used the "user class" properly
                          
#here it needs small changes with department id                                                                          
# ***to do****                 
#create groups for user coord and cores and add them into the groups
def register_user(request):
    
    # groups are created here
    if Group.objects.count() == 0:
        
        #for cores
        is_core =Group(name='core')
        is_core.save()
        user_core=Permission.objects.get(name='is_core')
        is_core.permissions.add(user_core)

        #for coords
        is_coord=Group(name='coord')
        is_coord.save()
        user_coord=Permission.objects.get(name='is_coord')
        is_coord.permissions.add(user_coord)
        
        #for vols
        is_vol  =Group(name='vol')
        is_vol.save()
        user_vol=Permission.objects.get(name='is_vol')
        is_vol.permissions.add(user_vol)
        
    if request.method=='POST':
        data=request.POST.copy()
        form = AddUserForm (data)
        
        if form.is_valid():
            if form.cleaned_data["password"] == form.cleaned_data["password_again"]:
                user = User.objects.create_user(
                    username = form.cleaned_data['username'],
                    email = form.cleaned_data['email'],
                    password = form.cleaned_data['password'],
		    

                    )        
		department=form.cleaned_data['department']
		Dept=Department.objects.get(Dept_Name=department)
                user.is_active=True #took from userportal
                user.save()
		user_profile = userprofile(
                        user = user,
			department_id=Dept.id,
                        emailid=form.cleaned_data['email'],
			
		     )
                user.save()



                

                try:
                    user_profile.save()
		    print "done da.."
                    #other thing required to be wriiten
                    return render_to_response('home/registered.html' , locals() ,context_instance= global_context(request))

                except:
                    print "not successful" #just for debugging purpose
                    raise	
        
           

    else:
        form = AddUserForm ()
        
    return render_to_response('users/register.html' , locals() ,context_instance= global_context(request))




#author: vivek
def invite_page(request):
    inviteform=invite_coord()

    return render_to_response('users/invite_coord.html',locals(),context_instance = global_context(request))






# author: vivek
def invite(request):
    inviteform=invite_coord()
    message=""
    if request.method=="POST":
        data=request.POST.copy()
        form=invite_coord(data)
        if form.is_valid():
            name=form.cleaned_data['name']
            emailid=form.cleaned_data['email_id']
            #please change this
            invite_details=invitation(
            core=User.objects.get(username="me"),# obviously needs a change
            invitee=name,
            emailid=emailid,
            time=datetime.datetime.now(),
            )
            try:
                invite_details.save()
                message ="coord invited "
                #activation key#
                salt = sha.new(str(random.random())).hexdigest()[:5]
                activation_key = sha.new(salt+name).hexdigest()
                coordname=name
                #sending mail here
                mail_template=get_template('users/emailcoords.html')
                body=mail_template.render(Context({coordname:coordname,
                                                   'SITE_URL':settings.SITE_URL,
                                                   'activationkey':activation_key
                                                   }))
                send_mail('Invitaiton from the core to join ERP',body,'noreplay@shaastra.org',emailid,fail_silently=False)
                message="mail sent"
                print "peace"
            except :
                message="mail could not be sent "
                print "problem da.."

    return render_to_response('tasks/create_task.html',locals(),context_instance = global_context(request))

                                          
                    
            
def contact_details(request):
    print "here "
    profile=userprofile.objects.get(user=request.user)
    
    profileform=personal_details(initial={'name':profile.name,
                                          'nick':profile.nickname,
                                          'roomnumber' :profile.roomnumber ,
                                          'hostel':profile.hostel,
                                          'summerstay':profile.summerstay,
                                          'chennai_number':profile.chennai_number,
                                          'summer_number':profile.summer_number,
                                          'emailid':profile.emailid,
                                          'rollno':profile.user,})

    return render_to_response('users/contact_details.html',locals(),context_instance = global_context(request))
    
  
def update(request):
    print "came in the function"
    name=request.session.get('username','nobody')
    print name
    if request.method=="POST":
        data=request.POST.copy()
        form=personal_details(data)
        if form.is_valid():
            print "hurray"
            profile=userprofile.objects.get(user=request.user)
            profile.nickname=form.cleaned_data['nick']
            profile.name=form.cleaned_data['name']
            profile.roomnumber=form.cleaned_data['roomnumber']
            profile.hostel=form.cleaned_data['hostel']
            profile.summerstay=form.cleaned_data['summerstay']
            profile.chennai_number=form.cleaned_data['chennai_number']
            profile.summer_number=form.cleaned_data['summer_number']
                        
            
            
            profile.save()
            
            profileform=personal_details(initial={'name':profile.name,
                                          'nick':profile.nickname,
                                          'roomnumber' :profile.roomnumber ,
                                          'hostel':profile.hostel,
                                          'summerstay':profile.summerstay,
                                          'chennai_number':profile.chennai_number,
                                          'summer_number':profile.summer_number,
                                          'emailid':profile.emailid,
                                          'rollno':profile.user,})
            
        else:
            profileform=personal_details()

    return render_to_response('users/contact_details.html',locals(),context_instance = global_context(request))
            
        
        
    
