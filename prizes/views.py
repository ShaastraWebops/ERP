# Create your views here.

from django.shortcuts import render_to_response, redirect, HttpResponseRedirect
from django.template.context import Context, RequestContext
from erp.misc.util import *
from erp.prizes.models import *
from erp.prizes.forms import *
from erp.department.models import *
from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import login_required
import csv
import itertools
import datetime
import re
# Function to handle an uploaded file.
from erp.prizes.file import handle_uploaded_file
from erp.prizes.eventParticipationPDF import generateEventParticipationPDF
from django.contrib.auth.decorators import login_required

@login_required
def event_participation_pdf(request,owner_name=None, event_id=None):
    if not event_id:
        events=Department.objects.filter(is_event=True)
        return render_to_response("prizes/generate_pdf.html", locals(), context_instance=global_context(request))
    event_id = int(event_id)
    return generateEventParticipationPDF(event_id)


@login_required
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

@login_required
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
            print "saved", new.shaastra_id, new.barcode
        else:
            if form.is_valid():
                participant=Participant.objects.filter(shaastra_id=form.cleaned_data['shaastra_id'])
                print "participant", participant
                try:
                    college = str(participant[0].college)
                except:
                    college=''
                    detail_error = True
                try:
                    college_roll = str(participant[0].college_roll)
                except:
                    college_roll=''
                    detail_error = True
                try:
                    name = str(participant[0].name)
                    print name
                except:
                    name=''
                    detail_error = True
                try:
                    mobile_number = str(participant[0].mobile_number)
                except:
                    mobile_number=''
                    detail_error = True
                if len(participant)==0 or len(form.cleaned_data['barcode'])!=5:
                    not_exists=True
                    return render_to_response('prizes/display_profile.html',locals(),context_instance=global_context(request))
                else:
                    values={'barcode':form.cleaned_data['barcode'],'college':college,'college_roll':college_roll,'name':name,'mobile_number':mobile_number}
                    participantform=ParticipantForm(instance=participant[0],initial=values)
    
    idList = [str(elem.shaastra_id) for elem in Participant.objects.all()]                
    return render_to_response('prizes/display_profile.html',locals(),context_instance=global_context(request))
        
@login_required
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
                    result = re.compile(r'^[^\W\d_]{2}\d{2}[^\W\d_]{1}\d{3}$')
                    if row[1]:
                        if result.match(row[1]):
                            shid = row[1].lower()
                            try:
                                new = Participant.objects.filter(shaastra_id=shid)[0]
                            except:
                                new = Participant(name='InstiJunta', gender='F', age=18, college='IIT Madras', college_roll=shid, shaastra_id=shid)
                                new.save()
                            new.events.add(event)
                            shaastra_ids.append(shid)
                        else:
                            try:
                                new=Participant.objects.filter(shaastra_id=row[1])[0]
                                new.events.add(event)
                                shaastra_ids.append(row[1])
                            except:
                                shaastra_ids_errors.append(row[1])
    else:
        form = DocumentForm() 
    return render_to_response('prizes/uploads.html',locals(),context_instance=global_context(request))

@login_required
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

@login_required
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

@login_required
def choosePosition(request,owner_name=None,event_name=None):
    try:
        eventname=Department.objects.get(id=event_name)
        eventdetails = EventDetails.objects.get(event = eventname)
    except:
        return redirect('erp.prizes.views.fillEventDetails', owner_name = request.user)
    positions= [i+1 for i in range(eventdetails.finalist_nos)]
    finalist_details = Prize.objects.filter(event=eventname)
    if str(request.user.get_profile().department) == 'Finance':
        PPM = True
    return render_to_response('prizes/choose_position.html',locals(),context_instance=global_context(request))    

@login_required
def fillEventDetails(request, owner_name=None, event_name=None):
    try:
        eventname=Department.objects.get(id=event_name)
    except:
        events=list(Department.objects.filter(is_event=True))
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

@login_required
def registerparticipants(request, owner_name=None, event_name=None):
    try:
        eventname = Department.objects.get(id=event_name)
    except:
        events=Department.objects.filter(is_event=True)
        page_name = "Event Registration"
        return render_to_response('prizes/eventchoices.html',locals(),context_instance=global_context(request))
    BarcodeMapFormset = modelformset_factory(BarcodeMap, form=EventRegnForm, extra=25)
    uploadform=DocumentForm()   
    #if error is reached, a participantList will still be displayed. formset will have the unsubmitted data.    
    participantList = Participant.objects.filter(events=eventname)
    if request.method == 'POST':
        barcodemapformset = BarcodeMapFormset (request.POST)
        if barcodemapformset.is_valid ():
            barcodemaps = barcodemapformset.save(commit=False)
            for barcodemap in barcodemaps:
                if not isinstance(barcodemap, BarcodeMap):
                    if not barcodemap:
                        return render_to_response('prizes/registerparticipants.html', locals(), context_instance = global_context(request))
                        
                try:
                    participant = BarcodeMap.objects.get(barcode=barcodemap.barcode).shaastra_id
                except:
                    #if a barcode isn't filled in, or a mapping doesn't exist.
                    try:
                        participant = Participant.objects.get(shaastra_id=barcodemap.shaastra_id)
                    except:
                        if barcodemap.shaastra_id:
                            # Shaastra ID was incorrect => Might be insti junta or incorrect
                            result = re.match(r'^[^\W\d_]{2}\d{2}[^\W\d_]{1}\d{3}$', barcodemap.shaastra_id)
                            if result:
                                participant = Participant(name='InstiJunta', gender='F', age=18, college='IIT Madras', college_roll=barcodemap.shaastra_id, shaastra_id=barcodemap.shaastra_id)
                                participant.save()
                            else:
                                error = barcodemap.shaastra_id
                                return render_to_response('prizes/registerparticipants.html', locals(), context_instance = global_context(request))
                                
                        else:
                            #The shaastra ID wasn't filled => incorrect barcode.
                            error = barcodemap.barcode
                            return render_to_response('prizes/registerparticipants.html', locals(), context_instance = global_context(request))
                participant.events.add(eventname)
    participantList = Participant.objects.filter(events=eventname)      #updated list
    barcodemapformset = BarcodeMapFormset(queryset=BarcodeMap.objects.none())
    idList = [str(elem.shaastra_id) for elem in Participant.objects.all()] 
    return render_to_response('prizes/registerparticipants.html', locals(), context_instance = global_context(request))

@login_required
def setFinal(request, owner_name=None, event_name=None):
    try:
        eventname=Department.objects.get(id=event_name)
        timestamp = str(datetime.datetime.now())
        f = open('prizes/finalevents.txt', 'a+')
        for line in f:
            if (event_name == line.strip('\n').split(',')[0]):
                f.close()
                return redirect('erp.prizes.views.fillEventDetails', owner_name = request.user)
        f.write(event_name + ',' + eventname.Dept_Name + ',' + timestamp +'\n')
        f.close()
    except:
        pass
    return redirect('erp.prizes.views.fillEventDetails', owner_name = request.user)

@login_required
def viewFinal(request, owner_name=None):
    try:
        eventdata = []
        f = open("prizes/finalevents.txt", 'r')
        for line in f:
            temp = line.strip('\n').split(',')
            eventdata.append(temp)
        f.close()       
    except:
        pass
    return render_to_response('prizes/viewfinal.html', locals(), context_instance = global_context(request))
