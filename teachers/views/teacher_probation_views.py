from django.views.generic import View
from teachers.models import Teacher_detail,completed_table,Teacher_posting_entry,Teacher_probation_entry
from teachers.forms import Teacher_probation_entryform
from django.shortcuts import *
from schoolnew.models import *
from django.contrib import messages
from django.db import *
from datetime import datetime
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache


class Teacher_probation_create(View):
    #@never_cache
    def get(self,request,**kwargs):
        if request.user.is_authenticated():
            import teacher_main_views
            if request.user.account.associated_with=='state' or request.user.account.associated_with=='DIPE' or request.user.account.associated_with=='CIPE' or request.user.account.associated_with=='Zone' or request.user.account.associated_with=='IAS' or request.user.account.associated_with=='IMS' :
                AEOENTRY=0
            else:
                AEOENTRY=teacher_main_views.aeoentrycheck(request.user.account.associated_with)
            tid=self.kwargs.get('pk')        
            staff_id = Teacher_detail.objects.get(id = tid) 
            basic_det=Basicinfo.objects.get(school_id=staff_id.school_id)
            sch_key = basic_det.id           
            school_id =staff_id.school_id
            dategovt=staff_id.dofsed
            staff_name=staff_id.name
            staff_uid=staff_id.count           
            posting_desg=Teacher_posting_entry.objects.filter(teacherid_id=tid).filter(Q(type_of_posting=1) | Q(type_of_posting=2))
            if posting_desg.count()==0:
                msg = " First make entries for Appointment details in Posting "
                messages.warning(request, msg)
                return redirect('teacher_personnel_entry_after',pk=tid)
            form=Teacher_probation_entryform()       
            edu_list = Teacher_probation_entry.objects.filter(teacherid_id=tid)      
            if edu_list.count()==0:
                messages.success(request, 'No Data')       
            return render(request,'teachers/probation/teacher_probation_detail_form.html',locals())
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
            form=Teacher_probation_entryform(request.POST,request.FILES) 
            edu_list = Teacher_probation_entry.objects.filter(teacherid_id=tid)       
            if form.is_valid(): 
                x=form.cleaned_data['designation']
                b=x.id
                if edu_list.count()==0:
                    regular=Teacher_probation_entry(teacherid_id=tid,
                                designation=form.cleaned_data['designation'],
                                order_no=form.cleaned_data['order_no'],
                                order_date=form.cleaned_data['order_date'],
                                date_of_clearance=form.cleaned_data['date_of_clearance'],
                                doprob_session = form.cleaned_data['doprob_session'],
                                )
                    regular.save()  
                    b=completed_table.objects.get(teacherid_id=staff_id)        
                    if b.Teacher_probation=='0':
                        b.id=b.id
                        b.teacherid_id=b.teacherid_id
                        b.Teacher_probation=3
                        b.save()     

                    msg = str(staff_name) + "(" + str(staff_uid)+") probation details added successfully."
                    messages.success(request, msg )  
                    return redirect('teacher_probation_create',pk=tid)
                else:
                    for i in edu_list:
                        if i.designation.id!=b:
                            regular=Teacher_probation_entry(teacherid_id=tid,
                                designation=form.cleaned_data['designation'],
                                order_no=form.cleaned_data['order_no'],
                                order_date=form.cleaned_data['order_date'],
                                date_of_clearance=form.cleaned_data['date_of_clearance'],
                                doprob_session = form.cleaned_data['doprob_session'],

                                )
                            regular.save()  
                            b=completed_table.objects.get(teacherid_id=staff_id)        
                            if b.Teacher_probation=='0':
                                b.id=b.id
                                b.teacherid_id=b.teacherid_id
                                b.Teacher_probation=3
                                b.save()     

                            msg = str(staff_name) + "(" + str(staff_uid)+") probation details added successfully."
                            messages.success(request, msg )  
                            return redirect('teacher_probation_create',pk=tid)
                        else:
                            msg = str(staff_name) + "(" + str(staff_uid)+") probation details for this designation is already added ."
                            messages.success(request, msg )   
                            return redirect('teacher_probation_create',pk=tid)
            else:
                print form.errors
                return render(request,'teachers/probation/teacher_probation_detail_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        
       

class teacher_probation_update(View):
    #@never_cache
    def get(self, request,**kwargs):
        if request.user.is_authenticated():
            tid=self.kwargs.get('pk')
            pk1=self.kwargs.get('pk1')
            staff_id = Teacher_detail.objects.get(id = tid)  
            basic_det=Basicinfo.objects.get(school_id=staff_id.school_id)
            sch_key = basic_det.id           
            school_id =staff_id.school_id        
            dategovt=staff_id.dofsed
            staff_name=staff_id.name
            staff_uid=staff_id.count   
            posting_desg=Teacher_posting_entry.objects.filter(teacherid_id=tid).filter(Q(type_of_posting=1) )             
            instance=Teacher_probation_entry.objects.get(id=pk1)
            form = Teacher_probation_entryform(instance=instance)        
            teacherid_id = instance.teacherid_id
            designation = instance.designation
            order_no=instance.order_no
            order_date = instance.order_date  
            date_of_clearance =instance.date_of_clearance     
            doprob_session = instance.doprob_session      
            return render(request,'teachers/probation/teacher_probation_detail_form.html',locals())
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
            posting_desg=Teacher_posting_entry.objects.filter(teacherid_id=tid).filter(Q(type_of_posting=1) | Q(type_of_posting=2))           
            form = Teacher_probation_entryform(request.POST,request.FILES)      
            mgnt_edit = Teacher_probation_entry.objects.get(id=pk1)
            if form.is_valid():
                mgnt_edit.designation=form.cleaned_data['designation']
                mgnt_edit.order_no=form.cleaned_data['order_no']
                mgnt_edit.order_date=form.cleaned_data['order_date']
                mgnt_edit.date_of_clearance=form.cleaned_data['date_of_clearance'] 
                mgnt_edit.doprob_session=form.cleaned_data['doprob_session']           
                mgnt_edit.save()
                messages.success(request,'probation Details Updated successfully')
                return redirect('teacher_probation_create',pk=tid)

            else:
                print form.errors
                return render(request,'teachers/probation/teacher_probation_detail_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

