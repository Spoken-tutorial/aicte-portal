from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

from portal.forms import *
from portal.models import *
import json

def current_year():
    return datetime.now().year
    
def get_application_id(user):
    try:
        return Application.objects.filter(user = user).first()
    except:
        return 0
    
@login_required
def home(request):
    user = request.user
    application_years = ApplicationYear.objects.filter(application = Application.objects.filter(user = user).last())
    context = {
        'application_years': application_years
    }
    return render(request, 'portal/templates/home.html', context)

@login_required
def application_year(request, application_year):
    user = request.user
    application_year = ApplicationYear.objects.select_related().filter(academic_year = application_year)
    if application_year:
        context = {
            'application_year': application_year
        }
        return render(request, 'portal/templates/application_year.html', context)
    else:
        print "404"

def application_base(request, param):
    user = request.user
    year = datetime.now()
    application_year = ''
    new_application = 0
    try:
       application = Application.objects.get(user_id = user.id)
    except ObjectDoesNotExist:
        application = Application()
        application.user_id = user.id
        application.institution_number = user.id
        application.save()
    last_year = ApplicationYear.objects.filter(application = application, academic_year = year.year-1).last()
    application_count = ApplicationYear.objects.filter(application = application).count()
    if not last_year:
            new_application = 1
    new_application_year = 1
    is_edit = 0
    if application_count >= 1:
        application_year = ApplicationYear.objects.filter(application = application, academic_year = year.year).last()
        if application_year:
            try:
                print 'Last Year: ' + str(last_year)
                param_val = getattr(application_year, param)
                if param_val != None:
                    is_edit = 1
                    if last_year and param_val == getattr(last_year, param):
                        is_edit = 2
                else:
                    if last_year:
                        setattr(application_year, param, getattr(last_year, param))
                        application_year.save()
                        is_edit = 2
                new_application_year = 0
            except:
                is_edit = 0
    print 'is_edit: ' + str(is_edit)
    if new_application_year:
        application_year = ApplicationYear()
        application_year.user_id = user.id
        application_year.application_id = application.id
        application_year.academic_year = year.year
        if new_application:
            application_year.application_type = 1
            application_year.chapter = 1
        else:
            application_year.application_type = 2
            application_year.chapter = int(last_year.chapter) + 1
        application_year.approval_status = 0
        application_year.current_application_id = str(application_year.chapter) +'-'+ str(application.id)
        application_year.application_opened = ''
        application_year.application_submitted = ''
        application_year.save()

    appDetails = {}
    appDetails['academic_year'] = str(year.year) + ' - ' + str(year.year + 1)
    appDetails['application'] = application.institution_number
    appDetails['status'] = 'New'
    return [application_year, is_edit, appDetails]

@login_required
def extension(request):
    base_data = application_base(request, 'institution_id')
    application_year = base_data[0]
    is_edit = base_data[1]
    appDetails = base_data[2]
    alert_success = ''
    alert_danger = ''

    if request.method == 'POST':
        form = InstitutionDetailForm(request.POST)
        if form.is_valid():
            institution = InstitutionDetail.objects.filter(institution_name = form.cleaned_data['institution_name'], state = form.cleaned_data['state'], district = form.cleaned_data['district'], location = form.cleaned_data['location'],  city = form.cleaned_data['city'], institution_type = form.cleaned_data['institution_type'], unaided_courses = form.cleaned_data['unaided_courses'], women_institute = form.cleaned_data['women_institute'], co_ed = form.cleaned_data['co_ed']).last()
            save_flag = 0
            if institution or is_edit == 1:
                institution = InstitutionDetail.objects.get(pk = application_year.institution_id)
                form = InstitutionDetailForm(request.POST, instance = institution)
                if form.is_valid():
                    save_flag = 1
            else:
                save_flag = 1
            if save_flag:
                institution = form.save()
                application_year.institution_id = institution.id
                application_year.save()
    else:
        form = InstitutionDetailForm()
        if is_edit:
            form = InstitutionDetailForm(instance = application_year.institution)
    context = {
        'form': form,
        'appDetails': appDetails,
        'alert_success': alert_success,
        'alert_danger': alert_danger
    }
    return render(request, 'portal/templates/extension.html', context)

@login_required
def organisation(request):
    base_data = application_base(request, 'organisation_id')
    application_year = base_data[0]
    is_edit = base_data[1]
    appDetails = base_data[2]
    alert_success = ''
    alert_danger = ''
    rid = 0
    if request.method == 'POST':
        form = OrganisationForm(request.POST)
        if form.is_valid():
            organisation = Organisation.objects.filter(name = form.cleaned_data['name'], organisation_type = form.cleaned_data['organisation_type'], state = form.cleaned_data['state'], district = form.cleaned_data['district'], location = form.cleaned_data['location'], city = form.cleaned_data['city']).last()
            save_flag = 0
            if organisation or is_edit == 1:
                organisation = Organisation.objects.get(pk = application_year.organisation_id)
                form = OrganisationForm(request.POST, instance = organisation)
                if form.is_valid():
                    save_flag = 1
            else:
                save_flag = 1
            if save_flag:
                organisation = form.save()
                application_year.organisation_id = organisation.id
                application_year.save()
    else:
        form = OrganisationForm()
        if is_edit:
            form = OrganisationForm(instance = application_year.organisation)
            rid = application_year.organisation.id
    context = {
        'form': form,
        'rid': rid,
        'appDetails': appDetails,
        'alert_success': alert_success,
        'alert_danger': alert_danger
    }
    return render(request, 'portal/templates/organisation.html', context)

