'use strict';
$(document).ready(function() {
  var currentText = '',
      longestText = '',
      onUserStroke,
      onSelection,
      agencyDatasource,
      agencyAdaptor,
      footerAdaptor;

  //  Set up the agency data source
  agencyDatasource = new Bloodhound({
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    limit: 500, // infinity
    prefetch: {url: '/api/agency/', filter: function(response) {
      return response.objects; }},
    datumTokenizer: function(d) {
      return []
        .concat(Bloodhound.tokenizers.whitespace(d.name))
        .concat(Bloodhound.tokenizers.whitespace(d.abbreviation));
    }
  });
  // always clear local storage for new requests, at least in dev
  agencyDatasource.clearPrefetchCache();
  agencyDatasource.initialize();

  //  Set up the agency adaptor
  agencyAdaptor = {
    name: 'agencies',
    displayKey: 'value',
    source: agencyDatasource.ttAdapter(),
    templates: {
      suggestion: Handlebars.compile('<h5 class="agency-name">{{name}}</h5>')
    }
  };
  //  Set up the footer link adaptor
  footerAdaptor = {
    name: 'footer',
    source: function(query, callback) {
      if (query.length > 0) {
        callback([{'query': query, 'isFooter': true}]);
      }
    },
    templates: {
      suggestion: Handlebars.compile('<h5>Search for "{{query}}" in keyterms and descriptions</h5>')
    }
  };

  //  Track the text as the user types
  onUserStroke = function(ev) {
    currentText = $(ev.target).val();
    if (currentText.length > longestText.length) {
      longestText = currentText;
    }
    //  blanked out the text after initially typing something
    else if (currentText.length === 0 && longestText.length > 0) {
      ga('send', 'event', 'contacts', 'did-not-want', longestText);
      longestText = '';
    }
  };

  //  If an agency was selected, notify analytics and redirect
  //  If the footer was selected, submit the form to redirect
  onSelection = function(ev, suggestion) {
    if (suggestion.isFooter) {
      $(ev.target).val(suggestion.query).closest('form').submit();
    }
    else {
      var callback = function() {
        window.location = '/contacts/' + suggestion.slug + '/';
      };
      ga('send', 'event', 'contacts', 'select-' + suggestion.slug,
         currentText, {'hitCallback': callback});
    }
  };

  //  Initialize typeahead
  $('.scrollable-dropdown-menu .typeahead').typeahead({
      hint: false,
      highlight: true,
      minLength: 1
    }, agencyAdaptor, footerAdaptor
  ).on('keyup', onUserStroke).on('typeahead:selected', onSelection);
});
