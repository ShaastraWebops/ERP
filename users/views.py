# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.template.loader import get_template
from django.template.context import Context, RequestContext
import datetime
from forms import UserProfileForm ,UserLoginForm
from models import *
#from django.NewForms import form_for_model
from django import forms


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
        form=UserProfileForm(data)
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
        context     = Context(request ,locals())
        return render_to_response('tasks/main.html' , locals() ,context_instance=context)
   

    else:

        
        form = UserProfileForm()

    
    context     = Context(request ,locals())
    return render_to_response('users/signin_core.html' , locals() ,context_instance=context)

#This is the login,logout, already logged in , home views.
def home (request):
    #we do not need these variable now
    redirected=request.session.get(request,"from_url")
    access_denied = request.session.get (request, "access_denied")
    logged_in = request.session.get(request, "logged_in")
    already_logged = request.session.get(request, "already_logged")
    key = request.session.session_key
    form = UserProfileForm()
    return render_to_response('home/home.html', locals(), context_instance= Context(request)) 

def edited (request):

    print dir(request.session)
    print request.session.keys()
    response = render_to_response('home/home.html', locals(), context_instance= Context(request)) 
    return response

def registered (request):

    redirected=request.session.get(request,"from_url")
    access_denied = request.session.get(request, "access_denied")
    logged_in = request.session.get (request, "logged_in")
    already_logged = request.session.get(request, "already_logged")
    return render_to_response('home/registered.html', locals(), context_instance= Context(request)) 




#@no_login
def login (request):

    redirected = request.session.get ("from_url", False)
    registered = request.session.get(request, "registered")
    #form = forms.UserLoginForm ()

    if request.method == 'POST':
        data = request.POST.copy()

        form = UserLoginForm (data)
	if form.is_valid():
            form = forms.UserLoginForm (data)
            if form.is_valid():
                user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data["password"])
                if user is not None and user.is_active == True:
                    auth.login (request, user)

                    url = request.session.get(request, "from_url")
                    # Handle redirection
                    if not url:
                        url = "%s/home/"%settings.SITE_URL

                    request.session['logged_in'] = True
                    response= HttpResponseRedirect (url)
                    try:
                        response.set_cookie('logged_out', 0)
                    except:
                        pass
                    return response
            else:
                request.session['invalid_login'] = True
                return HttpResponseRedirect (request.path)
        else: 
            invalid_login =request.session.get(request, "invalid_login")
            form = UserLoginForm ()
    else:
        pass
    return render_to_response('home/login_2.html', locals(), context_instance= Context(request)) 


def logout (request):
    if request.user.is_authenticated():
        auth.logout (request)
        url = "%s/home/"%settings.SITE_URL
        response= HttpResponseRedirect (url)
        try:
            response.set_cookie('logged_out', 1)
        except:
            pass
        return response

    return HttpResponseRedirect ('/home/')

