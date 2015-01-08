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
    first_course_year = forms.CharField(max_length = 4)
    std_code = forms.CharField(max_length = 6)
    land_phone = forms.CharField(max_length = 10)
    cell_phone = forms.CharField(max_length = 10)
    fax_number = forms.CharField(max_length = 10)
    
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
        model = InstitutionDetail

class OrganisationForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super(OrganisationForm, self).__init__(*args, **kwargs)
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
        model = Organisation

class TrusteeForm(forms.ModelForm):
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
    def __init__(self, *args, **kwargs):
        super(TrusteeForm, self).__init__(*args, **kwargs)
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
        model = Trustee
        exclude = ['organisation']

class ContactForm(forms.ModelForm):
    state = forms.ModelChoiceField(
        widget = forms.Select(attrs = {'class' : 'ac-state'}), queryset = State.objects.order_by('name'), empty_label = "--- None ---"
    )
    district = forms.ModelChoiceField(
        widget = forms.Select(attrs = {'class' : 'ac-district'}), queryset = District.objects.none(), empty_label = "--- None ---"
    )
    city = forms.ModelChoiceField(
        widget = forms.Select(attrs = {'class' : 'ac-city'}), queryset = City.objects.none(), empty_label = "--- None ---"
    )
    location = forms.ModelChoiceField(
        widget = forms.Select(attrs = {'class' : 'ac-location'}), queryset = Location.objects.none(), empty_label = "--- None ---"
    )
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
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
        model = ContactDetail

class LandForm(forms.ModelForm):
    location = forms.ChoiceField(
        widget = forms.Select(), choices = ((0,'Rural'),(1,'Other than Rural'),)
    )
    ownership_details = forms.ChoiceField(
        widget = forms.Select(), choices = ((0, 'Gift Deed'), (1, 'Government Lease'), (2, 'Registered Sale Deed'), )
    )
    class Meta:
        model = LandDetail

class PerLandDetailForm(forms.ModelForm):
    owner_govt_lease = forms.ChoiceField(
        widget = forms.Select(), choices = ((0, 'Select this if you Own Land'), (1, 'Select this if Land Belongs to Government Lease'), )
    )
    class Meta:
        model = PerLandDetail
        exclude = ['land_detail']

class BuildingDetailForm(forms.ModelForm):
    building_status = forms.ChoiceField(
        widget = forms.Select(), choices = ((0, 'Available'), (1, 'Under Construction'), (2, 'Proposed'), )
    )
    class Meta:
        model = BuildingDetail

class PerBuildingDetailForm(forms.ModelForm):
    class Meta:
        model = PerBuildingDetail
        exclude = ['building_detail']
 
class ProgramDetailForm(forms.ModelForm):
    new_existing = forms.ChoiceField(
        widget = forms.Select(), choices = ((0, 'New'), (1, 'Existing'), )
    )
    class Meta:
        model = ProgramDetail
        exclude = ['application_year']
        
