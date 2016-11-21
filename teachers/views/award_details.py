from django.views.generic import View
from teachers.models import Teacher_detail,completed_table,Months,Teacher_posting_entry, Awards, Award_Level, Teacher_award
from teachers.forms import Teacher_award_form
from django.shortcuts import *
from schoolnew.models import *
# from baseapp.models import *
from django.contrib import messages
from django.db import *
from datetime import datetime
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache



class award_create(View):
    #@never_cache
    def get(self,request,**kwargs):
        if request.user.is_authenticated():
            # school_id = request.user.account.associated_with
            tid=self.kwargs.get('pk')        
            staff_id = Teacher_detail.objects.get(id = tid)          
            basic_det=Basicinfo.objects.get(school_id=staff_id.school_id)
                
            school_id =staff_id.school_id    
            dategovt=staff_id.dofsed
            staff_name=staff_id.name
            staff_uid=staff_id.count           
            desig=Teacher_posting_entry.objects.all()
            month_value=Months.objects.all()
         
            exams=Awards.objects.all()
            camps=Award_Level.objects.all()
            form=Teacher_award_form()       
            edu_list = Teacher_award.objects.filter(teacherid_id=tid)      
            if edu_list.count()==0:
                messages.success(request, 'No Data')       
            return render(request,'teachers/award/award_details.html',locals())
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
            form=Teacher_award_form(request.POST,request.FILES) 
            
            if form.is_valid(): 
                regular=Teacher_award(teacherid_id=tid,
                                award_name=form.cleaned_data['award_name'],
                                level=form.cleaned_data['level'],
                                year=form.cleaned_data['year'],
                                remarks=form.cleaned_data['remarks'],
                               
                               )
                regular.save()  
                b=completed_table.objects.get(teacherid_id=staff_id)        
                if b.Teacher_award=='0':
                    b.id=b.id
                    b.teacherid_id=b.teacherid_id
                    b.Teacher_award=20
                    b.save()     

                msg = str(staff_name) + "(" + str(staff_uid)+") Award details added successfully."
                messages.success(request, msg )  
                return redirect('award_create',pk=tid)
                
            else:
                print form.errors
                return render(request,'teachers/award/award_details.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        
       

class award_update(View):
    #@never_cache
    def get(self, request,**kwargs):
        if request.user.is_authenticated():
            # school_id = request.user.account.associated_with
            tid=self.kwargs.get('pk')
            pk1=self.kwargs.get('pk1')
            desig=Teacher_posting_entry.objects.all()
            month_value=Months.objects.all()
            exams=Awards.objects.all()
            camps=Award_Level.objects.all()
            staff_id = Teacher_detail.objects.get(id = tid)          
            basic_det=Basicinfo.objects.get(school_id=staff_id.school_id)
                
            school_id =staff_id.school_id    
            dategovt=staff_id.dofsed
            staff_name=staff_id.name
            staff_uid=staff_id.count   
            instance=Teacher_award.objects.get(id=pk1)
            form = Teacher_award_form(instance=instance)        
            teacherid_id = instance.teacherid_id
            award_name=instance.award_name
            level=instance.level
            year=instance.year
            remarks=instance.remarks           
            return render(request,'teachers/award/award_details.html',locals())
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
            posting_desg=Teacher_award.objects.filter(teacherid_id=tid)
            form = Teacher_award_form(request.POST,request.FILES)      
            mgnt_edit = Teacher_award.objects.get(id=pk1)
            if form.is_valid():
                mgnt_edit.award_name=form.cleaned_data['award_name']
                mgnt_edit.level=form.cleaned_data['level']
                mgnt_edit.year=form.cleaned_data['year']
                mgnt_edit.remarks=form.cleaned_data['remarks']
                mgnt_edit.save()
                messages.success(request,'Award Winner Details Updated successfully')
                return redirect('award_create',pk=tid)

            else:
                print form.errors
                return render(request,'teachers/award/award_details.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


