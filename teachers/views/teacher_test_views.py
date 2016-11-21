from django.views.generic import View
from teachers.models import Teacher_detail,Teacher_test,test_master,Months,completed_table
from teachers.forms import Teacher_testform
from schoolnew.models import Basicinfo
from django.shortcuts import *
from django.contrib import messages
from django.db import *
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache


class Teacher_test_create(View):
    #@never_cache
    def get(self,request,**kwargs):
        if request.user.is_authenticated():
            import teacher_main_views
            if request.user.account.associated_with=='state' or request.user.account.associated_with=='DIPE' or request.user.account.associated_with=='CIPE' or request.user.account.associated_with=='Zone' or request.user.account.associated_with=='IAS' or request.user.account.associated_with=='IMS' :
                AEOENTRY=0
            else:
                AEOENTRY=teacher_main_views.aeoentrycheck(request.user.account.associated_with)
            form=Teacher_testform()
            tid=self.kwargs.get('pk')        
            staff_id = Teacher_detail.objects.get(id = tid)          
            basic_det=Basicinfo.objects.get(school_id=staff_id.school_id)
            school_id =staff_id.school_id
            dob=staff_id.dob
            staff_name=staff_id.name
            staff_uid=staff_id.count 
            dob=staff_id.dob        
            edu_list = Teacher_test.objects.filter(teacherid_id=tid)
            test=test_master.objects.all()
            mmonth=Months.objects.all()        
            if edu_list.count()==0: 
                messages.success(request, 'No Data') 
            teachers_posting_list = Teacher_test.objects.filter(teacherid_id=staff_id) 
            edu_list = Teacher_test.objects.filter(teacherid_id=staff_id) 
            return render(request,'teachers/test/teacher_test_form.html',locals()) 
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
       
    #@never_cache
    def post(self,request,**kwargs):
        if request.user.is_authenticated():
            form=Teacher_testform(request.POST,request.FILES)
            tid=self.kwargs.get('pk')        
            staff_id = Teacher_detail.objects.get(id = tid)          
            dategovt=staff_id.dofsed
            staff_name=staff_id.name
            staff_uid=staff_id.count         
            mmonth=Months.objects.all()           
            if form.is_valid():            
                test=Teacher_test(teacherid_id=tid,
                            tests_passed=form.cleaned_data['tests_passed'],
                            month=form.cleaned_data['month'],
                            year=form.cleaned_data['year'],
                            reg_no=form.cleaned_data['reg_no'],
                            gaz_no=form.cleaned_data['gaz_no'],
                            gaz_date=form.cleaned_data['gaz_date'],
                            page_no=form.cleaned_data['page_no'],
                            )
                test.save()
               
                b=completed_table.objects.get(teacherid_id=tid)        
                if b.Teacher_testpass=='0':
                    b.id=b.id
                    b.teacherid_id=b.teacherid_id
                    b.Teacher_testpass=7
                    b.save()
                msg = str(staff_name) + "(" + str(staff_uid)+") Test Passed details added successfully." 
                messages.success(request, msg ) 
                return redirect('teacher_test_create',pk=tid)

            else:
                print form.errors
                return render(request,'teachers/test/teacher_test_form.html',locals())  
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


class teacher_test_update(View):
    #@never_cache
    def get(self, request,**kwargs):
        if request.user.is_authenticated():
            tid=self.kwargs.get('pk')
            pk1=self.kwargs.get('pk1')
            staff_id = Teacher_detail.objects.get(id = tid)          
            basic_det=Basicinfo.objects.get(school_id=staff_id.school_id)
            school_id =staff_id.school_id
            dob=staff_id.dob 
            staff_name=staff_id.name
            staff_uid=staff_id.count              
            instance=Teacher_test.objects.get(id=pk1)       
            test=test_master.objects.all()
            mmonth=Months.objects.all()   
            form = Teacher_testform(instance=instance)
            teacherid_id = instance.teacherid_id
            tests_passed=instance.tests_passed
            month = instance.month  
            year =instance.year
            reg_no =instance.reg_no
            gaz_no =instance.gaz_no
            gaz_date =instance.gaz_date
            page_no = instance.page_no
            return render(request,'teachers/test/teacher_test_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    #@never_cache
    def post(self,request,**kwargs):
        if request.user.is_authenticated():
            tid=self.kwargs.get('pk')
            pk1=self.kwargs.get('pk1')
            staff_id = Teacher_detail.objects.get(id = tid)          
            dategovt=staff_id.dofsed
            staff_name=staff_id.name
            staff_uid=staff_id.count       
            test=test_master.objects.all()
            mmonth=Months.objects.all()            
            form = Teacher_testform(request.POST,request.FILES)       
            mgnt_edit = Teacher_test.objects.get(id=pk1)
            if form.is_valid():
                mgnt_edit.tests_passed=form.cleaned_data['tests_passed']
                mgnt_edit.month=form.cleaned_data['month']
                mgnt_edit.year=form.cleaned_data['year']
                mgnt_edit.reg_no=form.cleaned_data['reg_no'] 
                mgnt_edit.gaz_no=form.cleaned_data['gaz_no']
                mgnt_edit.gaz_date=form.cleaned_data['gaz_date']
                mgnt_edit.page_no=form.cleaned_data['page_no']           
                mgnt_edit.save()
                messages.success(request,'Test Passed Details Updated successfully')
                return redirect('teacher_test_create',pk=tid)
            else:
                print form.errors
                return render(request,'teachers/test/teacher_test_form.html',locals()) 
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))