class CourseDetailForm(forms.ModelForm):
    level_of_course = forms.ChoiceField(
        widget = forms.Select(), choices = ((0, 'DIPLOMA'), (1, 'POST DIPLOMA'), (2, 'POST GRADUATE DIPLOMA'), (3, 'POST GRADUATE CERTIFICATE'), (4, 'FELLOWSHIP'), (5, 'UNDER GRADUATE'), (5, 'POST GRADUATE'), )
    )
    shift = forms.ChoiceField(
        widget = forms.Select(), choices = ((0, '1 st Shift'), (1, '2 ed Shift'), )
    )
    course_duration = forms.ChoiceField(
        widget = forms.Select(), choices = ((0, '0.5'), (1, '1'), (1.5, '1.5'), (2, '2'), (2.5, '2.5'), (3, '3'), (3.5, '3.5'), (4, '4'), (4.5, '4.5'), (5, '5'), (5.5, '5.5'), (6, '6'), (6.5, '6.5'), )
    )
    full_part_time = forms.ChoiceField(
        widget = forms.Select(), choices = ((0, 'Full Time'), (1, 'Part Time'), )
    )
    accreditation_status = forms.ChoiceField(
        widget = forms.Select(), choices = ((0, 'ACCRIDITED'), (1, 'NOT ACCRIDITED'), (2, 'NOT ELIGIBLE'), (3, 'ELIGBLE NOT APPLIED'), (4, 'APPLIED PENDING'), (5, 'NOT APPLICABLE'), )
    )
    accreditation_type = forms.ChoiceField(
        widget = forms.Select(), choices = ((0, 'NAAC'), (1, 'NBA'), (2, 'OTHERS'))
    )
    nri = forms.ChoiceField(
        widget = forms.Select(), choices = ((0, 'Not interested'), (1, 'New Request'), (2, 'Applied to Continue'), (3, 'Applied to Closure'), )
    )
    pio = forms.ChoiceField(
        widget = forms.Select(), choices = ((0, 'Not interested'), (1, 'New Request'), (2, 'Applied to Continue'), (3, 'Applied to Closure'), )
    )
    mode_of_conduct = forms.ChoiceField(
        widget = forms.Select(), choices = ((0, 'Regular'), (1, 'Distance'), )
    )
    course_type = forms.ChoiceField(
        widget = forms.Select(), choices = ((0, 'Self-Financed'), (1, 'Aided'), )
    )
    govt_recommendation = forms.ChoiceField(
        widget = forms.Select(), choices = ((0, 'Applied'), (1, 'Not Recommended'), (2, 'Yet to Apply'), (3, 'Not Applicable'), (4, 'Data not Entered'), )
    )
    board_recommendation = forms.ChoiceField(
        widget = forms.Select(), choices = ((0, 'Applied'), (1, 'Not Recommended'), (2, 'Yet to Apply'), (3, 'Not Applicable'), (4, 'Data not Entered'), )
    )
    #status = forms.ChoiceField(
    #    widget = forms.Select(), choices = ((0, 'Not Available'), (1, 'Available'), )
    #)
    class Meta:
        model = CourseDetail
        exclude = ['application']

class FacultyDetailForm(forms.ModelForm):
    state = forms.ModelChoiceField(
        widget = forms.Select(attrs = {'class' : 'ac-state'}), queryset = State.objects.order_by('name'), empty_label = "--- None ---"
    )
    district = forms.ModelChoiceField(
        widget = forms.Select(attrs = {'class' : 'ac-district'}), queryset = District.objects.none(), empty_label = "--- None ---"
    )
    city = forms.ModelChoiceField(
        widget = forms.Select(attrs = {'class' : 'ac-city'}), queryset = City.objects.none(), empty_label = "--- None ---"
    )
    location = forms.ModelChoiceField(
        widget = forms.Select(attrs = {'class' : 'ac-location'}), queryset = Location.objects.none(), empty_label = "--- None ---"
    )
    def __init__(self, *args, **kwargs):
        super(FacultyDetailForm, self).__init__(*args, **kwargs)
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
        model = FacultyDetail
        exclude = ['application_year']

class InstructionalAreaForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(InstructionalAreaForm, self).__init__(*args, **kwargs)
        per_building_detail = forms.ModelChoiceField(label='State', cache_choices=True, queryset = PerBuildingDetail.objects.filter(building_detail__in = ApplicationYear.objects.filter(user = user).values_list('building_id')).values_list('id', 'building_name'), empty_label = "--- None ---", help_text = "", error_messages = {'required':'State field required.'})
        if args:
            if 'per_building_detail' in args[0]:
                per_building_detail = forms.ModelChoiceField(label='State', cache_choices=True, queryset = PerBuildingDetail.objects.filter(building_detail__in = ApplicationYear.objects.filter(user = user).values_list('building_id')).values_list('id', 'building_name'), empty_label = "--- None ---", help_text = "", error_messages = {'required':'State field required.'})
        
    class Meta:
        model = InstructionalArea
        exclude = ('application',)

class CommonFacilitiesForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(CommonFacilitiesForm, self).__init__(*args, **kwargs)
        per_building_detail = forms.ModelChoiceField(label='State', cache_choices=True, queryset = PerBuildingDetail.objects.filter(building_detail__in = ApplicationYear.objects.filter(user = user).values_list('building_id')).values_list('id', 'building_name'), empty_label = "--- None ---", help_text = "", error_messages = {'required':'State field required.'})
        if args:
            if 'per_building_detail' in args[0]:
                per_building_detail = forms.ModelChoiceField(label='State', cache_choices=True, queryset = PerBuildingDetail.objects.filter(building_detail__in = ApplicationYear.objects.filter(user = user).values_list('building_id')).values_list('id', 'building_name'), empty_label = "--- None ---", help_text = "", error_messages = {'required':'State field required.'})
        
    class Meta:
        model = CommonFacilities
        exclude = ['application']

class AmenitiesAreaForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(AmenitiesAreaForm, self).__init__(*args, **kwargs)
        per_building_detail = forms.ModelChoiceField(label='State', cache_choices=True, queryset = PerBuildingDetail.objects.filter(building_detail__in = ApplicationYear.objects.filter(user = user).values_list('building_id')).values_list('id', 'building_name'), empty_label = "--- None ---", help_text = "", error_messages = {'required':'State field required.'})
        if args:
            if 'per_building_detail' in args[0]:
                per_building_detail = forms.ModelChoiceField(label='State', cache_choices=True, queryset = PerBuildingDetail.objects.filter(building_detail__in = ApplicationYear.objects.filter(user = user).values_list('building_id')).values_list('id', 'building_name'), empty_label = "--- None ---", help_text = "", error_messages = {'required':'State field required.'})
        
    class Meta:
        model = AmenitiesArea
        exclude = ['application']

class AdministrativeAreaForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(AdministrativeAreaForm, self).__init__(*args, **kwargs)
        per_building_detail = forms.ModelChoiceField(label='State', cache_choices=True, queryset = PerBuildingDetail.objects.filter(building_detail__in = ApplicationYear.objects.filter(user = user).values_list('building_id')).values_list('id', 'building_name'), empty_label = "--- None ---", help_text = "", error_messages = {'required':'State field required.'})
        if args:
            if 'per_building_detail' in args[0]:
                per_building_detail = forms.ModelChoiceField(label='State', cache_choices=True, queryset = PerBuildingDetail.objects.filter(building_detail__in = ApplicationYear.objects.filter(user = user).values_list('building_id')).values_list('id', 'building_name'), empty_label = "--- None ---", help_text = "", error_messages = {'required':'State field required.'})
        
    class Meta:
        model = AdministrativeArea
        exclude = ['application']

class OtherFacilitiesForm(forms.ModelForm):
    class Meta:
        model = OtherFacilities
        exclude = ['application']
        
class LaboratoryDetailForm(forms.ModelForm):
    class Meta:
        model = LaboratoryDetail
        exclude = ['application']

class LibraryBookForm(forms.ModelForm):
    class Meta:
        model = LibraryBook
        exclude = ['application']
 
class LibraryBookForm(forms.ModelForm):
    class Meta:
        model = LibraryBook 
        exclude = ['application']

class LibraryFacilityForm(forms.ModelForm):
    class Meta:
        model = LibraryFacility
        exclude = ['application']

class ComputationFacilityForm(forms.ModelForm):
    class Meta:
        model = ComputationFacility 
        exclude = ['application']

class TechnicalStaffForm(forms.ModelForm):
    class Meta:
        model = TechnicalStaff 
        exclude = ['application']

class JfdrDetailForm(forms.ModelForm):
    class Meta:
        model = JfdrDetail 
        exclude = ['application']

class FinancialDetailForm(forms.ModelForm):
    class Meta:
        model = FinancialDetail 
        exclude = ['application']

class CirculationAreaForm(forms.ModelForm):
    class Meta:
        model = CirculationArea 
        exclude = ['application']

class OperationalFundForm(forms.ModelForm):
    class Meta:
        model = OperationalFund 
        exclude = ['application']

class AdminLibraryStaffForm(forms.ModelForm):
    state = forms.ModelChoiceField(
        widget = forms.Select(attrs = {'class' : 'ac-state'}), queryset = State.objects.order_by('name'), empty_label = "--- None ---"
    )
    district = forms.ModelChoiceField(
        widget = forms.Select(attrs = {'class' : 'ac-district'}), queryset = District.objects.none(), empty_label = "--- None ---"
    )
    city = forms.ModelChoiceField(
        widget = forms.Select(attrs = {'class' : 'ac-city'}), queryset = City.objects.none(), empty_label = "--- None ---"
    )
    location = forms.ModelChoiceField(
        widget = forms.Select(attrs = {'class' : 'ac-location'}), queryset = Location.objects.none(), empty_label = "--- None ---"
    )
    def __init__(self, *args, **kwargs):
        super(AdminLibraryStaffForm, self).__init__(*args, **kwargs)
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
        model = AdminLibraryStaff 
        exclude = ['application']

