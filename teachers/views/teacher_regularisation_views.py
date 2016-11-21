from django.views.generic import View
from teachers.models import Teacher_regularisation_entry,Teacher_detail,completed_table,Teacher_posting_entry
from teachers.forms import Teacher_regularisation_entryform
from django.shortcuts import *
from django.contrib import messages
from schoolnew.models import *
from django.db import *
from datetime import datetime
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache



class Teacher_regularisation_create(View):
    #@never_cache
    def get(self,request,**kwargs):
        if request.user.is_authenticated():
            import teacher_main_views
            if request.user.account.associated_with=='state' or request.user.account.associated_with=='DIPE' or request.user.account.associated_with=='CIPE' or request.user.account.associated_with=='Zone' or request.user.account.associated_with=='IAS' or request.user.account.associated_with=='IMS' :
                AEOENTRY=0
            else:
                AEOENTRY=teacher_main_views.aeoentrycheck(request.user.account.associated_with)
            form=Teacher_regularisation_entryform()

           
            tid=self.kwargs.get('pk')        
            staff_id = Teacher_detail.objects.get(id = tid)       
            basic_det=Basicinfo.objects.get(school_id=staff_id.school_id)
            sch_key = basic_det.id           
            school_id =staff_id.school_id# request.user.account.associated_with   
            dategovt=staff_id.dofsed
            staff_name=staff_id.name
            staff_uid=staff_id.count    
            
            posting_desg=Teacher_posting_entry.objects.filter(teacherid_id=tid).filter(Q(type_of_posting=1) | Q(type_of_posting=2))
            if posting_desg.count()==0:
                msg = " First make entries in Posting  "
                messages.warning(request, msg)
                return redirect('teacher_personnel_entry_after',pk=tid)
                     
            edu_list = Teacher_regularisation_entry.objects.filter(teacherid_id=tid)
            if edu_list.count()==0:
                messages.success(request, 'No Data')         
            return render(request,'teachers/regularisation/teacher_regularisation_detail_form.html',locals())
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
            form=Teacher_regularisation_entryform(request.POST,request.FILES)    
            edu_list = Teacher_regularisation_entry.objects.filter(teacherid_id=tid)       
            if form.is_valid(): 
                x=form.cleaned_data['designation']
                b=x.id
                if edu_list.count()==0:
                    regular=Teacher_regularisation_entry(teacherid_id=tid,
                                    designation=form.cleaned_data['designation'],
                                    order_no=form.cleaned_data['order_no'],
                                    order_date=form.cleaned_data['order_date'],
                                    date_of_regularisation=form.cleaned_data['date_of_regularisation'],
                                    doregu_session = form.cleaned_data['doregu_session'],
                                    )
                    regular.save()   

                    b=completed_table.objects.get(teacherid_id=tid)            
                    if b.Teacher_regularisation=='0':                
                        b.id=b.id
                        b.teacherid_id=b.teacherid_id
                        b.Teacher_regularisation=2
                        b.save()
                    msg = str(staff_name) + "(" + str(staff_uid)+") Regularisation details added successfully."
                    messages.success(request, msg )   
                    return redirect('teacher_regularisation_create',pk=tid)
                else:
                    for i in edu_list:
                        if i.designation.id!=b:
                            regular=Teacher_regularisation_entry(teacherid_id=tid,
                                        designation=form.cleaned_data['designation'],
                                        order_no=form.cleaned_data['order_no'],
                                        order_date=form.cleaned_data['order_date'],
                                        date_of_regularisation=form.cleaned_data['date_of_regularisation'],
                                        doregu_session = form.cleaned_data['doregu_session'],
                                        )
                            regular.save()   

                            b=completed_table.objects.get(teacherid_id=tid)            
                            if b.Teacher_regularisation=='0':                
                                b.id=b.id
                                b.teacherid_id=b.teacherid_id
                                b.Teacher_regularisation=2
                                b.save()
                            msg = str(staff_name) + "(" + str(staff_uid)+") Regularisation details added successfully."
                            messages.success(request, msg )   
                            return redirect('teacher_regularisation_create',pk=tid)
                        else:
                            msg = str(staff_name) + "(" + str(staff_uid)+") Regularisation details for this designation is already added ."
                            messages.success(request, msg )   
                            return redirect('teacher_regularisation_create',pk=tid)
            else:
                print form.errors
                messages.warning(request,"Please press F5 key to fill the form again")
                return render(request,'teachers/regularisation/teacher_regularisation_detail_form.html',locals()) 
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


