# Create your views here.

from django.shortcuts import render_to_response, redirect, HttpResponseRedirect
from django.template.context import Context, RequestContext
from erp.misc.util import *
from erp.prizes.models import *
from django.forms.models import modelformset_factory

# TODO
"""def assign_barcode(request,owner_name=None):
    ParticipantFormset = modelformset_factory(Participant, fields=('barcode',), extra=25)
    if request.method == 'POST':
        participantformset = ParticipantFormset (request.POST)
        if participantformset.is_valid ():
            registered_participants = participantformset.save(commit=False)
            for registered_participant in registered_participants:
                participant = Participant.objects.get(barcode=registered_participant.barcode)
                participant.events.add(request.user.userprofile_set.all()[0].department);
    participantList = Participant.objects.filter(events=request.user.userprofile_set.all()[0].department)
    participantformset = ParticipantFormset(queryset=Participant.objects.none())    
    return render_to_response('prizes/registerparticipants.html', locals(), context_instance = global_context(request))    
"""

def prize_details(request,owner_name=None):
    WinnerFormset = modelformset_factory(Prize,fields=('participant','cheque'), extra=10)
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
    WinnerFormset = modelformset_factory(Prize,exclude=('event','user','cheque'), extra=3)
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
    ParticipantFormset = modelformset_factory(Participant, fields=('barcode',), extra=25)
    if request.method == 'POST':
        participantformset = ParticipantFormset (request.POST)
        if participantformset.is_valid ():
            registered_participants = participantformset.save(commit=False)
            for registered_participant in registered_participants:
                participant = Participant.objects.get(barcode=registered_participant.barcode)
                participant.events.add(request.user.userprofile_set.all()[0].department);
    participantList = Participant.objects.filter(events=request.user.userprofile_set.all()[0].department)
    participantformset = ParticipantFormset(queryset=Participant.objects.none())    
    return render_to_response('prizes/registerparticipants.html', locals(), context_instance = global_context(request))
