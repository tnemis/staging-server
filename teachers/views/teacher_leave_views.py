from django.views.generic import *
from teachers.models import *
from teachers.forms import *
from django.shortcuts import *
from baseapp.models import *
from django.contrib import messages
from django.db import *
from datetime import *
from datetime import datetime, timedelta
from django.views.generic import *
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache



class teacher_leave_entry_create(View):
    #@never_cache
    def get(self,request,**kwargs):
        if request.user.is_authenticated():
            import teacher_main_views
            if request.user.account.associated_with=='state' or request.user.account.associated_with=='DIPE' or request.user.account.associated_with=='CIPE' or request.user.account.associated_with=='Zone' or request.user.account.associated_with=='IAS' or request.user.account.associated_with=='IMS' :
                AEOENTRY=0
            else:
                AEOENTRY=teacher_main_views.aeoentrycheck(request.user.account.associated_with)
            leave_code=Teacher_leave_type.objects.all()
            tid=self.kwargs.get('pk')
            unique_id=Teacher_detail.objects.get(id=tid)
            basic_det=Basicinfo.objects.get(school_id=unique_id.school_id)
            school_id =unique_id.school_id
            doj=unique_id.dofsed
            try:

                records=Teacher_leave_master.objects.get(teacherid_id=unique_id)
                timez=records.timestamp
                validated=timez.date()
                
            except:
                msg = " First Make Leave Master "
                messages.warning(request, msg)
                return redirect('teacher_personnel_entry_after',pk=tid)
                family=Teacher_family_detail.objects.filter(teacherid_id=tid)
                

            edu_list = Teacher_leave.objects.filter(teacherid_id=tid)
            if edu_list.count()==0: 
                messages.success(request, 'No Data') 
            
            return render(request,'teachers/leave/teacher_leave_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    #@never_cache
    def post(self,request,**kwargs):
        if request.user.is_authenticated():
            unique_id=request.POST['unique_id']
            unique_name=request.POST['unique_name']
            data=Teacher_detail.objects.get(id=unique_id)
            doj=data.dofsed
            desig=data.designation
            doregular=data.doregu
            form = Teacher_leaveform(request.POST,request.FILES)
            if form.is_valid():  
                records=Teacher_leave_master.objects.get(teacherid_id=unique_id)
                no_of_days1=(form.cleaned_data['leave_to'])-(form.cleaned_data['leave_from'])
                no_of_days=no_of_days1.days  +1 
                           
                leave=Teacher_leave(teacherid_id=unique_id,
                            leave_type=form.cleaned_data['leave_type'],
                            leave_from=form.cleaned_data['leave_from'],
                            leave_to=form.cleaned_data['leave_to'],
                            order_no=form.cleaned_data['order_no'],
                            order_date=form.cleaned_data['order_date'],                        
                            )
                    
                b=completed_table.objects.get(teacherid_id=unique_id)        
                if b.Teacher_leav=='0':
                    b.id=b.id
                    b.teacherid_id=b.teacherid_id
                    b.Teacher_leav=9
                    b.save()
               
                desig_id=User_desig.objects.get(user_desig=desig)
                desig=desig_id.ser_type

                record=Teacher_leave_master.objects.get(teacherid_id=unique_id)

                if leave.leave_type_id==2:
                    if no_of_days >(record.el_ob-record.el_taken):
                        msg = " Leave Exceeds." 
                        messages.warning(request, msg ) 
                        return redirect('teacher_leave_entry_create',pk=unique_id)    
                    else:    
                        opening_balance=record.el_ob
                        
                        if (record.el_taken):
                            record.el_taken=int(record.el_taken)+int(no_of_days)
                        else:
                            record.el_taken=no_of_days
                        if (record.el_bal):                  
                            record.el_bal=int(record.el_bal)-int(no_of_days)
                        else:
                            record.el_bal=no_of_days

                        leave.ob=opening_balance
                        leave.taken=record.el_taken
                        leave.bal=record.el_bal
                        record.save()
                        leave.save()  
                        msg = str(unique_name) + " Leave details added successfully." 
                        messages.success(request, msg )  
                   
                elif leave.leave_type_id==3:
                    try: 
                        if desig==0:
                            years_of_exp=(leave.leave_from-doj).days/365.25
                            print 'staff'
                            if years_of_exp<2:
                                messages.success(request,'ML Not Eligible')
                                return redirect('teacher_leave_entry_create',pk=unique_id)
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
                            years_of_exp=(leave.leave_from-doregular).days/365.25
                            if years_of_exp<1:
                                messages.success(request,'ML Not Eligible')
                                return redirect('teacher_leave_entry_create',pk=unique_id)
                            elif years_of_exp>=1 and years_of_exp<15:
                                eligible_days=((leave.leave_from-doregular).days/1365.25)*10
                            elif years_of_exp>=15 and years_of_exp<20:
                                eligible_days=360
                            
                            elif years_of_exp>=20:
                                eligible_days=540
                        
                        record.uel_mc_ob=eligible_days

                        if no_of_days>eligible_days:
                            messages.warning(request,'ML Days Exceeds than available')
                            return redirect('teacher_leave_entry_create',pk=unique_id)
                        else:
                            opening_balance=record.uel_mc_ob
                            
                            if (record.uel_mc_taken):
                                record.uel_mc_taken=int(record.uel_mc_taken)+int(no_of_days)
                            else:
                                record.uel_mc_taken=no_of_days
                                              
                            leave.ob=opening_balance
                            leave.taken=record.uel_mc_taken
                            
                            record.uel_mc_bal=opening_balance-no_of_days
                            record.save()
                            leave.save()  
                            msg = str(unique_name) + " Leave details added successfully." 
                            messages.success(request, msg )  
                    except:
                        messages.warning(request,'ML Days Exceeds than available')


                elif leave.leave_type_id==4:
                    opening_balance=record.llp_mc_ob
                    if (record.llp_mc_taken):
                        record.llp_mc_taken=int(record.llp_mc_taken)+int(no_of_days)
                    else:
                        record.llp_mc_taken=no_of_days
                    leave.ob=opening_balance
                    leave.taken=record.llp_mc_taken
                    
                    record.save()
                    leave.save()  
                    msg = str(unique_name) + " Leave details added successfully." 
                    messages.success(request, msg )  
                elif leave.leave_type_id==10:
                     
                        if desig==05:
                            years_of_exp=(leave.leave_from-doj).days/365.25
                            
                            if years_of_exp>2:
                                
                                eligible_days=730

                            else:
                                messages.success(request,'LLP without MC Not Eligible')
                            
                        else:
                            years_of_exp=(leave.leave_from-doregular).days/365.25
                            if years_of_exp<15:
                                messages.success(request,'LLP without MC Not Eligible')
                            elif years_of_exp>=15:
                                eligible_days=180
                            
                        record.llp_womc_ob=eligible_days
                        if no_of_days>eligible_days:
                            messages.warning(request,'LLP without MC - Days Exceeds than Eligible ' + eligible_days  )
                        else:
                            opening_balance=record.llp_womc_ob
                            
                            if (record.llp_womc_taken):
                                record.llp_womc_taken=int(record.llp_womc_taken)+int(no_of_days)
                            else:
                                record.llp_womc_taken=no_of_days
                                              
                            record.llp_womc_bal=opening_balance-no_of_days
                            
                            leave.ob=opening_balance
                            leave.taken=record.llp_womc_taken
                            record.save()
                            leave.save()  
                            msg = str(unique_name) + " Leave details added successfully." 
                            messages.success(request, msg )  
                
                elif leave.leave_type_id==5:
                        
                        if desig==05:
                            years_of_exp=(leave.leave_from-doj).days/365.25
                            
                            if years_of_exp<10:
                                
                                eligible_days=90
                            else:
                                eligible_days=180
                            
                        else:
                            years_of_exp=(leave.leave_from-doregular).days/365.25
                            if years_of_exp<15:
                                messages.success(request,'UnEarned Leave Private Affairs Not Eligible')
                            elif years_of_exp>=15:
                                eligible_days=180
                            
                        record.uel_pa_ob=eligible_days
                        if no_of_days>eligible_days:
                            messages.warning(request,'UnEarned Leave Private Affairs - Days Exceeds than Eligible. Eligible Days - ' + str(eligible_days))
                        elif no_of_days>90:
                            messages.warning(request,'Maximum at any time - 90 days-TNLR 13')
                        else:
                            opening_balance=record.uel_pa_ob
                            
                            if (record.uel_pa_taken):
                                record.uel_pa_taken=int(record.uel_pa_taken)+int(no_of_days)
                            else:
                                record.uel_pa_taken=no_of_days
                                              
                            record.uel_pa_bal=opening_balance-no_of_days
                            
                            leave.ob=opening_balance
                            leave.taken=record.uel_pa_taken
                            record.save()
                            leave.save()  
                            msg = str(unique_name) + " Leave details added successfully." 
                            messages.success(request, msg )  
                            
                elif leave.leave_type_id==6:
                           
                            gender=data.gender
                            if gender=='Male':
                                messages.warning(request,'MATERNITY LEAVE only Eligible for Ladies')
                            else:
                                fam_details=Teacher_family_detail.objects.filter(teacherid_id=unique_id)
                                child_count=0

                                import datetime
                                leave.leave_to= (leave.leave_from + timedelta(days=180)).isoformat()
                                
                                for i in fam_details:
                                    if i.relation.id==2 or i.relation.id==3:
                                        child_count=child_count+1
                                if child_count>=2:
                                    messages.warning(request,'MATERNITY LEAVE only Eligible for 2 Babies')       
                                    record.maternity_leave_ob=child_count+1
                                elif child_count<2:
                                    record.maternity_leave_ob=child_count+1
                                    
                                    leave.ob=record.maternity_leave_ob * 180
                                    leave.taken=record.maternity_leave_ob
                                    leave.bal=2-child_count

                                    record.save()
                                    leave.save()   
                                    msg = str(unique_name) + " Leave details added successfully." 
                                    messages.success(request, msg )  
                elif leave.leave_type_id==7:
                            leave_reasons=request.POST['relation1']
                            if leave_reasons=='infectious disease':
                                eligible_days=21
                            elif leave_reasons=='participating in sporting events':
                                eligible_days=30
                            elif leave_reasons=='family planning':

                                gender=data.gender

                                if gender=='Male':
                                    eligible_days=8
                                else:
                                    eligible_days=21
                            leave.leave_to= (leave.leave_from + timedelta(days=eligible_days)).isoformat()
                            print leave.leave_to
                            
                            no_of_days=eligible_days
                            edu = Teacher_leave.objects.filter(teacherid_id=unique_id).filter(leave_type_id=7)
                            taken_days=0
                            for i in edu:
                                if i.leave_type_id==7:
                                    taken_days=taken_days+i.taken
                            if taken_days:
                                leave.ob=no_of_days+taken_days
                                leave.taken=no_of_days+taken_days
                                leave.bal=no_of_days+taken_days
                            else:
                                leave.ob=no_of_days
                                leave.taken=no_of_days
                                leave.bal=no_of_days
                            leave.save()
                            msg = str(unique_name) + " Leave details added successfully." 
                            messages.success(request, msg )  
                elif leave.leave_type_id==11:
                            gender=data.gender
                            if gender=='Male':
                                messages.warning(request,'Eligible for Ladies')
                            else:
                           
                                import datetime
                                leave.leave_to= (leave.leave_from + timedelta(days=42)).isoformat()
                                
                                edu = Teacher_leave.objects.filter(teacherid_id=tid).filter(leave_type_id=11)
                                taken_days=0
                                for i in edu:
                                    if i.leave_type_id==11:
                                        taken_days=taken_days+edu.taken

                                if taken_days:
                                    leave.bal=taken_days
                                    leave.taken=taken_days+42
                                else:
                                    leave.taken=42
                                

                                record.save()
                                leave.save()   
                                msg = str(unique_name) + " Leave details added successfully." 
                                messages.success(request, msg )  
                    
                return redirect('teacher_leave_entry_create',pk=unique_id)
            else:
                print form.errors
                return render(request,'teachers/leave/teacher_leave_form.html',locals()) 
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


class Teacher_leave_delete(View): 
    #@never_cache
    def get(self, request,**kwargs): 
        if request.user.is_authenticated():
            tid=self.kwargs.get('pk') 
            staff_name=request.session['staffname'] 
            data=Teacher_leave.objects.get(id=tid)

            staff_id=request.session['staffid']
            count=Teacher_leave.objects.filter(teacherid_id=staff_id).count()
            if count == 1 :
                data.delete()
                b=completed_table.objects.get(teacherid_id=staff_id)
                b.id=b.id
                b.teacherid_id=b.teacherid_id
                b.Teacher_leav=0
                b.save()
            else :
                data.delete()         
            msg= str(data.leave_type) + " Removed successfully" 
            messages.success(request, msg )        
            return HttpResponseRedirect('/teachers/teacher_leave_create/')
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


class teacher_leave_update(View):
    #@never_cache
    def get(self, request,**kwargs):
        if request.user.is_authenticated():
            tid=self.kwargs.get('pk')
            tid1=self.kwargs.get('pk1')
            unique_id=Teacher_detail.objects.get(id=tid)  
            school_id =unique_id.school_id
            instance=Teacher_leave.objects.get(id=tid1)
            form=Teacher_leaveform(instance=instance)
            edu_list = Teacher_leave.objects.filter(teacherid_id=tid)
            if edu_list.count()==0:
                messages.success(request,'No Data')        
            leave_code=Teacher_leave_type.objects.all()         
            basic_det=Basicinfo.objects.get(school_id=staff_id.school_id)
      
            teacherid_id = instance.teacherid_id
            leave_type = instance.leave_type        
            leave_from=instance.leave_from        
            leave_to = instance.leave_to  
            order_no = instance.order_no  
            order_date =instance.order_date         
            return render(request,'teachers/leave/teacher_leave_form.html',locals()) 
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

  
    #@never_cache
    def post(self,request,**kwargs):        
        if request.user.is_authenticated():
            tid=self.kwargs.get('pk')  
            tid1=self.kwargs.get('pk1')     
            instance=Teacher_leave.objects.get(id=tid1)        
            form = Teacher_leaveform(request.POST,request.FILES)
            data=Teacher_detail.objects.get(id=tid)
            doj=data.dofsed
            desig=data.designation
            doregular=data.doregu
            mgnt_edit = Teacher_leave.objects.get(id=tid1)        
            records=Teacher_leave_master.objects.get(teacherid_id=tid)
            if form.is_valid():
                no_of_days1=(form.cleaned_data['leave_to'])-(form.cleaned_data['leave_from'])
                no_of_days=no_of_days1.days  +1 
                changed_taken=no_of_days-mgnt_edit.taken
                
                mgnt_edit.leave_type=form.cleaned_data['leave_type']
                mgnt_edit.leave_from=form.cleaned_data['leave_from']
                mgnt_edit.leave_to=form.cleaned_data['leave_to']
                mgnt_edit.order_no=form.cleaned_data['order_no']
                mgnt_edit.order_date=form.cleaned_data['order_date']  
                  
                record=Teacher_leave_master.objects.get(teacherid_id=tid)
                if mgnt_edit.leave_type_id==2:
                    if changed_taken >(record.el_ob-record.el_taken):
                        msg = " Leave Exceeds." 
                        messages.warning(request, msg ) 
                        return redirect('teacher_leave_entry_create',pk=unique_id)    
                    else:    
                        opening_balance=record.el_ob
                        
                        if (record.el_taken):
                            record.el_taken=int(record.el_taken)+int(changed_taken)
                        else:
                            record.el_taken=changed_taken
                        if (record.el_bal):                  
                            record.el_bal=int(record.el_bal)-int(no_of_days)
                        else:
                            record.el_bal=no_of_days                  
                        
                        mgnt_edit.ob=opening_balance
                        mgnt_edit.taken=record.el_taken
                        
                        record.save()
                        mgnt_edit.save()  
                    
                elif mgnt_edit.leave_type_id==3:
                    
                    if desig==05:
                        years_of_exp=(mgnt_edit.leave_from-doj).days/365.25
                        print 'staff'
                        if years_of_exp<2:
                            messages.success(request,'ML Not Eligible')
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
                        years_of_exp=(mgnt_edit.leave_from-doregular).days/365.25
                        if years_of_exp<1:
                            messages.success(request,'ML Not Eligible')
                        elif years_of_exp>=1 and years_of_exp<15:
                            eligible_days=((mgnt_edit.leave_from-doregular).days/1365.25)*10
                        elif years_of_exp>=15 and years_of_exp<20:
                            eligible_days=360
                        
                        elif years_of_exp>=20:
                            eligible_days=540
                    
                    if changed_taken>eligible_days:
                        messages.warning(request,'ML Days Exceeds than available')
                    else:
                        opening_balance=record.uel_mc_ob
                        
                        if (record.uel_mc_taken):
                            record.uel_mc_taken=int(record.uel_mc_taken)+int(changed_taken)
                        else:
                            record.uel_mc_taken=changed_taken
                                          
                        mgnt_edit.ob=opening_balance
                        mgnt_edit.taken=record.uel_mc_taken
                        
                        record.save()
                        mgnt_edit.save()  

                elif mgnt_edit.leave_type_id==4:
                    opening_balance=record.llp_mc_ob
                    if (record.llp_mc_taken):
                        record.llp_mc_taken=int(record.llp_mc_taken)+int(changed_taken)
                    else:
                        record.llp_mc_taken=changed_taken
                    
                    mgnt_edit.ob=opening_balance
                    mgnt_edit.taken=record.llp_mc_taken
                    
                    record.save()
                    mgnt_edit.save()  
                
                elif mgnt_edit.leave_type_id==10:
                        if desig==05:
                            years_of_exp=(mgnt_edit.leave_from-doj).days/365.25
                            if years_of_exp>2:
                                eligible_days=730
                            else:
                                messages.success(request,'LLP without MC Not Eligible')
                        else:
                            years_of_exp=(mgnt_edit.leave_from-doregular).days/365.25
                            if years_of_exp<15:
                                messages.success(request,'LLP without MC Not Eligible')
                            elif years_of_exp>=15:
                                eligible_days=180
                                           
                        if changed_taken>eligible_days:
                            messages.warning(request,'LLP without MC - Days Exceeds than Eligible ' + eligible_days  )
                        else:
                            opening_balance=record.llp_womc_ob
                            
                            if (record.llp_womc_taken):
                                record.llp_womc_taken=int(record.llp_womc_taken)+int(changed_taken)
                            else:
                                record.llp_womc_taken=changed_taken
                                              
                            mgnt_edit.ob=opening_balance
                            mgnt_edit.taken=record.llp_womc_taken
                            
                            record.save()
                            mgnt_edit.save()  
                
                elif mgnt_edit.leave_type_id==5:
                      
                        if desig==05:
                            years_of_exp=(mgnt_edit.leave_from-doj).days/365.25
                            print 'staff'
                            if years_of_exp<10:
                                eligible_days=90
                            else:
                                eligible_days=180
                            
                        else:
                            years_of_exp=(mgnt_edit.leave_from-doregular).days/365.25
                            if years_of_exp<15:
                                messages.success(request,'UnEarned Leave Private Affairs Not Eligible')
                            elif years_of_exp>=15:
                                eligible_days=180
                                            
                        if changed_taken>eligible_days:
                            messages.warning(request,'UnEarned Leave Private Affairs - Days Exceeds than Eligible. Eligible Days - ' + str(eligible_days))
                        elif changed_taken>90:
                            messages.warning(request,'Maximum at any time - 90 days-TNLR 13')
                        else:
                            opening_balance=record.uel_pa_ob
                            
                            if (record.uel_pa_taken):
                                record.uel_pa_taken=int(record.uel_pa_taken)+int(changed_taken)
                            else:
                                record.uel_pa_taken=changed_taken
                                              
                            mgnt_edit.ob=opening_balance
                            mgnt_edit.taken=record.uel_pa_taken
                            record.save()
                            mgnt_edit.save()  
                            
                elif mgnt_edit.leave_type_id==6:
                           
                            gender=data.gender
                            if gender=='Male':
                                messages.warning(request,'MATERNITY LEAVE only Eligible for Ladies')
                            else:
                                fam_details=Teacher_family_detail.objects.filter(teacherid_id=unique_id)
                                child_count=0

                                import datetime
                                mgnt_edit.leave_to= (mgnt_edit.leave_from + timedelta(days=180)).isoformat()
                                
                                for i in fam_details:
                                    if i.relation.id==2 or i.relation.id==3:
                                        child_count=child_count+1
                                if child_count>=2:
                                    messages.warning(request,'MATERNITY LEAVE only Eligible for 2 Babies')       
                                    record.maternity_leave_ob=child_count+1
                                elif child_count<2:
                                    record.maternity_leave_ob=child_count+1
                
                                mgnt_edit.ob=record.maternity_leave_ob * 180
                                mgnt_edit.taken=record.maternity_leave_ob
                                mgnt_edit.bal=2-child_count

                                record.save()
                                mgnt_edit.save()   
                elif mgnt_edit.leave_type_id==7:
                            leave_reasons=request.POST['relation1']
                            if leave_reasons=='infectious disease':
                                eligible_days=21
                            elif leave_reasons=='participating in sporting events':
                                eligible_days=30
                            elif leave_reasons=='family planning':

                                gender=data.gender

                                if gender=='Male':
                                    eligible_days=8
                                else:
                                    eligible_days=21
                            mgnt_edit.leave_to= (mgnt_edit.leave_from + timedelta(days=eligible_days)).isoformat()
                            changed_taken=eligible_days
                            edu = Teacher_leave.objects.filter(teacherid_id=tid).filter(leave_type_id=7)
                            taken_days=0
                            for i in edu:
                                if i.leave_type_id==7:
                                    taken_days=taken_days+i.taken

                            if taken_days:
                                mgnt_edit.ob=changed_taken+taken_days
                                mgnt_edit.taken=changed_taken+taken_days
                                mgnt_edit.bal=changed_taken+taken_days
                            else:
                                mgnt_edit.ob=changed_taken
                                mgnt_edit.taken=changed_taken
                                mgnt_edit.bal=changed_taken
                            mgnt_edit.save()
                elif mgnt_edit.leave_type_id==11:
                           
                            gender=data.gender
                            if gender=='Male':
                                messages.warning(request,'Eligible for Ladies')
                            else:
                                import datetime
                                mgnt_edit.leave_to= (mgnt_edit.leave_from + timedelta(days=42)).isoformat()
                                
                                edu = Teacher_leave.objects.filter(teacherid_id=tid).filter(leave_type_id=11)
                                taken_days=0
                                for i in edu:
                                    if i.leave_type_id==11:
                                        taken_days=taken_days+edu.taken

                                if taken_days:
                                    mgnt_edit.bal=taken_days
                                    mgnt_edit.taken=taken_days+42
                                else:
                                    mgnt_edit.taken=42
                                
                                record.save()
                                mgnt_edit.save()   
                
              
                messages.success(request,'Leave  Details Updated successfully')
                    
                return redirect('teacher_leave_entry_create',pk=tid)
            else:
                print form.errors
                return render(request,'teachers/leave/teacher_leave_form.html',locals()) 
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))