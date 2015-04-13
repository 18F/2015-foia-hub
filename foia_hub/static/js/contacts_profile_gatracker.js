//script to track item clicks
$(function() {
    $('.foialibrary, .agency--email, .agency--site, .inaccurateinfo--email, .request--link, .request--email, .foiagov--search--link, .servicecenter--phone, .liaison--phone').on('click', function(item) {
       ga('send', 'event', this.className + "--click", document.location.pathname);
    });
});
