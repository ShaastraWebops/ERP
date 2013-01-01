from erp.prizes.models import *

def fullcopy():
    users=ParticipantUser.objects.using('main').all()
    for user in users:
        try:
            erp_user = Participant()
            erp_user.name = user.user.first_name + user.user.last_name
            erp_user.gender = user.gender
            erp_user.branch = user.branch
            erp_user.college = user.college.name
            erp_user.mobile_number = user.mobile_number
            erp_user.shaastra_id = user.shaastra_id
            erp_user.college_roll = user.college_roll
            erp_user.branch = user.branch
            erp_user.save()            
        except:
            pass
    f=open('prizes/pk.txt','w')
    f.write(str(erp_user.pk)) 
        
    
