from django import template
from portal.models import *

register = template.Library()

def get_trustee(user):
	trustee = Trustee.objects.filter(organisation__in = ApplicationYear.objects.filter(user = user)).order_by('id')
	return trustee

register.filter('get_trustee', get_trustee)

