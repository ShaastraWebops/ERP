from erp.prizes.models import *
'''
def fullcopy():
    users=ParticipantUser.objects.using('main').order_by('pk')
    length=len(users)
    for user in users:
        try:
            erp_user = Participant()
            erp_user.name = user.user.first_name + user.user.last_name
            erp_user.gender = user.gender
            erp_user.branch = user.branch
            try:
                erp_user.college = user.college.name
            except:
                pass
            erp_user.mobile_number = user.mobile_number
            erp_user.shaastra_id = user.shaastra_id
            erp_user.college_roll = user.college_roll
            erp_user.branch = user.branch
            erp_user.save()
        except:
            print 'did not save', user.pk
        f=open('prizes/pk.txt','w')
        f.write(str(length))
'''
import time

def check_and_copy():

    while True:
        f=open('prizes/pk.txt','rb')
        x=int(f.read())
        users=ParticipantUser.objects.using('main').order_by('pk')
        length=len(users)
        print length-x, "new instances copied"
        if x-length!=0:
            for user in users[(x-1):(length-1)]:
                try:
                    erp_user = Participant() 
                    erp_user.name = user.user.first_name + user.user.last_name
                    erp_user.gender = user.gender
                    erp_user.branch = user.branch
                    try:
                        erp_user.college = user.college.name
                    except:
                        pass
                    erp_user.mobile_number = user.mobile_number
                    erp_user.shaastra_id = user.shaastra_id
                    erp_user.college_roll = user.college_roll
                    erp_user.branch = user.branch
                    erp_user.save()
                    print "copied",user.pk
                except:
                    print 'did not save', user.pk
        f=open('prizes/pk.txt','w')
        f.write(str(length))
        f.close()
        time.sleep(2)
        print "Run check_and_copy delay-2"
