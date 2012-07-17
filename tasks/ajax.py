from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from models import *
from forms import *
from erp.dashboard.models import *
from erp.dashboard.forms import *

@dajaxice_register
def shout(request):
    dajax=Dajax()
    shout_form=shout_box_form()
    shouts=shout_box.objects.all()
    shout_form=shout_box_form(request.POST)            
    if shout_form.is_valid():
        new_shout = shout_form.save (commit = False)
        new_shout.user=request.user
        new_shout.nickname=page_owner.get_profile ().nickname
        new_shout.timestamp=datetime.datetime.now()
        new_shout.save ()
        shout_form = shout_box_form ()
        
    #call function to render html or return Json
    
 
        
    
