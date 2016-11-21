from django.views.generic import View
from teachers.models import Teacher_detail,completed_table,Exam_duty,Camp_duty,Teacher_result_exam,Months,Teacher_posting_entry
from teachers.forms import Teacher_result_exam_form
from django.shortcuts import *
from schoolnew.models import *
from baseapp.models import *
from django.contrib import messages
from django.db import *
from datetime import datetime
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache


class exam_camp_duty_create(View):
    #@never_cache
    def get(self,request,**kwargs):
        if request.user.is_authenticated():
            import teacher_main_views
            if request.user.account.associated_with=='state' or request.user.account.associated_with=='DIPE' or request.user.account.associated_with=='CIPE' or request.user.account.associated_with=='Zone' or request.user.account.associated_with=='IAS' or request.user.account.associated_with=='IMS' :
                AEOENTRY=0
            else:

                AEOENTRY=teacher_main_views.aeoentrycheck(request.user.account.associated_with)
                
            # school_id = request.user.account.associated_with
            tid=self.kwargs.get('pk')        
            staff_id = Teacher_detail.objects.get(id = tid) 
            basic_det=Basicinfo.objects.get(school_id=staff_id.school_id)
            sch_key = basic_det.id           
            school_id =staff_id.school_id

            dategovt=staff_id.dofsed
            staff_name=staff_id.name
            staff_uid=staff_id.count           
            desig=User_desig.objects.all()
            
            subjects=Subject.objects.order_by('subject_name').values('subject_name').distinct()
            month_value=Months.objects.all()
            exams=Exam_duty.objects.all()
            camps=Camp_duty.objects.all()
            form=Teacher_result_exam_form()       
            edu_list = Teacher_result_exam.objects.filter(teacherid_id=tid)      
            if edu_list.count()==0:
                messages.success(request, 'No Data')       
            return render(request,'teachers/exam_camp_duty/exam_camp_details.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    
    #@never_cache
    def post(self,request,**kwargs):
        if request.user.is_authenticated():
            school_id = request.user.account.associated_with
            tid=self.kwargs.get('pk')        
            staff_id = Teacher_detail.objects.get(id = tid)          
            dategovt=staff_id.dofsed
            staff_name=staff_id.name
            staff_uid=staff_id.count        
            form=Teacher_result_exam_form(request.POST,request.FILES) 
            subject=request.POST.getlist('subject')
            appeared=request.POST.getlist('appeared')
            passed=request.POST.getlist('passed')
            percentage=request.POST.getlist('percentage')        
            exam_duty=request.POST.getlist('exam_duty')
            val_camp=request.POST.getlist('val_camp')
         
            if form.is_valid(): 
                regular=Teacher_result_exam(teacherid_id=tid,
                                month=form.cleaned_data['month'],
                                year=form.cleaned_data['year'],                            
                                subject=subject[0],
                                appeared=appeared[0],
                                passed=passed[0],
                                percentage=percentage[0],
                                exam_duty=exam_duty[0],
                                val_camp=val_camp[0],
                               
                               )
                regular.save() 
                regular=Teacher_result_exam(teacherid_id=tid,
                                month=form.cleaned_data['month'],
                                year=form.cleaned_data['year'],                            
                                subject=subject[1],
                                appeared=appeared[1],
                                passed=passed[1],
                                percentage=percentage[1],
                                exam_duty=exam_duty[1],
                                val_camp=val_camp[1],
                               
                               )
                regular.save() 
       
                b=completed_table.objects.get(teacherid_id=staff_id)        
                if b.Teacher_result=='0':
                    b.id=b.id
                    b.teacherid_id=b.teacherid_id
                    b.Teacher_result=19
                    b.save()     

                msg = str(staff_name) + "(" + str(staff_uid)+") Exam details added successfully."
                messages.success(request, msg )  
                return redirect('exam_camp_duty_create',pk=tid)
                
            else:
                print form.errors
                return render(request,'teachers/exam_camp_duty/exam_camp_details.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

                
           

class exam_camp_duty_update(View):
    #@never_cache
    def get(self, request,**kwargs):
        if request.user.is_authenticated():
            # school_id = request.user.account.associated_with
            tid=self.kwargs.get('pk')
            pk1=self.kwargs.get('pk1')
            edu_list = Teacher_result_exam.objects.filter(teacherid_id=tid)      
            if edu_list.count()==0:
                messages.success(request, 'No Data')       
            desig=User_desig.objects.all()
            month_value=Months.objects.all()
            exams=Exam_duty.objects.all()
            camps=Camp_duty.objects.all()
            staff_id = Teacher_detail.objects.get(id = tid)  
            basic_det=Basicinfo.objects.get(school_id=staff_id.school_id)
            sch_key = basic_det.id           
            school_id =staff_id.school_id

            dategovt=staff_id.dofsed
            staff_name=staff_id.name
            staff_uid=staff_id.count   
            instance=Teacher_result_exam.objects.get(id=pk1)
            form = Teacher_result_exam_form(instance=instance)        
            teacherid_id = instance.teacherid_id
            month =instance.month  
            year=instance.year
           
            subject=instance.subject
            appeared=instance.appeared
            passed=instance.passed
            percentage=instance.percentage
            exam_duty=instance.exam_duty
            val_camp=instance.val_camp
               
            return render(request,'teachers/exam_camp_duty/exam_camp_details_upd.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    #@never_cache
    def post(self,request,**kwargs):
        if request.user.is_authenticated():
            school_id = request.user.account.associated_with
            tid=self.kwargs.get('pk')
            pk1=self.kwargs.get('pk1')
            staff_id = Teacher_detail.objects.get(id = tid)          
            dategovt=staff_id.dofsed       
            staff_name=staff_id.name
            staff_uid=staff_id.count   
            posting_desg=Teacher_result_exam.objects.filter(teacherid_id=tid)
            form = Teacher_result_exam_form(request.POST,request.FILES)      
            mgnt_edit = Teacher_result_exam.objects.get(id=pk1)
            if form.is_valid():
                mgnt_edit.month=form.cleaned_data['month']
                mgnt_edit.year=form.cleaned_data['year']           
                mgnt_edit.subject=form.cleaned_data['subject']
                mgnt_edit.appeared=form.cleaned_data['appeared']            
                mgnt_edit.passed=form.cleaned_data['passed']            
                mgnt_edit.percentage=form.cleaned_data['percentage']            
                mgnt_edit.exam_duty=form.cleaned_data['exam_duty']
                mgnt_edit.val_camp=form.cleaned_data['val_camp']            
                mgnt_edit.save()
                messages.success(request,'Examination Purpose Details Updated successfully')
                return redirect('exam_camp_duty_create',pk=tid)

            else:
                print form.errors
                return render(request,'teachers/exam_camp_duty/exam_camp_details_upd.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

