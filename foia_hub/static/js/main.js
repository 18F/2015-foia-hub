// global variables for the app

Env = {
};

Utils = {
  substringMatcher: function(strs) {
    return function findMatches(q, cb) {
      var matches, substrRegex;

      // an array that will be populated with substring matches
      matches = [];

      // regex used to determine if a string contains the substring `q`
      substrRegex = new RegExp(q, 'i');

      // iterate through the pool of strings and for any string that
      // contains the substring `q`, add it to the `matches` array
      $.each(strs, function(i, str) {
        if (substrRegex.test(str)) {
          // the typeahead jQuery plugin expects suggestions to a
          // JavaScript object, refer to typeahead docs for more info
          matches.push({ value: str });
        }
      });

      cb(matches);
    };
  }
};

$(document).ready(function(){
    var times_toggled = 0;
    var $bannerCloseButton = $("#notice--close");

    // if this browser supports localstorage, check for the value
    // that gets set to keep the banner closed once a user has clicked
    // the close button. if not present, show the banner.
    if (typeof window.localStorage !== 'undefined') {
        if (window.localStorage.getItem('keep-banner-closed') !== '1') {
            $('#notice').removeClass('hidden');
        }
    }
    $bannerCloseButton.click(function(){
        $("#notice").slideUp(function () {
          times_toggled++
            ga('send', {
              'hitType': 'event',
              'eventCategory': 'banner--close',
              'eventAction': 'toggledon' + document.location.pathname,
              'eventLabel': 'toggled-' + times_toggled,
            });
        });

        // when a user clicks or tabs to and hits enter on the banner
        // close button, set a local storage value that gets checked
        // on page load and determines whether banner is shown
        if (typeof window.localStorage !== 'undefined') {
            window.localStorage.setItem('keep-banner-closed', '1');
        }
    });
    // if someone tabs to the close button and hits enter, trigger
    // a click event
    $bannerCloseButton.keypress(function(e){
        // no need to check for e.keyCode vs e.which, jQuery fills which
        if (e.which === 13) {
            $(e.target).click();
        }
    });
    $("#notice--toggle").click(function(){
        $("#notice").slideToggle("slow", function() {
          times_toggled++
          if ($(this).is(":hidden"))
          {
            ga('send', {
              'hitType': 'event',
              'eventCategory': 'banner--hide',
              'eventAction': 'toggledon' + document.location.pathname,
              'eventLabel': 'toggled-' + times_toggled,
            });
          }
          else
          {
            ga('send', {
              'hitType': 'event',
              'eventCategory': 'banner--show',
              'eventAction': 'toggledon' + document.location.pathname,
              'eventLabel': 'toggled-' + times_toggled,
            });
          }
      });
    });
});

