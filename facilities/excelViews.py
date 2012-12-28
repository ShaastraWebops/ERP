from datetime import date
from xlwt import Workbook, easyxf
from django.http import HttpResponse, HttpResponseForbidden
from erp.facilities.models import *
from erp.department.models import Department
from erp.facilities.models import DATE_CHOICES,VENUE_CHOICES
from django.db.models import Q
 

style_body = easyxf('font: height 200, name Arial ;''borders: left thick, right thick, top thin, bottom thin;')
style_head = easyxf('font: height 280, name Arial, bold True;''borders: left thick, right thick, top thick, bottom thick;')
style_end = easyxf('borders: top thick;')
   
def test_excel(request):
    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % 'TestExcel.xls'

    book = Workbook()
    sheet1 = book.add_sheet('A Date')
    sheet1.row(1).height=int(255*1.5)
    sheet1.col(1).width=int(0.87/0.18*255*3.2)
    sheet1.write(1,1,date(2009,3,18),easyxf(
        'font: height 300, name Arial;'
        'borders: left thick, right thick, top thick, bottom thick;'
        'pattern: pattern solid, fore_colour red;',
        num_format_str='YYYY-MM-DD'
        ))
    book.save(response)
    return response

def generate_round_excel(request,round_id):

    rounder=EventRound.objects.get(id=round_id)
    items=FacilitiesObject.objects.filter(event_round=rounder)
    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s Facilities Requirements .xls' % (str(rounder.department)+'-'+rounder.name)
                                                                    
    book = Workbook()
    sheet1 = book.add_sheet('Round Requirements')
    sheet1.row(1).height=int(255*1.5)
    sheet1.col(1).width=int(0.87/0.18*255*3.2)
    '''sheet1.write(1,1,date(2009,3,18),easyxf(
        'font: height 300, name Arial;'
        'borders: left thick, right thick, top thick, bottom thick;'
        'pattern: pattern solid, fore_colour red;',
        num_format_str='YYYY-MM-DD'
        ))'''
    #sheet1.col(0).hidden=True
    sheet1.row(1).height=int(255*3)
    sheet1.write(1,1,str(rounder.department) + " - " + str(rounder.name),
                        easyxf('font: height 440, name Arial, bold True;'
                                # 'borders: left thick, right thick, top thick, bottom thick;'
                                # 'pattern: pattern solid, fore_colour white;'
                                ))
    sheet1.row(3).height=int(255*2)
    sheet1.write(3,1,"Venue :- " + rounder.venue,easyxf('font: height 360, name Arial, bold True;'))
    sheet1.row(4).height=int(255*1.5)
    sheet1.write(4,1,"Start :- " + str(rounder.start_hour) + ":"+str(rounder.start_minute)+"  "+rounder.start_date,
                                                 easyxf('font: height 300, name Arial, bold True;'))           
    
    sheet1.row(5).height=int(255*1.5)    
    sheet1.write(5,1,"End :- " + str(rounder.end_hour) + ":"+str(rounder.end_minute)+"  "+rounder.end_date,
                                                 easyxf('font: height 300, name Arial, bold True;')) 

    sheet1.row(7).height=int(255*1.35)
    sheet1.col(1).width=int(0.87/0.18*255*8.5)  
    sheet1.write(7,1,'Item name',style_head) 
    sheet1.col(2).width=int(0.87/0.18*255*3.5) 
    sheet1.write(7,2,'Required',style_head) 
    sheet1.col(3).width=int(0.87/0.18*255*5) 
    sheet1.write(7,3,'To be Recovered',style_head) 
    
    '''for i in range(7):
        sheet1.write(i+8,1,"Tryer to go",style_body)
        sheet1.write(i+8,2,"Go"+str(i),style_body)
        sheet1.write(i+8,3,"lalala"+str(i),style_body)
    '''
    i=0
    for item in items:
        sheet1.write(i+8,1,item.name.name,style_body)
        sheet1.write(i+8,2,str(item.quantity),style_body)
        sheet1.write(i+8,3,str(int(item.quantity*item.rec_fac)),style_body)
        i=i+1
    sheet1.write(i+8,1,'',style_end)
    sheet1.write(i+8,2,'',style_end)
    sheet1.write(i+8,3,'',style_end)

    book.save(response)
    return response

