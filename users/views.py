# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.template.loader import get_template
from django.template.context import Context, RequestContext
import datetime
from forms import * 
from django import forms
from erp.users import *
from erp.misc.util import *
import MySQLdb
from erp.department import *
from erp.users import models
from django.contrib.auth.models import Group



#author :vivek kumar bagaria
#description in short
#we take the details from the user
#store it in user profile
#please check if i have used the "user class" properly
                          
                                                                         
# ***to do****                 
#create groups for user coord and cores and add them into the groups
def register_user(request):
    
    # groups are created here
    if Group.objects.count()=0:
                 
        
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
        form = forms.AddUserForm (data)
        
        if form.is_valid():
            if form.cleaned_data["password"] == form.cleaned_data["password_again"]:
                user = models.User.objects.create_user(
                    username = form.cleaned_data['username'],
                    email = form.cleaned_data['email'],
                    password = form.cleaned_data['password']

                    )        
                user.is_active=True #took from userportal
                user.save()
		user_profile = models.userprofile(
                        user = user,
                        first_name = form.cleaned_data['first_name'].lower(),
                        last_name = form.cleaned_data['last_name'].lower(),
                        mobile_number = form.cleaned_data['mobile_number'],
                        department=Department.objects.get(Dept_Name=form.cleaned_data['department']),                        
			
		     )
                user.save()



                

                try:
                    user_profile.save()
                    #other thing required to be wriiten
                    return render_to_response('home/registered.html' , locals() ,context_instance= global_context(request))

                except:
		    user.save()
                    print "not successful" #just for debugging purpose
                    raise	
        
           

    else:
        form = forms.AddUserForm ()
        
    return render_to_response('users/register.html' , locals() ,context_instance= global_context(request))


