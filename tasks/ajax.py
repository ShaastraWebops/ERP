from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from models import *
from forms import *
from erp.dashboard.models import *
from erp.misc.helper import *
from erp.misc.util import *
from erp.tasks.render import *
from django.template import Template, Context
from django.template.loader import get_template
import datetime


@dajaxice_register
def shout(request, shout=None):
    print request.user, 'just shouted', shout, 'at', datetime.datetime.now()
    dajax=Dajax()
    if shout is not None:
        new_shout=add_shout(request, shout)
    shouts = shout_box.objects.all()
    template = get_template('tasks/shoutbox.html')
    html = template.render(Context({'shouts':shouts}))
    dajax.assign('#markup','innerHTML', html)
    dajax.assign('#shout_button','innerHTML', 'Shout!')
    return dajax.json()
          
    
def add_shout(request,shout):
    new_shout=shout_box()   
    new_shout.user = request.user
    new_shout.nickname = request.user.get_profile().nickname
    new_shout.comments = shout
    new_shout.timestamp = datetime.datetime.now()
    new_shout.save()
    print 'saved', new_shout 
        
    
