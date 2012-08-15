try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import textwrap
import datetime
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
    if date is not None :
        return "%s/%s/%s" % ( date.day,date.month,date.year)
    else :
        return 'Unfinished'
def FillToHalf(length):
    s=''
    i=0
    while i<55-length:
        s=s+'&nbsp;'
        i=i+1
    return s



def Show(request,elements,position_on_page,sno,task,is_task,coord_subtask,assigner_string,assignee_string,assignee_list) :
    aW = PAGE_WIDTH-2*FRAME_BORDER                                 # available width and height
    aH = position_on_page+FRAME_BORDER
    P = Paragraph(task.feedback,standard)
    w,h = P.wrap(aW, aH)
    if coord_subtask == 0 : 
        if is_task ==1 :                                                              # find required space  
            h= h+h2.fontSize+4*small_spacer_height+3*standard.fontSize 
        else:
            h= h+h2.fontSize+5*small_spacer_height+4*standard.fontSize     
    else :     
        if(assignee_list.__len__()!=0):        
            h= h+h2.fontSize+(1+3+assignee_list.__len__())*small_spacer_height+(assignee_list.__len__()+2+1)*standard.fontSize 
        else:
            h= h+h2.fontSize+(1+3+1)*small_spacer_height+(1+2+1)*standard.fontSize 
    nH=h+spacer_height
    if nH<=aH:
        
        elements.append(Paragraph('<b>%d. %s </b>' % (sno,task.subject),h2))
        elements.append(small_spacer)
        #elements.append(P)
        elements.append(Paragraph('<b>Deadline</b> : %s ' %DateString(task.deadline),standard))   
        elements.append(small_spacer)
        
        elements.append(Paragraph('<b>Creation Date</b> : %s %s<b>Completion Date</b> : %s' 
                                    %(DateString(task.creation_date),FillToHalf(DateString(task.creation_date).__len__()-1+22)
                                      ,DateString(task.completion_date)),standard)) 
        elements.append(small_spacer)               
        if coord_subtask == 0 :            
            elements.append(Paragraph('<b>Creator</b> : %s ' 
                                    % (assigner_string),standard))
            if is_task != 1:
                try:
                    elements.append(small_spacer)
                    elements.append(Paragraph('<b>Assigned To</b> : %s ' 
                                    % (assignee_string),standard))
                except:
                    pass
                elements.append(small_spacer)
            else:
                elements.append(small_spacer)
        else : 
            elements.append(Paragraph('<b>Creator</b> : %s' 
                                    % (assigner_string),standard))
            elements.append(small_spacer)
            try:            
                elements.append(Paragraph('<b>Assigned To</b> : %s ' 
                                        % (assignee_list[0].get_profile().name),standard))
                
                elements.append(small_spacer)
                i=1
                while i<assignee_list.__len__():
                    elements.append(Paragraph('%s %s' 
                                        % (FillToHalf(31) ,
                                           str(assignee_list[i].get_profile().name)),standard))
                    elements.append(small_spacer)
                    i=i+1
            
            except:
                elements.append(Paragraph('<b>Assigned To</b> : Unassigned ',standard))  
                elements.append(small_spacer)               
                          
        elements.append(Paragraph('<b>Feedback : </b>',standard))
        elements.append(P)
        elements.append(spacer)  
        position_on_page = position_on_page - nH                  # reduce the available height   
    elif nH>aH and h<=aH:        
        
        elements.append(Paragraph('<b>%d. %s </b>' % (sno,task.subject),h2))
        elements.append(small_spacer)
        #elements.append(P)
        elements.append(Paragraph('<b>Deadline</b> : %s ' %DateString(task.deadline),standard))   
        elements.append(small_spacer)
        
        elements.append(Paragraph('<b>Creation Date</b> : %s %s<b>Completion Date</b> : %s' 
                                    %(DateString(task.creation_date),FillToHalf(DateString(task.creation_date).__len__()-1+22)
                                      ,DateString(task.completion_date)),standard)) 
        elements.append(small_spacer)               
        if coord_subtask == 0 :            
            elements.append(Paragraph('<b>Creator</b> : %s ' 
                                    % (assigner_string),standard))
            if is_task != 1:
                try:
                    elements.append(small_spacer)
                    elements.append(Paragraph('<b>Assigned To</b> : %s ' 
                                    % (assignee_string),standard))
                except:
                    pass
                elements.append(small_spacer)
        else : 
            elements.append(Paragraph('<b>Creator</b> : %s' 
                                    % (assigner_string),standard))
            elements.append(small_spacer)
            try:            
                elements.append(Paragraph('<b>Assigned To</b> : %s ' 
                                        % (assignee_list[0].get_profile().name),standard))
                
                elements.append(small_spacer)
                i=1
                while i<assignee_list.__len__():
                    elements.append(Paragraph('%s %s' 
                                    % (FillToHalf(31) ,
                                       str(assignee_list[i].get_profile().name)),standard))
                    elements.append(small_spacer)
                    i=i+1
            
            except:
                elements.append(Paragraph('<b>Assigned To</b> : Unassigned ',standard))    
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
                                    %(DateString(task.creation_date),FillToHalf(DateString(task.creation_date).__len__()-1+22)
                                      ,DateString(task.completion_date)),standard)) 
        elements.append(small_spacer)               
        if coord_subtask == 0 :            
            elements.append(Paragraph('<b>Creator</b> : %s ' 
                                    % (assigner_string),standard))
            if is_task != 1:
                try:
                    elements.append(small_spacer)
                    elements.append(Paragraph('<b>Assigned To</b> : %s ' 
                                    % (assignee_string),standard))
                except:
                    pass
                elements.append(small_spacer)
        else : 
            elements.append(Paragraph('<b>Creator</b> : %s' 
                                    % (assigner_string),standard))
            elements.append(small_spacer)
            try:            
                elements.append(Paragraph('<b>Assigned To</b> : %s ' 
                                        % (assignee_list[0].get_profile().name),standard))
                
                elements.append(small_spacer)
                i=1
                while i<assignee_list.__len__():
                    elements.append(Paragraph('%s %s' 
                                    % (FillToHalf(31) ,
                                       str(assignee_list[i].get_profile().name)),standard))
                    elements.append(small_spacer)
                    i=i+1
            
            except:
                elements.append(Paragraph('<b>Assigned To</b> : Unassigned ',standard))  
                elements.append(small_spacer)               
        elements.append(Paragraph('<b>Feedback : </b>',standard))
        elements.append(P)
        elements.append(spacer)  
        position_on_page = position_on_page - nH                 # reduce the available height
    
   # print '%d - %d' % ( sno , position_on_page-FRAME_BORDER)    
    sno=sno+1
    return position_on_page,sno
