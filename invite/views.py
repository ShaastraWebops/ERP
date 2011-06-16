# Create your views here.
def login (request):

    redirected = request.session.get ("from_url", False)
    registered = session_get (request, "registered")
    form = forms.UserLoginForm ()

    if request.method == 'POST':
        data = request.POST.copy()
        if request.POST.get('from_unb',False):
	  if request.POST.get('from_url',False):
	    request.session['from_url']='http://www.shaastra.org/2010/helpdesk/forum.php?req=setuser'
	    print request.session['from_url']
        else:
	  form = forms.UserLoginForm (data)
	  if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data["password"])
            if user is not None and user.is_active == True:
                auth.login (request, user)

                url = session_get(request, "from_url")
                # Handle redirection
                if not url:
                    url = "%s/home/"%settings.SITE_URL
                
                request.session['logged_in'] = True

# This was added to get additional hospi information towards the end
#                if user.get_profile().profile_not_set :
#                    url = "%s/profile/"%settings.SITE_URL

                request.session['unb_User'] = user.username
                response= HttpResponseRedirect (url)
                try:
                    response.set_cookie("unb_User", request.session['unb_User'])
                    response.set_cookie('logged_out', 0)
                except:
                    pass
                return response
            else:
                request.session['invalid_login'] = True
                return HttpResponseRedirect (request.path)
    else: 
        invalid_login = session_get(request, "invalid_login")
        form = forms.UserLoginForm ()

    return render_to_response('home/login.html', locals(), context_instance= global_context(request)) 

