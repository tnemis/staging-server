from teachers.models import Teacher_detail,completed_table,Teacher_nomini,fund_category,Teacher_family_detail
from teachers.forms import Teacher_nominiform
from django.shortcuts import *
from schoolnew.models import Basicinfo
from django.contrib import messages
from django.db import *
from datetime import datetime
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache



class Teacher_nomini_create(View):
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
             
            school_id =staff_id.school_id            
                   
            dategovt=staff_id.dofsed
            staff_name=staff_id.name 
            staff_uid=staff_id.count        
            form=Teacher_nominiform()
            fund=fund_category.objects.all()
            family=Teacher_family_detail.objects.filter(teacherid_id=tid)
            if family.count()==0:
                messages.warning(request, 'First make entries in Family Details')
                return redirect('teacher_personnel_entry_after',pk=tid)
            edu_list = Teacher_nomini.objects.filter(teacherid_id=tid)       

            cps=0
            dcrg=0
            fbf=0
            gpf=0
            pension=0
            spf=0
            spf2000=0
            tpf=0
            
            for i in edu_list:
                if str(i.fund_name) == "CPS" :
                    cps=i.percentage + cps
                elif str(i.fund_name) == "DCRG" :
                    dcrg=i.percentage + dcrg
                elif str(i.fund_name) == "FBF" :
                    fbf=i.percentage + fbf
                elif str(i.fund_name) == "GPF" :
                    gpf=i.percentage + gpf
                elif str(i.fund_name) == "PENSION" :
                    pension=i.percentage + pension
                elif str(i.fund_name) == "SPF" :
                    spf=i.percentage + spf
                elif str(i.fund_name) == "SPF2000" :
                    spf2000=i.percentage + spf2000
                elif str(i.fund_name) == "TPF" :
                    tpf=i.percentage + tpf
                
            if edu_list.count()==0: 
                messages.success(request, 'No Data') 
            return render(request,'teachers/nomini/teacher_nomini_detail_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    
    #@never_cache
    def post(self,request,**kwargs):
        if request.user.is_authenticated():
            tid=self.kwargs.get('pk')        
            staff_id = Teacher_detail.objects.get(id = tid)          
            staff_name=staff_id.name 
            staff_uid=staff_id.count    
            form=Teacher_nominiform(request.POST,request.FILES)
            fund=fund_category.objects.all()
            if form.is_valid():            
                regular=Teacher_nomini(teacherid_id=tid,
                            fund_name=form.cleaned_data['fund_name'],
                            nominee_name=form.cleaned_data['nominee_name'],
                            other_nominee=form.cleaned_data['other_nominee'],
                            percentage=form.cleaned_data['percentage'],
                            nom_dt=form.cleaned_data['nom_dt'],
                            )
                regular.save() 

                b=completed_table.objects.get(teacherid_id=tid)
                if b.Teacher_financ=='0':
                    b.id=b.id
                    b.teacherid_id=b.teacherid_id
                    b.Teacher_financ=14
                    b.save()
                    msg = str(staff_name) + "(" + str(staff_uid)+") Finacial Nomini details added successfully." 
                    messages.success(request, msg ) 
                return redirect('teacher_nomini_create',pk=tid) 
            else:
                print form.errors
                return render(request,'teachers/nomini/teacher_nomini_detail_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class teacher_nomini_update(View):
    #@never_cache
    def get(self, request,**kwargs):
        if request.user.is_authenticated():
            tid=self.kwargs.get('pk') 
            pk1=self.kwargs.get('pk1') 
            staff_id = Teacher_detail.objects.get(id = tid) 
            basic_det=Basicinfo.objects.get(school_id=staff_id.school_id)
            school_id =staff_id.school_id            
            dategovt=staff_id.dofsed  
            staff_name=staff_id.name 
            staff_uid=staff_id.count     
            instance=Teacher_nomini.objects.get(id=pk1)       
            fund=fund_category.objects.all()
            family=Teacher_family_detail.objects.filter(teacherid_id=tid)
            form = Teacher_nominiform(instance=instance)
            teacherid_id = instance.teacherid_id
            fund_name = instance.fund_name
            nominee_name=instance.nominee_name
            other_nominee=instance.other_nominee       
            percentage = instance.percentage   
            nom_dt =instance.nom_dt    
            edu_list = Teacher_nomini.objects.filter(teacherid_id=tid) 
            cps=0
            dcrg=0
            fbf=0
            gpf=0
            pension=0
            spf=0
            spf2000=0
            tpf=0
            if str(other_nominee) != "None":
                fla=1
                
            elif str(nominee_name) != "None":
                fla=2

            for i in edu_list:
                per=i.percentage
                
                if fla==1:
                    if str(i.other_nominee)==str(other_nominee) and str(i.fund_name)==str(fund_name):
                        per = 0
                        
                elif str(i.nominee_name)==str(nominee_name) and str(i.fund_name)==str(fund_name):
                        per = 0
                        
                       
                if str(i.fund_name) == "CPS" :
                    cps=per + cps
                    
                elif str(i.fund_name) == "DCRG" :
                    dcrg=per + dcrg
                elif str(i.fund_name) == "FBF" :
                    fbf=per + fbf
                elif str(i.fund_name) == "GPF" :
                    gpf=per + gpf
                elif str(i.fund_name) == "PENSION" :
                    pension=per + pension
                elif str(i.fund_name) == "SPF" :
                    spf=per + spf
                elif str(i.fund_name) == "SPF2000" :
                    spf2000=per + spf2000
                elif str(i.fund_name) == "TPF" :
                    tpf=per + tpf 
            return render(request,'teachers/nomini/teacher_nomini_detail_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


    #@never_cache
    def post(self,request,**kwargs):
        if request.user.is_authenticated():
            tid=self.kwargs.get('pk') 
            pk1=self.kwargs.get('pk1') 
            staff_id = Teacher_detail.objects.get(id = tid)          
            dategovt=staff_id.dofsed  
            staff_name=staff_id.name 
            staff_uid=staff_id.count           
            form = Teacher_nominiform(request.POST,request.FILES)       
            mgnt_edit = Teacher_nomini.objects.get(id=pk1)
            if form.is_valid():
                mgnt_edit.fund_name=form.cleaned_data['fund_name']
                mgnt_edit.nominee_name=form.cleaned_data['nominee_name']
                mgnt_edit.other_nominee=form.cleaned_data['other_nominee']
               
                mgnt_edit.percentage=form.cleaned_data['percentage']
                mgnt_edit.nom_dt=form.cleaned_data['nom_dt']            
                mgnt_edit.save()
                messages.success(request,'Nomination Details Updated successfully')
                return redirect('teacher_nomini_create',pk=tid)          

            else:
                print form.errors
            return render(request,'teachers/nomini/teacher_nomini_detail_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


class Teacher_nomini_delete(View): 
    #@never_cache
    def get(self, request,**kwargs): 
        if request.user.is_authenticated():
            tid=self.kwargs.get('pk') 
            staff_name=request.session['staffname'] 
            data=Teacher_nomini.objects.get(id=tid)
            staff_id=request.session['staffid']
            count=Teacher_nomini.objects.filter(teacherid_id=staff_id).count()
            if count == 1 :
                data.delete()
                b=completed_table.objects.get(teacherid_id=staff_id)
                b.id=b.id
                b.teacherid_id=b.teacherid_id
                b.Teacher_financ=0
                b.save()
            else :
                data.delete() 
            
            msg= str(data.fund_name) + " Removed successfully" 
            messages.success(request, msg ) 
           
            return HttpResponseRedirect('/teachers/teacher_nomini_create/') 
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
