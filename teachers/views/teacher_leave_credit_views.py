from django.views.generic import *
from teachers.models import *
from teachers.forms import *
from django.shortcuts import *
from baseapp.models import *
from django.contrib import messages
from django.db import *
from datetime import datetime
import datetime

from django.views.generic import *
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache


class leave_master_view(View):
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

            fam=Teacher_family_detail.objects.filter(teacherid_id=tid)    

            data=Teacher_detail.objects.get(id=tid)
            basic_det=Basicinfo.objects.get(school_id=data.school_id)
            school_id =data.school_id   
            doj=data.dofsed
            desig1=data.designation
            desig_id=User_desig.objects.get(user_desig=desig1)
            desig=desig_id.ser_type

            doregular=data.doregu
                    
            import datetime
            today = datetime.date.today()
            years_of_exp=(today-doj).days/365.25
            if desig==0:
                if years_of_exp<2:
                    eligible_days=0
                elif years_of_exp>=2 and years_of_exp<5:
                    eligible_days=90
                elif years_of_exp>=5 and years_of_exp<10:
                    eligible_days=180
                elif years_of_exp>=10 and years_of_exp<15:
                    eligible_days=270
                elif years_of_exp>=15 and years_of_exp<20:
                    eligible_days=360
                elif years_of_exp>=20:
                    eligible_days=540
            else:
                years_of_exp=(today-doregular).days/365.25
                if years_of_exp<1:
                    eligible_days=0
                elif years_of_exp>=1 and years_of_exp<15:
                    eligible_days=(int(years_of_exp)*10)
                elif years_of_exp>=15 and years_of_exp<20:
                    eligible_days=360
                
                elif years_of_exp>=20:
                    eligible_days=540
            

            uel_mc_ob1=eligible_days
            
            if desig==0:
                if years_of_exp>2:
                    eligible_days=0
                else:
                    eligible_days=0
            else:
                years_of_exp=(today-doregular).days/365.25
                if years_of_exp<15:
                    eligible_days=180
                elif years_of_exp>=15:
                    eligible_days=365
                 
            llp_womc_ob1=eligible_days

            if desig==0:
                years_of_exp=(today-doj).days/365.25
                if years_of_exp<10:
                    eligible_days=90
                else:
                    eligible_days=180
               
            else:
                years_of_exp=(today-doregular).days/365.25
                if years_of_exp<15:
                    eligible_days=0
                elif years_of_exp>=15:
                    eligible_days=180
                

            uel_pa_ob1=eligible_days
           
            gender=data.gender
            if gender=='Male':
                maternity_leave_ob1=0
            else:
                fam_details=Teacher_family_detail.objects.filter(teacherid_id=unique_id)
                child_count=0

                import datetime
                            
                for i in fam_details:
                    if i.relation.id==2 or i.relation.id==3:
                        child_count=child_count+1
                if child_count>=2:
                    maternity_leave_ob1=child_count+1
                elif child_count<2:
                    maternity_leave_ob1=child_count+1
                maternity_leave_ob1=maternity_leave_ob1-1
            
            if fam.count()>0:
                try:
                    records=Teacher_leave_master.objects.filter(teacherid_id=tid)    
                    if records.count()>0:
                        return HttpResponseRedirect('/teachers/master_db_update/%d/' %int(tid))

                    else:        
                        return render(request,'teachers/leave_credit/teacher_leave_credit_form.html',locals())
                    
                except:
                    msg = " Make Leave Master "
                    messages.warning(request, msg)
                    return redirect('teacher_personnel_entry_after',pk=tid)

            else :
                msg = " Make Teacher's Family Details First "
                messages.warning(request, msg)
                return redirect('teacher_personnel_entry_after',pk=tid)

            return HttpResponseRedirect('/teachers/teacher_personnel_entry_after/%d/' %int(tid))
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    #@never_cache
    def post(self,request,**kwargs): 
        if request.user.is_authenticated():        
            unique_id=request.POST['unique_id']
            unique_name=request.POST['unique_name']
            form=Teacher_leave_masterform(request.POST)
            
            if form.is_valid():
                leave=Teacher_leave_master(
                    teacherid_id=unique_id,
                    
                    el_ob=form.cleaned_data['el_ob'],
                    el_taken=form.cleaned_data['el_taken'],
                    el_bal=form.cleaned_data['el_bal'],
                    uel_mc_ob=form.cleaned_data['uel_mc_ob'],
                    uel_mc_taken=form.cleaned_data['uel_mc_taken'],
                    uel_mc_bal=form.cleaned_data['uel_mc_bal'],
                    llp_mc_ob=form.cleaned_data['llp_mc_ob'],
                    llp_mc_taken=form.cleaned_data['llp_mc_taken'],
                    llp_mc_bal=form.cleaned_data['llp_mc_bal'],
                    uel_pa_ob=form.cleaned_data['uel_pa_ob'],
                    uel_pa_taken=form.cleaned_data['uel_pa_taken'],
                    uel_pa_bal=form.cleaned_data['uel_pa_bal'],
                    llp_womc_ob=form.cleaned_data['llp_womc_ob'],
                    llp_womc_taken=form.cleaned_data['llp_womc_taken'],
                    llp_womc_bal=form.cleaned_data['llp_womc_bal'],
                    spl_leave_ob=form.cleaned_data['spl_leave_ob'],
                    spl_leave_taken=form.cleaned_data['spl_leave_taken'],
                    spl_leave_bal=form.cleaned_data['spl_leave_bal'],
                    maternity_leave_ob=form.cleaned_data['maternity_leave_ob'],
                    maternity_leave_taken=form.cleaned_data['maternity_leave_taken'],
                    maternity_leave_bal=form.cleaned_data['maternity_leave_bal'],
                    
                    )
                leave.save()    
                msg = str(unique_name) + " Leave Master Created successfully."
                messages.success(request,msg)    
            else:
                messages.warning(request,form.errors)    
                print form.errors
           
            return redirect('teacher_personnel_entry_after',pk=unique_id)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class master_db_el_update(View):
    #@never_cache
    def get(self,request,**kwargs):
        if request.user.is_authenticated():
            records=Teacher_leave_master.objects.all()
            for el_ob_cl in records:
                el_ob_cl.el_ob = el_ob_cl.el_bal
                el_ob_cl.el_bal=0
                el_ob_cl.save()
                messages.success(request,'Opening Balance and Closing Balance InterChanged')    
                return HttpResponseRedirect('/')
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

      
class master_db_update(View):
    #@never_cache
    def get(self,request,**kwargs):
        if request.user.is_authenticated():
            tid=self.kwargs.get('pk')
            records=Teacher_leave_master.objects.filter(teacherid_id=tid)
            process=2
            label="Go Back"

            instance=Teacher_leave_master.objects.get(teacherid_id=tid)
            
            form = Teacher_leave_masterform(instance=instance)

            unique_id=Teacher_detail.objects.get(id=tid)
            basic_det=Basicinfo.objects.get(school_id=unique_id.school_id)
                
            school_id =unique_id.school_id   
     
            teacherid_id = instance.teacherid_id
            
            el_ob = instance.el_ob
            el_taken = instance.el_taken
            el_bal=instance.el_bal
            uel_mc_ob = instance.uel_mc_ob  
            uel_mc_taken =instance.uel_mc_taken 
            uel_mc_bal = instance.uel_mc_bal
            llp_mc_ob = instance.llp_mc_ob
            llp_mc_taken=instance.llp_mc_taken
            llp_mc_bal = instance.llp_mc_bal  
            uel_pa_ob =instance.uel_pa_ob 
            uel_pa_taken = instance.uel_pa_taken
            uel_pa_bal = instance.uel_pa_bal
            llp_womc_ob=instance.llp_womc_ob
            llp_womc_taken = instance.llp_womc_taken  
            llp_womc_bal =instance.llp_womc_bal 
            spl_leave_ob = instance.spl_leave_ob
            spl_leave_taken = instance.spl_leave_taken
            spl_leave_bal=instance.spl_leave_bal
            maternity_leave_ob = instance.maternity_leave_ob  
            maternity_leave_taken =instance.maternity_leave_taken 
            maternity_leave_bal =instance.maternity_leave_bal 

            return render(request,'teachers/leave_credit/teacher_leave_credit_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

 
class Teacher_leave_credit_create(View):
    #@never_cache
    def get(self,request,**kwargs):
        if request.user.is_authenticated():
            import teacher_main_views
            AEOENTRY=teacher_main_views.aeoentrycheck(request.user.account.associated_with)   
            form=Teacher_leave_creditform()
            tid=self.kwargs.get('pk')
            
            unique_id=Teacher_detail.objects.get(id=tid)
            basic_det=Basicinfo.objects.get(school_id=unique_id.school_id)
                
            school_id =unique_id.school_id   
     
            try:
                record=Teacher_leave_master.objects.get(teacherid_id=tid)
                el_ob=int(record.el_ob)
                el_taken=record.el_taken
                el_bal=record.el_bal
            except:
                msg = " First Make Leave Master "
                messages.warning(request, msg)
                return redirect('teacher_personnel_entry_after',pk=tid)

            edu_list = Teacher_leave_credit.objects.filter(teacherid_id=tid)
            if edu_list.count()==0:
                messages.success(request,'No Data')    
            
            return render(request,'teachers/leave_credit/teacher_leave_credit_form3.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    #@never_cache
    def post(self,request,**kwargs):
        if request.user.is_authenticated():
            form=Teacher_leave_creditform(request.POST,request.FILES)
            unique_id=request.POST['unique_id']
            
            unique_name=request.POST['unique_name']
            if form.is_valid():            
                credit=Teacher_leave_credit(teacherid_id=unique_id,
                            leave_type=form.cleaned_data['leave_type'],
                            effective_date=form.cleaned_data['effective_date'],
                            no_of_days_credit=form.cleaned_data['no_of_days_credit'],
                            previous_balance=form.cleaned_data['previous_balance'],
                            current_balance=form.cleaned_data['current_balance'],
                            )
                credit.save()
                record=Teacher_leave_master.objects.get(teacherid_id=unique_id)
                record.el_ob=credit.current_balance
                record.el_bal=record.el_bal+credit.no_of_days_credit
               
                record.save()
                      

                b=completed_table.objects.get(teacherid_id=unique_id)            
                if b.Teacher_leavcredit=='0':                
                    b.id=b.id
                    b.teacherid_id=b.teacherid_id
                    b.Teacher_leavcredit=10
                    b.save()
                msg = str(unique_name) + " Leave Credit details added successfully."
                messages.success(request, msg )   
                return redirect('teacher_leave_credit_create',pk=unique_id)
               
            else:
                print form.errors
                return render(request,'teachers/leave_credit/teacher_leave_credit_form3.html',locals()) 
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


class Teacher_leave_credit_delete(View): 
    #@never_cache
    def get(self, request,**kwargs): 
        if request.user.is_authenticated():
            tid=self.kwargs.get('pk') 
            staff_name=request.session['staffname'] 
            data=Teacher_leave_credit.objects.get(id=tid)

            staff_id=request.session['staffid']
            count=Teacher_leave_credit.objects.filter(teacherid_id=staff_id).count()
            if count == 1 :
                data.delete()
                b=completed_table.objects.get(teacherid_id=staff_id)
                b.id=b.id
                b.teacherid_id=b.teacherid_id
                b.Teacher_leavcredit=0
                b.save()
            else :
                data.delete() 
            
            msg= data.leave_type + " A Record from the Leave credit Removed successfully" 
            messages.success(request, msg )        
            return HttpResponseRedirect('/teachers/teacher_leave_credit_create/') 
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))



