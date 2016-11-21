from django.views.generic import View
from teachers.models import Teacher_detail,completed_table,Teacher_edu,Distinction,Months,Medium,Edu_subjects,Qualification
from schoolnew.models import Basicinfo
from teachers.forms import educationform
from django.shortcuts import *
from django.contrib import messages
from django.db import *
import _strptime
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache


class Teacher_education_create(View):
    #@never_cache
    def get(self,request,**kwargs):
        if request.user.is_authenticated():
            import teacher_main_views
            print 'request.user.account.associated_with'
            print request.user.account.associated_with
            if request.user.account.associated_with=='state' or request.user.account.associated_with=='DIPE' or request.user.account.associated_with=='CIPE' or request.user.account.associated_with=='Zone' or request.user.account.associated_with=='IAS' or request.user.account.associated_with=='IMS' :
                AEOENTRY=0
            else:
                AEOENTRY=teacher_main_views.aeoentrycheck(request.user.account.associated_with)   

            tid=self.kwargs.get('pk')        
            staff_id = Teacher_detail.objects.get(id = tid)  
            basic_det=Basicinfo.objects.get(school_id=staff_id.school_id)
            school_id =staff_id.school_id      
            dategovt=staff_id.dofsed
            staff_name=staff_id.name
            staff_uid=staff_id.count 
            dob=staff_id.dob 
            form=educationform()        
            qualification=Qualification.objects.all().order_by('qualification')
            subject=Edu_subjects.objects.all()
            medium_value=Medium.objects.all()
            month_value=Months.objects.all()
            class_value=Distinction.objects.all()
            edu_list = Teacher_edu.objects.filter(teacherid_id=tid)
            if edu_list.count()==0:
                messages.success(request,'No Data')        
            return render(request,'teachers/education/teacher_education_form_new.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    #@never_cache
    def post(self,request,**kwargs): 
        if request.user.is_authenticated():
            tid=self.kwargs.get('pk')        
            staff_id = Teacher_detail.objects.get(id = tid) 
            staff_name=staff_id.name
            staff_uid=request.POST['staff_uid']

            form=educationform(request.POST,request.FILES)
            
            try:
                if form.is_valid():            
                    education=Teacher_edu(teacherid_id=tid,
                                qualification=form.cleaned_data['qualification'],
                                subject=form.cleaned_data['subject'],
                                medium_of_instruction=form.cleaned_data['medium_of_instruction'],
                                month=form.cleaned_data['month'],
                                year=form.cleaned_data['year'],
                                university=form.cleaned_data['university'],
                                remarks=form.cleaned_data['remarks'],
                                )
                    education.save()
                    b=completed_table.objects.get(teacherid_id=tid)
                    if b.Teacher_edu=='0':
                        print b.id
                        b.id=b.id
                        b.Teacher_edu=5
                        b.save()                
                    msg = str(staff_name) + "(" + str(staff_uid)+") Education details added successfully."
                    messages.success(request, msg )
                    return redirect('teacher_education_create',pk=tid)
            except:
                messages.success(request, "Invalid Data. Please Try Again" )
                return redirect('teacher_education_create',pk=tid)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


class teacher_edu_update(View):
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
            instance=Teacher_edu.objects.get(id=pk1)     
            qualification=Qualification.objects.all()
            subject=Edu_subjects.objects.all()
            medium_value=Medium.objects.all()
            month_value=Months.objects.all()
            class_value=Distinction.objects.all()        
            form = educationform(instance=instance)
            teacherid_id = instance.teacherid_id
            qualification = instance.qualification
            subject=instance.subject
            medium_of_instruction = instance.medium_of_instruction  
            month =instance.month  
            year =instance.year
            university =instance.university
            remarks =instance.remarks       
            return render(request,'teachers/education/teacher_education_form_new.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


    #@never_cache
    def post(self,request,**kwargs):
        if request.user.is_authenticated():
            tid=self.kwargs.get('pk')
            pk1=self.kwargs.get('pk1')
            staff_id = Teacher_detail.objects.get(id = tid) 
            import teacher_main_views
            school_id=teacher_main_views.get_udisecode(staff_id.school_id)             
            dategovt=staff_id.dofsed
            staff_name=staff_id.name
            staff_uid=staff_id.count     
            instance=Teacher_edu.objects.get(id=pk1)
            form = educationform(request.POST,request.FILES)
            mgnt_edit = Teacher_edu.objects.get(id=pk1)
            if form.is_valid():
                mgnt_edit.qualification=form.cleaned_data['qualification']
                mgnt_edit.medium_of_instruction=form.cleaned_data['medium_of_instruction']
                mgnt_edit.month=form.cleaned_data['month']
                mgnt_edit.year=form.cleaned_data['year']            
                mgnt_edit.university=form.cleaned_data['university']
                mgnt_edit.remarks=form.cleaned_data['remarks']            
                mgnt_edit.save()
                messages.success(request,'Education Qualification Details Updated successfully')
                return redirect('teacher_education_create',pk=tid)
            else:
                print form.errors
                return render(request,'teachers/education/teacher_education_form_new.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


 
