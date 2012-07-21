try:

    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import textwrap
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm,inch
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.platypus import Table,Paragraph,SimpleDocTemplate,TableStyle
from reportlab.platypus.flowables import PageBreak,Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus.frames import Frame
from reportlab.rl_config import defaultPageSize
from django.http import HttpResponse
from erp.users.models import userprofile
from erp.tasks.models import Task,SubTask
from erp.department.models import Department    
from erp.misc.helper import is_core,is_coord

PAGE_HEIGHT, PAGE_WIDTH=A4

FRAME_BORDER=1.5*cm

small_spacer_height=0.5*cm
small_spacer = Spacer(width=0,height=small_spacer_height)
spacer_height=cm
spacer = Spacer(width=0, height=spacer_height)
big_spacer_height=1.5*cm
big_spacer = Spacer(width=0, height=big_spacer_height)

class MyDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename, **kw)
        template = PageTemplate('normal', [Frame(FRAME_BORDER,FRAME_BORDER,21*cm-2*FRAME_BORDER,29.7*cm-2*FRAME_BORDER, id='F1')])
        self.addPageTemplates(template)
    def afterFlowable(self, flowable):
        "Registers TOC entries."
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == 'Heading1':
                self.notify('TOCEntry', (0, text, self.page))
            elif style == 'Heading2':
                self.notify('TOCEntry', (1, text, self.page))
            

centered_caption = PS(name = 'centered',  
                      fontSize = 24,  
                      leading = 16,  
                      alignment = 1,  
                      spaceAfter = 20) 
centered = PS(name = 'centered',  
              fontSize = 20,  
              leading = 16,  
              alignment = 1,  
              spaceAfter = 20) 
h1 = PS(name = 'Heading1',
       fontSize = 18,
       leading = 16,
       leftIndent=-15)
h2 = PS(name = 'Heading2',
       fontSize = 14,
       leading = 14
       
       )
standard = PS(name = 'Usual Text',
       fontSize = 12,
       leading = 14,
       )

def DateString(date):
    return "%s/%s/%s" %(date.day,date.month,date.year)

def FillToHalf(length):
    s=''
    i=0
    while i<55-length:
        s=s+'&nbsp;'
        i=i+1
    return s


def ShowTask(request,elements,position_on_page,sno,task):
    '''When cores get something from another deprtment it's a task. When they give something to another department, it's
       a subtask. Nomenclature is pretty bad'''
    styles=getSampleStyleSheet()["Normal"]  
    coord_subtask = 0 
    if is_core(request.user):
        if task.creator.get_profile().department == request.user.get_profile().department:  
            '''If your department made the task , creator is assigner and the department is the assignee, as the model has no field for
           assignee, just his/her department.Technically this is a sub-task as the user gave the task to another department. Hence we 
           need to fetch the SubTask given to this task''' 
        
            assigner_string = str(task.creator.get_profile())
            assignee_string = ''
        elif request.user.get_profile().department == task.department :
            ''' In this case it is a task as the user belongs to the recieving department. So assigner is the creator - the guy from that
                department and this core's department is the assignee'''
            assigner_string = str(task.creator.get_profile())
            assignee_string = task.department.Dept_Name
        else : 
            ''' This is when the core tries to find the SubTasks given to his coords. Assigner is creator and a list of coords is the
                assignee'''
            coord_subtask = 1
            assigner_string = str(task.creator.get_profile())
            assignee_list = task.coords 
    
    else : 
            ''' This is when the core tries to find the SubTasks given to his coords. Assigner is creator and a list of coords is the 
                assignee'''
            coord_subtask = 1
            assigner_string = str(task.creator.get_profile())
            assignee_list = task.coords         

    aW = PAGE_WIDTH-2*FRAME_BORDER                                 # available width and height
    aH = position_on_page+FRAME_BORDER
    P = Paragraph(task.feedback,standard)
    w,h = P.wrap(aW, aH)
    if coord_subtask == 0 :                                                               # find required space  
        h= h+h2.fontSize+4*small_spacer_height+3*standard.fontSize 
    else :
        h= h+h2.fontSize+(3+len(assignee_list))*small_spacer_height+(len(assignee_list)+2)*standard.fontSize 
    

    nH=h+spacer_height
    if nH<=aH:
        
        elements.append(Paragraph('<b>%d. %s </b>' % (sno,task.subject),h2))
        elements.append(small_spacer)
        #elements.append(P)
        elements.append(Paragraph('<b>Deadline</b> : %s ' %DateString(task.deadline),standard))   
        elements.append(small_spacer)
        
        elements.append(Paragraph('<b>Creation Date</b> : %s %s<b>Completion Date</b> : %s' 
                                    %(DateString(task.creation_date),FillToHalf(len(DateString(task.creation_date))+16)
                                      ,DateString(task.completion_date)),standard)) 
        elements.append(small_spacer)               
        if coord_subtask == 0 :
            elements.append(Paragraph('<b>Creator</b> : %s %s<b>Assigned To</b> : %s' 
                                    % (assigner_string , FillToHalf(len(str(task.creator))+6) ,
                                        assignee_string),standard))
            elements.append(small_spacer)
        else : 
            elements.append(Paragraph('<b>Creator</b> : %s %s<b>Assigned To</b> : %s' 
                                    % (assigner_string , FillToHalf(len(str(task.creator))+6) ,
                                        str(assignee_list[0])),standard))
            elements.append(small_spacer)
            i=1
            while i<len(assignee_list):
                    elements.append(Paragraph('%s' 
                                    % (assigner_string , FillToHalf(0) ,
                                        str(assignee_list[i])),standard))
                    elements.append(small_spacer)
                  
        elements.append(Paragraph('<b>Feedback : </b>',standard))
        elements.append(P)
        elements.append(spacer)  
        position_on_page = position_on_page - nH                  # reduce the available height   
        print 3    
    elif nH>aH and h<=aH:        
        print 4     
        
        elements.append(Paragraph('<b>%d. %s </b>' % (sno,task.subject),h2))  
        
        elements.append(small_spacer)     
        #elements.append(P)
        elements.append(Paragraph('<b>Deadline</b> : %s ' %DateString(task.deadline),standard))
        elements.append(small_spacer)
        elements.append(Paragraph('<b>Creation Date</b> : %s %s<b>Completion Date</b> : %s' 
                                    %(DateString(task.creation_date),FillToHalf(len(DateString(task.creation_date))+16)
                                      ,DateString(task.completion_date)),standard)) 
        elements.append(small_spacer)                                 
        elements.append(Paragraph('<b>Creator</b> : %s %s<b>Assigned To</b> : %s' 
                                    % (str(task.creator.get_profile()) , FillToHalf(len(str(task.creator))+6) ,
                                        str(request.user.get_profile())),standard))
        elements.append(small_spacer)       
        elements.append(Paragraph('<b>Feedback : </b>',standard))
        elements.append(P)
        elements.append(PageBreak())
        
        position_on_page=PAGE_HEIGHT-FRAME_BORDER
    elif h>aH:
        elements.append(PageBreak())
        position_on_page=PAGE_HEIGHT-FRAME_BORDER
        elements.append(Paragraph('<b>%d. %s </b>' % (sno,task.subject),h2))
        elements.append(small_spacer)
        #elements.append(P)
        elements.append(Paragraph('<b>Deadline</b> : %s ' %DateString(task.deadline),standard))
        elements.append(small_spacer)
        elements.append(Paragraph('<b>Creation Date</b> : %s %s<b>Completion Date</b> : %s' 
                                    %(DateString(task.creation_date),FillToHalf(len(DateString(task.creation_date))+16)
                                      ,DateString(task.completion_date)),standard))  
        elements.append(small_spacer)                         
        elements.append(Paragraph('<b>Creator</b> : %s %s<b>Assigned To</b> : %s' 
                                    % (str(task.creator.get_profile()) , FillToHalf(len(str(task.creator))+6) ,
                                        str(request.user.get_profile())),standard))
        elements.append(small_spacer)       
        elements.append(Paragraph('<b>Feedback : </b>',standard)) 
        elements.append(P)        
        elements.append(spacer)
        print 5
        position_on_page = position_on_page - nH                 # reduce the available height
    
   # print '%d - %d' % ( sno , position_on_page-FRAME_BORDER)    
    sno=sno+1
    return position_on_page,sno
     

