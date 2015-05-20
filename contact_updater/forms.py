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
STATE_CHOICES = list(STATE_CHOICES)
STATE_CHOICES.insert(0, ('', '---------'))


class AgencyForm(forms.Form):

    slug = forms.CharField(widget=forms.HiddenInput())

    # Description
    description = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'description'}))

    # Public Liaison
    public_liaison_name = forms.CharField(
        label='Name',
        required=False,
        widget=forms.TextInput(attrs={'class': 'public_liaison_name'}))
    public_liaison_email = forms.EmailField(
        label='Email',
        required=False,
        widget=forms.EmailInput(attrs={'class': 'public_liaison_email'}))
    public_liaison_phone = forms.RegexField(
        label='Phone Number',
        required=False,
        regex=PHONE_RE,
        error_message=('Must contain a valid phone number'),
        widget=forms.TextInput(attrs={'class': 'public_liaison_phone'}))

    # Request Center
    phone = forms.RegexField(
        label='Phone Number',
        required=False,
        regex=PHONE_RE,
        error_message=('Must contain a valid phone number'),
        widget=forms.TextInput(attrs={'class': 'phone'}))

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
        widget=forms.TextInput(attrs={'class': 'zip_code'}))
    office_url = forms.URLField(
        label="Website URL",
        required=False,
        widget=forms.URLInput(attrs={'class': 'office_url'}))
    emails = forms.EmailField(
        label='Email',
        required=False,
        widget=forms.EmailInput(attrs={'class': 'email'}))

    fax = forms.RegexField(
        label='Fax Number',
        required=False,
        regex=PHONE_RE,
        error_message=('Must contain a valid phone number'),
        widget=forms.TextInput(attrs={'class': 'fax'}))

    # Other
    component_url = forms.URLField(
        label="Agency/component website",
        required=False,
        widget=forms.URLInput(attrs={'class': 'component_url'}))
    foia_libraries = forms.URLField(
        label="Reading room website",
        required=False,
        widget=forms.URLInput(attrs={'class': 'foia_libraries'}))
    regulations_website = forms.URLField(
        label="Regulations Website", required=False)
    common_requests = forms.CharField(
        label='Commonly requested topics',
        required=False,
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'common_requests'}))
    no_records_about = forms.CharField(
        label='Commonly misdirected topics',
        required=False,
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'no_records_about'}))
    request_instructions = forms.CharField(
        label='Request instructions',
        required=False,
        widget=forms.Textarea(
            attrs={'rows': 4, 'class': 'request_instructions'}))