def generate_event_excel(request,event_id):
    department=Department.objects.get(id=event_id)
    rounds=EventRound.objects.filter(department=department)
    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s Overall Facilities Requirements .xls' % (str(department))
                                                                    
    book = Workbook()
    i=0
    sheet = [ 0 for j in range(len(rounds)) ]
    for rounder in rounds:    
        items=FacilitiesObject.objects.filter(event_round=rounder)
        sheet[i] = book.add_sheet(str(rounder.number) +" - " + rounder.name + ' Requirements')
        sheet[i].row(1).height=int(255*1.5)
        sheet[i].col(1).width=int(0.87/0.18*255*3.2)
        '''sheet[i].write(1,1,date(2009,3,18),easyxf(
            'font: height 300, name Arial;'
            'borders: left thick, right thick, top thick, bottom thick;'
            'pattern: pattern solid, fore_colour red;',
            num_format_str='YYYY-MM-DD'
            ))'''
        #sheet[i].col(0).hidden=True
        sheet[i].row(1).height=int(255*3)
        sheet[i].write(1,1,str(rounder.department) + " - " + str(rounder.name),
                            easyxf('font: height 440, name Arial, bold True;'
                                    # 'borders: left thick, right thick, top thick, bottom thick;'
                                    # 'pattern: pattern solid, fore_colour white;'
                                    ))
        sheet[i].row(3).height=int(255*2)
        sheet[i].write(3,1,"Venue :- " + rounder.venue,easyxf('font: height 360, name Arial, bold True;'))
        sheet[i].row(4).height=int(255*1.5)
        sheet[i].write(4,1,"Start :- " + str(rounder.start_hour) + ":"+str(rounder.start_minute)+"  "+rounder.start_date,
                                                     easyxf('font: height 300, name Arial, bold True;'))           
        
        sheet[i].row(5).height=int(255*1.5)    
        sheet[i].write(5,1,"End :- " + str(rounder.end_hour) + ":"+str(rounder.end_minute)+"  "+rounder.end_date,
                                                     easyxf('font: height 300, name Arial, bold True;')) 

        sheet[i].row(7).height=int(255*1.35)
        sheet[i].col(1).width=int(0.87/0.18*255*8.5)  
        sheet[i].write(7,1,'Item name',style_head) 
        sheet[i].col(2).width=int(0.87/0.18*255*3.5) 
        sheet[i].write(7,2,'Required',style_head) 
        sheet[i].col(3).width=int(0.87/0.18*255*5) 
        sheet[i].write(7,3,'To be Recovered',style_head) 
        
        '''for i in range(7):
            sheet[i].write(i+8,1,"Tryer to go",style_body)
            sheet[i].write(i+8,2,"Go"+str(i),style_body)
            sheet[i].write(i+8,3,"lalala"+str(i),style_body)
        '''
        j=0
        for item in items:
            sheet[i].write(j+8,1,item.name.name,style_body)
            sheet[i].write(j+8,2,str(item.quantity),style_body)
            sheet[i].write(j+8,3,str(int(item.quantity*item.rec_fac)),style_body)
            j=j+1
        sheet[i].write(j+8,1,'',style_end)
        sheet[i].write(j+8,2,'',style_end)
        sheet[i].write(j+8,3,'',style_end)
        i=i+1

    book.save(response)
    return response


