$(document).ready(function(){
	
	
	
   $('#popupDatepicker').datepick();
   $('#id_deadline').datepick({ altFormat: 'dd-mm-yy' });


    $('#contacts ul > li')
	.find('ul:first')
	.stop(true, true)
	.slideToggle();

    $('#contacts ul > li ul')
	.click(function(e){
	    e.stopPropagation();
	})
	.filter(':not(:first)')
	.hide();
    
    $('#contacts ul > li, #contacts ul > li > ul > li').click(function(){
	$(this)
	    .find('ul:first')
	    .stop(true, true)
	    .slideToggle();
    });
});




