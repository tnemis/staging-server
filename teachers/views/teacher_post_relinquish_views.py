import sys
import os.path
from django.views.generic import View
from teachers.models import Teacher_relinquish_entry,Teacher_detail,completed_table,Teacher_posting_entry
from teachers.forms import Teacher_relinquisform 
from django.shortcuts import *
from django.contrib import messages
from schoolnew.models import User_desig,Basicinfo
from django.db import *
from datetime import datetime
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache


class Teacher_relinquis_create(View):
    #@never_cache
    def get(self,request,**kwargs):
        if request.user.is_authenticated():
            import teacher_main_views
            if request.user.account.associated_with=='state' or request.user.account.associated_with=='DIPE' or request.user.account.associated_with=='CIPE' or request.user.account.associated_with=='Zone' or request.user.account.associated_with=='IAS' or request.user.account.associated_with=='IMS' :
                AEOENTRY=0
            else:
                AEOENTRY=teacher_main_views.aeoentrycheck(request.user.account.associated_with)
            form=Teacher_relinquisform()       
            tid=self.kwargs.get('pk')        
            staff_id = Teacher_detail.objects.get(id = tid)  
            basic_det=Basicinfo.objects.get(school_id=staff_id.school_id)
                
            school_id =staff_id.school_id

            dategovt=staff_id.dofsed
            staff_name=staff_id.name
            staff_uid=staff_id.count           
            posting_desg=Teacher_posting_entry.objects.filter(teacherid_id=tid).filter(Q(type_of_posting=1) | Q(type_of_posting=2))
            designation_list=User_desig.objects.all()
        
         
            if posting_desg.count()==0:
                msg = " First make entries in Posting"
                messages.warning(request, msg)
                return redirect('teacher_personnel_entry_after',pk=tid)
                     
            edu_list = Teacher_relinquish_entry.objects.filter(teacherid_id=tid)
            if edu_list.count()==0:
                messages.success(request, 'No Data') 
                
            return render(request,'teachers/post_relinquish/teacher_post_relinquish_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    #@never_cache
    def post(self,request,**kwargs):
        if request.user.is_authenticated():
            form=Teacher_relinquisform(request.POST,request.FILES)
            tid=self.kwargs.get('pk')        
            staff_id = Teacher_detail.objects.get(id = tid)
            staff_name=staff_id.name
            staff_uid=staff_id.count    
            if form.is_valid():            
                relinq=Teacher_relinquish_entry(teacherid_id=staff_id.id,                       
                            current_designation = form.cleaned_data['current_designation'], 
                            promoted_to = form.cleaned_data['promoted_to'],
                            
                            date_of_relinqui=form.cleaned_data['date_of_relinqui'],
                            order_no=form.cleaned_data['order_no'],
                            
                            crucial_date_for_promotion=form.cleaned_data['crucial_date_for_promotion'],
                            promo_next_eligible_date=form.cleaned_data['promo_next_eligible_date'],
                            )
                relinq.save()  
                b=completed_table.objects.get(teacherid_id=staff_id)            
                if b.Teacher_post_relinquish=='0':                
                    b.id=b.id
                    b.teacherid_id=b.teacherid_id
                    b.Teacher_post_relinquish=4
                    b.save()
                msg = str(staff_name) + "(" + str(staff_uid)+") Relinquishment details added successfully."
                messages.success(request, msg )   
                return redirect('teacher_relinquis_create',pk=tid)            
            else:
                print form.errors            
                return render(request,'teachers/post_relinquish/teacher_post_relinquish_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class teacher_relinqui_update(View):
    #@never_cache
    def get(self, request,**kwargs):
        if request.user.is_authenticated():
            tid=self.kwargs.get('pk')
            pk1=self.kwargs.get('pk1')
            staff_id = Teacher_detail.objects.get(id = tid)          
            dategovt=staff_id.dofsed
            staff_name=staff_id.name
            staff_uid=staff_id.count     
            basic_det=Basicinfo.objects.get(school_id=staff_id.school_id)
            school_id =staff_id.school_id
            posting_desg=Teacher_posting_entry.objects.filter(teacherid_id=tid).filter(Q(type_of_posting=1) | Q(type_of_posting=2))
            designation_list=User_desig.objects.all()    
            instance=Teacher_relinquish_entry.objects.get(id=pk1)
            form = Teacher_relinquisform(instance=instance)
            teacherid_id = instance.teacherid_id
            current_designation = instance.current_designation
            promoted_to=instance.promoted_to
            date_of_relinqui =instance.date_of_relinqui   
            order_no=instance.order_no
            crucial_date_for_promotion = instance.crucial_date_for_promotion 
            promo_next_eligible_date = instance.promo_next_eligible_date   
            return render(request,'teachers/post_relinquish/teacher_post_relinquish_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    
    #@never_cache
    def post(self,request,**kwargs):
        if request.user.is_authenticated():
            tid=self.kwargs.get('pk')
            pk1=self.kwargs.get('pk1')
            staff_id = Teacher_detail.objects.get(id = tid)
            staff_name=staff_id.name
            staff_uid=staff_id.count          
            form=Teacher_relinquisform(request.POST,request.FILES) 
            mgnt_edit = Teacher_relinquish_entry.objects.get(id=pk1)
            if form.is_valid():
                mgnt_edit.current_designation=form.cleaned_data['current_designation']
                mgnt_edit.promoted_to=form.cleaned_data['promoted_to']
                mgnt_edit.date_of_relinqui=form.cleaned_data['date_of_relinqui']  
                mgnt_edit.order_no=form.cleaned_data['order_no']
                mgnt_edit.crucial_date_for_promotion=form.cleaned_data['crucial_date_for_promotion']   
                mgnt_edit.promo_next_eligible_date=form.cleaned_data['promo_next_eligible_date']                       
                mgnt_edit.save()
                messages.success(request,'Teacher Relinquish Details Updated successfully')
                return redirect('teacher_relinquis_create',pk=tid)
            else:
                print form.errors  
                return render(request,'teachers/post_relinquish/teacher_post_relinquish_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
