// Script to track index item and position
window.onload = function () {
    $('.agency--link').each(function(number) {
      this.onclick = function(){
        ga('send', {
          'hitType': 'event',
          'eventCategory': 'agency--link--click/' + document.location.search,
          'eventAction': 'position-' + number,
          'eventLabel': this.text
        });
      }
    })
}
