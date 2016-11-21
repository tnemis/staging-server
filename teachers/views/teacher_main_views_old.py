from django.views.generic import View
from teachers.models import *
from schoolnew.models import *
from teachers.forms import *
from django.shortcuts import *
from baseapp.models import  Differently_abled,Language
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import connection
from datetime import datetime,time
from itertools import *
from django.db.models import Sum,Count
import itertools
from operator import itemgetter, attrgetter
from collections import defaultdict
import json 
from django.utils import simplejson
import os
from django.conf import settings
import teacher_main_views
import reportlab
import cStringIO as StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape
from excel_response import ExcelResponse
from django.contrib.auth import authenticate, login

def get_udisecode(id):
    from schoolnew.models import Basicinfo
    basic_det=Basicinfo.objects.get(school_id=id)
            
    school_id =basic_det.school_id
    return school_id


class download_staff_list(View):
    def get(self,request,**kwargs):       
        if request.user.is_authenticated():
            school_id = request.user.account.associated_with   
            staff_list = Teacher_detail.objects.values('name','count','pension_number','dob','gender','designation__user_desig','subject__desig_sub_name','dofsed','doregu','doprob','father_name','dojocs','dor','religion__religion_name','community__community_name','sub_caste__caste_name','father_name','mother_name','spouse_name','mothertongue__language_name','landline','phone_number','increment_month','aadhaar_number','pan_number','health_number','bank_account_no','branch__ifsc_code','pres_add_flatno','pres_add_street','pres_add_area','pres_add_city','present_pincode','present_district__district_name','differently_abled_type').filter(school_id=school_id).filter(ofs_flag=False).filter(transfer_flag='No')
       
            data = [['Name of the Staff', 'Unique ID No', 'GPF/CPS No', 'Date of Birth', 'Gender', 'Designation','Subject', 'Date of Joining','Date of Regularisation','Date of completion of Probation',  'Date of Joining in the Present School', 'Date of Retirement', 'Religion', 'Community', 'Caste', 'Father Name', 'Mother Name','Spouse Name','Mother Tongue', 'Phone No.', 'Mobile No.','Month of Increment','Aadhaar No.','PAN No.','Health Insurance No.',  'Bank A/C No.', 'Bank IFSc Code','Flat No.','Stree Name','Area','Village/Town/City', 'Pincode','District','Differently Abled']]

            
            for i in staff_list:
               data.append([i['name'], i['count'], i['pension_number'], i['dob'], i['gender'], i['designation__user_desig'], i['subject__desig_sub_name'], i['dofsed'], i['doregu'], i['doprob'], i['dojocs'], i['dor'], i['religion__religion_name'], i['community__community_name'], i['sub_caste__caste_name'], i['father_name'], i['mother_name'], i['spouse_name'], i['mothertongue__language_name'], i['landline'], i['phone_number'], i['increment_month'], i['aadhaar_number'], i['pan_number'], i['health_number'], i['bank_account_no'], i['branch__ifsc_code'], i['pres_add_flatno'], i['pres_add_street'], i['pres_add_area'], i['pres_add_city'], i['present_pincode'], i['present_district__district_name'], i['differently_abled_type']])
            return ExcelResponse(data, 'Teacher_detail')
        else:
           return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

def aeoentrycheck(id_no):
    pups_pums=0
    off_cat=0
    sch_mgnt=0
    private_mgnt=0
    AEOENTRY=0
    check1=0
    check2=0
    check3=0
    check4=0
    offcat_id_list=[2,3,4,5,6,7,8,9,10,11]
    management_cate_id_list=[1,2]
    management_id_list=[1,2,3]
    sch_cate_id_list=[8,9,10,11,12,13]
    
    if (Basicinfo.objects.filter(school_id=id_no).count())>0:
                basic_det=Basicinfo.objects.get(school_id=id_no)
                sch_key = basic_det.id
                if (basic_det.offcat_id):
                    off_cat=int(basic_det.offcat_id)

                if (basic_det.manage_cate_id):
                    private_mgnt=int(basic_det.manage_cate_id)
                if(basic_det.sch_management_id):
                    sch_mgnt=int(basic_det.sch_management_id)
                if(basic_det.sch_cate_id):
                    pups_pums=int(basic_det.sch_cate_id)
                
                if off_cat not in offcat_id_list:
                    check1=1

                if check1==1:
                    if private_mgnt==1:
                        for item in management_id_list:
                            if item==sch_mgnt:
                                check3=1
                        if check3==1:
                            if pups_pums in sch_cate_id_list:
                                AEOENTRY=1

                    elif private_mgnt==2:
                        if pups_pums in sch_cate_id_list:
                                AEOENTRY=1
    return AEOENTRY

class Teacher_registration(View):
    def get(self,request,**kwargs):
        teachers_name_list_new=Teacher_detail.objects.all()
        return render(request,'teachers/teachers_post_list.html',locals())

class Teacher_personnel_entry(View):
    def get(self,request,**kwargs):      
        return render(request,'teachers/teacher_registration.html',locals())


class Teacher_personnel_entry_after(View):
   def get(self, request,**kwargs):
        tid=self.kwargs.get('pk')
        data=Teacher_detail.objects.get(id=tid)
        basic_det=Basicinfo.objects.get(school_id=data.school_id)
        if request.user.account.associated_with=='state' or request.user.account.associated_with=='DIPE' or request.user.account.associated_with=='CIPE' or request.user.account.associated_with=='Zone' or request.user.account.associated_with=='IAS' or request.user.account.associated_with=='IMS' :
            AEOENTRY=0
        else:

            AEOENTRY=teacher_main_views.aeoentrycheck(request.user.account.associated_with)   
        request.session['staffid']=data.id
        request.session['staffuid']=data.count
        request.session['staffname']=data.name
        return render(request,'teachers/teacher_registration.html',locals())        

class Teachers_unique_id_generation(View):
    def get(self,request,**kwargs):
        teachers_name_list_new=Teacher_detail.objects.all()
        return render(request,'teachers/teachers_unique_id_generation.html',locals())

class Teachers_block_level_reports(View):
    def get(self,request,**kwargs):
        return render(request,'teachers/block_level_report_home.html',locals())

class School_scale_register_entry(View):
    def get(self,request,**kwargs):
        form=School_scale_register_form()
        designation_list=Teacher_designation.objects.all()
        scale_of_pay_list=Teacher_pay_band.objects.all()
        return render(request,'teachers/school_scale_register_entry.html',locals())

    def post(self,request,**kwargs):
        form=School_scale_register_form(request.POST)
        if form.is_valid():
            Scale=School_scale_register(
                school_id=form.cleaned_data['school_id'],
                staff_id=form.cleaned_data['staff_id'],
                sanctioned_post=form.cleaned_data['sanctioned_post'],
                scale_of_pay=form.cleaned_data['scale_of_pay'],
                number_of_sanctioned=form.cleaned_data['number_of_sanctioned'],
                mode_of_sanctioned=form.cleaned_data['mode_of_sanctioned'],
                go_no=form.cleaned_data['go_no'],
                continuance_order_number=form.cleaned_data['continuance_order_number'],
                period_for_temp=form.cleaned_data['period_for_temp'],
                date=form.cleaned_data['date'],
                remarks=form.cleaned_data['remarks'],
                )
            Scale.save()
            return render(request,'teachers/school_scale_register_entry.html',locals())

class School_scale_register(View):
    def get(self,request,**kwargs):        
        return render(request,'teachers/school_scale_register_entry.html',locals())
       
