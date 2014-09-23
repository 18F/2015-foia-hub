'use strict';
$('body').ready(function() {
  var currentText = '',
      agencies = new Bloodhound({
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        prefetch: '/request/autocomplete',
        datumTokenizer: function(d) {
          return []
            .concat(Bloodhound.tokenizers.whitespace(d.name))
            .concat(Bloodhound.tokenizers.whitespace(d.description))
            .concat(Bloodhound.tokenizers.whitespace(d.abbreviation))
            .concat(Bloodhound.tokenizers.whitespace(
              d.keywords ? d.keywords.join(' ') : []))
          ;
        }});

  // always clear local storage for new requests, at least in dev
  agencies.clearPrefetchCache();
  agencies.initialize();

  $('.scrollable-dropdown-menu .typeahead').typeahead({
      hint: false,
      highlight: true,
      minLength: 1
    },
    {
      name: 'agencies',
      displayKey: 'value',
      source: agencies.ttAdapter(),
      templates: {
        suggestion: Handlebars.compile(
          [
            '<h5 class="agency-name">{{name}}</h5>',
            '<p class="agency-description">{{description}}</p>'
          ].join('')
        )
      }
    }
  //  Track the entry as the user types
  ).bind('keyup', function(ev) {
    currentText = $(ev.target).val();
  //  Option was selected - notify analytics and redirect
  }).bind('typeahead:selected', function(ev, suggestion) {
    var callback = function() {
      window.location = '/request/' + suggestion.slug + '/';
    };
    ga('send', 'event', 'contacts', 'select-' + suggestion.slug,
       currentText, {'hitCallback': callback});
  });

  // disable form submission
  $('form').submit(function() { return false; });

  $('input.agency').focus();
});
