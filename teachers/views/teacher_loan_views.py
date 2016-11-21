from django.views.generic import View
from teachers.models import Teacher_detail,completed_table,Teacher_loan,Teacher_loan_category
from teachers.forms import Teacher_loanform
from schoolnew.models import Basicinfo
from django.shortcuts import *
from django.contrib import messages
from django.db import *
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache


class Teacher_loan_create(View):
    #@never_cache
    def get(self,request,**kwargs):
        if request.user.is_authenticated():
          import teacher_main_views
          if request.user.account.associated_with=='state' or request.user.account.associated_with=='DIPE' or request.user.account.associated_with=='CIPE' or request.user.account.associated_with=='Zone' or request.user.account.associated_with=='IAS' or request.user.account.associated_with=='IMS' :
            AEOENTRY=0
          else:
            AEOENTRY=teacher_main_views.aeoentrycheck(request.user.account.associated_with)
            form=Teacher_loanform()
            tid=self.kwargs.get('pk')        
            staff_id = Teacher_detail.objects.get(id = tid)  
            basic_det=Basicinfo.objects.get(school_id=staff_id.school_id)
            school_id =staff_id.school_id            
            dategovt=staff_id.dofsed
            staff_name=staff_id.name
            staff_uid=staff_id.count        
            teach_loan=Teacher_loan_category.objects.all()
            edu_list = Teacher_loan.objects.filter(teacherid_id=tid)       
            if edu_list.count()==0: 
                messages.success(request, 'No Data') 
            return render(request,'teachers/loan/teacher_loan_form.html',locals())
        else:
          return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
   
    #@never_cache
    def post(self,request,**kwargs):
        if request.user.is_authenticated():
            form=Teacher_loanform(request.POST,request.FILES)
            school_id = request.user.account.associated_with
            tid=self.kwargs.get('pk')        
            staff_id = Teacher_detail.objects.get(id = tid)          
            dategovt=staff_id.dofsed
            staff_name=staff_id.name
            staff_uid=staff_id.count     
            teach_loan=Teacher_loan_category.objects.all()

            if form.is_valid():            
                loan=Teacher_loan(teacherid_id=tid,
                            loan_category=form.cleaned_data['loan_category'],
                            loan_purpose=form.cleaned_data['loan_purpose'],
                            sanctioned_amt=form.cleaned_data['sanctioned_amt'],
                            installments=form.cleaned_data['installments'],
                            monthly_installment=form.cleaned_data['monthly_installment'],
                            first_insta_date=form.cleaned_data['first_insta_date'],
                            sanctioned_order=form.cleaned_data['sanctioned_order'],
                            sanctioned_date=form.cleaned_data['sanctioned_date'],
                            )
                loan.save()      
                b=completed_table.objects.get(teacherid_id=tid)            
                if b.Teacher_lon=='0':                
                    b.id=b.id
                    b.teacherid_id=b.teacherid_id
                    b.Teacher_lon=12
                    b.save()
                msg = str(staff_name) + "(" + str(staff_uid)+") Loan details added successfully."
                messages.success(request, msg )   
                return redirect('teacher_loan_create',pk=tid)
            else:
              print form.errors
              return render(request,'teachers/loan/teacher_loan_form.html',locals())         
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


class teacher_loan_update(View):
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
            instance=Teacher_loan.objects.get(id=pk1)       
            teach_loan=Teacher_loan_category.objects.all()
            form = Teacher_loanform(instance=instance)
            teacherid_id = instance.teacherid_id
            loan_category = instance.loan_category
            loan_purpose=instance.loan_purpose
            sanctioned_amt = instance.sanctioned_amt  
            installments =instance.installments
            monthly_installment =instance.monthly_installment
            first_insta_date =instance.first_insta_date
            sanctioned_order =instance.sanctioned_order
            sanctioned_date =instance.sanctioned_date         
            return render(request,'teachers/loan/teacher_loan_form.html',locals())
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
            instance=Teacher_loan.objects.get(id=pk1)       
            teach_loan=Teacher_loan_category.objects.all()     
            form = Teacher_loanform(request.POST,request.FILES)
            mgnt_edit = Teacher_loan.objects.get(id=pk1)
            if form.is_valid():
                mgnt_edit.loan_category=form.cleaned_data['loan_category']
                mgnt_edit.loan_purpose=form.cleaned_data['loan_purpose']
                mgnt_edit.sanctioned_amt=form.cleaned_data['sanctioned_amt']
                mgnt_edit.installments=form.cleaned_data['installments']
                mgnt_edit.monthly_installment=form.cleaned_data['monthly_installment'] 
                mgnt_edit.first_insta_date=form.cleaned_data['first_insta_date'] 
                mgnt_edit.sanctioned_order=form.cleaned_data['sanctioned_order'] 
                mgnt_edit.sanctioned_date=form.cleaned_data['sanctioned_date']             
                mgnt_edit.save()
                messages.success(request,'Loan Details Updated successfully')
                return redirect('teacher_loan_create',pk=tid)
            else:
                print form.errors
                return render(request,'teachers/loan/teacher_loan_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))