class Teachers_school_level_name_list(View):
    def get(self,request,**kwargs):
            pups_pums=0
            off_cat=0
            sch_mgnt=0
            private_mgnt=0
            AEOENTRY=0
            check1=0
            check2=0
            check3=0
            check4=0
            offcat_id_list=[2,3,4,5,6,7,8,9,10,11]
            management_cate_id_list=[1,2]
            management_id_list=[1,2,3,4,5,6,7,8,9,10,32]
            sch_cate_id_list=[8,9,10,11,12,13]
        
            school_code=self.kwargs.get('pk') 
            basic_det=Basicinfo.objects.get(udise_code=school_code)
          
            if request.user.account.user_category_id == 2:
                        
                teachers_name_list_new = Teacher_detail.objects.filter(school_id=basic_det.school_id).filter(ofs_flag=False).filter(transfer_flag='No')
            elif request.user.account.user_category_id > 18:
                teachers_name_list_new = Teacher_detail.objects.filter(school_id=basic_det.school_id).filter(ofs_flag=False).filter(transfer_flag='No')
            elif request.user.account.user_category_id == 18:
                if not(basic_det.office_code):                        
                    teachers_name_list_new = Teacher_detail.objects.filter(school_id=basic_det.school_id).filter(ofs_flag=False).filter(transfer_flag='No')
                else:
                    teachers_name_list_new = Teacher_detail.objects.filter(school_id=basic_det.udise_code).filter(ofs_flag=False).filter(transfer_flag='No')
            elif request.user.account.user_category_id == 3:
                sc=scale_register_abstract.objects.all()
                for i in sc:
                    code=i.udise_code
                sc=Basicinfo.objects.get(udise_code=code)
                       
                teachers_name_list_new = Teacher_detail.objects.filter(school_id=sc.id).filter(ofs_flag=False).filter(transfer_flag='No')
            
            else:
                teachers_name_list_new = Teacher_detail.objects.filter(school_id=request.user.account.associated_with).filter(ofs_flag=False).filter(transfer_flag='No')
            if basic_det:
                    basic_det=Basicinfo.objects.get(udise_code=school_code)
                    sch_key = basic_det.id
                    if (basic_det.offcat_id):
                        off_cat=int(basic_det.offcat_id)
                    if basic_det.manage_cate_id:
                        private_mgnt=int(basic_det.manage_cate_id)
                    if basic_det.sch_management_id:
                        sch_mgnt=int(basic_det.sch_management_id)
                    if basic_det.sch_cate_id:
                        pups_pums=int(basic_det.sch_cate_id)
                                       
                    if off_cat not in offcat_id_list:
                        check1=1

                    if check1==1:
                        if private_mgnt==1:
                            for item in management_id_list:
                                if item==sch_mgnt:
                                    check3=1
                            if check3==1:
                                if pups_pums in sch_cate_id_list:
                                    AEOENTRY=1

                        elif private_mgnt==2:
                            if pups_pums in sch_cate_id_list:
                                    AEOENTRY=1
            if request.user.account.user_category_id==18:
                AEOENTRY=0
            teacher_count=teachers_name_list_new.count()
            if teacher_count==0:
                messages.warning(request, 'No data')
                if request.user.account.associated_with=='state' or request.user.account.associated_with=='DIPE' or request.user.account.associated_with=='CIPE' or request.user.account.associated_with=='Zone' or request.user.account.associated_with=='IAS' or request.user.account.associated_with=='IMS' or request.user.account.user_category_id > 18:
                    return HttpResponseRedirect('/teachers/staff_detailListView/')
                elif request.user.account.user_category_id == 18:
                    if basic_det.office_code==None:
                        return redirect('teacher_detailListView',cat_id=basic_det.school_id)
                    else:
                        return HttpResponseRedirect('/teachers/staff_detailListView/')
                else:
                    return HttpResponseRedirect('/teachers/teacher_detailListView/')
            superannum={}
            for i in teachers_name_list_new:
               
                if i.super_annum_flag ==False :
                 
                    dor=i.dor
                    dorfmt=i.dor.strftime("%d/%m/%Y")
                    d1 = datetime.strptime(dorfmt, "%d/%m/%Y")
                    
                    t=datetime.now()
                    today=t.strftime("%d/%m/%Y")
                    tod=datetime.strptime(today, "%d/%m/%Y")
                    
                    diff=d1-tod
                    superannum[i.id] = diff.days
                flag=i.school_office
            return render(request,'teachers/teachers_name_list.html',locals())
        
    
    def post(self,request,**kwargs):
        superannum=request.POST['superannum']
        if superannum == 'yes':
            super_annum_flag=True
        else:
            super_annum_flag=False
        tid=request.POST['tid']
        teachers_name = Teacher_detail.objects.filter(school_id=request.user.account.associated_with).filter(transfer_flag='No').filter(ofs_flag=False)
        teachers_name1=teachers_name.get(id=int(tid))
        if superannum=='yes' :
             teachers_name1.super_annum_flag =super_annum_flag
             teachers_name1.id=tid
             teachers_name1.save()
        elif superannum=='No' :
            return HttpResponseRedirect('/teachers/teacher_outofservice/%d/' %int(tid))
        
        basic_det=Basicinfo.objects.get(school_id=school_id)
        return redirect('teachers_school_level_name_list',pk=basic_det.udise_code)
        
def generate(i,j):
    mag_code=int(i)
    staff_type=int(j)
    if (mag_code==11 and staff_type==1):
        x=int(mag_code)*10000000+int(staff_type)*1000000+count_DSE_Teaching.objects.all().count()
        x+=1
        m=count_DSE_Teaching(count_DSE_Teaching=x)
        m.save()    
    elif (mag_code==11 or mag_code==22 and staff_type==2):
        x=11*10000000+int(staff_type)*1000000+count_DSE_Non_Teaching.objects.all().count()
        x+=1
        n=count_DSE_Non_Teaching(count_DSE_Non_Teaching=x)
        n.save()
    elif (mag_code==22 and staff_type==1):
        x=int(mag_code)*10000000+int(staff_type)*1000000+count_DEE_Teaching.objects.all().count()
        x+=1
        o=count_DEE_Teaching(count_DEE_Teaching=x)
        o.save()
        
    d=Count_id.objects.all().count()
    d+=1
    f=Count_id(count_stand=d)
    f.save()
    return x

