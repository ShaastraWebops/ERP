from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from erp.prizes.models import Prize
from django.template import Template, Context
from django.template.loader import get_template

@dajaxice_register
def submit(request,name=None,position=None,details=None):
    dajax=Dajax()
    new=Prize(Name=name,Position=position,details=details,user=request.user,event=request.user.get_profile ().department)
    if not new.cheque:
        new.cheque='<Not Assigned>'
    new.save()    
    prizes=Prize.objects.all().order_by('-pk')
    template=get_template('prizes/prize_table.html')
    markup=template.render(Context({'prizes':prizes}))
    dajax.assign('#prize_table','innerHTML',markup)
    return dajax.json()
    
@dajaxice_register
def assign(request,id=None,serial=None):
    dajax=Dajax()
    print "coming here", id, serial
    p=Prize.objects.filter(pk=id)[0]
    p.cheque=serial
    p.save()
    prizes=Prize.objects.all()
    template=get_template('prizes/assign_table.html')
    markup=template.render(Context({'prizes':prizes}))
    dajax.assign('#assign_table','innerHTML',markup)
    return dajax.json()
