from django.views.generic import View
from teachers.models import Teacher_training,Teacher_detail,completed_table
from django.views.generic import *
from schoolnew.models import Basicinfo
from teachers.forms import Teacher_trainingform
from django.shortcuts import *
from django.contrib import messages
from django.db import *
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache



class Teacher_training_create(View):
    #@never_cache
    def get(self,request,**kwargs):
        if request.user.is_authenticated():
            form=Teacher_trainingform()
            import teacher_main_views
            if request.user.account.associated_with=='state' or request.user.account.associated_with=='DIPE' or request.user.account.associated_with=='CIPE' or request.user.account.associated_with=='Zone' or request.user.account.associated_with=='IAS' or request.user.account.associated_with=='IMS' :
                AEOENTRY=0
            else:
                AEOENTRY=teacher_main_views.aeoentrycheck(request.user.account.associated_with)
            tid=self.kwargs.get('pk')    
            print tid    
            staff_id = Teacher_detail.objects.get(id = tid)          
            basic_det=Basicinfo.objects.get(school_id=staff_id.school_id)
                
            school_id =staff_id.school_id
            dategovt=staff_id.dofsed
            staff_name=staff_id.name
            staff_uid=staff_id.count      
            edu_list = Teacher_training.objects.filter(teacherid_id=tid)
            if edu_list.count()==0:
                messages.success(request, 'No Data')
            teachers_posting_list = Teacher_training.objects.filter(teacherid_id=tid) 
            return render(request,'teachers/training/teacher_training_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    #@never_cache
    def post(self,request,**kwargs):
        if request.user.is_authenticated():
            school_id = request.user.account.associated_with
            tid=self.kwargs.get('pk')        
            staff_id = Teacher_detail.objects.get(id = tid)          
            staff_name=staff_id.name
            staff_uid=staff_id.count       
            form=Teacher_trainingform(request.POST,request.FILES)
            if form.is_valid():            
                education=Teacher_training(teacherid_id=tid,
                            course=form.cleaned_data['course'],
                            institution=form.cleaned_data['institution'],
                            city=form.cleaned_data['city'],
                            country=form.cleaned_data['country'],
                            duration_from=form.cleaned_data['duration_from'],
                            duration_to=form.cleaned_data['duration_to'],
                            )
                education.save()
                b=completed_table.objects.get(teacherid_id=tid)
            
                if b.Teacher_trainin=='0':
                    b.id=b.id
                    b.teacherid_id=b.teacherid_id
                    b.Teacher_trainin=6
                    b.save()
                    
                msg = str(staff_name) + "(" + str(staff_uid)+") Training details added successfully." 
                messages.success(request, msg )       
                teach=education.teacherid_id 
                return redirect('teacher_training_create',pk=tid)

            else:
                print form.errors
                return render(request,'teachers/training/teacher_training_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))        
  
class teacher_training_update(View):
    #@never_cache
    def get(self, request,**kwargs):
        if request.user.is_authenticated():
            tid=self.kwargs.get('pk')
            pk1=self.kwargs.get('pk1')
            staff_id = Teacher_detail.objects.get(id = tid) 
            basic_det=Basicinfo.objects.get(school_id=staff_id.school_id)
            school_id =staff_id.school_id
            dategovt=staff_id.dofsed
            staff_name=staff_id.name
            staff_uid=staff_id.count           
            instance=Teacher_training.objects.get(id=pk1)        
            form = Teacher_trainingform(instance=instance)
            teacherid_id = instance.teacherid_id        
            course=instance.course
            institution = instance.institution  
            city =instance.city
            country =instance.country
            duration_from =instance.duration_from
            duration_to =instance.duration_to
            return render(request,'teachers/training/teacher_training_form.html',locals())
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
            form = Teacher_trainingform(request.POST,request.FILES)       
            mgnt_edit = Teacher_training.objects.get(id=pk1)
            if form.is_valid():           
                mgnt_edit.course=form.cleaned_data['course']
                mgnt_edit.institution=form.cleaned_data['institution']
                mgnt_edit.city=form.cleaned_data['city'] 
                mgnt_edit.country=form.cleaned_data['country']
                mgnt_edit.duration_from=form.cleaned_data['duration_from']
                mgnt_edit.duration_to=form.cleaned_data['duration_to']           
                mgnt_edit.save()
                messages.success(request,'Training Details Updated successfully')
                return redirect('teacher_training_create',pk=tid)           
            else:
                print form.errors
                return render(request,'teachers/training/teacher_training_form.html',{'edu_list':edu_list, 'pk':staff_id, 'staff_name':staff_name,'staff_uid':staff_uid,'dategovt':dategovt})
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