def trustee(request, organisation_id, trustee_id = None):
    if request.method == 'POST':
        form = TrusteeForm(request.POST)
        if form.is_valid():
            trustee = Trustee()
            if trustee_id:
                trustee.id = trustee_id
            trustee.organisation_id = organisation_id
            trustee.title = form.cleaned_data['title']
            trustee.first_name = form.cleaned_data['first_name']
            trustee.middle_name = form.cleaned_data['middle_name']
            trustee.last_name = form.cleaned_data['last_name']
            trustee.designation = form.cleaned_data['designation']
            trustee.dob = form.cleaned_data['dob']
            trustee.trustee_since = form.cleaned_data['trustee_since']
            trustee.trustee_till = form.cleaned_data['trustee_till']
            trustee.email = form.cleaned_data['email']
            trustee.pan = form.cleaned_data['pan']
            trustee.profession = form.cleaned_data['profession']
            trustee.academic_qualification = form.cleaned_data['academic_qualification']
            trustee.state = form.cleaned_data['state']
            trustee.district = form.cleaned_data['district']
            trustee.location = form.cleaned_data['location']
            trustee.city = form.cleaned_data['city']
            trustee.address1 = form.cleaned_data['address1']
            trustee.address2 = form.cleaned_data['address2']
            trustee.std_code = form.cleaned_data['std_code']
            trustee.land_phone = form.cleaned_data['land_phone']
            trustee.cell_phone = form.cleaned_data['cell_phone']
            trustee.save()
            return HttpResponseRedirect("/portal/organisation/")
            
    else:
        form = TrusteeForm()
        if trustee_id:
            try:
                trustee = Trustee.objects.get(pk = trustee_id)
                form = TrusteeForm(instance = trustee)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/trustee.html', context)

def contact(request):
    base_data = application_base(request, 'contact_id')
    application_year = base_data[0]
    is_edit = base_data[1]
    appDetails = base_data[2]
    alert_success = ''
    alert_danger = ''
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = ContactDetail.objects.filter(first_name = form.cleaned_data['first_name'], last_name = form.cleaned_data['last_name'], state = form.cleaned_data['state'], district = form.cleaned_data['district'], location = form.cleaned_data['location'], city = form.cleaned_data['city'], designation = form.cleaned_data['designation']).last()
            save_flag = 0
            if contact or is_edit == 1:
                contact = ContactDetail.objects.get(pk = application_year.contact_id)
                form = ContactForm(request.POST, instance = contact)
                if form.is_valid():
                    save_flag = 1
            else:
                save_flag = 1
            if save_flag:
                contact = form.save()
                application_year.contact_id = contact.id
                application_year.save()
    else:
        form = ContactForm()
        if is_edit:
            form = ContactForm(instance = application_year.contact)
            rid = application_year.contact.id
    context = {
        'form': form,
        'appDetails': appDetails,
        'alert_success': alert_success,
        'alert_danger': alert_danger
    }
    return render(request, 'portal/templates/contact.html', context)
    
def land(request):
    base_data = application_base(request, 'land_id')
    application_year = base_data[0]
    is_edit = base_data[1]
    appDetails = base_data[2]
    alert_success = ''
    alert_danger = ''
    rid = 0
    if request.method == 'POST':
        form = LandForm(request.POST)
        if form.is_valid():
            land = LandDetail.objects.filter(location = form.cleaned_data['location'], total_area_acres = form.cleaned_data['total_area_acres'], land_reg_with = form.cleaned_data['land_reg_with'], date_of_reg = form.cleaned_data['date_of_reg'], north_hilly_area = form.cleaned_data['north_hilly_area'], no_of_pieces = form.cleaned_data['no_of_pieces'], max_distance = form.cleaned_data['max_distance'], land_cert_issued_by = form.cleaned_data['land_cert_issued_by'], land_cert_issued_date = form.cleaned_data['land_cert_issued_date'], ownership_details = form.cleaned_data['ownership_details'], land_mordgaged = form.cleaned_data['land_mordgaged']).last()
            save_flag = 0
            if land or is_edit == 1:
                land = LandDetail.objects.get(pk = application_year.land_id)
                form = LandForm(request.POST, instance = land)
                if form.is_valid():
                    save_flag = 1
            else:
                save_flag = 1
            if save_flag:
                land = form.save()
                application_year.land_id = land.id
                application_year.save()
    else:
        form = LandForm()
        if is_edit:
            form = LandForm(instance = application_year.land)
            rid = application_year.land.id
    context = {
        'form': form,
        'rid': rid,
        'appDetails': appDetails,
        'alert_success': alert_success,
        'alert_danger': alert_danger
    }
    return render(request, 'portal/templates/land.html', context)

