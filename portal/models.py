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

class InstitutionType(models.Model):
    type = models.CharField(max_length = 255, unique = True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    def __unicode__(self):
        return self.type

class InstitutionDetail(models.Model):
    institution_name = models.CharField(max_length = 255)
    institution_address = models.TextField()
    state = models.ForeignKey(State)
    district = models.ForeignKey(District)
    location = models.ForeignKey(Location)
    city = models.ForeignKey(City)
    first_course_year = models.IntegerField()
    institution_type = models.ForeignKey(InstitutionType)
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

    #class Meta:
    #    unique_together = (('institution_name', 'state','district','location', 'city', 'institution_type', 'unaided_courses', 'women_institute', 'co_ed',),)

class OrganisationType(models.Model):
    name = models.CharField(max_length = 100)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

class Organisation(models.Model):
    name = models.CharField(max_length = 200)
    organisation_type = models.ForeignKey(OrganisationType)
    registered_with = models.CharField(max_length = 200)
    registered_date = models.DateField()
    registered_number = models.CharField(max_length = 100)
    address = models.TextField()
    state = models.ForeignKey(State)
    district = models.ForeignKey(District)
    location = models.ForeignKey(Location)
    city = models.ForeignKey(City)
    std_code = models.CharField(max_length = 15)
    land_phone = models.CharField(max_length = 15)
    cell_phone = models.CharField(max_length = 15)
    fax_number = models.CharField(max_length = 30)
    website = models.URLField(max_length = 255)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    #class Meta:
    #    unique_together = (('name', 'organisation_type', 'state', 'district', 'location', 'city',))

class Trustee(models.Model):
    organisation = models.ForeignKey(Organisation)
    title = models.CharField(max_length = 200)
    first_name = models.CharField(max_length = 200)
    middel_name = models.CharField(max_length = 200)
    lase_name = models.CharField(max_length = 200)
    designation = models.CharField(max_length = 200)
    dob = models.DateField()
    trustee_since = models.DateField()
    trustee_till = models.DateField()
    phone = models.CharField(max_length = 15)
    email = models.EmailField(max_length = 255)
    pan = models.CharField(max_length = 200)
    profession = models.CharField(max_length = 200)
    academic_qualification = models.CharField(max_length = 200)
    state = models.ForeignKey(State)
    district = models.ForeignKey(District)
    location = models.ForeignKey(Location)
    city = models.ForeignKey(City)
    address1 = models.CharField(max_length = 255)
    address2 = models.CharField(max_length = 255)
    std_code = models.CharField(max_length = 15)
    land_phone = models.CharField(max_length = 15)
    cell_phone = models.CharField(max_length = 15)

class ContactDetail(models.Model):
    title = models.CharField(max_length = 10)
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    address = models.TextField()
    state = models.ForeignKey(State)
    district = models.ForeignKey(District)
    location = models.ForeignKey(Location)
    city = models.ForeignKey(City)
    designation = models.CharField(max_length = 255)
    std_code = models.CharField(max_length = 15)
    land_phonee = models.CharField(max_length = 15)
    cell_phone = models.CharField(max_length = 15)
    alt_cell_phone = models.CharField(max_length = 15)
    fax_number = models.CharField(max_length = 30)
    email = models.EmailField(max_length = 255)
    alt_email = models.EmailField(max_length = 255)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    #class Meta:
    #    unique_together = (('first_name', 'last_name', 'state', 'district', 'location', 'city', 'designation'))

class LandDetail(models.Model):
    location = models.PositiveSmallIntegerField()
    total_area_acres = models.DecimalField(max_digits = 5, decimal_places = 2)
    land_reg_with = models.CharField(max_length = 255)
    date_of_reg = models.DateField()
    north_hilly_area = models.BooleanField()
    no_of_pieces = models.IntegerField()
    max_distance = models.DecimalField(max_digits = 8, decimal_places = 2)
    land_cert_issued_by = models.CharField(max_length = 255)
    land_cert_issued_date = models.DateField()
    ownership_details = models.PositiveSmallIntegerField()
    land_mordgaged = models.BooleanField()
    latitude_ns = models.PositiveSmallIntegerField()
    latitude_degree = models.IntegerField()
    latitude_minute = models.IntegerField()
    latitude_second = models.IntegerField()
    longitude_ew = models.PositiveSmallIntegerField()
    longitude_degree = models.IntegerField()
    longitude_minute = models.IntegerField()
    longitude_second = models.IntegerField()
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    #class Meta:
    #    unique_together = (('location', 'total_area_acres', 'land_reg_with', 'date_of_reg', 'north_hilly_area', 'no_of_pieces', 'max_distance', 'land_cert_issued_by', 'land_cert_issued_date', 'ownership_details', 'land_mordgaged'))

class PerLandDetail(models.Model):
    land_detail = models.ForeignKey(LandDetail)
    land_reg_no = models.CharField(max_length = 255)
    date_of_reg = models.DateField()
    area_of_land = models.DecimalField(max_digits = 8, decimal_places = 2)
    khasra_number = models.CharField(max_length = 255)
    plot_survey_no = models.CharField(max_length = 255)
    land_situated = models.CharField(max_length = 255)
    land_reg_name = models.CharField(max_length = 255)
    owner_govt_lease = models.PositiveSmallIntegerField()
    land_cert_issued = models.BooleanField()
    land_cert_authority = models.CharField(max_length = 255)
    is_mortgaged = models.BooleanField()
    bank_mortgaged = models.CharField(max_length = 255)
    land_required = models.DecimalField(max_digits = 8, decimal_places = 2)
    land_available = models.DecimalField(max_digits = 8, decimal_places = 2)

class BuildingDetail(models.Model):
    building_status = models.PositiveSmallIntegerField()
    built_area_planned = models.CharField(max_length = 255)
    built_area_ready = models.CharField(max_length = 255)
    built_area_planned = models.CharField(max_length = 255)
    built_area_ready = models.CharField(max_length = 255)
    carpet_area_instructional = models.CharField(max_length = 255)
    carpet_area_admin = models.CharField(max_length = 255)
    carpet_area_amenities = models.CharField(max_length = 255)
    funds_allocated = models.DecimalField(max_digits = 10, decimal_places = 2)
    loans = models.DecimalField(max_digits = 10, decimal_places = 2)
    own_share = models.DecimalField(max_digits = 10, decimal_places = 2)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

class PerBuildingDetail(models.Model):
    building_detail = models.ForeignKey(BuildingDetail)
    building_name = models.CharField(max_length = 255)
    building_number = models.CharField(max_length = 255)
    sanct_build_area = models.CharField(max_length = 255)
    const_build_area = models.CharField(max_length = 255)
    approved_carpet_area_inst = models.CharField(max_length = 255)
    const_carpet_area_inst = models.CharField(max_length = 255)
    approved_carpet_area_admin = models.CharField(max_length = 255)
    const_carpet_area_admin = models.CharField(max_length = 255)
    approved_carpet_area_amen = models.CharField(max_length = 255)
    const_carpet_area_amen = models.CharField(max_length = 255)
    total_area_approved = models.CharField(max_length = 255)
    total_area_constructed = models.CharField(max_length = 255)
    activities_conducted = models.CharField(max_length = 255)
    non_aicte_courses = models.CharField(max_length = 255)
    approving_authority = models.CharField(max_length = 255)
    approval_date = models.DateField()
    approval_number = models.CharField(max_length = 255)

class Program(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

class ProgramDetail(models.Model):
    program = models.ForeignKey(Program)
    programme = models.PositiveSmallIntegerField()
    new_existing = models.PositiveSmallIntegerField()
    instructional_area = models.ForeignKey(PerBuildingDetail)

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

class CourseDetail(models.Model):
    course = models.ForeignKey(Course)
    program_detail = models.ForeignKey(ProgramDetail)
    affiliating_board = models.CharField(max_length = 255)
    board_type = models.CharField(max_length = 255)
    level_of_course = models.PositiveSmallIntegerField()
    department = models.PositiveSmallIntegerField()
    course = models.CharField(max_length = 255)
    shift = models.PositiveSmallIntegerField()
    last_approved_intake = models.IntegerField()
    intake_applied_for = models.IntegerField()
    course_duration = models.IntegerField()
    year_started = models.IntegerField()
    full_part_time = models.PositiveSmallIntegerField()
    accreditation_status = models.PositiveSmallIntegerField()
    accreditation_from = models.DateField()
    accreditation_till = models.DateField()
    accreditation_letter_date = models.DateField()
    accreditation_letter_refno = models.CharField(max_length = 255)
    nri = models.PositiveSmallIntegerField()
    pio = models.PositiveSmallIntegerField()
    annual_fees = models.DecimalField(max_digits = 10, decimal_places = 2)
    no_of_faculty = models.IntegerField()
    govt_recommendation = models.PositiveSmallIntegerField()
    board_recommendation = models.PositiveSmallIntegerField()
    course_type = models.PositiveSmallIntegerField()
    mode_of_conduct = models.PositiveSmallIntegerField()

class Application(models.Model):
    institution_number = models.CharField(max_length = 255, unique = True)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

class ApplicationYear(models.Model):
    user = models.ForeignKey(User)
    application = models.ForeignKey(Application)
    institution = models.ForeignKey(InstitutionDetail, null = True)
    organisation = models.ForeignKey(Organisation, null = True)
    current_application_id = models.CharField(max_length = 255)
    academic_year = models.IntegerField()
    chapter = models.IntegerField()
    approval_status = models.PositiveSmallIntegerField()
    application_type = models.PositiveSmallIntegerField()
    application_opened = models.DateTimeField(auto_now_add = True)
    application_submitted = models.DateTimeField(auto_now = True) 

