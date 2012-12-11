from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax

@dajaxice_register
def submit(request,name=None,position=None,details=None):
    dajax=Dajax()
    print name, position, details    
    return dajax.json()
