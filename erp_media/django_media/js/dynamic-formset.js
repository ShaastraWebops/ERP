$(document).ready(function() {
    // Code adapted from http://djangosnippets.org/snippets/1389/

    // Django's default for formsets
    var form_prefix = "subtask_set";
    
    function updateElementIndex(el, index) {
	// Update the indices of attributes like for, id and name
	var id_regex = new RegExp('(' + form_prefix + '-\\d+-)');
	var replacement = form_prefix + '-' + index + '-';
	if ($(el).attr("for")) $(el).attr("for",
					  $(el).attr("for")
					  .replace(id_regex, replacement));
	if (el.id) el.id = el.id.replace(id_regex, replacement);
	if (el.name) el.name = el.name.replace(id_regex, replacement);
    }

    function updateFormIndices (currForm, formIndex) {
	// Relabel or rename all the relevant bits (all the
	// labels, input, select fields, etc.)
	$("th, td, .delete-checkbox, tbody", currForm)
	    .children().each(function() {
		updateElementIndex(this, formIndex);
	    });
    }

    function updateFormHeading (currForm) {
	// Call this after updating its elements' indices
	$(".subtask-heading:first", currForm)
	    .text ("Subtask " + (parseInt (getFormIndex (currForm)) + 1));
    }

    function getFormIndex (form) {
	// Get the index (marked by INDEX)
	// format is for="id_prefix-INDEX-DELETE"
	var id_regex = new RegExp(form_prefix + '-(\\d+)-DELETE');
	var for_text = $(".delete-checkbox > label", form).attr ("for");
	var index = id_regex.exec (for_text)[1];
	console.log (index);
	return index;
    }

    function isExistingSubtaskForm (form) {
	// If it's form ID is not present, it's a new subtask form
	if ($("#id_" + form_prefix + "-" + getFormIndex (form) + "-id").val () == "")
	    return false;
	return true;
    }
    
    function deleteForm(link) {
	// If it is a new form, remove it and update the rest
	// Else, mark for deletion on the server

	// TODO : The screen flickers when the bottom-most form is
	// deleted. Rest slide up gracefully. Fix it.
	// Right now - no sliding. Just removal.

	// Remove the form from which delete was called
	currForm = $(link).parents('.visible-form:first');
	currFormIndex = getFormIndex (currForm);

	if (isExistingSubtaskForm (currForm)) {
	    // Check the DELETE checkbox
	    if (confirm ("This subtask exists in our database. Mark for Deletion?")) {
		$("#id_" + form_prefix + "-" + currFormIndex + "-DELETE").attr ("checked", "checked");
		highlightDeletedForms ();
		// currForm.addClass ("to-be-deleted");
	    }
	}
	else {
	    // Update the total form count
	    var formCount = parseInt($('#id_' + form_prefix + '-TOTAL_FORMS')
				     .val());
	    $("#id_" + form_prefix + "-TOTAL_FORMS").val(formCount - 1);
	    
	    // Was too jerky for the last subtask form
	    // currForm.slideUp (function () {
	    $ (currForm).remove();
	    // Get all the remaining visible forms
	    $('.visible-form').each (function (index) {
		updateFormIndices (this, index);
		updateFormHeading (this);
	    });
	    // });
	}
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
    // 		    updateFormIndices (this, prefix, index + 1, false);
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

    function addForm(link) {
	// Copy the hidden form (with 'template-form' class) and
	// insert it at the end of all the forms.
	// Remove error messages and update all the form indices.

	var max_num_forms = 10;
	var formCount = parseInt($('#id_' + form_prefix + '-TOTAL_FORMS').val());
	console.log (formCount);

	// You can only submit a maximum of 10 subtasks
	if (formCount < max_num_forms) {
	    // Clone a form (without event handlers) from the template form
	    var currForm = $(".template-form:first").clone(false).get(0);
	    
	    // Set the index for the new form as formCount
	    var inner_txt = $(currForm).html().replace (/__prefix__/g, formCount);
	    // console.log (inner_txt);

	    $(currForm).html (inner_txt);

	    // Insert it before the add link
	    $(currForm).removeAttr('id')
		.hide()
		.insertBefore("#add")
		.slideDown(300);

	    // Add an event handler for the delete form link
	    $(currForm).find(".delete").click(function() {
		return deleteForm(this);
	    });

	    // This form should be visible
	    $(currForm).removeClass('template-form').addClass('visible-form');

	    // Update its heading
	    updateFormHeading (currForm);

	    // Update the total form count
	    $("#id_" + form_prefix + "-TOTAL_FORMS").val(formCount + 1);

	} // End if
	else {
	    alert("Sorry, you can only enter a maximum of " + (max_num_forms - 1) + " Subtasks.");
	}
	return false;
    }
    
    // Register the click event handlers
    $("#add").click(function(event) {
	event.preventDefault ();
	return addForm(this, form_prefix);
    });
    
    $(".delete").click(function(event) {
	event.preventDefault ();
	return deleteForm(this, form_prefix);
    });
    
    // Hide the Template form
    $ (".template-form").hide ();

    function highlightDeletedForms () {
	// Add class to-be-deleted to all forms which are marked to be
	// deleted
	$('.visible-form').each (function (index) {
	    if ($("#id_" + form_prefix + "-" + getFormIndex (this) + "-DELETE")
		.is (":checked")) {
		$(this).addClass ("to-be-deleted");
		$(".subtask-heading", this).append (" (Will be deleted)");
	    }
	});
    }

    // Highlight all deleted forms at the beginning (in case form had
    // errors and is being redisplayed)
    highlightDeletedForms ();

});
