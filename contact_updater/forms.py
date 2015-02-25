from django import forms


class AgencyData(forms.Form):

    description = forms.CharField(required=False, widget=forms.Textarea)

    public_liaison_name = forms.CharField(required=False)
    public_liaison_email = forms.EmailField(required=False)
    public_liaison_phone = forms.RegexField(
        required=False,
        regex=r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$',
        error_message=('Must contain a valid phone number'))

    phone = forms.RegexField(
        label='Public Phone Number',
        required=False,
        regex=r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$',
        error_message=('Must contain a valid phone number'))

    fax = forms.RegexField(
        label='Public Fax Number',
        required=False,
        regex=r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$',
        error_message=('Must contain a valid phone number'))

    request_form_url = forms.URLField(
        label='Request Form Link', required=False)
    foia_libraries = forms.CharField(
        label='Public Reading Room/FOIA Library Link', required=False)
    office_url = forms.URLField(required=False)

    # Will need to reformat the value
    address_lines = forms.CharField(
        label='Recipient', required=False, widget=forms.Textarea)
    street = forms.CharField(required=False)
    state = forms.CharField(required=False)
    city = forms.CharField(required=False)
    zip_code = forms.CharField(required=False)

    common_requests = forms.CharField(
        label='Commonly Requested Topics',
        help_text='(Types of requests which this office recives often)',
        required=False, widget=forms.Textarea)
    no_records_about = forms.CharField(
        label='Commonly Misdirected Topics',
        help_text='(Misdirected requests which this office recives often)',
        required=False, widget=forms.Textarea)
