from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.template.loader import get_template
from django.template.context import Context, RequestContext
from django.utils.translation import ugettext as _
from django.core.mail import send_mail,EmailMessage,SMTPConnection
from django.contrib.sessions.models import Session
# Create your views here.
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

def login(request):
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
                    return HttpResponseRedirect (redirected)
                else:

                    return HttpResponseRedirect("%s/%s/"
                                                %(settings.SITE_URL, user.username))

            else:
                request.session['invalid_login'] = True
                return HttpResponseRedirect (request.path)
                invalid_login =session_get(request, "invalid_login")
                form = forms.UserLoginForm ()
    else:
        print "not a post da"
        pass

    return render_to_response('home/login.html', locals(), context_instance= global_context(request))

def logout (request):
    if request.user.is_authenticated():
        auth.logout (request)
        url = "%s/home/"%settings.SITE_URL
        response= HttpResponseRedirect (url)
        try:
          #  response.set_cookie('unb_User',"")
            response.set_cookie('logged_out', 1)
        except:
            pass
        return response
    return render_to_response('home/home.html', locals(), context_instance= global_context(request))


def test (request):
    return render_to_response('home.html', locals(), context_instance= global_context(request))
