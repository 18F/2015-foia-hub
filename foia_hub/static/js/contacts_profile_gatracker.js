//script to track item clicks
$(function() {
    $('.foialibrary, .agency--email, .agency--site, .inaccurateinfo--email, .request--link, .request--email, .foiagov--search--link, .servicecenter--phone, .liaison--phone').on('click', function(item) {
        ga('send', {
          'hitType': 'event',
          'eventCategory': 'contact-info',
          'eventAction': 'info-click' +  document.location.pathname,
          'eventLabel': this.className
        });
    });
});