def perland(request, land_id, perland_id = None):
    if request.method == 'POST':
        form = PerLandDetailForm(request.POST)
        if form.is_valid():
            perland = PerLandDetail()
            if perland_id:
                perland.id = perland_id
            perland.land_detail_id = land_id
            perland.land_reg_no = form.cleaned_data['land_reg_no']
            perland.date_of_reg = form.cleaned_data['date_of_reg']
            perland.area_of_land = form.cleaned_data['area_of_land']
            perland.khasra_number = form.cleaned_data['khasra_number']
            perland.plot_survey_no = form.cleaned_data['plot_survey_no']
            perland.land_situated = form.cleaned_data['land_situated']
            perland.land_reg_name = form.cleaned_data['land_reg_name']
            perland.owner_govt_lease = form.cleaned_data['owner_govt_lease']
            perland.land_cert_issued = form.cleaned_data['land_cert_issued']
            perland.land_cert_authority = form.cleaned_data['land_cert_authority']
            perland.is_mortgaged = form.cleaned_data['is_mortgaged']
            perland.bank_mortgaged = form.cleaned_data['bank_mortgaged']
            perland.land_required = form.cleaned_data['land_required']
            perland.land_available = form.cleaned_data['land_available']
            perland.save()
            
    else:
        form = PerLandDetailForm()
        if perland_id:
            try:
                perland = PerLandDetail.objects.get(pk = perland_id)
                form = PerLandDetailForm(instance = perland)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/perland.html', context)

def building(request):
    base_data = application_base(request, 'building_id')
    application_year = base_data[0]
    is_edit = base_data[1]
    appDetails = base_data[2]
    alert_success = ''
    alert_danger = ''
    rid = 0
    if request.method == 'POST':
        form = BuildingDetailForm(request.POST)
        if form.is_valid():
            building = BuildingDetail.objects.filter(building_status = form.cleaned_data['building_status'], built_area_planned = form.cleaned_data['built_area_planned'], built_area_ready = form.cleaned_data['built_area_ready'], carpet_area_instructional = form.cleaned_data['carpet_area_instructional'], carpet_area_admin = form.cleaned_data['carpet_area_admin'], carpet_area_amenities = form.cleaned_data['carpet_area_amenities'], funds_allocated = form.cleaned_data['funds_allocated'], loans = form.cleaned_data['loans'], own_share = form.cleaned_data['own_share']).last()
            save_flag = 0
            if building or is_edit == 1:
                building = BuildingDetail.objects.get(pk = application_year.building_id)
                form = BuildingDetailForm(request.POST, instance = building)
                if form.is_valid():
                    save_flag = 1
            else:
                save_flag = 1
            if save_flag:
                building = form.save()
                application_year.building_id = building.id
                application_year.save()
    else:
        form = BuildingDetailForm()
        if is_edit:
            form = BuildingDetailForm(instance = application_year.building)
            rid = application_year.building.id
    context = {
        'form': form,
        'rid': rid,
        'appDetails': appDetails,
        'alert_success': alert_success,
        'alert_danger': alert_danger
    }
    return render(request, 'portal/templates/building.html', context)

def perbuilding(request, building_id, perbuilding_id = None):
    if request.method == 'POST':
        form = PerBuildingDetailForm(request.POST)
        if form.is_valid():
            perbuilding = PerBuildingDetail()
            if perbuilding_id:
                perbuilding.id = perbuilding_id
            perbuilding.building_detail_id = building_id
            perbuilding.building_name = form.cleaned_data['building_name']
            perbuilding.building_number = form.cleaned_data['building_number']
            perbuilding.sanct_build_area = form.cleaned_data['sanct_build_area']
            perbuilding.const_build_area = form.cleaned_data['const_build_area']
            perbuilding.approved_carpet_area_inst = form.cleaned_data['approved_carpet_area_inst']
            perbuilding.const_carpet_area_inst = form.cleaned_data['const_carpet_area_inst']
            perbuilding.approved_carpet_area_admin = form.cleaned_data['approved_carpet_area_admin']
            perbuilding.const_carpet_area_admin = form.cleaned_data['const_carpet_area_admin']
            perbuilding.approved_carpet_area_amen = form.cleaned_data['approved_carpet_area_amen']
            perbuilding.const_carpet_area_amen = form.cleaned_data['const_carpet_area_amen']
            perbuilding.total_area_approved = form.cleaned_data['total_area_approved']
            perbuilding.total_area_constructed = form.cleaned_data['total_area_constructed']
            perbuilding.activities_conducted = form.cleaned_data['activities_conducted']
            perbuilding.non_aicte_courses = form.cleaned_data['non_aicte_courses']
            perbuilding.approving_authority = form.cleaned_data['approving_authority']
            perbuilding.approval_date = form.cleaned_data['approval_date']
            perbuilding.approval_number = form.cleaned_data['approval_number']
            perbuilding.save()
            
    else:
        form = PerBuildingDetailForm()
        if perbuilding_id:
            try:
                perbuilding = PerBuildingDetail.objects.get(pk = perbuilding_id)
                form = PerBuildingDetailForm(instance = perbuilding)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/perbuilding.html', context)

