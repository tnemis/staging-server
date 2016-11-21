from django.views.generic import View
from teachers.models import Teacher_action,Teacher_detail,completed_table,Teacher_posting_entry,disp_rule,action
from schoolnew.models import Basicinfo
from teachers.forms import Teacher_actionform
from django.shortcuts import render,redirect,get_object_or_404,Http404,get_list_or_404
from django.db import *
from datetime import datetime
from django.contrib import messages
import teacher_main_views
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache

class Teacher_action_create(View):
    #@never_cache
    def get(self,request,**kwargs):
        if request.user.is_authenticated():
           
            import teacher_main_views

            if request.user.account.associated_with=='state' or request.user.account.associated_with=='DIPE' or request.user.account.associated_with=='CIPE' or request.user.account.associated_with=='Zone' or request.user.account.associated_with=='IAS' or request.user.account.associated_with=='IMS' :
                AEOENTRY=0
            else:

                AEOENTRY=teacher_main_views.aeoentrycheck(request.user.account.associated_with)
            try:
            
                # school_id = request.user.account.associated_with
                tid=self.kwargs.get('pk')
                unique_id=Teacher_detail.objects.get(id=tid)
                basic_det=Basicinfo.objects.get(school_id=unique_id.school_id)
                sch_key = basic_det.id           
                school_id =unique_id.school_id
                dategovt=unique_id.dofsed
                posting_desg=Teacher_posting_entry.objects.filter(teacherid_id=tid)
                if posting_desg.count()==0:
                    messages.warning(request, 'First make entries in Posting tab')
                    return redirect('teacher_personnel_entry_after',pk=tid)
                type_charge_memo1=disp_rule.objects.all()
                action_namee=action.objects.all()
                edu_list = Teacher_action.objects.filter(teacherid_id=tid).filter(cleared_flag=0)
                if edu_list.count()==0:
                    messages.success(request, 'No Record')
                    update=0
            except unique_id.DoesNotExist:
                messages.add_message(
                    self.request,
                    messages.ERROR,"No Teacher Data"
                )
            return render(request,'teachers/action/teacher_action_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
  
    #@never_cache
    def post(self,request,**kwargs):  
        if request.user.is_authenticated():   
            form=Teacher_actionform(request.POST,request.FILES)
            school_id = request.user.account.associated_with
            unique_id=request.POST['unique_id']
            unique_name=request.POST['unique_name']
                    
            if form.is_valid():   
                loan=Teacher_action(teacherid_id=unique_id,
                        post_name_charge_committed=form.cleaned_data['post_name_charge_committed'],
                        gist=form.cleaned_data['gist'],
                        charge_memo_number=form.cleaned_data['charge_memo_number'],
                        charge_memo_date=form.cleaned_data['charge_memo_date'],
                        charge_pending=form.cleaned_data['charge_pending'],
                        type_charge_memo=form.cleaned_data['type_charge_memo'],
                        a_individual_exp_date=form.cleaned_data['a_individual_exp_date'],
                        a_final_order_no=form.cleaned_data['a_final_order_no'],
                        a_final_order_date=form.cleaned_data['a_final_order_date'],
                        a_final_status=form.cleaned_data['a_final_status'],
                        a_increment_cut_years=form.cleaned_data['a_increment_cut_years'],
                        e_whether_suspented=form.cleaned_data['e_whether_suspented'],
                        e_suspension_order_date=form.cleaned_data['e_suspension_order_date'],
                        e_reinitiated_service=form.cleaned_data['e_reinitiated_service'],
                        e_reinitiated_date=form.cleaned_data['e_reinitiated_date'],
                        e_charge_memo=form.cleaned_data['e_charge_memo'],
                        b_individula_exp_date=form.cleaned_data['b_individula_exp_date'],
                        b_enquiry_officer_appointed=form.cleaned_data['b_enquiry_officer_appointed'],
                        b_enquiry_officer_app_date=form.cleaned_data['b_enquiry_officer_app_date'],
                        b_enquiry_officer_name=form.cleaned_data['b_enquiry_officer_name'],
                        b_enquiry_officer_rpt_received=form.cleaned_data['b_enquiry_officer_rpt_received'],
                        b_charges_proved=form.cleaned_data['b_charges_proved'],
                        b_addl_exp_individual_date=form.cleaned_data['b_addl_exp_individual_date'],
                        b_final_order_date=form.cleaned_data['b_final_order_date'],
                        b_punishment_type=form.cleaned_data['b_punishment_type'],
                        b_appeal_received=form.cleaned_data['b_appeal_received'],
                        b_appeal_date=form.cleaned_data['b_appeal_date'],
                        b_final_order_date_appeal=form.cleaned_data['b_final_order_date_appeal'],
                        b_increment_cut_years=form.cleaned_data['b_increment_cut_years'],
                        b_punishment_type_appeal=form.cleaned_data['b_punishment_type_appeal'],
                        b_increment_cut_years_appeal=form.cleaned_data['b_increment_cut_years_appeal']
                        )
                loan.save()           
           
                b=completed_table.objects.get(teacherid_id=unique_id)

                if b.Teacher_disaction=='0':
                    b.id=b.id
                    b.teacherid_id=b.teacherid_id
                    b.Teacher_disaction=18
                    b.save()
                msg = str(unique_name) + "(" + str(unique_id)+") Disciplinary Action details added successfully."
                messages.success(request, msg )       
                
                return redirect('teacher_action_create',pk=unique_id)
              
            else:
                print form.errors
                return render(request,'teachers/action/teacher_action_form.html',locals())        
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


class teacher_action_update(View):
    #@never_cache
    def get(self, request,**kwargs):
        if request.user.is_authenticated():
            process='Update'
            # school_id = request.user.account.associated_with
            tid=self.kwargs.get('pk')
            pk1=self.kwargs.get('pk1')
            unique_id=Teacher_detail.objects.get(id=tid)
            basic_det=Basicinfo.objects.get(school_id=unique_id.school_id)
            school_id =unique_id.school_id    
            posting_desg=Teacher_posting_entry.objects.filter(teacherid_id=tid)
            type_charge_memo1=disp_rule.objects.all()
            action_namee=action.objects.all()
            instance=Teacher_action.objects.get(id=pk1)
            form = Teacher_actionform(instance=instance)
            teacherid_id = instance.teacherid_id       
            post_name_charge_committed=instance.post_name_charge_committed
            gist=instance.gist
            charge_memo_number=instance.charge_memo_number
            charge_memo_date=instance.charge_memo_date
            charge_pending=instance.charge_pending

            type_charge_memo=instance.type_charge_memo
            a_individual_exp_date=instance.a_individual_exp_date
            a_final_order_no=instance.a_final_order_no
            a_final_order_date=instance.a_final_order_date
            a_final_status=instance.a_final_status
            a_increment_cut_years=instance.a_increment_cut_years
            e_whether_suspented=instance.e_whether_suspented
          
            e_suspension_order_date=instance.e_suspension_order_date
            e_reinitiated_service=instance.e_reinitiated_service
            
            e_reinitiated_date=instance.e_reinitiated_date
            e_charge_memo=instance.e_charge_memo
            b_individula_exp_date=instance.b_individula_exp_date
            b_enquiry_officer_appointed=instance.b_enquiry_officer_appointed
            b_enquiry_officer_app_date=instance.b_enquiry_officer_app_date
            b_enquiry_officer_name=instance.b_enquiry_officer_name
            b_enquiry_officer_rpt_received=instance.b_enquiry_officer_rpt_received
            b_charges_proved=instance.b_charges_proved
            b_addl_exp_individual_date=instance.b_addl_exp_individual_date
            b_final_order_date=instance.b_final_order_date
            b_punishment_type=instance.b_punishment_type
            b_appeal_received=instance.b_appeal_received
            b_appeal_date=instance.b_appeal_date
            b_final_order_date_appeal=instance.b_final_order_date_appeal  
            b_increment_cut_years=instance.b_increment_cut_years
            b_punishment_type_appeal=instance.b_punishment_type_appeal
            b_increment_cut_years_appeal=instance.b_increment_cut_years_appeal
            
            return render(request,'teachers/action/teacher_action_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    
    #@never_cache
    def post(self,request,**kwargs):
        if request.user.is_authenticated():
            school_id = request.user.account.associated_with
            tid=self.kwargs.get('pk')
            pk1=self.kwargs.get('pk1')
            unique_id=Teacher_detail.objects.get(id=tid)
            edu_list = Teacher_action.objects.filter(teacherid_id=unique_id).filter(cleared_flag=0)
            act_edit=Teacher_action.objects.get(id=pk1)
            form = Teacher_actionform(request.POST,request.FILES)

            posting_desg=Teacher_posting_entry.objects.filter(teacherid_id=tid)
            type_charge_memo1=disp_rule.objects.all()
            action_namee=action.objects.all()
            
            if form.is_valid():
                act_edit.teacherid_id=unique_id
                act_edit.post_name_charge_committed=form.cleaned_data['post_name_charge_committed']
                act_edit.gist=form.cleaned_data['gist']
                act_edit.charge_memo_number=form.cleaned_data['charge_memo_number']
                act_edit.charge_memo_date=form.cleaned_data['charge_memo_date']
                act_edit.charge_pending=form.cleaned_data['charge_pending']
                act_edit.type_charge_memo_id=form.cleaned_data['type_charge_memo']
                type_charge_check=disp_rule.objects.get(id=request.POST['type_charge_memo'])

                if str(type_charge_check)== '17(a)':
                    act_edit.a_individual_exp_date=form.cleaned_data['a_individual_exp_date']
                    act_edit.a_final_order_no=form.cleaned_data['a_final_order_no']
                    act_edit.a_final_order_date=form.cleaned_data['a_final_order_date']
                    act_edit.a_final_status=form.cleaned_data['a_final_status']
                    final=request.POST['a_final_status']
                    
                    if final=='2':
                        act_edit.a_increment_cut_years=form.cleaned_data['a_increment_cut_years']
                    else :
                        act_edit.a_increment_cut_years=''
                      
                    act_edit.e_whether_suspented=None
                    act_edit.e_suspension_order_date=None
                    act_edit.e_reinitiated_service=None
                    act_edit.e_reinitiated_date=None
                    act_edit.e_charge_memo=None
                    act_edit.b_individula_exp_date=None
                    act_edit.b_enquiry_officer_appointed=None
                    act_edit.b_enquiry_officer_app_date=None
                    act_edit.b_enquiry_officer_name=''
                    act_edit.b_enquiry_officer_rpt_received=None
                    act_edit.b_charges_proved=None
                    act_edit.b_addl_exp_individual_date=None
                    act_edit.b_final_order_date=None
                    act_edit.b_punishment_type_id=None
                    act_edit.b_appeal_received=None
                    act_edit.b_appeal_date=None
                    act_edit.b_final_order_date_appeal=None
                    act_edit.b_increment_cut_years=''
                    act_edit.b_punishment_type_appeal=None
                    act_edit.b_increment_cut_years_appeal=''

                elif str(type_charge_check)== '17(b)':
                    act_edit.a_individual_exp_date=None
                    act_edit.a_final_order_no=''
                    act_edit.a_final_order_date=None
                    act_edit.a_final_status=None
                    act_edit.a_increment_cut_years=''
                    act_edit.e_whether_suspented=None
                    act_edit.e_suspension_order_date=None
                    act_edit.e_reinitiated_service=''
                    act_edit.e_reinitiated_date=None
                    act_edit.e_charge_memo=None
                    act_edit.b_individula_exp_date=form.cleaned_data['b_individula_exp_date']
                    act_edit.b_enquiry_officer_appointed=form.cleaned_data['b_enquiry_officer_appointed']
                    enq=request.POST['b_enquiry_officer_appointed']
                    if enq== '1':
                        act_edit.b_enquiry_officer_app_date=form.cleaned_data['b_enquiry_officer_app_date']
                        act_edit.b_enquiry_officer_name=form.cleaned_data['b_enquiry_officer_name']
                        act_edit.b_enquiry_officer_rpt_received=form.cleaned_data['b_enquiry_officer_rpt_received']
                    else :
                        act_edit.b_enquiry_officer_app_date=None
                        act_edit.b_enquiry_officer_name=''
                        act_edit.b_enquiry_officer_rpt_received=None

                    act_edit.b_charges_proved=form.cleaned_data['b_charges_proved']
                    charge=request.POST['b_charges_proved']
                    if charge== '1':
                        act_edit.b_addl_exp_individual_date=form.cleaned_data['b_addl_exp_individual_date']
                        act_edit.b_final_order_date=form.cleaned_data['b_final_order_date']
                        act_edit.b_punishment_type_id=form.cleaned_data['b_punishment_type']
                        inc_yr=request.POST['b_punishment_type']
                        if inc_yr=='1'or inc_yr=='7':
                            act_edit.b_increment_cut_years=form.cleaned_data['b_increment_cut_years']
                        else :
                            act_edit.b_increment_cut_years=''
                        
                    else:
                        act_edit.b_addl_exp_individual_date=None
                        act_edit.b_final_order_date=None
                        act_edit.b_punishment_type_id=''
                        act_edit.b_increment_cut_years=''
                        

                    act_edit.b_appeal_received=form.cleaned_data['b_appeal_received']
                    appl=request.POST['b_appeal_received']
                    if appl=='1':
                        act_edit.b_appeal_date=form.cleaned_data['b_appeal_date']
                        act_edit.b_final_order_date_appeal=form.cleaned_data['b_final_order_date_appeal']
                        act_edit.b_punishment_type_appeal=form.cleaned_data['b_punishment_type_appeal']
                        flag=request.POST['b_punishment_type_appeal']
                        if flag == "Increment Cut Without Cummulative Effect" or flag == "Increment Cut With Cummulative Effect" :
                            act_edit.b_increment_cut_years_appeal=form.cleaned_data['b_increment_cut_years_appeal']
                        else:
                            act_edit.b_increment_cut_years_appeal=''
                    else:
                        act_edit.b_appeal_date=None
                        act_edit.b_final_order_date_appeal=None
                        act_edit.b_punishment_type_appeal=''
                        act_edit.b_increment_cut_years_appeal=''

                else:
                
                    act_edit.e_whether_suspented=form.cleaned_data['e_whether_suspented']
                    sus=request.POST['e_whether_suspented']
                    if sus=='1':
                        act_edit.e_suspension_order_date=form.cleaned_data['e_suspension_order_date']
                        act_edit.e_reinitiated_service=form.cleaned_data['e_reinitiated_service']
                        rein=request.POST['e_reinitiated_service']
                        if rein=='1':
                            act_edit.e_reinitiated_date=form.cleaned_data['e_reinitiated_date']
                        else:
                            act_edit.e_reinitiated_date=None
                    else :
                        act_edit.e_suspension_order_date=None
                        act_edit.e_reinitiated_service=''
                        act_edit.e_reinitiated_date=None
               
                    act_edit.e_charge_memo=form.cleaned_data['e_charge_memo']
                    charge_memo=disp_rule.objects.get(id=request.POST['e_charge_memo'])
                    if str(charge_memo)== '17(a)':
                        act_edit.a_individual_exp_date=form.cleaned_data['a_individual_exp_date']
                        act_edit.a_final_order_no=form.cleaned_data['a_final_order_no']
                        act_edit.a_final_order_date=form.cleaned_data['a_final_order_date']
                        act_edit.a_final_status=form.cleaned_data['a_final_status']
                        final=request.POST['a_final_status']
                        
                        if final=='2':
                            act_edit.a_increment_cut_years=form.cleaned_data['a_increment_cut_years']
                        else :
                            act_edit.a_increment_cut_years=''
                          
                        act_edit.b_individula_exp_date=None
                        act_edit.b_enquiry_officer_appointed=None
                        act_edit.b_enquiry_officer_app_date=None
                        act_edit.b_enquiry_officer_name=''
                        act_edit.b_enquiry_officer_rpt_received=None
                        act_edit.b_charges_proved=None
                        act_edit.b_addl_exp_individual_date=None
                        act_edit.b_final_order_date=None
                        act_edit.b_punishment_type_id=None
                        act_edit.b_appeal_received=None
                        act_edit.b_appeal_date=None
                        act_edit.b_final_order_date_appeal=None
                        act_edit.b_increment_cut_years=''
                        act_edit.b_punishment_type_appeal=None
                        act_edit.b_increment_cut_years_appeal=''
                    elif str(charge_memo)== '17(b)':
                        act_edit.a_individual_exp_date=None
                        act_edit.a_final_order_no=''
                        act_edit.a_final_order_date=None
                        act_edit.a_final_status=None
                        act_edit.a_increment_cut_years=''
                        act_edit.b_individula_exp_date=form.cleaned_data['b_individula_exp_date']
                        act_edit.b_enquiry_officer_appointed=form.cleaned_data['b_enquiry_officer_appointed']
                        enq=request.POST['b_enquiry_officer_appointed']
                        if enq== '1':
                            act_edit.b_enquiry_officer_app_date=form.cleaned_data['b_enquiry_officer_app_date']
                            act_edit.b_enquiry_officer_name=form.cleaned_data['b_enquiry_officer_name']
                            act_edit.b_enquiry_officer_rpt_received=form.cleaned_data['b_enquiry_officer_rpt_received']
                        else :
                            act_edit.b_enquiry_officer_app_date=None
                            act_edit.b_enquiry_officer_name=''
                            act_edit.b_enquiry_officer_rpt_received=None

                        act_edit.b_charges_proved=form.cleaned_data['b_charges_proved']
                        charge=request.POST['b_charges_proved']
                        if charge== '1':
                            act_edit.b_addl_exp_individual_date=form.cleaned_data['b_addl_exp_individual_date']
                            act_edit.b_final_order_date=form.cleaned_data['b_final_order_date']
                            act_edit.b_punishment_type_id=form.cleaned_data['b_punishment_type']
                            inc_yr=request.POST['b_punishment_type']
                            if inc_yr=='1' or inc_yr=='7':
                                act_edit.b_increment_cut_years=form.cleaned_data['b_increment_cut_years']
                            else :
                                act_edit.b_increment_cut_years=''
                        else:
                            act_edit.b_addl_exp_individual_date=None
                            act_edit.b_final_order_date=None
                            act_edit.b_punishment_type_id=''
                            act_edit.b_increment_cut_years=''
                            

                        act_edit.b_appeal_received=form.cleaned_data['b_appeal_received']
                        appl=request.POST['b_appeal_received']
                        if appl=='1':
                            act_edit.b_appeal_date=form.cleaned_data['b_appeal_date']
                            act_edit.b_final_order_date_appeal=form.cleaned_data['b_final_order_date_appeal']
                            act_edit.b_punishment_type_appeal=form.cleaned_data['b_punishment_type_appeal']
                            flag=request.POST['b_punishment_type_appeal']
                            if flag == "Increment Cut Without Cummulative Effect" or flag == "Increment Cut With Cummulative Effect" :
                                act_edit.b_increment_cut_years_appeal=form.cleaned_data['b_increment_cut_years_appeal']
                            else:
                                act_edit.b_increment_cut_years_appeal=''
                        else:
                            act_edit.b_appeal_date=None
                            act_edit.b_final_order_date_appeal=None
                            act_edit.b_punishment_type_appeal=''
                            act_edit.b_increment_cut_years_appeal=''
                        
                act_edit.save()
            else:
                print form.errors
                return render(request,'teachers/action/teacher_action_form.html',locals())

            messages.success(request,'Disciplinary Action Entry Altered ')

            return redirect('teacher_action_create',pk=tid)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class teacher_action_history(View):
    #@never_cache
    def get(self, request,**kwargs):
        if request.user.is_authenticated():
            school_id = request.user.account.associated_with
            tid=self.kwargs.get('pk')
            edu_list = Teacher_action.objects.filter(teacherid_id=tid)      
            return render(request,'teachers/action/control_trans.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
