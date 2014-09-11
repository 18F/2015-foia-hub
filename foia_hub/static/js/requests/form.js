var onRequestSuccess = function(data, status, xhr) {
  console.log("Success! Tracking: " + data.tracking_id);

  window.location = "/request/success/" + data.tracking_id;

  // var tracking = "0000000" + data.tracking_id;
  // var email = $(".email").val();
  // var agency_name = $(".agency_name").val();

  // // insert values into success message
  // $("#tracking-number").html(tracking);
  // $(".agency-name").html(agency_name);
  // $("#requester-email").html(email).attr("href", "mailto:" + email);

  // // show success form
  // $(".request.form, .request.agency").hide();
  // $(".request.success").show();

  // return false;
};

var onRequestFailure = function(xhr, status, err) {
  window.arguments = arguments;
  console.log("Failure.");

  $(".request.error").show();
  return false;
};

var collectRequestData = function() {
  var fee_limit = parseInt($(".upto").val());
  fee_limit = isNaN(fee_limit) ? 0 : fee_limit;

  return {
    first_name: $(".first_name").val(),
    last_name: $(".last_name").val(),
    email: $(".email").val(),
    body: $(".body").val(),

    documents_start: $("#document_start").val(),
    documents_end: $("#document_end").val(),
    fee_limit: fee_limit,

    agency_fields: {
      region: $(".agency_fields_region").val(),
      contract: $(".agency_fields_contract").val(),
    },

    agency: $(".agency_agency").val(),
    office: $(".agency_office").val()
  };
};

$("form.request").submit(function() {
  var data = collectRequestData();

  $.ajax({
    type: "POST",
    url: "/api/request/",
    data: JSON.stringify(data),
    processData: false,
    contentType: 'application/json'
  }).done(onRequestSuccess).fail(onRequestFailure);

  return false;
});


// date chooser
$("#document_end, #document_start").pickadate({
  format: 'mmmm d, yyyy'
});

// fee sync
var $upto = $(".upto");
var $fee = $(".fee-amount");
var onchange = function() {
  var val = parseInt($upto.val());
  if (isNaN(val)) val = 0;
  $fee.html("$" + val);
}
$upto.keyup(onchange);

// fee waiver toggle
$("#fee-waiver-request").change(function() {
  $("#fee-waiver-justification").toggle();
})
