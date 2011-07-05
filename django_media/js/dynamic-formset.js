$(document).ready(function() {
    // Code adapted from http://djangosnippets.org/snippets/1389/
    
    function updateElementIndex(el, prefix, ndx) {
	// Update the indices of attributes like for, id and name
	var id_regex = new RegExp('(' + prefix + '-\\d+-)');
	var replacement = prefix + '-' + ndx + '-';
	if ($(el).attr("for")) $(el).attr("for",
					  $(el).attr("for")
					  .replace(id_regex, replacement));
	if (el.id) el.id = el.id.replace(id_regex, replacement);
	if (el.name) el.name = el.name.replace(id_regex, replacement);
    }

    function updateFormElements (currForm, prefix, index, isNewForm) {
	// Relabel or rename all the relevant bits (all the
	// labels, input, select fields, etc.)
	$("th, td", currForm).children().each(function() {
	    updateElementIndex(this, prefix, index);
	    if (isNewForm){
		// Empty the field
		$(this).val("");
	    }
	});
	
	// Note : The hidden template form will have index 0
	// So, the visible forms will have 1-based index
	$("h4:first", currForm).text ("Subtask " + (index));
    }

    function deleteForm(link, prefix) {
	// Remove current form and update the rest

	// TODO : The screen flickers when the bottom-most form is
	// deleted. Rest slide up gracefully. Fix it.

	// Update the total form count
	var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
	$("#id_" + prefix + "-TOTAL_FORMS").val(formCount - 1);
	
	// Remove the form from which delete was called
	$(link).parents('.visible-form:first').slideUp (function () {
	    $ (this).remove();
	    // Get all the remaining visible forms
	    $('.visible-form').each (function (index) {
		// Since the visible form indices are 1-based
		updateFormElements (this, prefix, index + 1, false);
	    });
	});
	return false;
    }
    
    // Attempt to make the last form slide smoothly.
    // It disappears quickly, but so does everything else.

    // function deleteForm(link, prefix) {
    // 	// Remove current form and update the rest

    // 	// Update the total form count
    // 	var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    // 	$("#id_" + prefix + "-TOTAL_FORMS").val(formCount - 1);
	
    // 	var updateOtherForms =
    // 	    function (obj) {
    // 		$ (obj).remove();
    // 		// Get all the remaining visible forms
    // 		$('.visible-form').each (function (index) {
    // 		    // Since the visible form indices are 1-based
    // 		    updateFormElements (this, prefix, index + 1, false);
    // 		});
    // 	    }
    // 	parentForm = $(link).parents('.visible-form:first');
    // 	// Remove the form from which delete was called
    // 	console.log(parentForm);
    // 	if ($(parentForm).is('.visible-form:last')) {
    // 	    console.log ('This is the last one');
    // 	    updateOtherForms (parentForm);
    // 	}
    // 	else {
    // 	    $(parentForm).slideUp (300, updateOtherForms);
    // 	}
    // 	return false;
    // }

    function addForm(link, prefix) {
	// Copy the hidden form (with 'template-form' class) and
	// insert it at the end of all the forms.
	// Remove error messages and update all the form indices.

	var max_num_forms = 11;
	var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
	// You can only submit a maximum of 10 subtasks
	if (formCount < max_num_forms) {
	    // Clone a form (without event handlers) from the first form
	    var row = $(".template-form:last").clone(false).get(0);
	    
	    // Insert it before the hidden template form
	    $(row).removeAttr('id')
		.hide()
		.insertBefore(".template-form:last")
		.slideDown(300);

	    // Remove the bits we don't want in the new row/form
	    // e.g. error messages
	    $(".errorlist", row).remove();
	    $(".error", row).removeClass("error");

	    // Add an event handler for the delete form link
	    $(row).find(".delete").click(function() {
		return deleteForm(this, prefix);
	    });

	    // This form should be visible
	    $(row).removeClass('template-form').addClass('visible-form');

	    // Update its elements
	    updateFormElements (row, prefix, formCount, true);

	    // Update the total form count
	    $("#id_" + prefix + "-TOTAL_FORMS").val(formCount + 1);

	} // End if
	else {
	    alert("Sorry, you can only enter a maximum of " + (max_num_forms - 1) + " Subtasks.");
	}
	return false;
    }
    
    // Register the click event handlers
    $("#add").click(function(event) {
	event.preventDefault ();
	return addForm(this, "all");
    });
    
    $(".delete").click(function(event) {
	event.preventDefault ();
	return deleteForm(this, "all");
    });
    
    // Hide the Template form
    $ (".template-form").hide ();
    // $ ("table").css ("background-color", "red");
});