class Teacher_new_entry(View):    
    def get(self,request,**kwargs):
        code=self.kwargs.get('code')
        flag=int(self.kwargs.get('office_code'))
        school_office=flag
        teaching_entry=Staff.objects.get(id=code)
        desig=teaching_entry.post_name
        sub_staff=teaching_entry.post_sub
        staffs_type=teaching_entry.staff_cat
        stafs=staffs_type
        post_go_id=teaching_entry.id
        p_desg=User_desig.objects.get(user_desig=desig)
        
        service_type= p_desg.ser_type
        
        if request.user.account.user_category_id==1 or request.user.account.user_category_id==2 or request.user.account.user_category_id==18 or request.user.account.user_category_id==3 or request.user.account.user_category_id==18:
            basic_det=Basicinfo.objects.get(id=teaching_entry.school_key_id)
            sch_code=basic_det.school_id
        else:
            basic_det=Basicinfo.objects.get(id=teaching_entry.school_key_id)
            sch_code=basic_det.school_id
        
        if basic_det.sch_cate:
            pay_drawing_cata=basic_det.sch_cate.id   
        
        udise_code=basic_det.udise_code
        if request.user.account.user_category_id>2:
           management_type='Government' 
        else:
            management_type=str(basic_det.manage_cate)
        
        posting_desg=User_desig.objects.all()
        subject1=Desig_subjects.objects.all()

        form=Teacher_detailform()
        differently_abled_list = Differently_abled.objects.all().order_by('da_name')
        district_list = District.objects.all().exclude(district_name='None').order_by('district_name')
        present_district_list = Present_District.objects.all().exclude(district_name='None').order_by('district_name')
        permanent_district_list = Permanent_District.objects.all().exclude(district_name='None').order_by('district_name')
        language_list = Language.objects.all().exclude(language_name='Undefined').order_by('language_name')
        religion_list = T_Religion.objects.all().exclude(religion_name='Undefined').order_by('id')
        community_list = T_Community.objects.all().exclude(community_name='undefined').order_by('id')
        ban_dist=Bank_district.objects.all()
        bank_list = Bank.objects.all()
        
        pay_drawing_officer_list=Teacher_pay_officer.objects.all()
        sub_caste=T_Sub_Castes.objects.all()        
        differently_abled_type=''
        teacher_differently_abled=''
        post=Posting_type.objects.all()

        return render(request,'teachers/teacher_detail_form.html',locals())

    def post(self,request,**kwargs):
        code=self.kwargs.get('code')
        flag=int(self.kwargs.get('office_code'))
        form = Teacher_detailform(request.POST,request.FILES) 
        teaching_entry=Staff.objects.get(id=code)
 
        if request.user.account.user_category_id==1 or request.user.account.user_category_id==2 or request.user.account.user_category_id==18 or request.user.account.user_category_id==3 or request.user.account.user_category_id==18 or request.user.account.user_category_id>18:
            basic_det=Basicinfo.objects.get(id=teaching_entry.school_key_id)
        man = request.POST['management']
        management=basic_det.manage_cate_id
        if management:
            if management==1:
                directorate=basic_det.sch_directorate_id
                if directorate==1:
                    management=11
                elif basic_det.sch_directorate.department_code=='002':
                    management=22
        else:
            management=11
        sta = request.POST['stafs']
        pf_with_suffix= request.POST['pension_number'] +"/"+request.POST['suf_name']
               
        x=generate(management,sta)
        
        if form.is_valid():
            Teacher=Teacher_detail(
                count=x, 
                school_id = form.cleaned_data['school_id'],
                name = form.cleaned_data['name'],
                name_tamil = form.cleaned_data['name_tamil'],
                dob = form.cleaned_data['dob'],
                gender = form.cleaned_data['gender'],
                management = form.cleaned_data['management'],
                stafs = form.cleaned_data['stafs'],
                designation = form.cleaned_data['designation'], 
                subject = form.cleaned_data['subject'],  
                post_go_id = form.cleaned_data['post_go_id'],
                mother_name = form.cleaned_data['mother_name'], 
                father_name = form.cleaned_data['father_name'], 
                marital = form.cleaned_data['marital'],
                spouse_name = form.cleaned_data['spouse_name'], 
                religion = form.cleaned_data['religion'], 
                community=form.cleaned_data['community'],
                sub_caste = form.cleaned_data['sub_caste'],
                mothertongue = form.cleaned_data['mothertongue'],  
                native_district = form.cleaned_data['native_district'],
                imark1 = form.cleaned_data['imark1'], 
                imark2 = form.cleaned_data['imark2'], 
                blood_group = form.cleaned_data['blood_group'], 
                height = form.cleaned_data['height'], 
                weight = form.cleaned_data['weight'], 
                email = form.cleaned_data['email'], 
                phone_number = form.cleaned_data['phone_number'], 
                landline=form.cleaned_data['landline'],
                pan_number = form.cleaned_data['pan_number'], 
                aadhaar_number = form.cleaned_data['aadhaar_number'], 
                health_number = form.cleaned_data['health_number'],  
                bank_dist = form.cleaned_data['bank_dist'],
                bank = form.cleaned_data['bank'], 
                branch = form.cleaned_data['branch'], 
                bank_account_no = form.cleaned_data['bank_account_no'], 
                passport = form.cleaned_data['passport'],  
                passport_no = form.cleaned_data['passport_no'], 
                passport_date_from = form.cleaned_data['passport_date_from'], 
                passport_date_to = form.cleaned_data['passport_date_to'],
                pres_add_flatno= form.cleaned_data['pres_add_flatno'],
                pres_add_street= form.cleaned_data['pres_add_street'],
                pres_add_area= form.cleaned_data['pres_add_area'],
                pres_add_city= form.cleaned_data['pres_add_city'],
                present_pincode = form.cleaned_data['present_pincode'],
                present_district = form.cleaned_data['present_district'],
                perm_add_flatno= form.cleaned_data['perm_add_flatno'],
                perm_add_street= form.cleaned_data['perm_add_street'],
                perm_add_area= form.cleaned_data['perm_add_area'],
                perm_add_city= form.cleaned_data['perm_add_city'],
                permanent_pincode = form.cleaned_data['permanent_pincode'], 
                pension_name = form.cleaned_data['pension_name'],  
                pension_number = pf_with_suffix, 
                dofags = form.cleaned_data['dofags'],
                dojocs = form.cleaned_data['dojocs'],
                dojocs_session = form.cleaned_data['dojocs_session'],
                topocs = form.cleaned_data['topocs'],
                designation_fags = form.cleaned_data['designation_fags'],  
                dofsed = form.cleaned_data['dofsed'], 
                designation_fased = form.cleaned_data['designation_fased'],
                doregu = form.cleaned_data['doregu'],
                doregu_session = form.cleaned_data['doregu_session'],
                uta = form.cleaned_data['uta'], 
                uta_date = form.cleaned_data['uta_date'],
                uta_order_no=form.cleaned_data['uta_order_no'],
                doprob = form.cleaned_data['doprob'],
                doprob_session = form.cleaned_data['doprob_session'],
                typewite_skill_level = form.cleaned_data['typewite_skill_level'],
                tamil_jr = form.cleaned_data['tamil_jr'],
                tamil_sr = form.cleaned_data['tamil_sr'],
                eng_jr = form.cleaned_data['eng_jr'],
                eng_sr = form.cleaned_data['eng_sr'],
                employment_status = form.cleaned_data['employment_status'],
                appointed_aided = form.cleaned_data['appointed_aided'], 
                approval_aided_date = form.cleaned_data['approval_aided_date'], 
                aided_order_no = form.cleaned_data['aided_order_no'], 
                pay_drawing_officer = form.cleaned_data['pay_drawing_officer'],  
                increment_month = form.cleaned_data['increment_month'],  
                language_test = form.cleaned_data['language_test'], 
                evaluation = form.cleaned_data['evaluation'],  
                evaluation_date = form.cleaned_data['evaluation_date'], 
                eval_order_no = form.cleaned_data['eval_order_no'], 
                evaluation_auth=form.cleaned_data['evaluation_auth'], 
                teacher_differently_abled=form.cleaned_data['teacher_differently_abled'],
                differently_abled_type=form.cleaned_data['differently_abled_type'], 
                dor = form.cleaned_data['dor'],
                school_office=form.cleaned_data['school_office'],
                uploadfile=request.FILES['uploadfile'],
                )
            Teacher.save()

            teaching_entry=Staff.objects.get(id=code)
            teaching_entry.post_filled=teaching_entry.post_filled+1
            teaching_entry.post_vac=teaching_entry.post_vac-1
            teaching_entry.save()            

            c=completed_table(teacherid_id=Teacher.id,school_id=Teacher.school_id)
            c.save()
            
            
            msg = (Teacher.name).upper() +" "+ str(Teacher.designation) + "  added successfully." + " Staff Id : " + str(Teacher.count) +"."
            request.session['staffid']=Teacher.id
            request.session['staffuid']=Teacher.count
            request.session['staffname']=form.cleaned_data['name']
            staff_id=request.session['staffid']
            staff_name=request.session['staffname']
            
            photo_fetch= settings.MEDIA_ROOT+'/' + str(Teacher.uploadfile)
            photo_file=settings.MEDIA_ROOT+'/' + 'teachers_pics'+'/' + str(x) + ".jpg"
            
            os.rename(photo_fetch,photo_file)
           
            b=Teacher_detail.objects.get(count=x)
            
            if b.count==x:
                b.id=b.id
                b.uploadfile='teachers_pics'+'/' + str(x) + ".jpg"
                b.save()
            desig_id=User_desig.objects.get(user_desig=Teacher.designation)
            school_name2=basic_det.school_name + " -- " +str(basic_det.school_code)
            regular=Teacher_posting_entry(teacherid_id=Teacher.id,
                       designation=desig_id,
                       district_id=basic_det.district_id,
                       block_id=basic_det.block_id,
                       school_name1=school_name2,                        
                       type_of_posting=Teacher.topocs,
                       period_from=Teacher.dojocs                       
                       )
            regular.save()

            messages.success(request, msg )
            if request.user.account.user_category_id==2:
                return redirect('teacher_detailListView1',cat_id=Teacher.school_id)    
            elif request.user.account.user_category_id==18:
                if flag==1:
                    return redirect('teacher_detailListView',cat_id=Teacher.school_id)    
                else:
                    return HttpResponseRedirect('/teachers/staff_detailListView')
            elif request.user.account.user_category_id>=18:
                return HttpResponseRedirect('/teachers/staff_detailListView')                
            else:
                return HttpResponseRedirect('/teachers/teacher_detailListView')
        else:
            print form.errors
            return render (request,'teachers/teacher_detail_form.html',locals())
 

