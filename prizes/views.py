# Create your views here.

from django.shortcuts import render_to_response, redirect, HttpResponseRedirect
from django.template.context import Context, RequestContext
from erp.misc.util import *
from erp.prizes.models import *
from erp.prizes.forms import *
from erp.department.models import *
from django.forms.models import modelformset_factory

def assign_barcode(request,owner_name=None):
    BarcodeFormset = modelformset_factory(BarcodeMap, form=BarcodeForm, extra=10)
    if request.method == 'POST':
        barcodeformset = BarcodeFormset (request.POST)
        if barcodeformset.is_valid ():
            # We don't need to check if the object already exists and overwrite
            # because I was told that a single participant can have multiple barcodes
            barcodes=barcodeformset.save()
    barcodeformset =BarcodeFormset(queryset=BarcodeMap.objects.none())    
    return render_to_response('prizes/hospiregistration.html', locals(), context_instance = global_context(request))    


def prize_assign(request,owner_name=None):
    WinnerFormset = modelformset_factory(Prize, form=PrizeForm, extra=3)
    eventname=request.user.userprofile_set.all()[0].department
    if request.method == 'POST':
        winnerformset = WinnerFormset (request.POST)
        if winnerformset.is_valid ():
            for winnerform in winnerformset:
                if winnerform.has_changed():
                    barcode = winnerform.cleaned_data.get('barcode')
                    winner=winnerform.save(commit=False)
                    if barcode:
                        participant=BarcodeMap.objects.get(barcode=barcode).shaastra_id
                        winner.participant=participant
                    winner.event=eventname
                    winner.user=request.user
                    winner.save()           
    winnerList = Prize.objects.filter(event=eventname)
    winnerformset = WinnerFormset(queryset=Prize.objects.none()) 
    return render_to_response('prizes/prize_table.html',locals(),context_instance=global_context(request))

def cheque_assign(request,owner_name=None,event_name=None):
    if not event_name:
        events=Department.objects.all()#.filter(is_event=True)
        return render_to_response('prizes/cheque_event.html',locals(),context_instance=global_context(request))
    WinnerFormset = modelformset_factory(Prize, fields=('participant','cheque'),form=ChequeForm, extra=10)
    eventname=Department.objects.filter(id=event_name)
    print eventname
    if request.method == 'POST':
        winnerformset = WinnerFormset (request.POST)
        if winnerformset.is_valid ():
            winners = winnerformset.save(commit=False)
            for winner in winners:
                try:
                    obj=Prize.objects.get(event=eventname, participant=winner.participant)
                    obj.cheque=winner.cheque
                    obj.save()
                except:
                    pass
    winnerList = Prize.objects.filter(event=eventname)
    winnerformset = WinnerFormset(queryset=Prize.objects.none())
    for form in winnerformset:
        form.fields['participant'].queryset=Participant.objects.filter(prize__event=eventname)
    return render_to_response('prizes/cheque_table.html',locals(),context_instance=global_context(request))

    
def registerparticipants(request, owner_name=None):
    BarcodeMapFormset = modelformset_factory(BarcodeMap, form=BarcodeForm, extra=25)
    eventname = request.user.userprofile_set.all()[0].department
    if request.method == 'POST':
        barcodemapformset = BarcodeMapFormset (request.POST)
        if barcodemapformset.is_valid ():
            barcodemaps = barcodemapformset.save(commit=False)
            for barcodemap in barcodemaps:
                try:
                    participant = BarcodeMap.objects.get(barcode=barcodemap.barcode).shaastra_id
                except:
                    #if a barcode isn't filled in, or a mapping doesn't exist.
                    try:
                        participant = Participant.objects.get(shaastra_id=barcodemap.shaastra_id)
                    except:
                        #The shaastra ID wasn't filled => incorrect barcode.
                        error = barcodemap.barcode
                        return render_to_response('prizes/registerparticipants.html', locals(), context_instance = global_context(request))
                participant.events.add(eventname)
    participantList = Participant.objects.filter(events=eventname)
    barcodemapformset = BarcodeMapFormset(queryset=BarcodeMap.objects.none())    
    return render_to_response('prizes/registerparticipants.html', locals(), context_instance = global_context(request))
