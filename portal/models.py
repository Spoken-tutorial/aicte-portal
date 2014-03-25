from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class State(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = (("code","name"),)

class District(models.Model):
    state = models.ForeignKey(State)
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = (("state", "code","name"),)

class City(models.Model):
    state = models.ForeignKey(State)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = (("name","state"),)

class Location(models.Model):
    district = models.ForeignKey(District)
    name = models.CharField(max_length=200)
    pincode = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = (("name","district","pincode"),)

class Institution_Type(models.Model):
    type = models.CharField(max_length = 255, unique = True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    def __unicode__(self):
        return self.type

class Institution_Detail(models.Model):
    institution_name = models.CharField(max_length = 255)
    institution_address = models.TextField()
    state = models.ForeignKey(State)
    district = models.ForeignKey(District)
    location = models.ForeignKey(Location)
    city = models.ForeignKey(City)
    first_course_year = models.IntegerField()
    institution_type = models.ForeignKey(Institution_Type)
    unaided_courses = models.BooleanField()
    women_institute = models.BooleanField()
    co_ed = models.BooleanField()
    std_code = models.CharField(max_length = 15)
    land_phone = models.CharField(max_length = 15)
    cell_phone = models.CharField(max_length = 15)
    fax_number = models.CharField(max_length = 30)
    primary_email = models.EmailField(max_length = 255)
    secondary_email = models.EmailField(max_length = 255)
    website = models.URLField(max_length = 255)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

class Application(models.Model):
    application_number = models.CharField(max_length = 255, unique = True)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)


class Application_Detail(models.Model):
    institution = models.ForeignKey(Institution_Detail)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)


class Application_Year(models.Model):
    application = models.ForeignKey(Application)
    application_detail = models.ForeignKey(Application_Detail)
    permanent_institute_id = models.CharField(max_length = 255)
    academic_year = models.IntegerField()
    chapter = models.IntegerField()
    approval_status = models.BooleanField()
    application_type = models.PositiveSmallIntegerField()
    application_opened = models.DateTimeField(auto_now_add = True)
    application_submitted = models.DateTimeField(auto_now = True) 