class Teacher_update(View):
    def get(self, request,**kwargs):
        tid=self.kwargs.get('pk')
        instance = Teacher_detail.objects.get(id=tid)
        
        desig=instance.designation
        p_desg=User_desig.objects.get(user_desig=desig)
        
        service_type= p_desg.ser_type
        sub_staff=instance.subject
        sch_code= instance.school_id 
        post_go_id = instance.post_go_id
        basic_det=Basicinfo.objects.get(school_id=sch_code)      
        form = Teacher_detailform(instance=instance)
        count=instance.count
        photo = instance.uploadfile
        name = instance.name  
        dob = instance.dob
        dor = instance.dor
        gender=instance.gender
        management = instance.management  

        designation= instance.designation.id
        subject= instance.subject.id

        stafs =instance.stafs  
        mother_name = instance.mother_name  
        father_name =  instance.father_name  
        marital = instance.marital  
        spouse_name = instance.spouse_name   
        religion_value = instance.religion   
        community=instance.community  
        sub_caste = instance.sub_caste  
        mothertongue = instance.mothertongue  
        native_district = instance.native_district  
        imark1 = instance.imark1  
        imark2 = instance.imark2  
        bg =instance.blood_group  
        height = instance.height  
        weight = instance.weight  
        email = instance.email  
        phone_number =instance.phone_number  
        landline=instance.landline
        pan_number = instance.pan_number  
        aadhaar_number = instance.aadhaar_number  
        health_number =instance.health_number 
        bank_dist = instance.bank_dist
        school_office=instance.school_office
        bank = instance.bank  
        branch = instance.branch  
        bank_account_no = instance.bank_account_no  
        passport = instance.passport  
        passport_no = instance.passport_no  
        passport_date_from = instance.passport_date_from  
        passport_date_to = instance.passport_date_to 
        pres_add_flatno=instance.pres_add_flatno
        pres_add_street=instance.pres_add_street
        pres_add_area=instance.pres_add_area
        pres_add_city=instance.pres_add_city
        present_district=instance.present_district
        present_pincode=instance.present_pincode
        perm_add_flatno=instance.perm_add_flatno
        perm_add_street=instance.perm_add_street
        perm_add_area=instance.perm_add_area
        perm_add_city=instance.perm_add_city
        permanent_pincode =instance.permanent_pincode
        p_name = instance.pension_name  
        
        q = instance.pension_number  
        a=q.split('/')
        pension_number=a[0]
        suf_name=a[1]
        
        designation = instance.designation  
        subject = instance.subject  
        dofags = instance.dofags  
        designation_fags = instance.designation_fags   
        dofsed = instance.dofsed  
        dojocs=instance.dojocs
        dojocs_session=instance.dojocs_session
        topocs=instance.topocs
        designation_fased_value = instance.designation_fased  
        
        a=User_desig.objects.get(id=designation_fased_value)
        designation_fased_value_text=a.user_desig
        doregu = instance.doregu  
        doregu_session = instance.doregu_session  
        uta = instance.uta  
        uta_date = instance.uta_date  
        uta_order_no= instance.uta_order_no  
        doprob = instance.doprob  
        doprob_session = instance.doprob_session  
        
        typewite_skill_level = instance.typewite_skill_level  
        tamil_jr = instance.tamil_jr
        tamil_sr = instance.tamil_sr
        eng_jr = instance.eng_jr
        eng_sr = instance.eng_sr
        
        emp_status = instance.employment_status 

        teacher_differently_abled=instance.teacher_differently_abled
        differently_abled_type=instance.differently_abled_type

        
        appointed_aided = instance.appointed_aided
        appointed_aided_date=instance.appointed_aided_date
        approval_aided_date = instance.approval_aided_date 
        aided_order_no = instance.aided_order_no  
        pay = instance.pay_drawing_officer  
        increment = instance.increment_month  
        language_test = instance.language_test  
        evaluation = instance.evaluation  
        evaluation_date = instance.evaluation_date  
        eval_order_no = instance.eval_order_no  
        evaluation_auth=instance.evaluation_auth  

        district_list = District.objects.all().exclude(district_name='None').order_by('district_name')
        language_list = Language.objects.all().exclude(language_name='Undefined').order_by('language_name')
        religion_list = T_Religion.objects.all().exclude(religion_name='Undefined').order_by('id')
        community_list = T_Community.objects.all().exclude(community_name='undefined').order_by('id')
        sub_caste=T_Sub_Castes.objects.all()
        ban_dist = Bank_district.objects.all()
        present_district_list=Present_District.objects.all()
        permanent_district_list=Permanent_District.objects.all()
        pay_drawing_officer_list=Teacher_pay_officer.objects.all()
        posting_desg=User_desig.objects.all()
        post=Posting_type.objects.all()
        uploadfile=instance.uploadfile
        photo_file=settings.MEDIA_ROOT+'/' + 'teachers_pics'+'/' + str(count) + ".jpg"



        return render(request,'teachers/teacher_detail_form.html',locals())
    
    def post(self,request,**kwargs):
        pk=self.kwargs.get('pk')

        form1 = Teacher_detailform1(request.POST,request.FILES)     
        if form1.is_valid():
            print 'valid'
        else:
            print ' not valid'
            print form1.cleaned_data['designation']
            print form1.errors
        teacher_edit = Teacher_detail.objects.get(id=pk)
       
        count = teacher_edit.count
        school_id=teacher_edit.school_id

        school_office=teacher_edit.school_office
      
        teacher_edit.count=count
        teacher_edit.school_id=school_id      
        teacher_edit.school_office=school_office
        
        stud_photo = teacher_edit.uploadfile
       

        pf_with_suffix= request.POST['pension_number'] +"/"+request.POST['suf_name']
        if request.POST.get('clear_photo') == "True":
            photo_file=settings.MEDIA_ROOT+'/' + 'teachers_pics'+'/' + str(count) + ".jpg"
            
            os.remove(photo_file)
            student1_photo=request.FILES['uploadfile']
            student_photo = student1_photo
        else:
            student_photo = stud_photo  

               
        if form1.is_valid():
            c=form1.cleaned_data['pension_name'] + "/" + request.POST['suf_name']
            teacher_edit.name=form1.cleaned_data['name']
            teacher_edit.dob=form1.cleaned_data['dob']
            teacher_edit.gender=form1.cleaned_data['gender']
            teacher_edit.management=form1.cleaned_data['management']
            teacher_edit.stafs=form1.cleaned_data['stafs']
            teacher_edit.designation=form1.cleaned_data['designation']
            teacher_edit.dojocs = form1.cleaned_data['dojocs']
            teacher_edit.dojocs_session=form1.cleaned_data['dojocs_session']
            teacher_edit.topocs = form1.cleaned_data['topocs']
            teacher_edit.subject=form1.cleaned_data['subject']
            teacher_edit.post_go_id = form1.cleaned_data['post_go_id']
            teacher_edit.mother_name=form1.cleaned_data['mother_name']
            teacher_edit.father_name=form1.cleaned_data['father_name']
            teacher_edit.marital=form1.cleaned_data['marital']
            teacher_edit.spouse_name=form1.cleaned_data['spouse_name']
            teacher_edit.religion=form1.cleaned_data['religion']
            teacher_edit.community=form1.cleaned_data['community']
            teacher_edit.sub_caste=form1.cleaned_data['sub_caste']
            teacher_edit.mothertongue=form1.cleaned_data['mothertongue']
            teacher_edit.native_district=form1.cleaned_data['native_district']
            teacher_edit.imark1=form1.cleaned_data['imark1']
            teacher_edit.imark2=form1.cleaned_data['imark2']
            
            teacher_edit.blood_group=form1.cleaned_data['blood_group']
            teacher_edit.height=form1.cleaned_data['height']
            teacher_edit.weight=form1.cleaned_data['weight']
            teacher_edit.email=form1.cleaned_data['email']
            teacher_edit.phone_number=form1.cleaned_data['phone_number']
            teacher_edit.landline=form1.cleaned_data['landline']
            teacher_edit.pan_number=form1.cleaned_data['pan_number']
            teacher_edit.aadhaar_number=form1.cleaned_data['aadhaar_number']
            teacher_edit.health_number=form1.cleaned_data['health_number']
            teacher_edit.bank_dist =form1.cleaned_data['bank_dist']
            teacher_edit.bank=form1.cleaned_data['bank']
            teacher_edit.branch=form1.cleaned_data['branch']
            teacher_edit.bank_account_no=form1.cleaned_data['bank_account_no']
            teacher_edit.passport=form1.cleaned_data['passport']
            teacher_edit.passport_no=form1.cleaned_data['passport_no']
            teacher_edit.passport_date_from=form1.cleaned_data['passport_date_from']
            teacher_edit.passport_date_to=form1.cleaned_data['passport_date_to']
            teacher_edit.pres_add_flatno=form1.cleaned_data['pres_add_flatno']
            teacher_edit.pres_add_street=form1.cleaned_data['pres_add_street']
            teacher_edit.pres_add_area=form1.cleaned_data['pres_add_area']
            teacher_edit.pres_add_city=form1.cleaned_data['pres_add_city']
            teacher_edit.present_pincode=form1.cleaned_data['present_pincode']
            teacher_edit.perm_add_flatno=form1.cleaned_data['perm_add_flatno']
            teacher_edit.perm_add_street=form1.cleaned_data['perm_add_street']
            teacher_edit.perm_add_area=form1.cleaned_data['perm_add_area']
            teacher_edit.perm_add_city=form1.cleaned_data['perm_add_city']
            teacher_edit.permanent_pincode=form1.cleaned_data['permanent_pincode']
            teacher_edit.teacher_differently_abled=form1.cleaned_data['teacher_differently_abled']
            teacher_edit.differently_abled_type=form1.cleaned_data['differently_abled_type']


            teacher_edit.pension_name=form1.cleaned_data['pension_name']
            teacher_edit.pension_number=pf_with_suffix#form1.cleaned_data['pension_number']
            teacher_edit.designation=form1.cleaned_data['designation']
            teacher_edit.subject=form1.cleaned_data['subject']
            teacher_edit.dofags=form1.cleaned_data['dofags']
            teacher_edit.designation_fags=form1.cleaned_data['designation_fags']
            teacher_edit.dofsed=form1.cleaned_data['dofsed']
            teacher_edit.designation_fased=form1.cleaned_data['designation_fased']
            teacher_edit.doregu=form1.cleaned_data['doregu']
            teacher_edit.doregu_session=form1.cleaned_data['doregu_session']
            teacher_edit.uta=form1.cleaned_data['uta']
            teacher_edit.uta_date=form1.cleaned_data['uta_date']
            teacher_edit.uta_order_no=form1.cleaned_data['uta_order_no']
            teacher_edit.doprob=form1.cleaned_data['doprob']
            teacher_edit.doprob_session=form1.cleaned_data['doprob_session']
            # teacher_edit.designation_relinq=form1.cleaned_data['designation_relinq']
            teacher_edit.typewite_skill_level=form1.cleaned_data['typewite_skill_level']
            teacher_edit.tamil_jr = form1.cleaned_data['tamil_jr']
            teacher_edit.tamil_sr = form1.cleaned_data['tamil_sr']
            teacher_edit.eng_jr = form1.cleaned_data['eng_jr']
            teacher_edit.eng_sr = form1.cleaned_data['eng_sr']
            teacher_edit.employment_status=form1.cleaned_data['employment_status']
            teacher_edit.appointed_aided=form1.cleaned_data['appointed_aided']
            teacher_edit.appointed_aided_date=form1.cleaned_data['appointed_aided_date']
            teacher_edit.approval_aided_date=form1.cleaned_data['approval_aided_date']
            teacher_edit.aided_order_no=form1.cleaned_data['aided_order_no']
            teacher_edit.evaluation = form1.cleaned_data['evaluation']  
            teacher_edit.evaluation_date = form1.cleaned_data['evaluation_date'] 
            teacher_edit.eval_order_no = form1.cleaned_data['eval_order_no'] 
            teacher_edit.evaluation_auth=form1.cleaned_data['evaluation_auth'] 
            teacher_edit.uploadfile=student_photo
            teacher_edit.dor=form1.cleaned_data['dor']
            teacher_edit.save()
        else:
            print form1.errors
            return render (request,'teachers/teacher_detail_form.html',locals())
        if request.POST.get('clear_photo') == "True":
            photo_file=settings.MEDIA_ROOT+'/' + 'teachers_pics'+'/' + str(count) + ".jpg"
            photo_fetch= settings.MEDIA_ROOT+'/' + str(teacher_edit.uploadfile)
            os.rename(photo_fetch,photo_file)
            
        b=Teacher_detail.objects.get(count=count)
            
        if b.count==count:
            b.id=b.id
            b.uploadfile='teachers_pics'+'/' + str(count) + ".jpg"
            b.save()
        msg = str(form1.cleaned_data['name']) +" "+ str(form1.cleaned_data['designation']) + "  details updated successfully." + "  Id : " + str(count) +"."
        request.session['staffid']=count
        request.session['staffname']=form1.cleaned_data['name']
        staff_id=request.session['staffid']
        staff_name=request.session['staffname']
        messages.success(request, msg )
        
        basic_det=Basicinfo.objects.get(school_id=b.school_id)
        return redirect('teachers_school_level_name_list',pk=basic_det.udise_code)


