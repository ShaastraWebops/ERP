# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.template.loader import get_template
from django.template.context import Context, RequestContext
import datetime
from forms import UserProfileForm
from models import *
from django.newforms import form_for_model


#author :vivek kumar bagaria
#description in short
#we take the details from the user
#store it in user profile
#please check if i have used the "user class" properly
                          
                                                                         
# ***to do****                 
#create groups for user coord and cores and add them into the groups
def create_core(request):
    success_message="you have not been registered"
    if request.method=='POST':
        data=request.POST.copy()
        form=forms.UserProfileForm(data)
        if form.is_valid():
            if form.cleaned_data["password"] == form.cleaned_data["password_again"]:
                user = models.User.objects.create_user(username = form.cleaned_data['username'],email = form.cleaned_data['email'],password = form.cleaned_data['password'])
                user.is_staff=True #took from userportal
                user.save()
                user_profile=models.Userprofile(user = user,
                                                first_name = form.cleaned_data['first_name'],
                                                last_name  = form.cleaned_data['last_name'],
                                                department = form.cleaned_data['department'],
                                                mobile_number= form.cleaned_data['mobile_number'],
                                                department_monitor = form.cleaned_data['department_monitor']
                                                )
                try:
                    user_profile.save()
                    #other thing required to be wriiten
                    success_message="you have not been registered"
                    
                except:
                    user.delete();
                    user_profile.delete()

    else:
        form=forms.UserProfile()

    
    context     = Context(request ,{ 'user':user,})
    return render_to_response('users/signin_core.html ' , locals() ,context_instance=context)


