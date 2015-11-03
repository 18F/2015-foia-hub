from django import forms
from localflavor.us.forms import USStateField, USZipCodeField
from localflavor.us.us_states import STATE_CHOICES

PHONE_RE = (
    r"""(?P<prefix>\+?[\d\s\(\)\-]*)"""
    r"""(?P<area_code>\(?\d{3}\)?[\s\-\(\)]*)"""
    r"""(?P<first_three>\d{3}[\-\s\(\)]*)"""
    r"""(?P<last_four>\d{4}[\-\s]*)"""
    r"""(?P<extension>[\s\(,]*?ext[ .]*?\d{3,5})?"""
    r"""(?P<tty>\s*\(tty)?"""
)
PHONE_PATTERN = '(?:\(\d{3}\)|\d{3})[- ]?\d{3}[- ]?\d{4}'
STATE_CHOICES = list(STATE_CHOICES)
STATE_CHOICES.insert(0, ('', '---------'))


class AgencyForm(forms.Form):

    slug = forms.CharField(widget=forms.HiddenInput())

    # Description
    description = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'agency_description',
            'maxlength': 500}))

    # Chief Foia officer
    chief_officer_name = forms.CharField(
        label='Name',
        required=False,
        widget=forms.TextInput(attrs={'class': 'chief_officer_name'}))
    chief_officer_email = forms.EmailField(
        label='Email',
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'chief_officer_email',
            'data-parsley-type-message': 'Please enter a valid email.'
        }))
    chief_officer_phone = forms.RegexField(
        label='Phone Number',
        required=False,
        regex=PHONE_RE,
        widget=forms.TextInput(attrs={
            'class': 'chief_officer_phone',
            'data-parsley-pattern-message':
                'Please enter a valid phone number.',
            'pattern': PHONE_PATTERN}))

    # Public Liaison
    public_liaison_name = forms.CharField(
        label='Name',
        required=False,
        widget=forms.TextInput(attrs={'class': 'public_liaison_name'}))
    public_liaison_email = forms.EmailField(
        label='Email',
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'public_liaison_email',
            'data-parsley-type-message': 'Please enter a valid email.'
        }))
    public_liaison_phone = forms.RegexField(
        label='Phone Number',
        required=False,
        regex=PHONE_RE,
        widget=forms.TextInput(attrs={
            'class': 'public_liaison_phone',
            'data-parsley-pattern-message':
                'Please enter a valid phone number.',
            'pattern': PHONE_PATTERN}))

    # Request Center
    phone = forms.RegexField(
        label='Phone Number',
        required=False,
        regex=PHONE_RE,
        widget=forms.TextInput(attrs={
            'class': 'phone',
            'data-parsley-pattern-message':
                'Please enter a valid phone number.',
            'pattern': PHONE_PATTERN}))

    # FOIA Request Submission
    address_line_1 = forms.CharField(
        label='Mailing address 1',
        required=False,
        widget=forms.TextInput(attrs={'class': 'address_line_1'}))
    address_line_2 = forms.CharField(
        label='Mailing address 2',
        required=False,
        widget=forms.TextInput(attrs={'class': 'address_line_2'}))
    city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'city'}))
    state = USStateField(
        required=False,
        widget=forms.Select(
            choices=STATE_CHOICES, attrs={'class': 'state'}))
    zip_code = USZipCodeField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'zip_code',
            'data-parsley-pattern-message': 'Please enter a valid zip code.',
            'pattern': '\d{5,5}(-\d{4,4})?'}))
    office_url = forms.URLField(
        label="Website URL",
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'office_url',
            'data-parsley-type-message': 'Please enter a valid url.',
        }))
    emails = forms.EmailField(
        label='Email',
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'email',
            'data-parsley-type-message': 'Please enter a valid email.',
        }))
    fax = forms.RegexField(
        label='Fax Number',
        required=False,
        regex=PHONE_RE,
        error_message=('Must contain a valid phone number'),
        widget=forms.TextInput(attrs={
            'class': 'fax',
            'data-parsley-pattern-message': 'Please enter a valid fax number.',
            'pattern': PHONE_PATTERN}))

    # Other
    component_url = forms.URLField(
        label="Agency/component website",
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'component_url',
            'data-parsley-type-message': 'Please enter a valid url.',
        }))
    foia_libraries = forms.URLField(
        label="FOIA library website",
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'foia_libraries',
            'data-parsley-type-message': 'Please enter a valid url.',
        }))
    regulations_website = forms.URLField(
        label="Regulations website",
        required=False,
        widget=forms.URLInput(attrs={
            'data-parsley-type-message': 'Please enter a valid url.'
        }))
    common_requests = forms.CharField(
        label='Commonly requested topics',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'common_requests',
            'maxlength': 500}))
    no_records_about = forms.CharField(
        label='Commonly misdirected topics',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'no_records_about',
            'maxlength': 500}))
    request_instructions = forms.CharField(
        label='Request instructions',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'request_instructions',
            'maxlength': 500}))