class Teacher_delete(View):
    def get(self, request,**kwargs):
        tid=self.kwargs.get('pk')
        data=Teacher_detail.objects.get(id=tid)
        return render(request,'teachers/teacher_delete.html',locals())

    def post(self, request,**kwargs):
        tid=self.kwargs.get('pk')
        data=Teacher_detail.objects.get(id=tid)
        msg = data.name +" with "+ str(data.designation) + "  details removed successfully." 
        data.delete()
        messages.success(request,msg)
        basic_det=Basicinfo.objects.get(school_id=school_id)
        return redirect('teachers_school_level_name_list',pk=basic_det.udise_code)


class school_search10(View):
    def get(self,request,**kwargs): 
        if request.is_ajax():
            q = request.GET.get('term', '')
            udise =request.GET.get('term', '')[0:2]
            dist=(request.GET.get('district',''))
            blockid=Block.objects.get(block_name=dist)
          
            if  udise.isdigit() :
                
                school_nam = Basicinfo.objects.filter(block_id=blockid).filter(udise_code__icontains = int(q) )    
            else :
                
                school_nam = Basicinfo.objects.filter(block_id=blockid).filter(school_name__icontains = q )

            results = []
            
            for rec in school_nam:
                flag=Teacher_detail.objects.filter(transfer_flag='Yes')
                for i in flag:
                    if i.school_id==rec.school_id:
                        i_json = {}
                        i_json = i.id
                        i_json= str(rec.udise_code)+"-"+str(rec.school_name) +"-" +  str(dist)
                        results.append(i_json)
                        data = json.dumps(results)
                        mimetype = 'application/json'
                        break
        else:
            data = 'fail'
            mimetype = 'application/json'
        return HttpResponse(data,mimetype)

