from django.views.generic import View
from teachers.models import Teacher_detail,completed_table,Teacher_ltc,ltc_leave_type,ltc_destination,ltc_base
from teachers.forms import Teacher_ltcform
from schoolnew.models import Basicinfo
from django.shortcuts import *
from django.contrib import messages
from django.db import *
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache


class Teacher_ltc_create(View):
    #@never_cache
    def get(self,request,**kwargs):
        if request.user.is_authenticated():
            import teacher_main_views
            if request.user.account.associated_with=='state' or request.user.account.associated_with=='DIPE' or request.user.account.associated_with=='CIPE' or request.user.account.associated_with=='Zone' or request.user.account.associated_with=='IAS' or request.user.account.associated_with=='IMS' :
                AEOENTRY=0
            else:
                AEOENTRY=teacher_main_views.aeoentrycheck(request.user.account.associated_with)
            school_id = request.user.account.associated_with
            tid=self.kwargs.get('pk')        
            staff_id = Teacher_detail.objects.get(id = tid)   
            basic_det=Basicinfo.objects.get(school_id=staff_id.school_id)
               
            school_id =staff_id.school_id            
                
            dategovt=staff_id.dofsed 
            staff_name=staff_id.name 
            staff_uid=staff_id.count    
            form=Teacher_ltcform() 
            blockk=ltc_base.objects.all()
            eeee=ltc_destination.objects.all()
            leave=ltc_leave_type.objects.all()
            edu_list = Teacher_ltc.objects.filter(teacherid_id=tid)              
            if edu_list.count()==0:
                messages.success(request, 'No Data')
            return render(request,'teachers/ltc/teacher_ltc_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    #@never_cache
    def post(self,request,**kwargs):
        if request.user.is_authenticated():
            form = Teacher_ltcform(request.POST,request.FILES)
            school_id = request.user.account.associated_with
            tid=self.kwargs.get('pk')        
            staff_id = Teacher_detail.objects.get(id = tid)          
            dategovt=staff_id.dofsed 
            staff_name=staff_id.name 
            staff_uid=staff_id.count  

            if form.is_valid():            
                ltc=Teacher_ltc(teacherid_id=tid,
                            from_year=form.cleaned_data['from_year'],
                            block_yeear=form.cleaned_data['block_yeear'],
                            leave_from=form.cleaned_data['leave_from'],
                            leave_to=form.cleaned_data['leave_to'],
                            destination_type=form.cleaned_data['destination_type'],
                            leave_type=form.cleaned_data['leave_type'],
                            sanction_amt=form.cleaned_data['sanction_amt'],
                            no_of_days_sanctioned=form.cleaned_data['no_of_days_sanctioned'],
                            sanction_order=form.cleaned_data['sanction_order'],
                            sanction_date=form.cleaned_data['sanction_date'],                        
                            )
                ltc.save()
                b=completed_table.objects.get(teacherid_id=tid)
            
                if b.Teacher_ltcc=='0':
                    b.id=b.id
                    b.teacherid_id=b.teacherid_id
                    b.Teacher_ltcc=17
                    b.save()

                msg = str(staff_name) + "(" + str(staff_uid)+") LTC details added successfully."
                messages.success(request, msg )       
                return redirect('teacher_ltc_create',pk=tid) 
            else:
                print form.errors
                msg = str(staff_name) + "(" + str(staff_uid)+") LTC details Check."
                messages.warning(request, msg );
                messages.success(request, 'Press Refresh  button')
                return render(request,'teachers/ltc/teacher_ltc_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


class teacher_ltc_update(View):
    #@never_cache
    def get(self, request,**kwargs):
        if request.user.is_authenticated():
            school_id = request.user.account.associated_with 
            tid=self.kwargs.get('pk') 
            pk1=self.kwargs.get('pk1') 
            staff_id = Teacher_detail.objects.get(id = tid)
            basic_det=Basicinfo.objects.get(school_id=staff_id.school_id)
                
            school_id =staff_id.school_id            
                   
            dategovt=staff_id.dofsed 
            staff_name=staff_id.name 
            staff_uid=staff_id.count           
            instance=Teacher_ltc.objects.get(id=pk1)
            eeee=ltc_destination.objects.all()
            blockk=ltc_base.objects.all()
            leave=ltc_leave_type.objects.all()
            form = Teacher_ltcform(instance=instance)
            teacherid_id = instance.teacherid_id
            from_year = instance.from_year
            block_yeear = instance.block_yeear
            leave_from=instance.leave_from
            leave_to = instance.leave_to  
            destination_type =instance.destination_type   
            leave_type = instance.leave_type
            sanction_amt=instance.sanction_amt
            sanction_order = instance.sanction_order  
            sanction_date =instance.sanction_date       
            return render(request,'teachers/ltc/teacher_ltc_form.html',locals())
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
            form = Teacher_ltcform(request.POST,request.FILES)
            
            mgnt_edit = Teacher_ltc.objects.get(id=pk1)
            if form.is_valid():
                mgnt_edit.from_year=form.cleaned_data['from_year']
                mgnt_edit.block_yeear=form.cleaned_data['block_yeear']
                mgnt_edit.leave_from=form.cleaned_data['leave_from']
                mgnt_edit.leave_to=form.cleaned_data['leave_to']
                mgnt_edit.destination_type=form.cleaned_data['destination_type']   
                mgnt_edit.leave_type=form.cleaned_data['leave_type']
                mgnt_edit.sanction_amt=form.cleaned_data['sanction_amt']
                mgnt_edit.sanction_order=form.cleaned_data['sanction_order']
                mgnt_edit.sanction_date=form.cleaned_data['sanction_date']               
                mgnt_edit.save()
                messages.success(request,'LTC Details Updated successfully')
                return redirect('teacher_ltc_create',pk=tid) 
            else:
                print form.errors
                return render(request,'teachers/ltc/teacher_ltc_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    







