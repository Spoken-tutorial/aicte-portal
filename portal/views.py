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

@login_required
def extension(request):
    """ 
    Create ontime Application number to institution. If exits use that.
    Ceate Create a new year erxtension.
    """
    user = request.user
    try:
       application = Application.objects.get(user_id = user.id)
       is_new_application = 0
    except ObjectDoesNotExist:
        application = Application()
        application.user_id = user.id
        application.application_number = user.id
        application.save()
        is_new_application = 1
    
    year = datetime.now()
    academic_year = Application_Year.objects.filter(application = application, academic_year= year.year).last()
    alert_danger = ''
    appDetails = {}
    is_edit = 0
    appDetails['academic_year'] = str(year.year)+' - '+str(year.year+1)
    appDetails['application'] = application.application_number
    appDetails['status'] = 'New'
    if academic_year:
        appDetails['academic year'] = str(academic_year.academic_year)+' - '+str(academic_year.academic_year+1)
        if academic_year.academic_year == year.year:
            is_edit = 1

    if request.method == 'POST':
        form = InstitutionDetailForm(request.POST)
        save_only_institute = 0
        if request.POST['id']:
            institution = Institution_Detail.objects.get(id=request.POST['id'])
            form = InstitutionDetailForm(request.POST, instance = institution)
            save_only_institute = 1
        alert_success = ''
        alert_danger = ''
        if form.is_valid():
            # Save institution detail
            try:
                if save_only_institute:
                    institution = form.save()
                else:
                    institution = form.save()
                    # Save application detail
                    application_detail = Application_Detail()
                    application_detail.institution = institution
                    application_detail.save()
                
                    # Save application year
                    application = Application.objects.get(user = user)
                    application_year = Application_Year()
                    application_year.application_id = application.id
                    application_year.application_detail_id = application_detail.id
                    application_year.academic_year = year.year
                    application_year.chapter = 1
                    application_year.approval_status = 0
                    application_year.application_type = 1
                    application_year.application_opened = ''
                    application_year.application_submitted = ''
                    application_year.save()
                alert_success = 'Record updated successfully'
            except:
                alert_danger = 'Record already exist for this '
                print "record already exist!"
            return HttpResponseRedirect("/portal")


        context = {
            'form': form,
            'appDetails': appDetails,
            'alert_success': alert_success,
            'alert_danger': alert_danger
        }
        return render(request, 'portal/templates/extension.html', context)
    else:
        if is_edit:
            form = InstitutionDetailForm(instance = academic_year.application_detail.institution)
        else:
            form = InstitutionDetailForm()
        context = {
            'form': form,
            'appDetails': appDetails,
            'alert_success': '',
            'alert_danger': alert_danger
        }
        return render(request, 'portal/templates/extension.html', context)

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
