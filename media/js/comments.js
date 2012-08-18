function comment(object_id, is_task){
        if (is_task=='True'){
            var comments_field_id = '#comments_field_task_' + object_id
            var comments_alert ='#comments_alert_task_'+ object_id
            elementid = '#comments_table_task_' + object_id
        }
        else {
            var comments_field_id = '#comments_field_subtask_' + object_id
            var comments_alert ='#comments_alert_subtask_'+ object_id
            elementid = '#comments_table_subtask_' + object_id
        }
        
        var comment = $(comments_field_id).val()
        if (comment=='')
        {
            $(comments_alert).show()
        }
        else {
        $(comments_field_id).val('')
        Dajaxice.tasks.comment(Dajax.process, {
                    'object_id' : object_id,
                    'comment' : comment,
                    'is_task' : is_task,
                    'elementid': elementid
                });
        }
    }
 
    
