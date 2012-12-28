from django.template import *
from django.http import *
from django.shortcuts import *
from django.template import *
import csv

from erp.facilities.models import *
from erp.department.models import Department
from erp.misc.helper import *
from erp.misc.util import *

def create_items(request):
    facilities_tab = True
    print "Kafka"
    ga_items=['Projector-HD','Projector-Normal','Projector Screen-Standard','Table-Iron','Table-Stainless Steel','Table-Wooden',
              'Tablecloth','Chairs-Normal','Chairs-Judges','Bouquet','White Board','Water Bottles (500ml)',
              'Barricades','Hockey Cones','Pedestal Fans','Extension Cords','Spike Buster- 5 Amp','Spike Buster- 15 Amp']  
    materials_items=['Pen','Buzzer','Stopwatch','Whistle','Pencil','Eraser','Sharpner','Marker-Permanent',
                           'Marker-Whiteboard(Black)','Marker-Whiteboard (Red)','Marker-Whiteboard (Blue)','Marker-Whiteboard(Green)',
                           'Marker-OHP','Tape-Cello Tape','Tape-Duct Tape','Tape-Double Sided Tape','Tape-Electrical Insulation Tape',
                           'Measuring Tape','Penknife','Scissors','A4 Sheets','Chalk','Stapler','Stapler Pins','Notepad',
                           'Folders-Stick File','Folder-Box Folder','Rubber Bands','Stamp pad','OHP Sheets'] 
    pa_items = ['Mikes-Normal','Mikes-Cordless','Mikes-Collar','Speaker-Normal','Speaker-Amplifier']
    water_items=['Water Bottles','Bubble Cans']
    dept = Department.objects.get(id=57)
    j=1
    string=[]
    with open('facilities/recfac.csv', 'rb') as csvfile:
        read = csv.reader(csvfile, delimiter=',')
        print '\n\n'   
        for row in read:
            string.append(row)
    print string
    print float(string[10][1])
    for i in ga_items:
        try :
            ItemList.objects.get(name=str(i))
            print "kl"
        except:
            print "as"
            a=ItemList()
            a.name=str(i)
            print a.name
            a.rec_fac=float(string[j][1])
            print string[j][1]
            print a.rec_fac
            a.department=dept
            a.target="GA"
            j=j+1
            a.save()
    for i in pa_items:
        try :
            ItemList.objects.get(name=str(i))
            print "kl"
        except:
            print "as"
            a=ItemList()
            a.name=str(i)
            print a.name
            a.rec_fac=float(string[j][1])
            print float(string[j][1])
            print a.rec_fac
            a.department=dept
            a.target="PA"
            j=j+1
            a.save()
    for i in water_items:
        try :
            ItemList.objects.get(name=str(i))
            print "kl"
        except:
            print "as"
            a=ItemList()
            a.name=str(i)
            print a.name
            a.rec_fac=float(string[j][1])
            print float(string[j][1])
            print a.rec_fac
            a.department=dept
            a.target="Water"
            j=j+1
            a.save()

    for i in materials_items:
        try :
            ItemList.objects.get(name=str(i))
            print "kl"
        except:
            print "as"
            a=ItemList()
            a.name=str(i)
            print a.name
            a.rec_fac=float(string[j][1])
            print float(string[j][1])
            print a.rec_fac
            a.department=dept
            a.target="Materials"
            j=j+1
            a.save()
    equipment_items = ['Computers-Laptop','Computers-Desktop']
    dept = Department.objects.get(id=59)
    for i in equipment_items:
        try :
            ItemList.objects.get(name=str(i))
            print "kl"
        except:
            print "as"
            a=ItemList()
            a.name=str(i)
            print a.name
            a.rec_fac=float(string[j][1])
            print float(string[j][1])
            print a.rec_fac
            a.department=dept
            a.target="Equipment"
            j=j+1
            a.save()
    other_items = ['Special-CD/DVD','Special-Weighing Machine','Special-Hacksaw Blade','Special-Chalkpowder (No. of Boxes)',
                   'Special-Rope,Nylon (Length m)','Special-Rope-Jute (Length m)',
                   'Special-Fire Extinguishers','Special-First Aid Box','Special-Screwdriver/Tester',
                   'Special-Router-Normal','Special-Router-Wifi']
    dept = Department.objects.get(id=58)
    for i in other_items:
        try :
            ItemList.objects.get(name=str(i))
            print "why"
        except:
            print "you"
            a=ItemList()
            a.name=str(i)
            print a.name
            a.rec_fac=float(string[j][1])
            print float(string[j][1])
            print a.rec_fac
            a.department=dept
            a.target="Special"
            j=j+1
            a.save()
    itemlist=ItemList.objects.all()
    return render_to_response('facilities/test.html',locals(),context_instance=global_context(request))  

def create_rounds(request):
    departments = Department.objects.filter(is_event=True)
    itemlist=ItemList.objects.all()
    new_list =[]
    for department in departments:
    
        try :
            print "c"
            exist = EventRound.objects.get(department=department,number=1)
            print "x"
            allround = EventRound.objects.filter(department=department).order_by('-number')
            print allround[0].number
            e=EventRound()
            e.number = allround[0].number + 1
            e.department=department
            e.name = "Round " + str(e.number)
            e.save()
            new_list.append(e)
            print "f"
        except:
            print "b"
            e=EventRound()
            e.number=1
            e.department=department 
            e.name = "Round " + str(e.number)
            new_list.append(e)
            e.save()
    print "Round Generation Complete "
    for rounder in new_list:
        print rounder.department
        print "\n\n"
        for item in itemlist:
            fac_obj=FacilitiesObject(department=rounder.department,event_round=rounder,name=item)
            fac_obj.save()
            print item.name
    '''for rounder in EventRound.objects.filter(id=1):
        print rounder.department
        print "\n\n"
        for item in itemlist:
            fac_obj=FacilitiesObject(department=rounder.department,event_round=rounder,name=item)
            fac_obj.save()
            print item.name'''
    return render_to_response('facilities/test.html',locals(),context_instance=global_context(request))  

def use_data(request): 
    string =[]
    with open('facilities/dryrun.csv', 'rb') as csvfile:
        read = csv.reader(csvfile, delimiter=',')
        print '\n\n'   
        for row in read:
            string.append(row)
    string_mod=string[3:]
    items=ItemList.objects.all()
    for row in string_mod:
        try:        
            department=Department.objects.get(Dept_Name=row[0])
        
        except:
            print "Does Not Exist"
            continue
        print row[0]
        e=EventRound()
        e.description = "Round - " + row[1] +" ; Venue - " + row[2]
        try :
            print "c"
            exist = EventRound.objects.get(department=department,number=1)
            print "x"
            allround = EventRound.objects.filter(department=department).order_by('-number')
            print allround[0].number
            e.number = allround[0].number + 1
            e.department=department
            if row[1] is not '':
                e.name = "Round " + str(e.number)
            else:
                e.name = row[1]
            e.save()
            print "f"
        except:
            print "b"
            e.number=1
            e.department=department 
            if row[1] is not '':
                e.name = "Round " + str(e.number)
            else:
                e.name = row[1]
            e.save()
        i=3
        for item in items:
            if row[i] is not '':
                number = int(row[i])
            else:
                number=0
            a=FacilitiesObject(department=department,event_round=e,name=item,quantity=number,rec_fac=item.rec_fac)
            a.save()
            i=i+1
    
    
    
    return render_to_response('facilities/test.html',locals(),context_instance=global_context(request))



    
 