def faculty(request, application_year_id = None, faculty_detail_id = None):
    user = request.user
    if application_year_id == None and faculty_detail_id == None:
        application_year =  ApplicationYear.objects.get(academic_year = current_year, user = user)
        faculty_details = FacultyDetail.objects.filter(application_year = application_year)
        context = {
            'faculty_details': faculty_details,
            'application_year': application_year.id
        }
        return render(request, 'portal/templates/faculty_details_index.html', context)
        
    if request.method == 'POST':
        form = FacultyDetailForm(request.POST)
        print " validatind..."
        if form.is_valid():
            form_data = form.save(commit=False)
            if faculty_detail_id:
                form_data.id = faculty_detail_id
            form_data.application_year_id = application_year_id
            form_data.save()
            return HttpResponseRedirect("/portal/faculty-details/")
    else:
        form = FacultyDetailForm()
        if faculty_detail_id:
            try:
                faculty_detail = FacultyDetail.objects.get(pk = faculty_detail_id)
                form = FacultyDetailForm(instance = faculty_detail)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/faculty_details.html', context)

def program_detail(request, application_year_id = None, program_detail_id = None):
    user = request.user
    if application_year_id == None and program_detail_id == None:
        application_year =  ApplicationYear.objects.get(academic_year = current_year, user = user)
        program_details = ProgramDetail.objects.filter(application_year = application_year)
        context = {
            'program_details': program_details,
            'application_year': application_year.id
        }
        return render(request, 'portal/templates/program_detail_index.html', context)
        
    if request.method == 'POST':
        form = ProgramDetailForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            if program_detail_id:
                form_data.id = program_detail_id
            form_data.application_year_id = application_year_id
            form_data.save()
            return HttpResponseRedirect("/portal/program-details/")
    else:
        form = ProgramDetailForm()
        if program_detail_id:
            try:
                program_detail = ProgramDetail.objects.get(pk = program_detail_id)
                form = ProgramDetailForm(instance = program_detail)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/program_detail.html', context)

def course_detail(request, application_id = None, course_detail_id = None):
    user = request.user
    if application_id == None and course_detail_id == None:
        application =  Application.objects.get(user = user)
        course_details = CourseDetail.objects.filter(application = application)
        context = {
            'course_details': course_details,
            'application': application.id
        }
        return render(request, 'portal/templates/course_detail_index.html', context)
        
    if request.method == 'POST':
        form = CourseDetailForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            if course_detail_id:
                form_data.id = course_detail_id
            form_data.application_id = application_id
            form_data.save()
            return HttpResponseRedirect("/portal/course-details/")
    else:
        form = CourseDetailForm()
        if course_detail_id:
            try:
                program_detail = CourseDetail.objects.get(pk = course_detail_id)
                form = CourseDetailForm(instance = program_detail)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/course_detail.html', context)