def ReportGen(request):
    buff=StringIO()      
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=ReportOnShaastra.pdf'
    sno=1
    elements=[]
    toc = TableOfContents()
   
    # For conciseness we use the same styles for headings and TOC entries
    toc.levelStyles = [h1, h2]
    elements.append(Paragraph('Table Of Contents',centered))
    elements.append(toc)
    elements.append(PageBreak())

    position_on_page=PAGE_HEIGHT-FRAME_BORDER
    
    users_in_department=userprofile.objects.filter(department = request.user.get_profile().department )
    if is_core(request.user):    
        tasks=Task.objects.filter(creator__in = users_in_department ).order_by('creation_date')
        elements.append(Paragraph('Tasks made by your Department',h1))
        elements.append(big_spacer)
        position_on_page = position_on_page - h1.fontSize - big_spacer_height
    
        for task in tasks:
          position_on_page,sno=ShowTask(request,elements,position_on_page,sno,task)

        elements.append(PageBreak())    
        position_on_page=PAGE_HEIGHT-FRAME_BORDER
        elements.append(Paragraph('SubTasks given to your Department',h1))
        elements.append(big_spacer)
        tasks=SubTask.objects.filter(department = request.user.get_profile().department ).order_by('creation_date')
        position_on_page = position_on_page - h1.fontSize - big_spacer_height
    
        for task in tasks:
          position_on_page,sno=ShowTask(request,elements,position_on_page,sno,task)
        elements.append(PageBreak())
    

    position_on_page=PAGE_HEIGHT-FRAME_BORDER
    elements.append(big_spacer)
    
    sno=1
    if is_core(request.user):
        subtasks=SubTask.objects.filter(creator__in = users_in_department).order_by('creation_date')        
        elements.append(Paragraph('Sub-Tasks given to your coords',h1))
        position_on_page = position_on_page - h1.fontSize - big_spacer_height          
        
    if is_coord(request.user):         
        subtasks=SubTask.objects.filter(coords__contains = request.user ).order_by('creation_date')        
        elements.append(Paragraph('Sub-Tasks given to you',h1))
        position_on_page = position_on_page - h1.fontSize - big_spacer_height
    for subtask in subtasks:
        position_on_page,sno=ShowTask(request,elements,position_on_page,sno,subtask)
            
    doc  = MyDocTemplate(buff)     
    doc.multiBuild(elements)
    response.write(buff.getvalue())
    return response

