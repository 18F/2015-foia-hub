$(function(){
    var error_list = $('#error-list'),
        addErrorItem,
        removeErrorItem;

   // Function to allow error list
   addErrorItem = function (fieldInstance) {
        var errorMsg = ParsleyUI.getErrorsMessages(fieldInstance).join(';');
        var errorElement = fieldInstance.$element[0];
        var errorElementLabel = errorElement.previousElementSibling.innerHTML;
        var errorOffice = errorElement.parentNode.parentNode.parentNode.getElementsByClassName('agency-name')[0].innerHTML;
        var error = "<b>" + errorOffice + "'s </b>" + errorElementLabel
        if (errorMsg == "This field is required.")
            error += " is missing.";
        else
            error += " is invalid.";
        var lis = error_list.find('li').filter(function (){ return this.id == errorElement.id})
        if (lis.length == 1){
            lis[0].innerHTML = error
        }
        else{
            var li = document.createElement("li");
            li.id = errorElement.id
            li.innerHTML = error
            error_list[0].appendChild(li);
            error_list.find("li").sort(function(first, second) {
                return $(first).text().toLowerCase().localeCompare($(second).text().toLowerCase());
            }).each(function() {
                error_list.append(this);
            });
        }
    };
    removeErrorItem = function (fieldInstance){
        var errorElement = fieldInstance.$element[0];
        var error_list_items = error_list.find('li');
        if (error_list_items.length > 0){
            error_list_items.each(function () {
                if(errorElement.id == this.id){
                    error_list[0].removeChild(this);
                }
            })
        }
        else {
            document.getElementById('submit-agency').className = 'submit-valid';
        }
    };

    // Make some fields required
   $(".public_liaison_name,.public_liaison_email,.agency_description,.address_line_1,.city,.state,.zip_code").prop('required', true)

    // Setting the default required message for parsely
    window.ParsleyConfig.i18n.en.required="This field is required."

    // Setup Parsely keyup triggers
    $('form').find(':input').each(function(){
         this.setAttribute("data-parsley-trigger", "keyup");
    });

    // Setup error listners
    $.listen('parsley:field:error', function (fieldInstance) {
        document.getElementById('submit-agency').className = 'submit-invalid';
        // Only create error list if the agency is decentralized
        if (document.getElementById("form_selector")) {
            addErrorItem(fieldInstance);
        }
    });

    // Set up success listener to remove items from error list
    $.listen('parsley:field:success', function (fieldInstance) {
        removeErrorItem(fieldInstance)
    });

    // Init Parsely
    $('form').parsley().validate();
    // Validate form, but scroll to top
    $('body').scrollTop(0);


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
