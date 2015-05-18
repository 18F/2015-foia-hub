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
        widget=forms.Textarea(attrs={'rows': 3}))

    # Public Liaison
    public_liaison_name = forms.CharField(label='Name', required=False)
    public_liaison_email = forms.EmailField(label='Email', required=False)
    public_liaison_phone = forms.RegexField(
        label='Phone Number',
        required=False,
        regex=PHONE_RE,
        error_message=('Must contain a valid phone number'))

    # Request Center
    phone = forms.RegexField(
        label='Phone Number',
        required=False,
        regex=PHONE_RE,
        error_message=('Must contain a valid phone number'))

    # FOIA Request Submission
    address_line_1 = forms.CharField(label='Mailing address 1', required=False)
    address_line_2 = forms.CharField(label='Mailing address 2', required=False)
    city = forms.CharField(required=False)
    state = USStateField(
        widget=forms.Select(choices=STATE_CHOICES), required=False)
    zip_code = USZipCodeField(required=False)

    office_url = forms.URLField(
        label="Website URL", required=False, initial='http://')
    emails = forms.EmailField(label='Email', required=False)

    fax = forms.RegexField(
        label='Fax Number',
        required=False,
        regex=PHONE_RE,
        error_message=('Must contain a valid phone number'))

    # Other
    component_url = forms.URLField(
        label="Agency/component website", required=False, initial='http://')
    foia_libraries = forms.URLField(
        label="Reading room website", required=False, initial='http://')
    regulations_website = forms.URLField(
        label="Regulations Website", required=False, initial='http://')
    common_requests = forms.CharField(
        label='Commonly requested topics',
        required=False, widget=forms.Textarea(attrs={'rows': 4}))
    no_records_about = forms.CharField(
        label='Commonly misdirected topics',
        required=False, widget=forms.Textarea(attrs={'rows': 4}))
    request_instructions = forms.CharField(
        label='Request instructions',
        required=False, widget=forms.Textarea(attrs={'rows': 4}))
