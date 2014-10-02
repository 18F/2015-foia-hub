from django_assets import Bundle, register


scss_all = Bundle(
    'foia_hub/static/sass/main.scss',
    filters='scss',
    output='foia_hub/static/css/main.css'
)
register('scss_all', scss_all)
