$(document).ready(function() {
    var agencyDatasource,
        gaTimeout = 500,
        getKeys,
        onSelection,
        substrRegex,
        substringMatcher,
        typeahead;
    //  Set up the agency data source
    agencyDatasource = new Bloodhound({
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        limit: 500,
        prefetch: {
          url: '/api/agency/',
          filter: function(response) {
            return response.objects;
          }
        },
        datumTokenizer: function(d) {
          return []
            .concat(Bloodhound.tokenizers.whitespace(d.name))
            .concat(Bloodhound.tokenizers.whitespace(d.abbreviation));
        }
    });
    onSelection = function(ev, suggestion) {
        var agency = suggestion.slug
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
    typeahead = $('#contact-typeahead').typeahead({
        hint: false,
        highlight: true,
        minLength: 1
      },
      {
        name: 'agencies',
        displayKey: 'name',
        source: agencyDatasource
      }).on('typeahead:selected', onSelection);
});
