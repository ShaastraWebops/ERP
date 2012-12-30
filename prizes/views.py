# Create your views here.

from django.shortcuts import render_to_response, redirect, HttpResponseRedirect
from django.template.context import Context, RequestContext
from erp.misc.util import *
from erp.prizes.models import *
from erp.prizes.forms import *
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


def prize_details(request,owner_name=None):
    WinnerFormset = modelformset_factory(Prize, fields=('participant','cheque'), form=PrizeForm, extra=10)
    eventname=request.user.userprofile_set.all()[0].department
    if request.method == 'POST':
        winnerformset = WinnerFormset (request.POST)
        if winnerformset.is_valid ():
            winners = winnerformset.save(commit=False)
            for winner in winners:
                try:    
                    exists=Prize.objects.get(participant=winner.participant,event=eventname)
                    exists.user=request.user
                    exists.cheque=winner.cheque
                    exists.save()
                except:
                    winner.user=request.user
                    winner.event=eventname
                    winner.save()
    winnerList = Prize.objects.filter(event=eventname)
    winnerformset = WinnerFormset(queryset=Prize.objects.none()) 
    return render_to_response('prizes/assign_table.html',locals(),context_instance=global_context(request))

def prize_assign(request,owner_name=None):
    WinnerFormset = modelformset_factory(Prize, exclude=('event','user','cheque'), form=PrizeForm, extra=3)
    eventname=request.user.userprofile_set.all()[0].department
    if request.method == 'POST':
        winnerformset = WinnerFormset (request.POST)
        if winnerformset.is_valid ():
            winners = winnerformset.save(commit=False)
            for winner in winners:
                try:    
                    exists=Prize.objects.get(participant=winner.participant,event=eventname)
                    exists.user=request.user
                    exists.details=winner.details
                    exists.position=winner.position
                    exists.save()
                except:
                    winner.user=request.user
                    winner.event=eventname
                    winner.save()
    winnerList = Prize.objects.filter(event=eventname)
    winnerformset = WinnerFormset(queryset=Prize.objects.none()) 
    return render_to_response('prizes/prize_table.html',locals(),context_instance=global_context(request))
    
    
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
