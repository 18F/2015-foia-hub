(function() {

  var COLLAPSE_THRESHOLD = 480,
      KLASS = 'collapsed',
      collapsed = false;

  var nav = $('nav')
    .data(KLASS, false)
    .on('click tap', toggle);

  $(window).on('resize', throttle(resize, 100));
  resize();

  function resize() {
    var width = window.innerWidth;
    var shouldCollapse = width < COLLAPSE_THRESHOLD;
    console.log(width, 'should collapse?', shouldCollapse, 'is collapsed?', collapsed);

    if (shouldCollapse && !collapsed) {
      console.log('collapsing nav');
      nav.addClass(KLASS).data(KLASS, true);
      collapsed = true;
    } else if (!shouldCollapse && collapsed) {
      console.log('expanding nav');
      nav.removeClass(KLASS).data(KLASS, false);
      collapsed = false;
    } else {
      console.log('no state change (', shouldCollapse, collapsed, ')');
    }
    updateIcon();
  }

  function toggle() {
    collapsed = !collapsed;
    nav.toggleClass(KLASS, collapsed);
    updateIcon();
  }

  function updateIcon() {
    var collapsed = nav.hasClass(KLASS),
        icon = nav.find('.fa'),
        match = icon.attr('class').match(/(fa-\w+-)/),
        prefix = match ? match[1] : '';
    icon
      .toggleClass(prefix + 'down', collapsed)
      .toggleClass(prefix + 'up', !collapsed);
  }

  function throttle(fn, time) {
    var timeout;
    return function() {
      if (timeout) return;
      var that = this;
      var args = arguments;
      fn.apply(that, args);
      timeout = setTimeout(function() {
        clearTimeout(timeout);
        timeout = null;
      }, time);
    };
  }

})();
