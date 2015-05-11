// Script to track index item and position
window.onload = function () {
    $('.agency--link').each(function(number) {
      this.onclick = function(){
        ga('send', {
          'hitType': 'event',
          'eventCategory': 'agency--link',
          'eventAction': 'click--agency--' + document.location.search,
          'eventLabel': this.text + '--' + number
        });
      }
    })
}