def optimize_excel(request,day_number):
    date_str = DATE_CHOICES[(int(day_number)-5)][0]
    date_str_1,date_str_2 = date_str.split(',')
    date_str_name = date_str_1+date_str_2
    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s Optimized Facilities.xls' %date_str_name

    book = Workbook()
    sheet1 = book.add_sheet('Required before 1PM')
    sheet2 = book.add_sheet('Recovered before 1PM')
    sheet3 = book.add_sheet('Required after 1PM')
    sheet4 = book.add_sheet('Recovered after 1PM')
    sheet1.row(1).height=int(255*3)
    sheet1.write(1,1,"Venue Specific Item Requirements before 1 PM",
                        easyxf('font: height 440, name Arial, bold True;'
                                # 'borders: left thick, right thick, top thick, bottom thick;'
                                # 'pattern: pattern solid, fore_colour white;'
                                ))
    sheet2.row(1).height=int(255*3)
    sheet2.write(1,1,"Venue Specific Item Recoveries before 1 PM",
                        easyxf('font: height 440, name Arial, bold True;'
                                # 'borders: left thick, right thick, top thick, bottom thick;'
                                # 'pattern: pattern solid, fore_colour white;'
                                ))    
    sheet3.write(1,1,"Venue Specific Item Recoveries before 1 PM",
                        easyxf('font: height 440, name Arial, bold True;'
                                # 'borders: left thick, right thick, top thick, bottom thick;'
                                # 'pattern: pattern solid, fore_colour white;'
                                ))
    sheet3.row(1).height=int(255*3)
    sheet4.write(1,1,"Venue Specific Item Recoveries before 1 PM",
                        easyxf('font: height 440, name Arial, bold True;'
                                # 'borders: left thick, right thick, top thick, bottom thick;'
                                # 'pattern: pattern solid, fore_colour white;'
                                ))
    sheet4.row(1).height=int(255*3)
    i=1
    sheet1.row(4).height=int(255*2)
    sheet2.row(4).height=int(255*2)
    sheet3.row(4).height=int(255*2)
    sheet4.row(4).height=int(255*2)
    for ven in VENUE_CHOICES:
        venue=ven[0]
        sheet1.col(i+1).width=int(0.87/0.18*255*3.5) 
        sheet1.write(4,i+1,venue,style_head)
        sheet2.col(i+1).width=int(0.87/0.18*255*3.5) 
        sheet2.write(4,i+1,venue,style_head)
        sheet3.col(i+1).width=int(0.87/0.18*255*3.5) 
        sheet3.write(4,i+1,venue,style_head)
        sheet4.col(i+1).width=int(0.87/0.18*255*3.5) 
        sheet4.write(4,i+1,venue,style_head)
        i=i+1
    items = ItemList.objects.all()
    sheet1.col(1).width=int(0.87/0.18*255*10) 
    sheet2.col(1).width=int(0.87/0.18*255*10)
    sheet3.col(1).width=int(0.87/0.18*255*10) 
    sheet4.col(1).width=int(0.87/0.18*255*10)  
    i=0
    for item in items:
        sheet1.row(i+5).height=int(255*2.5)
        sheet1.write(i+5,1,item.name,style_head)
        sheet2.row(i+5).height=int(255*2.5)
        sheet2.write(i+5,1,item.name,style_head)
        sheet3.row(i+5).height=int(255*2.5)
        sheet3.write(i+5,1,item.name,style_head)
        sheet4.row(i+5).height=int(255*2.5)
        sheet4.write(i+5,1,item.name,style_head)
        i=i+1
    for i in (2,3,9,12,15):
        sheet1.col(i+1).width=int(0.87/0.18*255*5.3)
        sheet2.col(i+1).width=int(0.87/0.18*255*5.3)
        sheet3.col(i+1).width=int(0.87/0.18*255*5.3)
        sheet4.col(i+1).width=int(0.87/0.18*255*5.3)
    
    a=[ [ 0 for i in range(len(VENUE_CHOICES)) ] for j in range(len(items))]
    b=[ [ 0 for i in range(len(VENUE_CHOICES)) ] for j in range(len(items))]
    c=[ [ 0 for i in range(len(VENUE_CHOICES)) ] for j in range(len(items))]
    d=[ [ 0 for i in range(len(VENUE_CHOICES)) ] for j in range(len(items))]
    i=0
    for ven in VENUE_CHOICES:
        venue=ven[0]
        print venue
        all_rounds = EventRound.objects.filter(start_date=date_str,venue=venue)
        alter_rounds = all_rounds.filter(start_hour__lte=13)
        first_rounds = alter_rounds.filter(end_hour__lte=13)
        second_rounds = alter_rounds.filter(end_hour__gt=13)
        third_rounds = all_rounds.filter(start_hour__gt=13)
        print first_rounds
        for rounder in first_rounds:
            objs=rounder.facilitiesobject_set.exclude(quantity=0)
            for obj in objs:
                print "foo"
                number=obj.name.id-1
               
                a[number][i]=a[number][i]+obj.quantity
                b[number][i]=b[number][i]+int(obj.quantity*obj.rec_fac)
        for rounder in second_rounds:
            objs=rounder.facilitiesobject_set.exclude(quantity=0)
            for obj in objs:
                print "bar"
                number=obj.name.id-1
                
                a[number][i]=a[number][i]+obj.quantity
                d[number][i]=d[number][i]+int(obj.quantity*obj.rec_fac)
        for rounder in third_rounds:
            objs=rounder.facilitiesobject_set.exclude(quantity=0)
            for obj in objs:
                print "lot"
                number=obj.name.id-1
                
                c[number][i]=c[number][i]+obj.quantity
                d[number][i]=d[number][i]+int(obj.quantity*obj.rec_fac)
        i=i+1
    i=0
    j=0
    for item in items:
        j=0
        for ven in VENUE_CHOICES:
            sheet1.write(i+5,j+2,a[i][j],style_body)
            sheet2.write(i+5,j+2,b[i][j],style_body) 
            sheet3.write(i+5,j+2,c[i][j],style_body)
            sheet4.write(i+5,j+2,d[i][j],style_body)      
            j=j+1
        i=i+1              
    print a
    book.save(response)
    return response

    '''=0
    for ven in VENUE_CHOICES:
        i=0
        venue=ven[0]
        rounds = EventRound.objects.filter(start_date=date_str,venue=venue)
        for rounder in rounds:
            items = rounder.facilitiesobject_set.all()
            print items
        for rounder in rounds:
            sheet1.write(i+5,j+2,rounder.name,style_body)
            i=i+1
        j=j+1'''
    '''i=0
    j=0
    a=[ [ 0 for i in range(len(VENUE_CHOICES)) ] for j in range(len(items))]
    b=[ [ 0 for i in range(len(VENUE_CHOICES)) ] for j in range(len(items))]
    c=[ [ 0 for i in range(len(VENUE_CHOICES)) ] for j in range(len(items))]
    d=[ [ 0 for i in range(len(VENUE_CHOICES)) ] for j in range(len(items))]
    for item in items:        
        j=0
        print item.name
        for ven in VENUE_CHOICES:
            rounds = EventRound.objects.filter(start_date=date_str,venue=venue)
            venue=ven[0]
            print venue
            all_obj = FacilitiesObject.objects.filter(name=item)
            for obj in all_obj:
                rounder=obj.event_round
                print rounder.name
                if rounder in rounds:
                    if rounder.start_hour<13:
                        a[i][j]=a[i][j]+obj.quantity 
                        if rounder.end_hour<13:
                            b[i][j]=b[i][j]+obj.quantity*obj.rec_fac
                        else:
                            d[i][j]=d[i][j]+obj.quantity*obj.rec_fac
                    else:
                        c[i][j]=c[i][j]+obj.quantity
                        d[i][j]=d[i][j]+obj.quantity*obj.rec_fac
            sheet1.write(i+5,j+2,a[i][j],style_body)
            sheet2.write(i+5,j+2,b[i][j],style_body)
            j=j+1
        i=i+1'''
    
    '''for item in items:        
        j=0
        print item.name'''

    


    