class teacher_leave_credit_update(View):
    #@never_cache
    def get(self, request,**kwargs):
        if request.user.is_authenticated():
            tid=self.kwargs.get('pk')
            tid1=self.kwargs.get('pk1')
            unique_id=Teacher_detail.objects.get(id=tid)  
            basic_det=Basicinfo.objects.get(school_id=unique_id.school_id)
                
            school_id =unique_id.school_id   
     
            
            instance=Teacher_leave_credit.objects.get(id=tid1)
            
            form=Teacher_leave_creditform(instance=instance)
            edu_list = Teacher_leave_credit.objects.filter(teacherid_id=tid1)
            teacherid_id = instance.teacherid_id
            leave_type = instance.leave_type
            effective_date = instance.effective_date
            no_of_days_credit = instance.no_of_days_credit
            previous_balance = instance.previous_balance
            current_balance = instance.current_balance
            return render(request,'teachers/leave_credit/teacher_leave_credit_form3.html',locals()) 
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        
    #@never_cache
    def post(self,request,**kwargs):
        if request.user.is_authenticated():
            tid=self.kwargs.get('pk')  
            tid1=self.kwargs.get('pk1')     
            unique_id=request.POST['unique_id']
            unique_name=request.POST['unique_name']
            instance=Teacher_leave_credit.objects.get(id=tid1)
            record=Teacher_leave_master.objects.get(teacherid_id=unique_id)
            form = Teacher_leave_creditform(request.POST,request.FILES)
            
            mgnt_edit = Teacher_leave_credit.objects.get(id=tid1)
            if form.is_valid():
                before_entry=mgnt_edit.no_of_days_credit - form.cleaned_data['no_of_days_credit']
                mgnt_edit.leave_type=form.cleaned_data['leave_type']
                mgnt_edit.effective_date=form.cleaned_data['effective_date']
                mgnt_edit.no_of_days_credit=form.cleaned_data['no_of_days_credit']
                mgnt_edit.previous_balance=form.cleaned_data['previous_balance'] 
                mgnt_edit.current_balance=form.cleaned_data['current_balance']           
                mgnt_edit.save()
                messages.success(request,'Leave Credit Details Updated successfully')

                record.el_bal=form.cleaned_data['current_balance']           
                
                record.el_ob=record.el_bal
                record.save()  
                return redirect('teacher_leave_credit_create',pk=unique_id)
            else:
                print form.errors
                return render(request,'teachers/leave_credit/teacher_leave_credit_form3.html',locals()) 
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class Teacher_leave_credit_create1(View):
    #@never_cache
    def get(self,request,**kwargs):
        if request.user.is_authenticated():
            import datetime

            school_code=self.kwargs.get('pk') 
            basic_det=Basicinfo.objects.get(udise_code=school_code)
               
            school_id =basic_det.school_id   
            entry_flag=0
            data_entry=0
            hm_rec=0
            same_month=0
            now = datetime.datetime.now()
            if now.month==1 or now.month==7 :
                try:
                    rec=Teacher_leave_credit.objects.filter(school_id=basic_det.school_id,stafs='Non Teaching')
                    if rec.count()==0:
                        record=Teacher_detail.objects.filter(school_id=basic_det.school_id,stafs='Non Teaching').filter(ofs_flag=False).filter(transfer_flag='No').filter(super_annum_flag=False)
                        rec1=Teacher_detail.objects.get(school_id=basic_det.school_id,designation__contains='Head Master').filter(ofs_flag=False).filter(transfer_flag='No').filter(super_annum_flag=False)
                    if rec.count() > 0:
                        for i in rec:
                            t=(i.timestamp).month
                            if (i.timestamp).month ==now.month or (i.timestamp).month==(now.month)+1 :
                                same_month=1
                            else:
                                i.delete()

                        if same_month==1:
                            record=Teacher_leave_credit.objects.filter(school_id=basic_det.school_id,stafs='Non Teaching')
                except:
                    record=Teacher_detail.objects.filter(school_id=basic_det.school_id,stafs='Non Teaching').filter(ofs_flag=False).filter(transfer_flag='No')
            elif now.month==6:
                try:
                    rec=Teacher_leave_credit.objects.filter(school_id=basic_det.school_id,stafs='Teaching')
                   
                    if rec.count()==0:
                        record=Teacher_detail.objects.filter(school_id=basic_det.school_id,stafs='Teaching').filter(ofs_flag=False).filter(transfer_flag='No').filter(super_annum_flag=False)
                    if rec.count() > 0:
                        for i in rec:
                            t=(i.timestamp).month
                            if (i.timestamp).month ==now.month or (i.timestamp).month==(now.month)+1 :
                                same_month=1
                            else:
                                i.delete()

                        if same_month==1:
                            record=Teacher_leave_credit.objects.filter(school_id=basic_det.school_id,stafs='Teaching')
                except:
                    record=Teacher_detail.objects.filter(school_id=basic_det.school_id,stafs='Teaching').filter(ofs_flag=False).filter(transfer_flag='No').filter(super_annum_flag=False)
            else:
                record=Teacher_leave_credit.objects.filter(school_id=basic_det.school_id)
                if record.count()==0:
                    msg = " EL Credit only allowed in the month of January and June for Non-Teaching Staffs and July for Teaching Staffs"
                    messages.warning(request, msg ) 
                    data_entry=1
                else:
                    entry_flag=1

            AEOENTRY=1
            return render(request,'teachers/leave_credit/teacher_leave_credit_form3.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    #@never_cache
    def post(self,request,**kwargs):
        if request.user.is_authenticated():
            try:
                if str(request.POST['a'])==str('hm'):

                    b=Teacher_leave_credit(school_id=basic_det.school_id,teacherid_id=request.POST['b'],
                        effective_date= request.POST['aeffective_date'],
                        no_of_days_credit= request.POST['ano_of_days_credit'],
                        stafs='Non Teaching',
                        designation=request.POST['c'],
                        complete_flag=1,
                       
                        )
                    b.save()
            except:
                pass
            
            emp_id=request.POST.getlist('emp_id')
            effective_date=request.POST.getlist('effective_date')
            no_of_days_credit=request.POST.getlist('no_of_days_credit')
            emp_cat=request.POST.getlist('emp_cat')
            emp_designation=request.POST.getlist('emp_desig')
            
            for entry in range(len(effective_date)):
                c=effective_date[entry]
                yymmddformat = datetime.datetime.strptime(c,'%d/%m/%Y').strftime('%Y-%m-%d')
                a=Teacher_leave_credit(school_id=basic_det.school_id,teacherid_id=emp_id[entry],
                    effective_date= yymmddformat,
                    no_of_days_credit= no_of_days_credit[entry],
                    stafs=emp_cat[entry],
                    designation=emp_designation[entry],
                    complete_flag=1,
                   
                    )
                          
                if (Teacher_leave_master.objects.filter(teacherid_id=emp_id[entry]).count())>0:      
                    record=Teacher_leave_master.objects.get(teacherid_id=emp_id[entry])
                    record.el_ob=record.el_bal
                    record.el_bal=int(record.el_bal)+int(no_of_days_credit[entry])
               
                    record.save()
                    a.save()
                else :
                    msg = " Leave Master should be updated First."
                    messages.success(request, msg ) 
                    return HttpResponseRedirect('/teachers/teachers_school_level_name_list/') 
                
            msg = " Leave Credit details added successfully."
            messages.success(request, msg )   
            
            basic_det=Basicinfo.objects.get(school_id=basic_det.school_id)
            return redirect('teachers_school_level_name_list',pk=basic_det.udise_code)
            return HttpResponseRedirect('/teachers/teachers_school_level_name_list/') 
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))