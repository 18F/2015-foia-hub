// Script to track index item and position
window.onload = function () {
    $('.agency--link').each(function(number) {
      this.onclick = function(){
      ga('send', 'event', 'agency--link--click',
        'position--' + number + '--' + this.text , document.location.search);
      }
    })
}
