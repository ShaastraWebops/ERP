from django.shortcuts import render_to_response, redirect
#from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.template.loader import get_template
from django.template.context import Context, RequestContext
from django.utils.translation import ugettext as _
from django.core.mail import send_mail,EmailMessage,SMTPConnection
from django.contrib.sessions.models import Session
from erp.home.forms import *
from erp.misc.helper import *
import models,forms
from erp.misc.util import *
# Take care of session variable
from erp.home import models
from erp.users.models import *

def home(request):
    redirected = session_get (request,"from_url")
    access_denied = (request, "access_denied")
    logged_in = session_get (request, "logged_in")
    already_logged = session_get (request, "already_logged")
    return render_to_response('home/home.html', locals(), context_instance= global_context(request))

# <> So Users once logged in, can't access the login page
def login(request):
    if request.user.is_authenticated():
        return redirect ('erp.tasks.views.display_portal', owner_name = request.user.username)
    redirected = request.session.get ("from_url", False)
    just_registered = session_get(request, "just_registered")
    form = forms.UserLoginForm ()
    print "just before if"
    if request.method == 'POST':
        print "in the login , it is post"
        data = request.POST.copy()
    
        form =forms. UserLoginForm (data)
        if form.is_valid():
                user = auth.authenticate(username=form.cleaned_data['username'],
                                         password=form.cleaned_data["password"])
                if user is not None and user.is_active == True:
                    auth.login (request, user)
        
        
                    # WHERE THE HELL IS THIS USED?
                    # url = session_get(request, "from_url")
                    # # Handle redirection
                    # if not url:
                    #     url = "%s/home/"%settings.SITE_URL
        
        
                    request.session['logged_in'] = True
        
                    try:
                        response.set_cookie('logged_out', 0)
                    except:
                        pass

                    if redirected:
                        return redirect (redirected)
                    else:
                        return redirect ('erp.tasks.views.display_portal',
                                         owner_name = user.username)
                else:
                    invalid_login_message="Incorrect username or password. Please try again."
                    print "the user has not logged in -invalid "
                    request.session['invalid_login'] = True
                    print request.path
                    return render_to_response('home/login.html', locals(), context_instance= global_context(request))
                    #return HttpResponseRedirect (request.path)
                    invalid_login =session_get(request, "invalid_login")
                    form = forms.UserLoginForm ()
        else:
            pass
    
    return render_to_response('home/login.html', locals(), context_instance= global_context(request))
    
def logout (request):
    print 'HERE'
    if request.user.is_authenticated():
        auth.logout (request)
        response= redirect ('erp.home.views.login')

        try:
          #  response.set_cookie('unb_User',"")
            response.set_cookie('logged_out', 1)
        except:
            pass
        return response
    return render_to_response('home/login.html', locals(), context_instance= global_context(request))

def forgot_password(request):

    forgot_form=forgot_password_form()
    if request.method == 'POST':
        data = request.POST.copy()
        form =forms. forgot_password_form (data)
        print "checking details for forgot_password"
        if form.is_valid():
            try:
                print form.cleaned_data['email_id'] , "is the username entered"
                user=User.objects.get(username=form.cleaned_data['username'] , email=form.cleaned_data['email_id'])
                print "the user with this name and emailid exists "
                invalid_login_message ="such and such a username exists dotn worry"
                # here to send email to the coord
                coordname=form.cleaned_data['username']
                hyperlink=settings.SITE_URL+"/testonly_ignore"
                mail_header="follow the link and change your password , once you log in"
                email_id=form.cleaned_data['email_id']
                mail=[email_id,]
                invalid_message="if it stops here there is some problem in getting mail template"
                mail_template=get_template("home/forgot_password_mail.html")
                invalid_login_message ="We have tried to mail you but then there is some internal problem ,get_template works"
                body=mail_template.render(Context({'coordname':coordname,
                                                   'SITE_URL':hyperlink,
                                                   'new_password':"password"
                                                   }))
                invalid_message="body ban gayi , send_mail mai gadbad"
                send_mail(mail_header,body,'noreply@shaastra.org',mail,fail_silently=False)
                #message=mail_coord(hyperlink ,mail_header ,coordname ,  "home/forgot_password_mail.html",mail)
                invalid_login_message ="We have mailed you your new password if any further problem contact the webops dept"                
                return render_to_response('home/login.html', locals(), context_instance= global_context(request))
        
            except:
                pass #invalid_login_message= "details given by u dont match , please for further clarification contact webops  dept"
    else:
        print "problem in forgot_password_view"
    form = forms.UserLoginForm ()    
    return render_to_response('home/forgot_password.html', locals(), context_instance= global_context(request))
