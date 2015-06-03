// Make some fields required
$(function(){
   $(".agency_description,.public_liaison_phone,.phone,.address_line_1,.city,.state,.zip_code,.component_url").prop('required', true)
});

// Set up Validatr
jQuery(function ($) {
    $('form').validatr({'showall': true});
});

// Make forms visible
$(function(){
    $( "#form_selector" ).change( function() {
        // Keep the rest of the forms hidden
        $("div[id^=office_]").hide();
        var form_id = document.getElementById("form_selector").value;
        // Show selected form
        document.getElementById("office_" + form_id).style.display = "block";
        $("#office_" + form_id).show();
    });
})

$(document).ready(function() {

    // Set max
    var max = 500;

    // Init the char number
    $('#charNum').text(max - $('.agency_description').val().length + '/500 characters');

    // Set a lister to change on keyup
    $('.agency_description').keyup(function () {

        var len = $(this).val().length;
        if (len >= max) {
        $('#charNum').text('You have reached the limit');
        } else {
            var char = max - len;
            $('#charNum').text(char + '/500 characters');
        }
    });
});
