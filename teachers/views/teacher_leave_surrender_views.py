from django.views.generic import *
from teachers.models import *
from teachers.forms import *
from django.shortcuts import *
from baseapp.models import *
from django.contrib import messages
from django.db import *
from datetime import datetime
from django.views.generic import *
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache


class Teacher_leave_surrender_create(View):
    #@never_cache
    def get(self,request,**kwargs):
        if request.user.is_authenticated():
            import teacher_main_views
            if request.user.account.associated_with=='state' or request.user.account.associated_with=='DIPE' or request.user.account.associated_with=='CIPE' or request.user.account.associated_with=='Zone' or request.user.account.associated_with=='IAS' or request.user.account.associated_with=='IMS' :
                AEOENTRY=0
            else:

                AEOENTRY=teacher_main_views.aeoentrycheck(request.user.account.associated_with)
            tid=self.kwargs.get('pk')
            unique_id=Teacher_detail.objects.get(id=tid)
            basic_det=Basicinfo.objects.get(school_id=unique_id.school_id)
      
            school_id =unique_id.school_id
            form=Teacher_leave_surrenderform()
            try:

                record=Teacher_leave_master.objects.get(teacherid_id=tid)
                timez=record.timestamp
                validated=timez.date()
           
                el_bal=int(record.el_bal)

            except:
                msg = " First Make Leave Master "
                messages.warning(request, msg)
                return redirect('teacher_personnel_entry_after',pk=tid)

            edu_list = Teacher_leave_surrender.objects.filter(teacherid_id=tid) 
            if edu_list.count()==0: 
                messages.success(request, 'No Data') 

            return render(request,'teachers/leave_surrender/teacher_leave_surrender_form3.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    
    #@never_cache
    def post(self,request,**kwargs):
        if request.user.is_authenticated():
            form=Teacher_leave_surrenderform(request.POST,request.FILES)
            tid=self.kwargs.get('pk')
         
            unique_id=request.POST['unique_id']
            unique_name=request.POST['unique_name']
            record=Teacher_leave_master.objects.get(teacherid_id=unique_id)

            if form.is_valid():      
                if (form.cleaned_data['no_of_days']>record.el_bal): 
                    msg = " Surrender Days Exceeds "
                    messages.warning(request, msg )   
                    return redirect('teacher_leave_surrender_create',pk=unique_id)
                else:
                    if (form.cleaned_data['no_of_days']>30): 
                        msg = " Surrender Should not Exceed 30 Days "
                        messages.warning(request, msg )   
                        return redirect('teacher_leave_surrender_create',pk=unique_id)
                    else:
                        surrender=Teacher_leave_surrender(teacherid_id=tid,
                                    surrender_date=form.cleaned_data['surrender_date'],
                                    current_balance_days=form.cleaned_data['current_balance_days'],
                                    no_of_days=form.cleaned_data['no_of_days'],
                                    order_no=form.cleaned_data['order_no'],
                                    order_date=form.cleaned_data['order_date'],                   
                                    )
                        surrender.save() 
                        
                        
                        record.el_bal=record.el_bal-surrender.no_of_days
                        record.el_ob=record.el_bal
                        
                        record.save()     
                        b=completed_table.objects.get(teacherid_id=unique_id)            
                        if b.Teacher_leavsurr=='0':                
                            b.id=b.id
                            b.teacherid_id=b.teacherid_id
                            b.Teacher_leavsurr=11
                            b.save()
                        msg = str(unique_name) + " Regularisation details added successfully."
                        messages.success(request, msg )   
                        return redirect('teacher_leave_surrender_create',pk=unique_id)
            else:
                print form.errors
                return render(request,'teachers/leave_surrender/teacher_leave_surrender_form3.html',locals()) 
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
  
class Teacher_leave_surrender_delete(View): 
    #@never_cache
    def get(self, request,**kwargs):
        if request.user.is_authenticated(): 
            tid=self.kwargs.get('pk') 
            staff_name=request.session['staffname'] 
            data=Teacher_leave_surrender.objects.get(id=tid)

            staff_id=request.session['staffid']
            count=Teacher_leave_surrender.objects.filter(teacherid_id=staff_id).count()
            if count == 1 :
                data.delete()
                b=completed_table.objects.get(teacherid_id=staff_id)
                b.id=b.id
                b.teacherid_id=b.teacherid_id
                b.Teacher_leavsurr=0
                b.save()
            else :
                data.delete()
            
            msg=str(data.surrender_date) + " Removed successfully" 
            messages.success(request, msg )        
            return HttpResponseRedirect('/teachers/teacher_leave_surrender_create/') 
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


class teacher_leave_surrender_update(View):
    #@never_cache
    def get(self, request,**kwargs):
        if request.user.is_authenticated():
            tid=self.kwargs.get('pk')
            tid1=self.kwargs.get('pk1')
            unique_id=Teacher_detail.objects.get(id=tid)  
            basic_det=Basicinfo.objects.get(school_id=unique_id.school_id)
                
            school_id =unique_id.school_id    
            instance=Teacher_leave_surrender.objects.get(id=tid1)
            form = Teacher_leave_surrenderform(instance=instance)
            teacherid_id = instance.teacherid_id
            surrender_date = instance.surrender_date
            current_balance_days=instance.current_balance_days
            no_of_days = instance.no_of_days 
            order_no = instance.order_no
            no_of_days = instance.no_of_days 
            order_date =instance.order_date         
            return render(request,'teachers/leave_surrender/teacher_leave_surrender_form3.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    #@never_cache
    def post(self,request,**kwargs):
        if request.user.is_authenticated():
            tid=self.kwargs.get('pk')  
            tid1=self.kwargs.get('pk1')     
            instance=Teacher_leave.objects.get(id=tid1)        
            unique_id=request.POST['unique_id']
            unique_name=request.POST['unique_name']
            record=Teacher_leave_master.objects.get(teacherid_id=unique_id)
            
                 
            instance=Teacher_leave_surrender.objects.get(id=tid1)
            form = Teacher_leave_surrenderform(request.POST,request.FILES)
           
            mgnt_edit = Teacher_leave_surrender.objects.get(id=tid1)

            if form.is_valid():
                if (form.cleaned_data['no_of_days']>record.el_bal): 
                    msg = " Surrender Days Exceeds "
                    messages.warning(request, msg )   
                    return redirect('teacher_leave_surrender_create',pk=unique_id)
                else:
                    if (form.cleaned_data['no_of_days']>30): 
                        msg = " Surrender Should not Exceed 30 Days "
                        messages.warning(request, msg )   
                        return redirect('teacher_leave_surrender_create',pk=unique_id)
                    else:
                        print mgnt_edit.no_of_days 
                        print form.cleaned_data['no_of_days']
                        
                        before_entry=mgnt_edit.no_of_days - form.cleaned_data['no_of_days']
                        print before_entry
                        mgnt_edit.surrender_date=form.cleaned_data['surrender_date']
                        mgnt_edit.current_balance_days=form.cleaned_data['current_balance_days']
                        mgnt_edit.no_of_days=form.cleaned_data['no_of_days']
                        mgnt_edit.order_no=form.cleaned_data['order_no']
                        mgnt_edit.no_of_days=form.cleaned_data['no_of_days']
                        mgnt_edit.order_date=form.cleaned_data['order_date']            
                        mgnt_edit.save()
                        messages.success(request,'Leave Surrender Details Updated successfully')
                        print record.el_bal

                        record.el_bal=record.el_bal+before_entry
                        record.el_ob=record.el_bal
                        record.save()  
                        return redirect('teacher_leave_surrender_create',pk=unique_id)
            else:
                print form.errors
                return render(request,'teachers/leave_surrender/teacher_leave_surrender_form3.html',locals()) 
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

