from django import forms

PHONE_RE = (
    r"""(?P<prefix>\+?[\d\s\(\)\-]*)"""
    r"""(?P<area_code>\(?\d{3}\)?[\s\-\(\)]*)"""
    r"""(?P<first_three>\d{3}[\-\s\(\)]*)"""
    r"""(?P<last_four>\d{4}[\-\s]*)"""
    r"""(?P<extension>[\s\(,]*?ext[ .]*?\d{3,5})?"""
    r"""(?P<tty>\s*\(tty)?"""
)


class AgencyData(forms.Form):

    slug = forms.CharField(widget=forms.HiddenInput())

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}))

    public_liaison_name = forms.CharField(required=False)
    public_liaison_email = forms.EmailField(required=False)
    public_liaison_phone = forms.RegexField(
        required=False,
        regex=PHONE_RE,
        error_message=('Must contain a valid phone number'))

    phone = forms.RegexField(
        label='Public Phone Number',
        required=False,
        regex=PHONE_RE,
        error_message=('Must contain a valid phone number'))

    fax = forms.RegexField(
        label='Public Fax Number',
        required=False,
        regex=PHONE_RE,
        error_message=('Must contain a valid phone number'))

    request_form_url = forms.URLField(
        label='Request Form Link', required=False)
    foia_libraries = forms.CharField(
        label='Public Reading Room/FOIA Library Link', required=False)
    office_url = forms.URLField(required=False)

    address_lines = forms.CharField(
        label='Recipient', required=False,
        widget=forms.Textarea(attrs={'rows': 3}))
    street = forms.CharField(required=False)
    state = forms.CharField(required=False)
    city = forms.CharField(required=False)
    zip_code = forms.CharField(required=False)

    common_requests = forms.CharField(
        label='Commonly Requested Topics',
        help_text='(Types of requests which this office receives often)',
        required=False, widget=forms.Textarea(attrs={'rows': 3}))
    no_records_about = forms.CharField(
        label='Commonly Misdirected Topics',
        help_text='(Misdirected requests which this office receives often)',
        required=False, widget=forms.Textarea(attrs={'rows': 3}))
