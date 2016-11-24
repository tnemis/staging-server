from django.views.generic import View,ListView, DetailView, CreateView, \
    DeleteView, UpdateView, \
    ArchiveIndexView, DateDetailView, \
    DayArchiveView, MonthArchiveView, \
    TodayArchiveView, WeekArchiveView, \
    YearArchiveView
from django.contrib import messages
from forms import Child_detailform
from baseapp.forms import Pool_databaseform
from django.shortcuts import *
from students.models import *
from django.db.models import Q
from baseapp.models import *
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger
from datetime import *
from django import template
from django.contrib import messages
from excel_response import ExcelResponse
from django.utils import simplejson
# from schemes.models import Student_schemes_2016_2017
import os
from django.conf import settings
from django.core.files.base import ContentFile
from django.db.models import *
from datetime import datetime
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import RequestContext
from django.conf import settings
import ho.pisa as pisa
import cStringIO as StringIO
import cgi
import os

        
        

class Nominal_roll_list(View):
    def get(self,request,**kwargs):
        pk=self.kwargs.get('pk')
        school_code = self.kwargs.get('school_code')
        school_id = request.user.account.associated_with
        schl_id = School.objects.get(id=school_id)
        class_students=Child_detail.objects.filter(school_id=school_id,transfer_flag__in=[0,2],class_studying=pk)
        child_detail_list = class_students.values("name","aadhaar_eid_number","aadhaar_uid_number","gender","dob","community__community_name","religion__religion_name","mothertounge__language_name","phone_number","child_differently_abled","differently_abled","child_disadvantaged_group","disadvantaged_group","subcaste__caste_name","nationality__nationality","house_address","native_district","pin_code","blood_group","mother_name","mother_occupation","father_name","father_occupation","parent_income","class_studying__class_studying","group_code__group_name","attendance_status","sport_participation","education_medium__education_medium","district__district_name","block__block_name","unique_id_no","school_id","staff_id","bank__bank","bank_account_no","schemes","academic_year__academic_year","transfer_flag","transfer_date","name_tamil","class_section","student_admitted_section","school_admission_no","bank_ifsc_code","sports_player","sports_name","community_certificate","child_status","height","weight","laptop_issued","laptop_slno","guardian_name")
        udise=schl_id.school_code
        if pk == '12':
            data = [[udise],
            ['S.no',
            'Unique Id',
            'Name', 
            'Gender', 
            'DoB', 
            'Differently_abled',
            'Differently_abled_id',
            'Religion',
            'Community', 
            'Subcaste',
            'Class',
            'Section',
            'Aadhaar',
            'Father name',
            'Mother name',
            'Mobile',
            'GROUP_CODE',
            'SUB1',
            'MED1',
            'SUB2',
            'MED2',
            'SUB3',
            'MED3',
            'SUB4',
            'MED4',
            'SUB5',
            'MED5',
            'SUB6',
            'MED6',
            'FLAG',
            'EXSUB',
            'SSLC_SCIENCE_PRAC_EXP']]
            S_No=0
            for i in child_detail_list:
                S_No+=1
                data.append([S_No,
                    str(i['unique_id_no']),
                    i['name'], 
                    i['gender'],
                    i['dob'],
                    i['child_differently_abled'],
                    i['differently_abled'],
                    i['religion__religion_name'], 
                    i['community__community_name'], 
                    i['subcaste__caste_name'],
                    i['class_studying__class_studying'],
                    i['class_section'],
                    i['aadhaar_uid_number'],
                    i['father_name'],
                    i['mother_name'],
                    i['phone_number'],
                    i['group_code__group_name'],
                    ])
            return ExcelResponse(data, 'HS_Nominal_roll_list',)

        if pk == '10':
            data = [[udise],
            ['S.no',
            'Unique Id',
            'Name', 
            'Gender', 
            'DoB', 
            'Differently_abled',
            'Differently_abled_id',
            'Religion',
            'Community', 
            'Subcaste',
            'Class',
            'Section',
            'Aadhaar',
            'Father name',
            'Mother name',
            'Mobile',
            'GROUP_CODE',
            'SUB1',
            'MED1',
            'SUB2',
            'MED2',
            'SUB3',
            'MED3',
            'SUB4',
            'MED4',
            'SUB5',
            'MED5',
            'SUB6',
            'MED6',
            'FLAG',
            'EXSUB',
            'SSLC_SCIENCE_PRAC_EXP']]
            S_No=0
            for i in child_detail_list:
                S_No+=1
                data.append([S_No,
                    str(i['unique_id_no']),
                    i['name'], 
                    i['gender'],
                    i['dob'],
                    i['child_differently_abled'],
                    i['differently_abled'],
                    i['religion__religion_name'], 
                    i['community__community_name'], 
                    i['subcaste__caste_name'],
                    i['class_studying__class_studying'],
                    i['class_section'],
                    i['aadhaar_uid_number'],
                    i['father_name'],
                    i['mother_name'],
                    i['phone_number'],
                    i['group_code__group_name'],
                    ])
            return ExcelResponse(data, 'SSLC_Nominal_roll_list')
  
