# Create your views here.

from django.shortcuts import render_to_response, redirect, HttpResponseRedirect
from django.template.context import Context, RequestContext
from erp.misc.util import *
from erp.prizes.models import *
from erp.prizes.forms import *
from erp.department.models import *
from django.forms.models import modelformset_factory
import csv
# Function to handle an uploaded file.
from erp.prizes.file import handle_uploaded_file

def display_portal(request,owner_name=None,shaastra_id=None):
    if shaastra_id:
        try:
            participant=Participant.objects.filter(shaastra_id=shaastra_id)[0]
            try:
                values={'barcode':BarcodeMap.objects.filter(shaastra_id=participant)[0].barcode}
                form=ParticipantForm(instance=participant,initial=values)
            except:
                form=ParticipantForm(instance=participant)
            return render_to_response('prizes/display_prize.html',locals(),context_instance=global_context(request))   
        except:
            not_exists=True
            return render_to_response('prizes/display_prize.html',locals(),context_instance=global_context(request))   
    else:
        HttpResponseRedirect('/')


def assign_barcode_new(request,owner_name=None,shaastra_id=None):
    form=DetailForm()
    if request.method == 'POST':
        form=DetailForm(request.POST)
        part=ParticipantForm(request.POST)
        if part.is_valid():
            participant=Participant.objects.filter(shaastra_id=part.cleaned_data['shaastra_id'])[0]
            new=BarcodeMap()
            new.shaastra_id=participant
            new.barcode=part.cleaned_data['barcode']
            new.save()
            form=DetailForm()
            saved=True
        else:
            if form.is_valid():
                participant=Participant.objects.filter(shaastra_id=form.cleaned_data['shaastra_id'])
                if len(participant)==0 or len(form.cleaned_data['barcode'])!=5:
                    not_exists=True
                    return render_to_response('prizes/display_profile.html',locals(),context_instance=global_context(request))
                else:
                    values={'barcode':form.cleaned_data['barcode']}
                    participantform=ParticipantForm(instance=participant[0],initial=values)
                    
    return render_to_response('prizes/display_profile.html',locals(),context_instance=global_context(request))
        
def upload_file(request,owner_name=None,event_name=None):
    if not event_name:
        events=Department.objects.filter(is_event=True)
        return render_to_response('prizes/registration_event.html',locals(),context_instance=global_context(request))
    event=Department.objects.filter(id=event_name)[0]
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            valid = True
            shaastra_ids=[]
            barcodes=[]
            shaastra_ids_errors=[]
            barcodes_errors=[]
            f = request.FILES['docfile']
            data = [row for row in csv.reader(f.read().splitlines())]
            for row in data:
                print row
                if len(row[0])==5:
                    try:
                        new=BarcodeMap.objects.filter(barcode=row[0])[0].shaastra_id
                        new.events.add(event) 
                        new.save()
                        barcodes.append(row[0])
                    except:
                        barcodes_errors.append(row[0])
                else:
                    try:
                        new=Participant.objects.filter(shaastra_id=row[1])[0]
                        new.events.add(event)
                        new.save()
                        shaastra_ids.append(row[1])                                  
                    except:
                        shaastra_ids_errors.append(row[1])
    else:
        form = DocumentForm() 
    return render_to_response('prizes/uploads.html',locals(),context_instance=global_context(request))

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
                    print form.fields
    barcodeformset =BarcodeFormset(queryset=BarcodeMap.objects.none())    
    return render_to_response('prizes/hospiregistration.html', locals(), context_instance = global_context(request))    

