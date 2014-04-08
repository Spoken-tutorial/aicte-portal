from django.contrib import admin
from portal.models import *
# Register your models here.

class OrganisationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'updated')
    
class InstitutionTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'created', 'updated')

class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'updated')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'updated')

class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'updated')

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'updated')

class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created', 'updated')

class LevelAdmin(admin.ModelAdmin):
    list_display = ('level', 'created', 'updated')

admin.site.register(OrganisationType, OrganisationTypeAdmin)
admin.site.register(InstitutionType, InstitutionTypeAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(University, UniversityAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Level, LevelAdmin)
