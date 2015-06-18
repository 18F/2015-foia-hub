$(function(){
    window.ParsleyConfig.i18n.en.required="This field is required."
    // Make some fields required
   $(".public_liaison_name,.public_liaison_email,.agency_description,.address_line_1,.city,.state,.zip_code").prop('required', true)

   // Function to allow error list
   var validateActions = function (fieldInstance) {
        var arrErrorMsg = ParsleyUI.getErrorsMessages(fieldInstance);
        var errorMsg = arrErrorMsg.join(';');
        var errorElement = fieldInstance.$element[0];
        var errorElementLabel = errorElement.previousElementSibling.innerHTML;
        var errorOffice = errorElement.parentNode.parentNode.parentNode.getElementsByClassName('agency-name')[0].innerHTML;
        var error = "<b>" + errorOffice + "</b>" + "'s " + errorElementLabel + " field is incomplete";
        var ul = $('#error-list');
        var li = ul.find('li').filter(function (){ return this.id == errorElement.id})
        if (li.length == 1){
            li.innerHTML = error
        }
        else{
            var li = document.createElement("li");
            li.id = errorElement.id
            li.innerHTML = error
            ul[0].appendChild(li);
        }
    };

    // Setup Parsely keyup triggers
    $('form').find(':input').each(function(){
         this.setAttribute("data-parsley-trigger", "keyup");
    });

    // Setup error listners
    $.listen('parsley:field:error', function (fieldInstance) {
        document.getElementById('submit-agency').className = 'submit-invalid';
        // Only create error list if the agency is decentralized
        if (document.getElementById("form_selector")) {
            validateActions(fieldInstance);
        }
    });

    // Init Parsely
    $('form').parsley().validate();
    // Validate form, but scroll to top
    $('body').scrollTop(0);

    // Set up success listener to remove items from error list
    $.listen('parsley:field:success', function (fieldInstance) {
        var errorElement = fieldInstance.$element[0];
        $('#error-list').find('li').each(function () {
            if(errorElement.id == this.id){
                document.getElementById("error-list").removeChild(this);
            }
        });
        document.getElementById('submit-agency').className = 'submit-valid';
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

    // Set Char counters
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