class Teacher_transfer(View):
    def get(self, request,**kwargs):
        school_code=self.kwargs.get('pk') 
        basic_det=Basicinfo.objects.get(udise_code=school_code)
        transfer_data = Teacher_detail.objects.filter(school_id=basic_det.school_id)
            
        AEOENTRY=1
        form=Teacher_transfer_purpose_form()    
        form1=Teacher_transfer_history_form()
        New_school_id=school_code 
                     
        return render(request,'teachers/teacher_transfer.html',locals())
    
    def post(self,request,**kwargs):
        old_school_name=request.POST['school_name']
        new_school_id=request.POST['new_school_id']
        data=old_school_name.split("-")
        old_school_data = Basicinfo.objects.filter(school_name__icontains = data[1]).filter(udise_code=data[0])
        old_school_id=old_school_data[0].school_id
        transfer_data = Teacher_detail.objects.filter(school_id=old_school_id)

        return render(request,'teachers/avail_teac_namelist.html',locals())
        
class avail_teac_namelist(View):
    def get(self, request,**kwargs):
        tid=self.kwargs.get('pk')
        school_code=self.kwargs.get('school_code')
        transfer_data=Teacher_detail.objects.filter(id=tid)
        New_school_id=school_code
        if transfer_data[0].school_office==1:
            basic_det=Basicinfo.objects.get(school_id=New_school_id)
        else:
            basic_det=Basicinfo.objects.get(udise_code=New_school_id)
        teaching=Staff.objects.filter(school_key_id=basic_det.id)
        for i in teaching :
            desig=User_desig.objects.get(id=i.post_name_id)
            sub=Desig_subjects.objects.get(id=i.post_sub_id,desig_id=desig.id)
            if desig.id==transfer_data[0].designation_id :
                if sub.id==transfer_data[0].subject_id :
                    if i.post_vac > 0:        
                        return render(request,'teachers/teachers_transfer_name_list.html',locals())
                    else :        
                        msg =  "No vaccant post available.Create the post before transfer."
                        messages.success(request, msg )
                        return render(request,'teachers/avail_teac_namelist.html',locals()) 
        msg =  "No vaccant post available.Create the post before transfer."
        messages.success(request, msg )
        return render(request,'teachers/avail_teac_namelist.html',locals()) 

    def post(self,request,**kwargs):
        school_code=self.kwargs.get('school_code')
        tid=self.kwargs.get('pk')
        New_school_id= int(school_code) 
        
        transfer_school_name=Teacher_detail.objects.get(id=tid)
        if request.user.account.user_category_id ==18:        
            sch_id_chk = Basicinfo.objects.get(udise_code=New_school_id)    
        else:
            sch_id_chk = Basicinfo.objects.get(udise_code=New_school_id)
        teaching=Staff.objects.filter(school_key_id=sch_id_chk.id)
            
        for i in teaching :
            desig=User_desig.objects.get(id=i.post_name_id)
            sub=Desig_subjects.objects.get(id=i.post_sub_id)
            if desig.id==transfer_school_name.designation_id :
                if sub.id==transfer_school_name.subject_id :
                    if i.post_sanc==i.post_filled+i.post_vac:
                        i.post_filled=i.post_filled+1
                        i.post_vac=i.post_vac - 1
                        i.save()
                    else:
                        msg =  "No vaccant post available.Create the post before transfer."
                        messages.success(request, msg)
                        return render(request,'teachers/teachers_transfer_name_list.html',locals())

        if transfer_school_name.udise_code < 33000000000:
            transfer_school_name.school_office=2
        else:
            transfer_school_name.school_office=1

        transfer_school_name.transfer_flag='No'
        
        sch=transfer_school_name.school_id
        
        from datetime import datetime as DT
        l =[]
        maxdate=Teacher_transfer_history.objects.filter(teacher=tid)
        if maxdate.count()>0:
            for i in maxdate:
                l.append((i.releiving_order_date))
            tr_records=Teacher_transfer_history.objects.get(teacher=tid,releiving_order_date=max(l))
        else:
            tr_records=Teacher_transfer_history.objects.get(teacher=tid)
        c=request.POST['joining_order_date']
        yymmddformat = datetime.strptime(c,'%d/%m/%Y').strftime('%Y-%m-%d')

        tr_records.joining_order_date=yymmddformat
        tr_records.joining_order_no=request.POST['oining_order_no']
         
        transfer_school_name.school_id=sch_id_chk.school_id
        transfer_school_name.save()
        tr_records.new_school_id=sch_id_chk.school_id
        tr_records.save()
        desig_id=User_desig.objects.get(id=tr_records.Designation_after_transfer)
        school_name2=sch_id_chk.school_name + " -- " +str(sch_id_chk.school_code)
        regular=Teacher_posting_entry(teacherid_id=tid,
                        designation_id=desig_id.id,
                        block_id=sch_id_chk.block_id,
                        school_name1=school_name2,
                        district_id=sch_id_chk.district_id,
                        type_of_posting_id=3,
                        period_from=tr_records.joining_order_date,
                        
                        )
        regular.save()  
        return render(request,'teachers/m.html',locals())

class Teacher_transfer_parent(View):
    def get(self, request,**kwargs):
        tid=self.kwargs.get('pk')
        subjects=Desig_subjects.objects.all().order_by('desig_sub_name')     
        transfer_data = Teacher_detail.objects.get(id=tid)
        basic_det=Basicinfo.objects.get(school_id=transfer_data.school_id)
        AEOENTRY=1
        dategovt=transfer_data.dofsed
        designations=User_desig.objects.all()
        form1=Teacher_transfer_history_form()
        return render(request,'teachers/teacher_tr_parent.html',locals())

    def post(self,request,**kwargs):
        old_school_id=request.POST['old_school_id']
        old_school_data=Basicinfo.objects.filter(school_id=old_school_id)
        tid=self.kwargs.get('pk')
        transfer_data = Teacher_detail.objects.get(id=tid)
        desig=User_desig.objects.filter()
        teaching=Staff.objects.filter(school_key_id=old_school_data[0].id)
        
        for i in teaching :
            desig=User_desig.objects.get(id=i.post_name_id)
            sub=Desig_subjects.objects.get(id=i.post_sub_id)
            if desig.id==transfer_data.designation_id :
                if sub.id==transfer_data.subject_id :
                    if i.post_sanc==i.post_filled+i.post_vac:
                        i.post_filled=i.post_filled-1
                        i.post_vac=i.post_vac + 1
                        i.save()
                    else:
                        msg =  "No vaccant post available.Create the post before transfer."
                        messages.success(request, msg)
                        return render(request,'teachers/teacher_tr_parent.html',locals())

        old_subject=transfer_data.subject

        reason=request.POST['reason']       
        
        form1=Teacher_transfer_history_form(request.POST)
        
        Designation_after_transfer=''
        
        transfer_data.transfer_flag ='Yes'

        transfer_data.save()

        if form1.is_valid():
            if int(reason)==4:
                Designation_after_transfer=form1.cleaned_data['Designation_after_transfer']
                subject_after_promotion=form1.cleaned_data['subject_after_promotion']
            else:
                Designation_after_transfer=transfer_data.designation_id
                subject_after_promotion=transfer_data.subject_id

            Tr_History=Teacher_transfer_history(
            teacher=tid,
            old_school_id=old_school_id,
            reason=reason,
            prev_subject=form1.cleaned_data['prev_subject'],
            subject_after_promotion=subject_after_promotion,
            previous_designation=form1.cleaned_data['previous_designation'],
            Designation_after_transfer=Designation_after_transfer,
            releiving_order_no=form1.cleaned_data['releiving_order_no'],
            releiving_order_date=form1.cleaned_data['releiving_order_date'],
          
            )
            Tr_History.save()

            transfer_data.designation_id=Designation_after_transfer
            transfer_data.subject_id=subject_after_promotion
            transfer_data.save()
        else:
            print form1.errors

        basic_det=Basicinfo.objects.get(school_id=old_school_id)
        return redirect('teachers_school_level_name_list',pk=basic_det.udise_code)


