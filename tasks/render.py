from erp.dashboard.models import *
import cgi

#Enter the Django Template you would code in the html   

def script():   
    DJANGO_TEMPLATE =  '''{% for field in shouts %} <tr>
                        <td id="shouterts name"><span id="nickname" ><a href="{% url users.views.view_profile owner_name=field.user %}">{{field.user}}</a>: 
                        </span> &nbsp; </td>
                        <td><span id="comment" >{{field.comments}}</span></td>
                        <td></td>
                        </tr> {% endfor %}'''
    
    exclude_start = len("{% for field in shouts %}")
    exclude_end = len(DJANGO_TEMPLATE) - len("{% endfor %}")
    return DJANGO_TEMPLATE[exclude_start:exclude_end]


#enter logic and syntax replacements

def replace(request, shout):
    index = {
               "{% url users.views.view_profile owner_name=field.user %}": "/erp/%s/users/profile" %(shout.user.username),
               "{{field.comments}}": cgi.escape(str(shout)),
               "{{field.user}}": cgi.escape(str(shout.user.username)),
            }
    return index
    

def render_markup(request):
    #Displays only 50 shouts.
    all_shouts = shout_box.objects.order_by('time_stamp')
    count = 0
    markup=[]
    for shout in all_shouts:
        base_script=script()
        replace_dict = replace(request, shout)
        for key in replace_dict.keys():
            base_script = base_script.replace((key),replace_dict[key])
        markup.append(base_script)
    return markup
    
    
    


    
    
    
    