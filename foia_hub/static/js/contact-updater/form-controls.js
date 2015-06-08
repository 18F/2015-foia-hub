// Make some fields required
$(function(){
   $(".agency_description,.public_liaison_phone,.phone,.address_line_1,.city,.state,.zip_code,.component_url").prop('required', true)
});

// Set up Parsely
$(function() {
    //setup key listners
    $('form').find(':input').each(function(){
         this.setAttribute("data-parsley-trigger", "keyup");
    });
    $('form').parsley().validate();
    //validate form, but scroll to
    $('body').scrollTop(0);
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
});

// Set Char counters
$(function(){
    $('textarea[id$=-description]').each(function() {
        // Get the current char count
        var max = 500;
        var current_len = $(this).val().length
        // Create and insert text counters
        var charDiv = document.createElement("div");
        charDiv.setAttribute("id", "charNum" + this.name);
        charDiv.innerHTML = current_len + "/500 characters";
        this.parentNode.insertBefore(charDiv, this.nextSibling);
        // Set a listener to change on keyup
        $(this).keyup(function () {
            var len = $(this).val().length;
            if (len >= max) {
            $("#charNum" + this.name).text('You have reached the limit');
            } else {
                var char = len;
                $("#charNum" + this.name).text(char + '/500 characters');
            }
        });
    });
});