class Teacher_full_detail(View):
    def get (self,request,**kwargs):
        pk=self.kwargs.get('pk')
        pups_pums=0
        teacher = Teacher_detail.objects.get(id=pk)
        if request.user.account.user_category_id ==2 or request.user.account.user_category_id == 1:
            basic_det=Basicinfo.objects.get(school_id=teacher.school_id)
            AEOENTRY=aeoentrycheck(request.user.account.associated_with)
        elif request.user.account.user_category_id ==18:
            basic_det=Basicinfo.objects.get(school_id=teacher.school_id) 
        else:
            basic_det=Basicinfo.objects.get(school_id=teacher.school_id) 
        pups_pums=0    
        if basic_det.sch_cate_id:
            pups_pums=int(basic_det.sch_cate_id)
        if pups_pums==8 or pups_pums== 9 or pups_pums==10 or pups_pums==11 or pups_pums==12 or pups_pums==13:
            if request.user.account.user_category_id ==18:
                entry=1
            else:
                entry=0
        else:
            entry=1
    
        edu_list = Teacher_edu.objects.filter(teacherid_id=pk)
        school_info=Basicinfo.objects.get(school_id=teacher.school_id)      

        return render(request,'teachers/teacher_full_detail.html',locals())

class myview(View):
    def get(self,request,**kwargs):   
        pk=self.kwargs.get('pk')
        teacher = Teacher_detail.objects.get(id=pk)
        school=Basicinfo.objects.get(school_id=teacher.school_id)
        posting_list = Teacher_posting_entry.objects.filter(teacherid_id=pk)
        regularasation_list = Teacher_regularisation_entry.objects.filter(teacherid_id=pk)
        probation_list = Teacher_probation_entry.objects.filter(teacherid_id=pk)
        training_list = Teacher_training.objects.filter(teacherid_id=pk)
        testpass_list = Teacher_test.objects.filter(teacherid_id=pk)
        gpfloan_list = Teacher_GPF_loan.objects.filter(teacherid_id=pk)
        leave_list = Teacher_leave.objects.filter(teacherid_id=pk)
        action_list = Teacher_action.objects.filter(teacherid_id=pk)
        family_list = Teacher_family_detail.objects.filter(teacherid_id=pk)
        nomini_list = Teacher_nomini.objects.filter(teacherid_id=pk)
        loan_list = Teacher_loan.objects.filter(teacherid_id=pk)
        ltc_list = Teacher_ltc.objects.filter(teacherid_id=pk)
        leavesurr_list = Teacher_leave_surrender.objects.filter(teacherid_id=pk)
        immovalble_list = Teacher_immovalble_property.objects.filter(teacherid_id=pk)
        movable_list = Teacher_movable_property.objects.filter(teacherid_id=pk)
        leavecredit_list = Teacher_leave_credit.objects.filter(teacherid_id=pk)
        a=teacher.count
        edu_list = Teacher_edu.objects.filter(teacherid_id=pk)
        exam_list=Teacher_result_exam.objects.filter(teacherid_id=pk)
        award_list=Teacher_award.objects.filter(teacherid_id=pk)
        response = HttpResponse(content_type='application/pdf')
        filename = str(a)
        photo=settings.MEDIA_URL
        root=settings.MEDIA_ROOT
        
        response['Content-Disposition'] = 'attachement; filename={0}.pdf'.format(filename)
        pdf=render_to_pdf(
                'teachers/printpdf.html',
                {
                    
                    'teacher':teacher,
                    'edu_list':edu_list,
                    'school':school,
                    'pagesize':'A4',
                    'MEDIA_URL':root,
                    'posting_list':posting_list,
                    'regularasation_list':regularasation_list,
                    'probation_list':probation_list,
                    'training_list':training_list,
                    'testpass_list':testpass_list,
                    'gpfloan_list':gpfloan_list,
                    'leave_list':leave_list,
                    'action_list':action_list,
                    'family_list':family_list,
                    'nomini_list':nomini_list,
                    'loan_list':loan_list,
                    'ltc_list':ltc_list,
                    'leavesurr_list':leavesurr_list,
                    'immovalble_list':immovalble_list,
                    'movable_list':movable_list,
                    'leavecredit_list':leavecredit_list,
                    'exam_list':exam_list,
                    'award_list':award_list
                }
            )
        response.write(pdf)
        return response

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

class Teacher_full_detail_more(View):
    def get (self,request,**kwargs):
        pk=self.kwargs.get('pk')
        edu_list = Teacher_edu.objects.filter(teacherid_id=pk)
        posting_list = Teacher_posting_entry.objects.filter(teacherid_id=pk)
        regularasation_list = Teacher_regularisation_entry.objects.filter(teacherid_id=pk)
        probation_list = Teacher_probation_entry.objects.filter(teacherid_id=pk)
        training_list = Teacher_training.objects.filter(teacherid_id=pk)
        testpass_list = Teacher_test.objects.filter(teacherid_id=pk)
        gpfloan_list = Teacher_GPF_loan.objects.filter(teacherid_id=pk)
        leave_list = Teacher_leave.objects.filter(teacherid_id=pk)
        teacher = Teacher_detail.objects.get(id=pk)
        basic_det=Basicinfo.objects.get(school_id=teacher.school_id)
        return render(request,'teachers/teacher_full_detail2.html',locals())

class Teacher_full_detail_more1(View):
    def get (self,request,**kwargs):
        pk=self.kwargs.get('pk')
        exam_list=Teacher_result_exam.objects.filter(teacherid_id=pk)
        award_list=Teacher_award.objects.filter(teacherid_id=pk)
        action_list = Teacher_action.objects.filter(teacherid_id=pk)
        family_list = Teacher_family_detail.objects.filter(teacherid_id=pk)
        nomini_list = Teacher_nomini.objects.filter(teacherid_id=pk)
        loan_list = Teacher_loan.objects.filter(teacherid_id=pk)
        ltc_list = Teacher_ltc.objects.filter(teacherid_id=pk)
        leavesurr_list = Teacher_leave_surrender.objects.filter(teacherid_id=pk)
        immovalble_list = Teacher_immovalble_property.objects.filter(teacherid_id=pk)
        movable_list = Teacher_movable_property.objects.filter(teacherid_id=pk)
        leavecredit_list = Teacher_leave_credit.objects.filter(teacherid_id=pk)
        teacher = Teacher_detail.objects.get(id=pk)
        basic_det=Basicinfo.objects.get(school_id=teacher.school_id)
        return render(request,'teachers/teacher_full_detail3.html',locals())        

