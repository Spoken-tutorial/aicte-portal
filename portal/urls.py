from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'aicte.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'portal.views.home', name='home'),
    url(r'^application/(\d+)/$', 'portal.views.application_year', name='application_year'),
    url(r'^extension/$', 'portal.views.extension', name='extension'),
    url(r'^organisation/$', 'portal.views.organisation', name='organisation'),
    url(r'^contact-details/$', 'portal.views.contact', name='contact'),
    url(r'^land-details/$', 'portal.views.land', name='land'),
    url(r'^building-details/$', 'portal.views.building', name='building'),
    
    url(r'^faculty-details/$', 'portal.views.faculty', name='faculty'),
    url(r'^faculty-details/(\d+)/$', 'portal.views.faculty', name='newfaculty'),
    url(r'^faculty-details/(\d+)/(\d+)/$', 'portal.views.faculty', name='editfaculty'),
    
    url(r'^program-details/$', 'portal.views.program_detail', name='program_detail'),
    url(r'^program-details/(\d+)/$', 'portal.views.program_detail', name='newprogram_detail'),
    url(r'^program-details/(\d+)/(\d+)/$', 'portal.views.program_detail', name='editprogram_detail'),
    
    url(r'^course-details/$', 'portal.views.course_detail', name='course_detail'),
    url(r'^course-details/(\d+)/$', 'portal.views.course_detail', name='newcourse_detail'),
    url(r'^course-details/(\d+)/(\d+)/$', 'portal.views.course_detail', name='editcourse_detail'),
    
    url(r'^instructional-area/$', 'portal.views.instructionalarea', name='instructionalarea'),
    url(r'^instructional-area/(\d+)/$', 'portal.views.instructionalarea', name='newinstructionalarea'),
    url(r'^instructional-area/(\d+)/(\d+)/$', 'portal.views.instructionalarea', name='editinstructionalarea'),
    
    url(r'^common-facility/$', 'portal.views.common_facility', name='common_facility'),
    url(r'^common-facility/(\d+)/$', 'portal.views.common_facility', name='newcommon_facility'),
    url(r'^common-facility/(\d+)/(\d+)/$', 'portal.views.common_facility', name='editcommon_facility'),
    
    url(r'^amenities-area/$', 'portal.views.amenities_area', name='amenities_area'),
    url(r'^amenities-area/(\d+)/$', 'portal.views.amenities_area', name='newamenities_area'),
    url(r'^amenities-area/(\d+)/(\d+)/$', 'portal.views.amenities_area', name='editamenities_area'),
    
    url(r'^administrative-area/$', 'portal.views.administrative_area', name='administrative_area'),
    url(r'^administrative-area/(\d+)/$', 'portal.views.administrative_area', name='newadministrative_area'),
    url(r'^administrative-area/(\d+)/(\d+)/$', 'portal.views.administrative_area', name='editadministrative_area'),
    
    url(r'^other-facilities/$', 'portal.views.other_facility', name='other_facility'),
    url(r'^other-facilities/(\d+)/$', 'portal.views.other_facility', name='newother_facility'),
    url(r'^other-facilities/(\d+)/(\d+)/$', 'portal.views.other_facility', name='editother_facility'),
    
    url(r'^laboratory-details/$', 'portal.views.laboratory_detail', name='laboratory_detail'),
    url(r'^laboratory-details/(\d+)/$', 'portal.views.laboratory_detail', name='newlaboratory_detail'),
    url(r'^laboratory-details/(\d+)/(\d+)/$', 'portal.views.laboratory_detail', name='editlaboratory_detail'),
    
    url(r'^library-books/$', 'portal.views.library_book', name='library_book'),
    url(r'^library-books/(\d+)/$', 'portal.views.library_book', name='newlibrary_book'),
    url(r'^library-books/(\d+)/(\d+)/$', 'portal.views.library_book', name='editlibrary_book'),
    
    url(r'^trustee/(\d+)/$', 'portal.views.trustee', name='trustee'),
    url(r'^trustee/(\d+)/(\d+)/$', 'portal.views.trustee', name='edittrustee'),
    
    url(r'^perland/(\d+)/$', 'portal.views.perland', name='perland'),
    url(r'^perland/(\d+)/(\d+)/$', 'portal.views.perland', name='editperland'),
    
    url(r'^perbuilding/(\d+)/$', 'portal.views.perbuilding', name='perbuilding'),
    url(r'^perbuilding/(\d+)/(\d+)/$', 'portal.views.perbuilding', name='editperbuilding'),
    
    url(r'^ejournals/$', 'portal.views.ejournal', name='ejournal'),
    url(r'^ejournals/(\d+)/$', 'portal.views.ejournal', name='newejournal'),
    url(r'^ejournals/(\d+)/(\d+)/$', 'portal.views.ejournal', name='editejournal'),
    
    url(r'^library-facilities/$', 'portal.views.library_facilities', name='library_facilities'),
    url(r'^library-facilities/(\d+)/$', 'portal.views.library_facilities', name='newlibrary_facilities'),
    url(r'^library-facilities/(\d+)/(\d+)/$', 'portal.views.library_facilities', name='editlibrary_facilities'),
    
    url(r'^computation-facilities/$', 'portal.views.computation_facilities', name='computation_facilities'),
    url(r'^computation-facilities/(\d+)/$', 'portal.views.computation_facilities', name='newcomputation_facilities'),
    url(r'^computation-facilities/(\d+)/(\d+)/$', 'portal.views.computation_facilities', name='editcomputation_facilities'),
    
    url(r'^technical-staffs/$', 'portal.views.technical_staffs', name='technical_staffs'),
    url(r'^technical-staffs/(\d+)/$', 'portal.views.technical_staffs', name='newtechnical_staffs'),
    url(r'^technical-staffs/(\d+)/(\d+)/$', 'portal.views.technical_staffs', name='edittechnical_staffs'),
    
    url(r'^jfdr-details/$', 'portal.views.jfdr_details', name='jfdr_details'),
    url(r'^jfdr-details/(\d+)/$', 'portal.views.jfdr_details', name='newjfdr_details'),
    url(r'^jfdr-details/(\d+)/(\d+)/$', 'portal.views.jfdr_details', name='editjfdr_details'),
    
    url(r'^financial-details/$', 'portal.views.financial_details', name='financial_details'),
    url(r'^financial-details/(\d+)/$', 'portal.views.financial_details', name='newfinancial_details'),
    url(r'^financial-details/(\d+)/(\d+)/$', 'portal.views.financial_details', name='editfinancial_details'),
    
    url(r'^circulation-areas/$', 'portal.views.circulation_areas', name='circulation_areas'),
    url(r'^circulation-areas/(\d+)/$', 'portal.views.circulation_areas', name='newcirculation_areas'),
    url(r'^circulation-areas/(\d+)/(\d+)/$', 'portal.views.circulation_areas', name='editcirculation_areas'),

    url(r'^operational-funds/$', 'portal.views.operational_funds', name='operational_funds'),
    url(r'^operational-funds/(\d+)/$', 'portal.views.operational_funds', name='newoperational_funds'),
    url(r'^operational-funds/(\d+)/(\d+)/$', 'portal.views.operational_funds', name='editoperational_funds'),

    url(r'^admin-library-staff/$', 'portal.views.admin_library_staff', name='admin_library_staff'),
    url(r'^admin-library-staff/(\d+)/$', 'portal.views.admin_library_staff', name='newadmin_library_staff'),
    url(r'^admin-library-staff/(\d+)/(\d+)/$', 'portal.views.admin_library_staff', name='editadmin_library_staff'),

    url(r'^fee-structure/$', 'portal.views.fee_structure', name='fee_structure'),
    url(r'^fee-structure/(\d+)/$', 'portal.views.fee_structure', name='newfee_structure'),
    url(r'^fee-structure/(\d+)/(\d+)/$', 'portal.views.fee_structure', name='editfee_structure'),

    url(r'^hostel-facilities/$', 'portal.views.hostel_facilities', name='hostel_facilities'),
    url(r'^hostel-facilities/(\d+)/$', 'portal.views.hostel_facilities', name='newhostel_facilities'),
    url(r'^hostel-facilities/(\d+)/(\d+)/$', 'portal.views.hostel_facilities', name='edithostel_facilities'),

    url(r'^head-of-institute/$', 'portal.views.head_of_institute', name='head_of_institute'),
    url(r'^head-of-institute/(\d+)/$', 'portal.views.head_of_institute', name='newhead_of_institute'),
    url(r'^head-of-institute/(\d+)/(\d+)/$', 'portal.views.head_of_institute', name='edithead_of_institute'),

    url(r'^grants-received/$', 'portal.views.grants_received', name='grants_received'),
    url(r'^grants-received/(\d+)/$', 'portal.views.grants_received', name='newgrants_received'),
    url(r'^grants-received/(\d+)/(\d+)/$', 'portal.views.grants_received', name='editgrants_received'),

    url(r'^student-details/$', 'portal.views.student_details', name='student_details'),
    url(r'^student-details/(\d+)/$', 'portal.views.student_details', name='newstudent_details'),
    url(r'^student-details/(\d+)/(\d+)/$', 'portal.views.student_details', name='editstudent_details'),
    
    url(r'^anti-ragging/$', 'portal.views.anti_ragging', name='anti_ragging'),
    
    url(r'^anti-ragging-details/(\d+)/$', 'portal.views.anti_ragging_details', name='newanti_ragging_details'),
    url(r'^anti-ragging-details/(\d+)/(\d+)/$', 'portal.views.anti_ragging_details', name='editanti_ragging_details'),
    
    url(r'^ombudsman/$', 'portal.views.ombudsman', name='ombudsman'),
    
    url(r'^ombudsman-details/(\d+)/$', 'portal.views.ombudsman_details', name='newombudsman_details'),
    url(r'^ombudsman-details/(\d+)/(\d+)/$', 'portal.views.ombudsman_details', name='editombudsman_details'),
    
    #Ajax
    url(r'^ajax-state/$', 'portal.views.ajax_state', name='ajax_state'),
    url(r'^ajax-location/$', 'portal.views.ajax_location', name='ajax_location'),
    url(r'^ajax-pincode/$', 'portal.views.ajax_pincode', name='ajax_pincode'),
)
