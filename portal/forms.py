from django import forms
from django.forms import ModelForm
from portal.models import *

class InstitutionDetailForm(forms.ModelForm):
    state = forms.ModelChoiceField(
        widget = forms.Select(attrs = {'class' : 'ac-state'}), queryset = State.objects.order_by('name'), empty_label = "--- None ---"
    )
    district = forms.ModelChoiceField(
        label='District',  widget = forms.Select(attrs = {'class' : 'ac-district'}), queryset = District.objects.none(), empty_label = "--- None ---"
    )
    city = forms.ModelChoiceField(
        label='City',  widget = forms.Select(attrs = {'class' : 'ac-city'}), queryset = City.objects.none(), empty_label = "--- None ---"
    )
    location = forms.ModelChoiceField(
        label='Location',  widget = forms.Select(attrs = {'class' : 'ac-location'}), queryset = Location.objects.none(), empty_label = "--- None ---"
    )
    id = forms.CharField(widget = forms.HiddenInput(attrs={'class': 'special'}), required = False)

    def __init__(self, *args, **kwargs):
        super(InstitutionDetailForm, self).__init__(*args, **kwargs)
        #prevent ajax loaded data
        if args:
            if 'district' in args[0]:
                if args[0]['district'] and args[0]['district'] != '' and args[0]['district'] != 'None':
                    self.fields["location"].queryset = Location.objects.filter(district__id=args[0]['district'])

            if 'state' in args[0]:
                if args[0]['state'] != '' and args[0]['state'] != 'None':
                    self.fields["district"].queryset = District.objects.filter(state__id=args[0]['state'])
                    self.fields["city"].queryset = City.objects.filter(state__id=args[0]['state'])

        if 'instance' in kwargs:
            initial = kwargs["instance"]
            self.fields["location"].queryset = Location.objects.filter(district__id=initial.district_id)
            self.fields["district"].queryset = District.objects.filter(state__id=initial.state_id)
            self.fields["city"].queryset = City.objects.filter(state__id=initial.state_id)

    class Meta:
        model = Institution_Detail

