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
            for form in barcodeformset:
                barcodes=form.save()
                if not isinstance(barcodes, BarcodeMap):
                    if not barcodes:
                        return render_to_response('prizes/hospiregistration.html', locals(), context_instance = global_context(request))    
                else:
                    form=BarcodeForm()
    barcodeformset =BarcodeFormset(queryset=BarcodeMap.objects.none())    
    return render_to_response('prizes/hospiregistration.html', locals(), context_instance = global_context(request))    


def prize_assign(request,owner_name=None,event_name=None):
    if not event_name:
        events=Department.objects.filter(is_event=True)
        page_name = "Assign Prizes"
        return render_to_response('prizes/eventchoices.html',locals(),context_instance=global_context(request))
    WinnerFormset = modelformset_factory(Prize, form=PrizeForm, extra=3)
    eventname=Department.objects.filter(id=event_name)
    #if error is reached, a winnerList will still be displayed. formset will have the unsubmitted data.
    winnerList = Prize.objects.filter(event=eventname)
    if request.method == 'POST':
        winnerformset = WinnerFormset (request.POST)
        if winnerformset.is_valid ():
            for winnerform in winnerformset:
                if winnerform.has_changed():
                    barcode = winnerform.cleaned_data.get('barcode')
                    winner=winnerform.save(commit=False)
                    if barcode:
                        try:
                            participant=BarcodeMap.objects.get(barcode=barcode).shaastra_id
                            winner.participant=participant
                        except:
                            #incorrect barcode
                            error = barcode
                            return render_to_response('prizes/prize_table.html',locals(),context_instance=global_context(request))
                    winner.event=eventname
                    winner.user=request.user
                    winner.save()
    winnerList = Prize.objects.filter(event=eventname)         #updated list                               
    winnerformset = WinnerFormset(queryset=Prize.objects.none())
    for form in winnerformset:
        form.fields['participant'].queryset=Participant.objects.filter(events=eventname)
    return render_to_response('prizes/prize_table.html',locals(),context_instance=global_context(request))

def cheque_assign(request,owner_name=None,event_name=None):
    if not event_name:
        events=Department.objects.filter(is_event=True)
        page_name = "Assign Cheques"
        return render_to_response('prizes/eventchoices.html',locals(),context_instance=global_context(request))
    WinnerFormset = modelformset_factory(Prize, fields=('participant','cheque'),form=ChequeForm, extra=10)
    eventname=Department.objects.filter(id=event_name)
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

def fillEventDetails(request, owner_name=None, event_name=None):
    try:
        eventname=Department.objects.get(id=event_name)
    except:
        events=Department.objects.filter(is_event=True)
        page_name = "Event Details"
        return render_to_response('prizes/eventchoices.html',locals(),context_instance=global_context(request))
    if request.method == 'POST':
        try:
            eventdetails = EventDetails.objects.get(event=eventname)
            eventdetailsform = EventDetailsForm(request.POST, instance=eventdetails)
        except:    
            eventdetailsform = EventDetailsForm(request.POST)
        if eventdetailsform.is_valid():
            eventdetails = eventdetailsform.save(commit=False)
            eventdetails.event = eventname
            eventdetails.save()
            success = True
    try:
        eventdetails = EventDetails.objects.get(event=eventname)
        eventdetailsform = EventDetailsForm(instance=eventdetails, event=eventname)
    except:
        eventdetailsform = EventDetailsForm(event=eventname)
    return render_to_response('prizes/event_details.html', locals(), context_instance = global_context(request))    


def registerparticipants(request, owner_name=None, event_name=None):
    try:
        eventname = Department.objects.get(id=event_name)
        eventdetails = EventDetails.objects.get(event=eventname)
    except:
        return redirect('erp.prizes.views.fillEventDetails', owner_name = request.user)
    BarcodeMapFormset = modelformset_factory(BarcodeMap, form=EventRegnForm, extra=eventdetails.team_nos)
    #if error is reached, a participantList will still be displayed. formset will have the unsubmitted data.    
    participantList = Participant.objects.filter(events=eventname)
    if request.method == 'POST':
        barcodemapformset = BarcodeMapFormset (request.POST)
        if barcodemapformset.is_valid ():
            for forms in barcodemapformset:
                teamname = form.cleaned_data.get('team_id')
                try:
                    team = Team.objects.get(name=teamname)
                except:
                    team = Team(name=teamname)
                    team.save()
                team.events.add(eventname)
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
    participantList = Participant.objects.filter(events=eventname)      #updated list
    teamList = Team.objects.filter(events=eventname)
    barcodemapformset = BarcodeMapFormset(queryset=BarcodeMap.objects.filter(shaastra_id__events=eventname))
    idList = [str(elem.shaastra_id) for elem in Participant.objects.all()] 
    return render_to_response('prizes/registerparticipants.html', locals(), context_instance = global_context(request))