def instructionalarea(request, application_id = None, instructionalarea_id = None):
    user = request.user
    if application_id == None and instructionalarea_id == None:
        application =  Application.objects.get(user = user)
        instructionalareas = InstructionalArea.objects.filter(application = application)
        context = {
            'instructionalareas': instructionalareas,
            'application': application.id
        }
        return render(request, 'portal/templates/instructional_area_index.html', context)
        
    if request.method == 'POST':
        form = InstructionalAreaForm(user, request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            if instructionalarea_id:
                form_data.id = instructionalarea_id
            form_data.application_id = application_id
            form_data.save()
            return HttpResponseRedirect("/portal/instructional-area/")
    else:
        form = InstructionalAreaForm(user)
        if instructionalarea_id:
            print instructionalarea_id, "SSSSSSS"
            try:
                instructionalarea = InstructionalArea.objects.get(pk = instructionalarea_id)
                print " instance", instructionalarea
                form = InstructionalAreaForm(user, instance = instructionalarea)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/instructional_area.html', context)

def common_facility(request, application_id = None, common_facility_id = None):
    user = request.user
    if application_id == None and common_facility_id == None:
        application =  Application.objects.get(user = user)
        common_facilities = CommonFacilities.objects.filter(application = application)
        context = {
            'common_facilities': common_facilities,
            'application': application.id
        }
        return render(request, 'portal/templates/common_facility_index.html', context)
        
    if request.method == 'POST':
        form = CommonFacilitiesForm(user, request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            if common_facility_id:
                form_data.id = common_facility_id
            form_data.application_id = application_id
            form_data.save()
            return HttpResponseRedirect("/portal/common-facility/")
    else:
        form = CommonFacilitiesForm(user)
        if common_facility_id:
            try:
                common_facility = CommonFacilities.objects.get(pk = common_facility_id)
                form = CommonFacilitiesForm(user, instance = common_facility)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/common_facilities.html', context)
    
def amenities_area(request, application_id = None, amenities_area_id = None):
    user = request.user
    if application_id == None and amenities_area_id == None:
        application =  Application.objects.get(user = user)
        amenities_areas = AmenitiesArea.objects.filter(application = application)
        context = {
            'amenities_areas': amenities_areas,
            'application': application.id
        }
        return render(request, 'portal/templates/amenities_area_index.html', context)
        
    if request.method == 'POST':
        form = AmenitiesAreaForm(user, request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            if amenities_area_id:
                form_data.id = amenities_area_id
            form_data.application_id = application_id
            form_data.save()
            return HttpResponseRedirect("/portal/amenities-area/")
    else:
        form = AmenitiesAreaForm(user)
        if amenities_area_id:
            try:
                amenities_area = AmenitiesArea.objects.get(pk = amenities_area_id)
                form = AmenitiesAreaForm(user, instance = amenities_area)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/amenities_area.html', context)
    
def administrative_area(request, application_id = None, administrative_area_id = None):
    user = request.user
    if application_id == None and administrative_area_id == None:
        application =  Application.objects.get(user = user)
        administrative_areas = AdministrativeArea.objects.filter(application = application)
        context = {
            'administrative_areas': administrative_areas,
            'application': application.id
        }
        return render(request, 'portal/templates/administrative_area_index.html', context)
        
    if request.method == 'POST':
        form = AdministrativeAreaForm(user, request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            if administrative_area_id:
                form_data.id = administrative_area_id
            form_data.application_id = application_id
            form_data.save()
            return HttpResponseRedirect("/portal/administrative-area/")
    else:
        form = AdministrativeAreaForm(user)
        if administrative_area_id:
            try:
                administrative_area = AdministrativeArea.objects.get(pk = administrative_area_id)
                form = AdministrativeAreaForm(user, instance = administrative_area)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/administrative_area.html', context)

def other_facility(request, application_id = None, other_facility_id = None):
    user = request.user
    if application_id == None and other_facility_id == None:
        application =  Application.objects.get(user = user)
        other_facilities = OtherFacilities.objects.filter(application = application)
        context = {
            'other_facilities': other_facilities,
            'application': application.id
        }
        return render(request, 'portal/templates/other_facilities_index.html', context)
        
    if request.method == 'POST':
        form = OtherFacilitiesForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            if other_facility_id:
                form_data.id = other_facility_id
            form_data.application_id = application_id
            form_data.save()
            return HttpResponseRedirect("/portal/other-facilities/")
    else:
        form = OtherFacilitiesForm()
        if other_facility_id:
            try:
                other_facility = OtherFacilities.objects.get(pk = other_facility_id)
                form = OtherFacilitiesForm(instance = other_facility)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/other_facilities.html', context)
    
def laboratory_detail(request, application_id = None, laboratory_detail_id = None):
    user = request.user
    if application_id == None and laboratory_detail_id == None:
        application =  Application.objects.get(user = user)
        laboratory_details = LaboratoryDetail.objects.filter(application = application)
        context = {
            'laboratory_details': laboratory_details,
            'application': application.id
        }
        return render(request, 'portal/templates/laboratories_detail_index.html', context)
        
    if request.method == 'POST':
        form = LaboratoryDetailForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            if laboratory_detail_id:
                form_data.id = laboratory_detail_id
            form_data.application_id = application_id
            form_data.save()
            return HttpResponseRedirect("/portal/laboratory-details/")
    else:
        form = LaboratoryDetailForm()
        if laboratory_detail_id:
            try:
                laboratory_detail = LaboratoryDetail.objects.get(pk = laboratory_detail_id)
                form = LaboratoryDetailForm(instance = laboratory_detail)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/laboratory_details.html', context)

def library_book(request, application_id = None, library_book_id = None):
    user = request.user
    if application_id == None and library_book_id == None:
        application =  Application.objects.get(user = user)
        library_books = LibraryBook.objects.filter(application = application)
        context = {
            'library_books': library_books,
            'application': application.id
        }
        return render(request, 'portal/templates/library_books_index.html', context)
        
    if request.method == 'POST':
        form = LibraryBookForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            if library_book_id:
                form_data.id = library_book_id
            form_data.application_id = application_id
            form_data.save()
            return HttpResponseRedirect("/portal/library-books/")
    else:
        form = LibraryBookForm()
        if library_book_id:
            try:
                library_book = LibraryBook.objects.get(pk = library_book_id)
                form = LibraryBookForm(instance = library_book)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/library_books.html', context)

def ejournal(request, application_id = None, ejournal_id = None):
    user = request.user
    if application_id == None and ejournal_id == None:
        application =  Application.objects.get(user = user)
        ejournals = Ejournal.objects.filter(application = application)
        context = {
            'ejournals': ejournals,
            'application': application.id
        }
        return render(request, 'portal/templates/ejournals_index.html', context)
        
    if request.method == 'POST':
        form = EjournalForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            if ejournal_id:
                form_data.id = ejournal_id
            form_data.application_id = application_id
            form_data.save()
            return HttpResponseRedirect("/portal/ejournals/")
    else:
        form = EjournalForm()
        if ejournal_id:
            try:
                ejournal = Ejournal.objects.get(pk = ejournal_id)
                form = EjournalForm(instance = ejournal)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/ejournals.html', context)

def library_facilities(request, application_id = None, library_facilities_id = None):
    user = request.user
    if application_id == None and library_facilities_id == None:
        application =  Application.objects.get(user = user)
        library_facilities = LibraryFacility.objects.filter(application = application)
        context = {
            'library_facilities': library_facilities,
            'application': application.id
        }
        return render(request, 'portal/templates/library_facilities_index.html', context)
        
    if request.method == 'POST':
        form = LibraryFacilityForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            if library_facilities_id:
                form_data.id = library_facilities_id
            form_data.application_id = application_id
            form_data.save()
            return HttpResponseRedirect("/portal/library-facilities/")
    else:
        form = LibraryFacilityForm()
        if library_facilities_id:
            try:
                library_facilities = LibraryFacility.objects.get(pk = library_facilities_id)
                form = LibraryFacilityForm(instance = library_facilities)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/library_facilities.html', context)

def computation_facilities(request, application_id = None, computation_facilities_id = None):
    user = request.user
    if application_id == None and computation_facilities_id == None:
        application =  Application.objects.get(user = user)
        computation_facilities = ComputationFacility.objects.filter(application = application)
        context = {
            'computation_facilities': computation_facilities,
            'application': application.id
        }
        return render(request, 'portal/templates/computation_facilities_index.html', context)
        
    if request.method == 'POST':
        form = ComputationFacilityForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            if computation_facilities_id:
                form_data.id = computation_facilities_id
            form_data.application_id = application_id
            form_data.save()
            return HttpResponseRedirect("/portal/computation-facilities/")
    else:
        form = ComputationFacilityForm()
        if computation_facilities_id:
            try:
                computation_facilities = ComputationFacility.objects.get(pk = computation_facilities_id)
                form = ComputationFacilityForm(instance = computation_facilities)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/computation_facilities.html', context)

def technical_staffs(request, application_id = None, technical_staffs_id = None):
    user = request.user
    if application_id == None and technical_staffs_id == None:
        application =  Application.objects.get(user = user)
        technical_staffs = TechnicalStaff.objects.filter(application = application)
        context = {
            'technical_staffs': technical_staffs,
            'application': application.id
        }
        return render(request, 'portal/templates/technical_staffs_index.html', context)
        
    if request.method == 'POST':
        form = TechnicalStaffForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            if technical_staffs_id:
                form_data.id = technical_staffs_id
            form_data.application_id = application_id
            form_data.save()
            return HttpResponseRedirect("/portal/technical-staffs/")
    else:
        form = TechnicalStaffForm()
        if technical_staffs_id:
            try:
                technical_staffs = TechnicalStaff.objects.get(pk = technical_staffs_id)
                form = TechnicalStaffForm(instance = technical_staffs)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/technical_staffs.html', context)

def jfdr_details(request, application_id = None, jfdr_details_id = None):
    user = request.user
    if application_id == None and jfdr_details_id == None:
        application =  Application.objects.get(user = user)
        jfdr_details = JfdrDetail.objects.filter(application = application)
        context = {
            'jfdr_details': jfdr_details,
            'application': application.id
        }
        return render(request, 'portal/templates/jfdr_details_index.html', context)
        
    if request.method == 'POST':
        form = JfdrDetailForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            if jfdr_details_id:
                form_data.id = jfdr_details_id
            form_data.application_id = application_id
            form_data.save()
            return HttpResponseRedirect("/portal/jfdr-details/")
    else:
        form = JfdrDetailForm()
        if jfdr_details_id:
            try:
                jfdr_details = JfdrDetail.objects.get(pk = jfdr_details_id)
                form = JfdrDetailForm(instance = jfdr_details)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/jfdr_details.html', context)

def financial_details(request, application_id = None, financial_details_id = None):
    user = request.user
    if application_id == None and financial_details_id == None:
        application =  Application.objects.get(user = user)
        financial_details = FinancialDetail.objects.filter(application = application)
        context = {
            'financial_details': financial_details,
            'application': application.id
        }
        return render(request, 'portal/templates/financial_details_index.html', context)
        
    if request.method == 'POST':
        form = FinancialDetailForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            if financial_details_id:
                form_data.id = financial_details_id
            form_data.application_id = application_id
            form_data.save()
            return HttpResponseRedirect("/portal/financial-details/")
    else:
        form = FinancialDetailForm()
        if financial_details_id:
            try:
                financial_details = FinancialDetail.objects.get(pk = financial_details_id)
                form = FinancialDetailForm(instance = financial_details)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/financial_details.html', context)

def circulation_areas(request, application_id = None, circulation_areas_id = None):
    user = request.user
    if application_id == None and circulation_areas_id == None:
        application =  Application.objects.get(user = user)
        circulation_areas = CirculationArea.objects.filter(application = application)
        context = {
            'circulation_areas': circulation_areas,
            'application': application.id
        }
        return render(request, 'portal/templates/circulation_areas_index.html', context)
        
    if request.method == 'POST':
        form = CirculationAreaForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            if circulation_areas_id:
                form_data.id = circulation_areas_id
            form_data.application_id = application_id
            form_data.save()
            return HttpResponseRedirect("/portal/circulation-areas/")
    else:
        form = CirculationAreaForm()
        if circulation_areas_id:
            try:
                circulation_areas = CirculationArea.objects.get(pk = circulation_areas_id)
                form = CirculationAreaForm(instance = circulation_areas)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/circulation_areas.html', context)
    
def operational_funds(request, application_id = None, operational_funds_id = None):
    user = request.user
    if application_id == None and operational_funds_id == None:
        application =  Application.objects.get(user = user)
        operational_funds = OperationalFund.objects.filter(application = application)
        context = {
            'operational_funds': operational_funds,
            'application': application.id
        }
        return render(request, 'portal/templates/operational_funds_index.html', context)

    if request.method == 'POST':
        form = OperationalFundForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            if operational_funds_id:
                form_data.id = operational_funds_id
            form_data.application_id = application_id
            form_data.save()
            return HttpResponseRedirect("/portal/operational-funds/")
    else:
        form = OperationalFundForm()
        if operational_funds_id:
            try:
                operational_funds = OperationalFund.objects.get(pk = operational_funds_id)
                form = OperationalFundForm(instance = operational_funds)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/operational_funds.html', context)

def admin_library_staff(request, application_id = None,  admin_library_staff_id = None):
    user = request.user
    if application_id == None and admin_library_staff_id == None:
        application =  Application.objects.get(user = user)
        admin_library_staff = AdminLibraryStaff.objects.filter(application = application)
        context = {
            'admin_library_staff': admin_library_staff,
            'application': application.id
        }
        return render(request, 'portal/templates/admin_library_staff_index.html', context)

    if request.method == 'POST':
        form = AdminLibraryStaffForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            if admin_library_staff_id:
                form_data.id = admin_library_staff_id
            form_data.application_id = application_id
            form_data.save()
            return HttpResponseRedirect("/portal/admin-library-staff/")
    else:
        form = AdminLibraryStaffForm()
        if admin_library_staff_id:
            try:
                admin_library_staff = AdminLibraryStaff.objects.get(pk = admin_library_staff_id)
                form = AdminLibraryStaffForm(instance = admin_library_staff)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/admin_library_staff.html', context)

def fee_structure(request, application_id = None, fee_structure_id = None):
    user = request.user
    if application_id == None and fee_structure_id == None:
        application =  Application.objects.get(user = user)
        fee_structures = FeeStructure.objects.filter(application = application)
        context = {
            'fee_structures': fee_structures,
            'application': application.id
        }
        return render(request, 'portal/templates/fee_structure_index.html', context)

    if request.method == 'POST':
        form = FeeStructureForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            if fee_structure_id:
                form_data.id = fee_structure_id
            form_data.application_id = application_id
            form_data.save()
            return HttpResponseRedirect("/portal/fee-structure/")
    else:
        form = FeeStructureForm()
        if fee_structure_id:
            try:
                fee_structure = FeeStructure.objects.get(pk = fee_structure_id)
                form = FeeStructureForm(instance = fee_structure)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/fee_structure.html', context)

def hostel_facilities(request, application_id = None, hostel_facilities_id = None):
    user = request.user
    if application_id == None and hostel_facilities_id == None:
        application =  Application.objects.get(user = user)
        hostel_facilities = HostelFacilities.objects.filter(application = application)
        context = {
            'hostel_facilities': hostel_facilities,
            'application': application.id
        }
        return render(request, 'portal/templates/hostel_facilities_index.html', context)
        
    if request.method == 'POST':
        form = HostelFacilitiesForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            if hostel_facilities_id:
                form_data.id = hostel_facilities_id
            form_data.application_id = application_id
            form_data.save()
            return HttpResponseRedirect("/portal/hostel-facilities/")
    else:
        form = HostelFacilitiesForm()
        if hostel_facilities_id:
            try:
                hostel_facilities = HostelFacilities.objects.get(pk = hostel_facilities_id)
                form = HostelFacilitiesForm(instance = hostel_facilities)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/hostel_facilities.html', context)

def head_of_institute(request, application_id = None, head_of_institute_id= None):
    user = request.user
    if application_id == None and head_of_institute_id == None:
        application =  Application.objects.get(user = user)
        heads_of_institute = HeadOfInstitute.objects.filter(application = application)
        context = {
            'heads_of_institute': heads_of_institute,
            'application': application.id
        }
        return render(request, 'portal/templates/head_of_institute_index.html', context)
        
    if request.method == 'POST':
        form = HeadOfInstituteForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            if head_of_institute_id:
                form_data.id = head_of_institute_id
            form_data.application_id = application_id
            form_data.save()
            return HttpResponseRedirect("/portal/head-of-institute/")
    else:
        form = HeadOfInstituteForm()
        if head_of_institute_id:
            try:
                head_of_institute = HeadOfInstitute.objects.get(pk = head_of_institute_id)
                form = HeadOfInstituteForm(instance = head_of_institute)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/head_of_institute.html', context)

def grants_received(request, application_id = None, grants_received_id = None):
    user = request.user
    if application_id == None and grants_received_id == None:
        application =  Application.objects.get(user = user)
        grants_received = GrantsReceived.objects.filter(application = application)
        context = {
            'grants_received': grants_received,
            'application': application.id
        }
        return render(request, 'portal/templates/grants_received_index.html', context)

    if request.method == 'POST':
        form = GrantsReceivedForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            if grants_received_id:
                form_data.id = grants_received_id
            form_data.application_id = application_id
            form_data.save()
            return HttpResponseRedirect("/portal/grants-received/")
    else:
        form = GrantsReceivedForm()
        if grants_received_id:
            try:
                grants_received = GrantsReceived.objects.get(pk = grants_received_id)
                form = GrantsReceivedForm(instance = grants_received)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/grants_received.html', context)

def student_details(request, application_id = None, student_details_id = None):
    user = request.user
    if application_id == None and student_details_id == None:
        application =  Application.objects.get(user = user)
        student_details = StudentDetail.objects.filter(application = application)
        context = {
            'student_details': student_details,
            'application': application.id
        }
        return render(request, 'portal/templates/student_details.html', context)

    if request.method == 'POST':
        form = StudentDetailForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            if student_detail_id:
                form_data.id = student_details_id
            form_data.application_id = application_id
            form_data.save()
            return HttpResponseRedirect("/portal/student-details/")
    else:
        form = StudentDetailForm()
        if student_details_id:
            try:
                student_details = StudentDetail.objects.get(pk = student_details_id)
                form = StudentDetailForm(instance = student_details)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/student_details.html', context)

def anti_ragging(request):
    user = request.user
    rid = 0
    if request.method == 'POST':
        form = AntiRaggingForm(request.POST)
        application = get_application_id(user)
        if form.is_valid():
            form_data = form.save(commit=False)
            anti_ragging = AntiRagging.objects.filter(application = application).first()
            if anti_ragging:
                form_data.id = anti_ragging.id
            form_data.application_id = application.id
            form_data.save()
            return HttpResponseRedirect("/portal/anti-ragging/")
    else:
        form = AntiRaggingForm()
        application = get_application_id(user)
        if application:
            try:
                anti_ragging = AntiRagging.objects.filter(application = application).first()
                form = AntiRaggingForm(instance = anti_ragging)
                rid = anti_ragging.id
            except:
                print "404"
    context = {
        'form': form,
        'rid': rid,
    }
    return render(request, 'portal/templates/anti_ragging.html', context)
    
def anti_ragging_details(request, antiragging_id, anti_ragging_details_id = None):
    if request.method == 'POST':
        form = AntiRaggingDetailForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            if anti_ragging_details_id:
                form_data.id = anti_ragging_details_id
            form_data.antiragging_id = antiragging_id
            form_data.save()
            
    else:
        form = AntiRaggingDetailForm()
        if anti_ragging_details_id:
            try:
                print anti_ragging_details_id
                anti_ragging_details = AntiRaggingDetail.objects.get(pk = anti_ragging_details_id)
                form = AntiRaggingDetailForm(instance = anti_ragging_details)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/anti_ragging_details.html', context)

def ombudsman(request):
    user = request.user
    rid = 0
    if request.method == 'POST':
        form = OmbudsmanForm(request.POST)
        application = get_application_id(user)
        if form.is_valid():
            form_data = form.save(commit=False)
            ombudsman = Ombudsman.objects.filter(application = application).first()
            if ombudsman:
                form_data.id = ombudsman.id
            form_data.application_id = application.id
            form_data.save()
            return HttpResponseRedirect("/portal/ombudsman/")
    else:
        form = OmbudsmanForm()
        application = get_application_id(user)
        if application:
            try:
                ombudsman = Ombudsman.objects.filter(application = application).first()
                form = OmbudsmanForm(instance = ombudsman)
                rid = ombudsman.id
            except:
                print "404"
    context = {
        'form': form,
        'rid': rid,
    }
    return render(request, 'portal/templates/ombudsman.html', context)
    
def ombudsman_details(request, ombudsman_id, ombudsman_details_id = None):
    if request.method == 'POST':
        form = OmbudsmanDetailForm(request.POST)
        if form.is_valid():
            form_data = form.save(commit=False)
            if ombudsman_details_id:
                form_data.id = ombudsman_details_id
            form_data.ombudsman_id = ombudsman_id
            form_data.save()
            return HttpResponseRedirect("/portal/ombudsman/")
            
    else:
        form = OmbudsmanDetailForm()
        if ombudsman_details_id:
            try:
                print ombudsman_details_id
                ombudsman_details = OmbudsmanDetail.objects.get(pk = ombudsman_details_id)
                form = OmbudsmanDetailForm(instance = ombudsman_details)
            except:
                print "404"
    context = {
        'form': form,
    }
    return render(request, 'portal/templates/ombudsman_details.html', context)
    

#Ajax Request and Responces
@csrf_exempt
def ajax_state(request):
    """ Ajax: Get, District, City based State selected """
    if request.method == 'POST':
        state = request.POST.get('state')
        district = District.objects.filter(state=state)
        city = City.objects.filter(state=state)
        data = []
        tmp = ''
        for i in district:
            tmp +='<option value='+str(i.id)+'>'+i.name+'</option>'
            
        if(tmp):
            data.append('<option value = None> -- None -- </option>'+tmp)
        else:
            data.append(tmp)
        
        tmp = ''
        for i in city:
            tmp +='<option value='+str(i.id)+'>'+i.name+'</option>'
            
        if(tmp):
            data.append('<option value = None> -- None -- </option>'+tmp)
        else:
            data.append(tmp)

        return HttpResponse(json.dumps(data), mimetype='application/json')

@csrf_exempt
def ajax_location(request):
    """ Ajax: Get the location based on district selected """
    if request.method == 'POST':
        district = request.POST.get('district')
        location = Location.objects.filter(district=district)
        tmp = '<option value = None> -- None -- </option>'
        for i in location:
            tmp +='<option value='+str(i.id)+'>'+i.name+'</option>'
        return HttpResponse(json.dumps(tmp), mimetype='application/json')

@csrf_exempt
def ajax_pincode(request):
    """ Ajax: Get the pincode based on location selected """
    if request.method == 'POST':
        location = request.POST.get('location')
        location = Location.objects.get(pk=location)
        return HttpResponse(json.dumps(location.pincode), mimetype='application/json')
