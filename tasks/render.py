from erp.dashboard.models import *

def render_markup(request):
    all_shouts = shout_box.objects.all()
    markup=r'<table>        {% for field in shouts %}        <tr>            <td id="shouterts name"><span id="nickname" ><a href="{% url users.views.view_profile owner_name=field.user%}">{{field.nickname}}</a>: </span> &nbsp; </td>            <td><span id="comment" >{{field.comments}}</span></td>            <td></td>        </tr>      {% endfor %}   </table>'
    print "this is", markup
    return markup
    
    
    
    
    
    