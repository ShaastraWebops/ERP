from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from models import *
from forms import *
from erp.dashboard.models import *
from erp.misc.helper import *
from erp.misc.util import *
from erp.tasks.render import *
import datetime


@dajaxice_register
def shout(request, shout=None):
    print request.user, 'just shouted', shout, 'at', datetime.datetime.now()
    dajax=Dajax()
    if shout is not None:
        new_shout=add_shout(request, shout)
    markup=render_markup(request)
    dajax.assign('#shoutbox','innerHTML', markup)
    print markup
    return dajax.json()
          
    
def add_shout(request,shout):
    new_shout=shout_box()   
    new_shout.user = request.user
    new_shout.nickname = request.user.get_profile().nickname
    new_shout.comments = shout
    new_shout.timestamp = datetime.datetime.now()
    new_shout.save()
    print 'saved', new_shout 
        
    