class teacher_regularisation_update(View):
    #@never_cache
    def get(self, request,**kwargs):
        if request.user.is_authenticated():
            tid=self.kwargs.get('pk')  
            staff_id = Teacher_detail.objects.get(id = tid)     
            basic_det=Basicinfo.objects.get(school_id=staff_id.school_id)
            sch_key = basic_det.id
            school_id = staff_id.school_id
            desig_sub= Desig_subjects.objects.all()
            if ((basic_det.sch_cate_id==1)|(basic_det.sch_cate_id==11)):
                posting_desg= User_desig.objects.filter((Q(user_cate='SCHOOL&OFFICE')|Q(user_cate='SCHOOL')) & Q(user_level__isnull=True)|Q(user_level='PS'))
            elif ((basic_det.sch_cate_id==2)|(basic_det.sch_cate_id==4)|(basic_det.sch_cate_id==12)):
                posting_desg= User_desig.objects.filter((Q(user_cate='SCHOOL&OFFICE')|Q(user_cate='SCHOOL')) & Q(user_level__isnull=True)|Q(user_level='MS'))
            elif ((basic_det.sch_cate_id==6)|(basic_det.sch_cate_id==7)|(basic_det.sch_cate_id==8)) :
                posting_desg= User_desig.objects.filter((Q(user_cate='SCHOOL&OFFICE')|Q(user_cate='SCHOOL')) & Q(user_level__isnull=True)|Q(user_level='HS')|Q(user_level='HRHS'))
            elif ((basic_det.sch_cate_id==3)|(basic_det.sch_cate_id==5)|(basic_det.sch_cate_id==9)|(basic_det.sch_cate_id==10)):
                posting_desg= User_desig.objects.filter((Q(user_cate='SCHOOL&OFFICE')|Q(user_cate='SCHOOL')) & Q(user_level__isnull=True)|Q(user_level='HR')|Q(user_level='HRHS'))
            else:
                posting_desg= User_desig.objects.filter((Q(user_cate='SCHOOL&OFFICE')|Q(user_cate='OFFICE')) & Q(user_level__isnull=True))

            tid=self.kwargs.get('pk')
            pk1=self.kwargs.get('pk1')
            staff_id = Teacher_detail.objects.get(id = tid)          
            dategovt=staff_id.dofsed
            staffid_1=staff_id.stafs
            staff_name=staff_id.name
            staff_uid=staff_id.count   
             
            posting_desg=Teacher_posting_entry.objects.filter(teacherid_id=tid).filter(Q(type_of_posting=1) | Q(type_of_posting=2))      
            instance=Teacher_regularisation_entry.objects.get(id=pk1)         
            form = Teacher_regularisation_entryform(instance=instance)
            doregu_session = instance.doregu_session 
            teacherid_id = instance.teacherid_id
            designation = instance.designation
            order_no=instance.order_no
            order_date = instance.order_date  
            date_of_regularisation =instance.date_of_regularisation         
            return render(request,'teachers/regularisation/teacher_regularisation_detail_form.html',locals())
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
            staffid_1=staff_id.stafs
            staff_name=staff_id.name
            staff_uid=staff_id.count             
            instance=Teacher_regularisation_entry.objects.get(id=pk1)              
            form = Teacher_regularisation_entryform(request.POST,request.FILES)       
            mgnt_edit = Teacher_regularisation_entry.objects.get(id=pk1)
            if form.is_valid():
                mgnt_edit.designation=form.cleaned_data['designation']
                mgnt_edit.order_no=form.cleaned_data['order_no']
                mgnt_edit.order_date=form.cleaned_data['order_date']
                mgnt_edit.date_of_regularisation=form.cleaned_data['date_of_regularisation']      
                mgnt_edit.doregu_session=form.cleaned_data['doregu_session']      
                mgnt_edit.save()
                messages.success(request,'Regularisation Details Updated successfully')
                return redirect('teacher_regularisation_create',pk=tid)
            else:
                print form.errors
                return render(request,'teachers/regularisation/teacher_regularisation_detail_form.html',locals()) 
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