class Teacher_transfer_name_list(View):
    def get(self,request,**kwargs):
        try:
            school_code = self.request.GET.get('school_code')
            if request.user.account.user_category_id == 2:
                child_detail_list = School_child_count.objects.get(school__school_code=school_code, school__block_id= request.user.account.associated_with)
            elif request.user.account.user_category_id == 5:
                child_detail_list = School_child_count.objects.get(school__school_code=school_code, school__block_id= request.user.account.associated_with)
            elif request.user.account.user_category_id == 6 or request.user.account.user_category_id == 7 or request.user.account.user_category_id == 8 or request.user.account.user_category_id == 12 or request.user.account.user_category_id == 13 or request.user.account.user_category_id == 14:
                child_detail_list = School_child_count.objects.get(school__school_code=school_code, school__district_id= request.user.account.associated_with)
            elif request.user.account.user_category_id == 9 or request.user.account.user_category_id == 10 or request.user.account.user_category_id == 11 or request.user.account.user_category_id == 15 or request.user.account.user_category_id == 16 or request.user.account.user_category_id == 17 or request.user.account.user_category_id == 4:
                child_detail_list = School_child_count.objects.get(school__school_code=school_code)    
            else:
                teachers_name_list_new = Teacher_detail.objects.filter(school_id=request.user.account.associated_with)

            return render(request,'teachers/teachers_transfer_name_list.html',locals())
        except Teacher_personal_detail.DoesNotExist:
            messages.add_message(
                self.request,
                messages.ERROR,"No Teacher Data"
            )
            return render(request,'teachers/teachers_transfer_name_list.html',locals())


class Teacher_entry_details(View):
    def get(self,request,**kwargs):
        school_code=self.kwargs.get('pk') 
        basic_det=Basicinfo.objects.get(udise_code=school_code)
        print basic_det.school_id
        teachers = Teacher_detail.objects.filter(school_id=basic_det.school_id).filter(ofs_flag=False).filter(transfer_flag='No')
        complete=completed_table.objects.filter(school_id=basic_det.school_id) 
        return render(request,'teachers/teacher_entry_details.html',locals())

class Teacher_outofservice_create(View):
    def get(self,request,**kwargs):
        tid=self.kwargs.get('pk')    
        teachers=Teacher_detail.objects.get(id=tid) 
        dategovt=teachers.dofsed
        staff_uid=teachers.count
        staff_name=teachers.name
        basic_det=Basicinfo.objects.get(school_id=teachers.school_id)      
        return render(request,'teachers/outofservice/teacher_outofservice_form.html',locals())

    def post(self,request,**kwargs): 
        tid=self.kwargs.get('pk') 
        teachers=Teacher_detail.objects.get(id=tid)

        if teachers.ofs_flag==False:
            teachers.id=teachers.id
            teachers.ofs_reason=request.POST ['type_outofservice']
            c=request.POST['ofs_date']
            d2 = datetime.strptime(c,'%d/%m/%Y').strftime('%Y-%m-%d')
            teachers.ofs_date=d2
            teachers.ofs_flag=True
            teachers.save()
        b=completed_table.objects.get(teacherid_id=tid)
        if b.ofs_flag==False:
            b.id=b.id
            b.teacherid_id=b.teacherid_id
            b.ofs_flag=True
            b.save()
        messages.success(request,'Out of Service Details Updated successfully')   
        basic_det=Basicinfo.objects.get(school_id=teachers.school_id)
        return redirect('teachers_school_level_name_list',pk=basic_det.udise_code)

class teacher_promotion(View):
    def get(self, request,**kwargs):
        tid=self.kwargs.get('pk')
        
        AEOENTRY=1
        transfer_data = Teacher_detail.objects.get(id=tid)
        dategovt=transfer_data.dofsed
        b=transfer_data.designation.id
        a=transfer_data.subject.id
        if (Basicinfo.objects.filter(school_id=transfer_data.school_id).count())>0:
            basic_det=Basicinfo.objects.get(school_id=transfer_data.school_id)
            sch_key = basic_det.id
            designations=Staff.objects.filter(school_key=sch_key).distinct()
            desig1={}
            sub1={}
            subjects=Desig_subjects.objects.all()
            
            for i in designations :
                if i.post_vac > 0 : 
                    user_desig=User_desig.objects.get(id=i.post_name_id)
                    desig_sub=Desig_subjects.objects.get(id=i.post_sub_id)
                    desig1[i.post_name_id]=user_desig.user_desig
                    sub1[i.post_sub_id]=desig_sub.desig_sub_name + ' - ' + user_desig.user_desig
           
        form1=Teacher_transfer_history_form()
        return render(request,'teachers/teacher_promote_within.html',locals())

    def post(self,request,**kwargs):
        old_school_id=request.POST['old_school_id']
        old_school_data=Basicinfo.objects.get(school_id=old_school_id)
        tid=self.kwargs.get('pk')
        transfer_data = Teacher_detail.objects.get(id=tid)
        basic_det=Basicinfo.objects.get(school_id=transfer_data.school_id)
        desig_reset=User_desig.objects.get(user_desig=transfer_data.designation)
        sub_reset=Desig_subjects.objects.get(desig_sub_name=transfer_data.subject,desig_id=desig_reset.id) 
        teaching_rec=Staff.objects.filter(school_key_id=basic_det.id)
        for i in teaching_rec:
            if i.post_name_id==desig_reset.id and i.post_sub_id==sub_reset.id:
                    if i.post_sanc==i.post_filled+i.post_vac:
                        i.post_filled=i.post_filled -1
                        i.post_vac=i.post_vac+1
                        i.save()

        form1=Teacher_transfer_history_form(request.POST)        
        if form1.is_valid():            
            desig1=User_desig.objects.get(id=form1.cleaned_data['Designation_after_transfer'])
            sub1=Desig_subjects.objects.get(id=form1.cleaned_data['subject_after_promotion'])
            Tr_History=Teacher_transfer_history(
            teacher=tid,
            old_school_id=old_school_id,
            prev_subject=form1.cleaned_data['prev_subject'],
            previous_designation=form1.cleaned_data['previous_designation'],
            Designation_after_transfer=desig1.id,
            subject_after_promotion=sub1.id,
            releiving_order_no=form1.cleaned_data['releiving_order_no'],
            releiving_order_date=form1.cleaned_data['releiving_order_date'],
            joining_order_no=form1.cleaned_data['joining_order_no'],
            joining_order_date=form1.cleaned_data['joining_order_date'],
            )
            Tr_History.save()
            regular=Teacher_posting_entry.objects.get(teacherid_id=tid,period_to=None)
            regular.period_to=Tr_History.releiving_order_date                
            transfer_data.subject_id=Tr_History.subject_after_promotion
            transfer_data.designation_id=Tr_History.Designation_after_transfer            
            transfer_data.save()
           
            school_name2=basic_det.school_name + " -- " +str(basic_det.school_code)
            regular1=Teacher_posting_entry(teacherid_id=tid,
                        designation_id=Tr_History.Designation_after_transfer,
                        block_id=basic_det.block_id,
                        school_name1=school_name2,
                        district_id=basic_det.district_id,
                        type_of_posting_id=2,
                        period_from=Tr_History.joining_order_date,
                        
                        )
            messages.success(request, 'Transfer (within same school) completed successfully' )
            transfer_data=Teacher_detail.objects.get(id=tid)
            teaching=Staff.objects.filter(school_key_id=basic_det.id)

            for i in teaching :
                if i.post_name==transfer_data.designation :
                    if i.post_sub==transfer_data.subject :
                        if i.post_sanc==i.post_filled+i.post_vac:
                            i.post_filled=i.post_filled +1
                            i.post_vac=i.post_vac-1
                            i.save()
                        else:
                            messages.success(request, 'Post Vacant or Post sanction error' )
                            return render(request,'teachers/teacher_promote_within.html',locals())
            regular1.save()              
            regular.save()  
           
            return redirect('teachers_school_level_name_list',pk=basic_det.udise_code)
        else:
            print form1.errors
        return redirect('teachers_school_level_name_list',pk=basic_det.udise_code)