def prize_assign(request, owner_name=None, event_name=None, position=None):
    try:
        eventname=Department.objects.get(id=event_name)
        eventdetails = EventDetails.objects.get(event = eventname)
    except:
        return redirect('erp.prizes.views.fillEventDetails', owner_name = request.user, event_name=event_name)
    if not position or (int(position)-1) not in range(eventdetails.finalist_nos):
        return redirect('erp.prizes.views.choosePosition', owner_name = request.user, event_name=event_name)
    #if error is reached, a winnerList will still be displayed. formset will have the unsubmitted data.
    if request.method == 'POST':
        try:
            prize = Prize.objects.get(event=eventname, position=position)
            prizeform = PrizeForm(request.POST, instance=prize)
        except:
            prizeform = PrizeForm(request.POST)
        if  prizeform.is_valid():
            prize = prizeform.save(commit=False)
            if not isinstance(prize, Prize):
                if not prize:
                    return render_to_response('prizes/prize_table.html', locals(), context_instance = global_context(request))            
            prize.event = eventname
            prize.user=request.user
            prize.position = position
            prize.save()
            success = True
     
    try:
        prize = Prize.objects.get(event=eventname, position=position)         #updated list                              
        prizeform = PrizeForm(instance=prize, eventdetails=eventdetails, position=position)
    except:
        prizeform = PrizeForm(eventdetails=eventdetails, position=position)
    idList = [str(elem.shaastra_id) for elem in Participant.objects.filter(events=eventname)]    
    return render_to_response('prizes/prize_table.html',locals(),context_instance=global_context(request))

def choosePosition(request,owner_name=None,event_name=None):
    try:
        eventname=Department.objects.get(id=event_name)
        eventdetails = EventDetails.objects.get(event = eventname)
    except:
        return redirect('erp.prizes.views.fillEventDetails', owner_name = request.user)
    positions= [i+1 for i in range(eventdetails.finalist_nos)]
    finalist_details = Prize.objects.filter(event=eventname)
    if str(request.user.get_profile().department) == 'QMS':
        QMS = True
    return render_to_response('prizes/choose_position.html',locals(),context_instance=global_context(request))    

def fillEventDetails(request, owner_name=None, event_name=None):
    try:
        eventname=Department.objects.get(id=event_name)
    except:
        events=Department.objects.filter(is_event=True)
        page_name = "Event Details"
        return render_to_response('prizes/eventchoices.html',locals(),context_instance=global_context(request))
    if str(request.user.get_profile().department) == 'Hospitality':
        return redirect('erp.prizes.views.choosePosition', owner_name = request.user, event_name=event_name)
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
    except:
        events=Department.objects.filter(is_event=True)
        page_name = "Event Registration"
        return render_to_response('prizes/eventchoices.html',locals(),context_instance=global_context(request))
    BarcodeMapFormset = modelformset_factory(BarcodeMap, form=BarcodeForm, extra=25)
    uploadform=DocumentForm()   
    #if error is reached, a participantList will still be displayed. formset will have the unsubmitted data.    
    participantList = Participant.objects.filter(events=eventname)
    if request.method == 'POST':
        barcodemapformset = BarcodeMapFormset (request.POST)
        if barcodemapformset.is_valid ():
            #for forms in barcodemapformset:
            #    teamname = form.cleaned_data.get('team_id')
            #    try:
            #        team = Team.objects.get(name=teamname)
            #    except:
            #        team = Team(name=teamname)
            #        team.save()
            #   team.events.add(eventname)
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
    #teamList = Team.objects.filter(events=eventname)
    barcodemapformset = BarcodeMapFormset(queryset=BarcodeMap.objects.none())
    idList = [str(elem.shaastra_id) for elem in Participant.objects.all()] 
    return render_to_response('prizes/registerparticipants.html', locals(), context_instance = global_context(request))
    
"""
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
"""

"""
def prize_assign(request,owner_name=None,event_name=None):
    try:
        eventname=Department.objects.get(id=event_name)
    except:
        events=Department.objects.filter(is_event=True)
        page_name = "Assign Prizes"
        return render_to_response('prizes/eventchoices.html',locals(),context_instance=global_context(request))
        
    WinnerFormset = modelformset_factory(Prize, form=PrizeForm, extra=3)
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
"""