class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure 
        exclude = ['application']

class HostelFacilitiesForm(forms.ModelForm):
    class Meta:
        model = HostelFacilities 
        exclude = ['application']

class AntiRaggingForm(forms.ModelForm):
    affidavit_from_student_hostel = forms.ChoiceField(
        widget = forms.Select(), choices = ((0, 'No'), (1, 'Yes'), (2, 'No Hostel'),)
    )
    affidavit_from_parent_hostel = forms.ChoiceField(
        widget = forms.Select(), choices = ((0, 'No'), (1, 'Yes'), (2, 'No Hostel'),)
    )
    class Meta:
        model = AntiRagging 
        exclude = ['application']

class AntiRaggingDetailForm(forms.ModelForm):
    committee_type = forms.ChoiceField(
        widget = forms.Select(), choices = ((0, 'Anti-Ragging Committee'), (1, 'Anti-Ragging Squad'), )
    )
    class Meta:
        model = AntiRaggingDetail 
        exclude = ['antiragging']

class HeadOfInstituteForm(forms.ModelForm):
    class Meta:
        model = HeadOfInstitute 
        exclude = ['application']

class OmbudsmanForm(forms.ModelForm):
    class Meta:
        model = Ombudsman 
        exclude = ['application']

class OmbudsmanDetailForm(forms.ModelForm):
    committee_type = forms.ChoiceField(
        widget = forms.Select(), choices = ((0, 'Grievance Redressal'), (1, 'OMBUDSMAN'), )
    )
    class Meta:
        model = OmbudsmanDetail 
        exclude = ['ombudsman']

class GrantsReceivedForm(forms.ModelForm):
    class Meta:
        model = GrantsReceived 
        exclude = ['application']

class StudentDetailForm(forms.ModelForm):
    class Meta:
        model = StudentDetail 
        exclude = ['application_year']

class EjournalForm(forms.ModelForm):
    class Meta:
        model = Ejournal 
        exclude = ['application']

class LibraryFacilityForm(forms.ModelForm):
    class Meta:
        model = LibraryFacility
        exclude = ['application']

class ComputationFacilityForm(forms.ModelForm):
    class Meta:
        model = ComputationFacility
        exclude = ['application']

class TechnicalStaffForm(forms.ModelForm):
    state = forms.ModelChoiceField(
        widget = forms.Select(attrs = {'class' : 'ac-state'}), queryset = State.objects.order_by('name'), empty_label = "--- None ---"
    )
    district = forms.ModelChoiceField(
        widget = forms.Select(attrs = {'class' : 'ac-district'}), queryset = District.objects.none(), empty_label = "--- None ---"
    )
    city = forms.ModelChoiceField(
        widget = forms.Select(attrs = {'class' : 'ac-city'}), queryset = City.objects.none(), empty_label = "--- None ---"
    )
    location = forms.ModelChoiceField(
        widget = forms.Select(attrs = {'class' : 'ac-location'}), queryset = Location.objects.none(), empty_label = "--- None ---"
    )
    def __init__(self, *args, **kwargs):
        super(TechnicalStaffForm, self).__init__(*args, **kwargs)
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
        model = TechnicalStaff
        exclude = ['application']

class JfdrDetailForm(forms.ModelForm):
    class Meta:
        model = JfdrDetail
        exclude = ['application']

class FinancialDetailForm(forms.ModelForm):
    class Meta:
        model = FinancialDetail
        exclude = ['application']

class CirculationAreaForm(forms.ModelForm):
    area_type = forms.ChoiceField(
        widget = forms.Select(), choices = ((0, 'Corridors'), (1, 'Other Common Area(in Sqm)'), (2, 'other areas (in Sqm)'), )
    )
    class Meta:
        model = CirculationArea
        exclude = ['application']
