$(document).ready(function() {
    // question mark link
    // more info toggle
    $('.slidedown').on('click', function(e) {
        e.preventDefault();

        var $link = $(this),
            $messageBox = $link.parent('li').next('.expandable');

        $messageBox.slideToggle('fast', function() {
            var $icon = $link.find('span');
            if ($messageBox.is(':visible')) {
                $icon.removeClass('fa-question-circle').addClass('fa-times-circle');
                ga('send', {
                  'hitType': 'event',
                  'eventCategory': 'extrainfo--open',
                  'eventAction': 'openon' + document.location.pathname,
                  'eventLabel': this.id,
                });
            }
            else {
                $icon.removeClass('fa-times-circle').addClass('fa-question-circle');
                ga('send', {
                  'hitType': 'event',
                  'eventCategory': 'extrainfo--close',
                  'eventAction': 'closeon' + document.location.pathname,
                  'eventLabel': this.id,
                });
            }
        });
    });
});
