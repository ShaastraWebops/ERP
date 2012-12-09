from datetime import date
from xlwt import Workbook, easyxf
from django.http import HttpResponse, HttpResponseForbidden
from erp.facilities.models import *
from erp.department.models import Department
    



def test_excel(request):
    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % 'TestExcel.xls'

    book = Workbook()
    sheet1 = book.add_sheet1('A Date')
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
    style_body = easyxf('font: height 200, name Arial ;''borders: left thick, right thick, top thin, bottom thin;')
    style_head = easyxf('font: height 280, name Arial, bold True;''borders: left thick, right thick, top thick, bottom thick;')
    style_end = easyxf('borders: top thick;')
    sheet1.row(7).height=int(255*1.35)
    sheet1.col(1).width=int(0.87/0.18*255*8.5)  
    sheet1.write(7,1,'Item name',style_head) 
    sheet1.col(2).width=int(0.87/0.18*255*3.5) 
    sheet1.write(7,2,'Required',style_head) 
    sheet1.col(3).width=int(0.87/0.18*255*3.5) 
    sheet1.write(7,3,'Recovered',style_head) 
    
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

    
