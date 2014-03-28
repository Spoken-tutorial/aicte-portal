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

def home(request):
    return HttpResponseRedirect('/accounts/login/')

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
            trustee.phone = form.cleaned_data['phone']
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