def ShowTask(request,elements,position_on_page,sno,task):
    '''When cores get something from another deprtment it's a task. When they give something to another department, it's
       a subtask. Nomenclature is pretty bad'''
    styles=getSampleStyleSheet()["Normal"]  
    print 'Task display'
    coord_subtask = 0 
    is_task = 1
    assignee_list=[]
    assigner_string = str(task.creator.get_profile().name)
    assignee_string=''
    position_on_page,sno = Show(request,elements,position_on_page,sno,task,
                                is_task,coord_subtask,assigner_string,assignee_string,assignee_list) 
    return position_on_page,sno
    
def ShowSubTask(request,elements,position_on_page,sno,task):
    styles=getSampleStyleSheet()["Normal"]  
    coord_subtask = 0 
    is_task = 0
    assignee_list=[]
    assignee_string=''
    if is_core(request.user):
        if task.creator.get_profile().department == request.user.get_profile().department:  
        
                ''' This is when the core tries to find the SubTasks given to his coords. Assigner is creator and a list of coords is the
                assignee'''

                print '2323232'
                
                assigner_string = str(task.creator.get_profile().name)
                assignee_list = task.coords.all()               
                coord_subtask = 1
        elif request.user.get_profile().department == task.department :
            ''' In this case it is a task as the user belongs to the recieving department. So assigner is the creator - the guy from that
                department and this core's department is the assignee'''
            assigner_string = str(task.creator.get_profile().name)
            assignee_string = task.department.Dept_Name
        

    else : 
        ''' This is when the coord tries to find the SubTasks given to his coords. Assigner is creator and a list of coords is the 
            assignee'''
        coord_subtask = 1
        assigner_string = str(task.creator.get_profile().name)
        assignee_list = task.coords.all()         
    
    position_on_page,sno = Show(request,elements,position_on_page,sno,task,
                                is_task,coord_subtask,assigner_string,assignee_string,assignee_list)
    return position_on_page,sno 

def ReportGen(request, owner_name):
    buff=StringIO()      
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=ReportOnShaastra.pdf'
    sno=1
    elements=[]
    toc = TableOfContents()
   
    # For conciseness we use the same styles for headings and TOC entries
    toc.levelStyles = [h1, h2]
    elements.append(Paragraph('Shaastra Report',centered))
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
        print 'q'
        for task in tasks:
            position_on_page,sno=ShowTask(request,elements,position_on_page,sno,task)
        print 'r'
        elements.append(PageBreak())    
        position_on_page=PAGE_HEIGHT-FRAME_BORDER
        elements.append(Paragraph('SubTasks given to your Department',h1))
        elements.append(big_spacer)
        tasks=SubTask.objects.filter(department = request.user.get_profile().department ).order_by('creation_date')
        position_on_page = position_on_page - h1.fontSize - big_spacer_height
    
        for task in tasks:
            position_on_page,sno=ShowSubTask(request,elements,position_on_page,sno,task)
        elements.append(PageBreak())
    

    position_on_page=PAGE_HEIGHT-FRAME_BORDER
    
    sno=1
    if is_core(request.user):
        print 'p'
        subtasks=SubTask.objects.filter(creator__in = users_in_department).order_by('creation_date')  
      
        elements.append(Paragraph('Sub-Tasks given to your coords',h1))
        elements.append(big_spacer)
        position_on_page = position_on_page - h1.fontSize - big_spacer_height          
        
    elif is_coord(request.user):         
        subtasks = request.user.subtask_set.all().order_by('creation_date')         
        elements.append(Paragraph('Sub-Tasks given to you',h1))
        elements.append(big_spacer)
        position_on_page = position_on_page - h1.fontSize - big_spacer_height
       
    for subtask in subtasks:
        position_on_page,sno=ShowSubTask(request,elements,position_on_page,sno,subtask)
            
    doc  = MyDocTemplate(buff)     
    doc.multiBuild(elements)
    response.write(buff.getvalue())
    return response

