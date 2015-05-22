// Make some fields required
$(function(){
   $(".description,.public_liaison_phone,.phone,.address_line_1,.city,.state,.zip_code,.component_url").prop('required', true)
});

// Make forms visible
$( "#form_selector" ).change( function() {
    // Keep the rest of the forms hidden
    $("div[id^=office_]").hide();
    var form_id = document.getElementById("form_selector").value;
    // Show selected form
    document.getElementById("office_" + form_id).style.display = "block";
    $("#office_" + form_id).show();
});
