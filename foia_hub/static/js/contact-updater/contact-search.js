'use strict';
$(document).ready(function() {
    var gaTimeout = 500,
        onSelection,
        substrRegex,
        substringMatcher,
        typeahead;

    onSelection = function(ev, suggestion) {
        var agency = agencies[suggestion]
        var callback = function() {
              clearTimeout(timeout);
              window.location = '/update-contacts/' + agency + '/';
            },
            timeout = setTimeout(callback, gaTimeout);
        ga('send', {
            'hitType': 'event',
            'eventCategory': 'contact-updater-select',
            'eventAction': 'select-agency--' + agency,
            'eventLabel': document.location.pathname},
            {'hitCallback': callback});
    }
    substringMatcher = function(strs) {
      return function findMatches(q, cb) {
        var matches, substringRegex;
        matches = [];
        substrRegex = new RegExp(q, 'i');
        $.each(strs, function(i, str) {
          if (substrRegex.test(str)) {
            matches.push(str);
          }
        });
        cb(matches);
      };
    };
    typeahead = $('#contact-typeahead').typeahead({
        hint: false,
        highlight: true,
        minLength: 1
      },
      {
        name: 'agencies',
        source: substringMatcher(Object.keys(agencies))
      }).on('typeahead:selected', onSelection);
});
