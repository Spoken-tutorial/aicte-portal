from django import template
from portal.models import *

register = template.Library()

def get_trustee(user):
	trustee = Trustee.objects.filter(organisation__in = ApplicationYear.objects.filter(user = user).values_list('organisation_id')).order_by('id')
	return trustee

def get_perland(user):
	perland = PerLandDetail.objects.filter(land_detail__in = ApplicationYear.objects.filter(user = user).values_list('land_id')).order_by('id')
	return perland

def get_perbuilding(user):
	perbuilding = PerBuildingDetail.objects.filter(building_detail__in = ApplicationYear.objects.filter(user = user).values_list('building_id')).order_by('id')
	return perbuilding

def get_antiragging_details(rid):
	antiragging_details = AntiRaggingDetail.objects.filter(antiragging_id=rid).order_by('id')
	return antiragging_details

def get_ombudsman_details(rid):
	ombudsman_details = OmbudsmanDetail.objects.filter(ombudsman_id=rid).order_by('id')
	return ombudsman_details
	
#Common Value
def area_type(key):
    area_type_list = ['Corridors', 'Other Common Area(in Sqm)', 'other areas (in Sqm)']
    return area_type_list[key]

register.filter('get_trustee', get_trustee)
register.filter('get_perland', get_perland)
register.filter('get_perbuilding', get_perbuilding)
register.filter('area_type', area_type)
register.filter('get_antiragging_details', get_antiragging_details)
register.filter('get_ombudsman_details', get_ombudsman_details)

