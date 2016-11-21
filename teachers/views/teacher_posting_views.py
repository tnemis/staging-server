from django.views.generic import View
from teachers.models import Teacher_posting_entry,Teacher_detail,completed_table,Posting_type
from schoolnew.models import User_desig,Desig_subjects,Basicinfo,School_category,District,Block
from teachers.forms import Teacher_detailform,Teacher_posting_entryform
from django.shortcuts import *
from django.contrib import messages
from django.db import *
from datetime import datetime
from django.db.models import Q
import json 
from django.utils import simplejson
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache




class school_search2(View):
    #@never_cache
    def get(self,request,**kwargs): 
        if request.is_ajax():
            q = request.GET.get('term', '')
            udise =request.GET.get('term', '')[0:2]
            dist=(request.GET.get('district',''))
            blockid=Block.objects.get(block_name=dist)
            
            if  udise.isdigit() :
                school_nam = Basicinfo.objects.filter(block_id=blockid).filter(udise_code__icontains = int(q) )    
            else :
                school_nam = Basicinfo.objects.filter(block_id=blockid).filter(school_name__icontains = q )
 
            results = []
            for drug in school_nam:
                
                drug_json = {}
                drug_json = drug.id
                drug_json= str(drug.udise_code)+"- "+str(drug.school_name)
                
                results.append(drug_json)
            data = json.dumps(results)
            mimetype = 'application/json'
        else:
            data = 'fail'
            mimetype = 'application/json'
        return HttpResponse(data,mimetype)
        

class Teacher_posting_create(View):
    #@never_cache
    def get(self,request,**kwargs):
        if request.user.is_authenticated():
            import teacher_main_views
            if request.user.account.associated_with=='state' or request.user.account.associated_with=='DIPE' or request.user.account.associated_with=='CIPE' or request.user.account.associated_with=='Zone' or request.user.account.associated_with=='IAS' or request.user.account.associated_with=='IMS' :
                AEOENTRY=0
            else:
                AEOENTRY=teacher_main_views.aeoentrycheck(request.user.account.associated_with)
            form=Teacher_posting_entryform()  

            school_id = request.user.account.associated_with
            tid=self.kwargs.get('pk')  
              
            staff_id = Teacher_detail.objects.get(id = tid)          
            dategovt=staff_id.dofsed
            if staff_id.stafs=='Teaching':
                staffid_1=1
            else:
                staffid_1=2
            
            staff_name=staff_id.name
            staff_uid=staff_id.count     
            basic_det=Basicinfo.objects.get(school_id=staff_id.school_id)
            sch_key = basic_det.id
            desig_sub= Desig_subjects.objects.all()
            if basic_det.sch_cate_id:
                chk_catid=School_category.objects.get(id=basic_det.sch_cate_id)
                if ((chk_catid.category_code=='1')|(chk_catid=='11')):          
                    posting_desg= User_desig.objects.filter(Q(user_cate='SCHOOL') & Q(user_level__isnull=True)|Q(user_level='PS'))
                elif ((chk_catid.category_code=='2')|(chk_catid.category_code=='4')|(chk_catid.category_code=='12')):
                    posting_desg= User_desig.objects.filter(Q(user_cate='SCHOOL') & Q(user_level__isnull=True)|Q(user_level='MS')|Q(user_level='HRHSMS'))
                elif ((chk_catid.category_code=='6')|(chk_catid.category_code=='7')|(chk_catid.category_code=='8')) :
                    posting_desg= User_desig.objects.filter(Q(user_cate='SCHOOL') & Q(user_level__isnull=True)|Q(user_level='HS')|Q(user_level='HRHS')|Q(user_level='HRHSMS'))
                elif ((chk_catid.category_code=='3')|(chk_catid.category_code=='5')|(chk_catid.category_code=='9')|(chk_catid.category_code=='10')):
                    posting_desg= User_desig.objects.filter(Q(user_cate='SCHOOL') & Q(user_level__isnull=True)|Q(user_level='HR')|Q(user_level='HRHS')|Q(user_level='HRHSMS'))
            else:
                posting_desg= User_desig.objects.all()

            post=Posting_type.objects.all()
            edu_list = Teacher_posting_entry.objects.filter(teacherid_id=tid)      
            if edu_list.count()==0:
                messages.success(request, 'No Data')
            return render(request,'teachers/posting/teacher_posting_detail_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    #@never_cache
    def post(self,request,**kwargs):
        if request.user.is_authenticated():
            form=Teacher_posting_entryform(request.POST,request.FILES) 
          
            tid=self.kwargs.get('pk')        
            staff_id = Teacher_detail.objects.get(id = tid)
            school_id =staff_id.school_id 
            staff_name=staff_id.name
            staff_uid=staff_id.count    
            if form.is_valid():             
                regular=Teacher_posting_entry(teacherid_id=tid,
                            designation=form.cleaned_data['designation'],
                            block=form.cleaned_data['block'],
                            school_name1=form.cleaned_data['school_name1'],
                            district=form.cleaned_data['district'],
                            type_of_posting=form.cleaned_data['type_of_posting'],
                            period_from=form.cleaned_data['period_from'],
                            period_to=form.cleaned_data['period_to'],
                            )
                regular.save()      

                b=completed_table.objects.get(school_id=school_id,teacherid_id=staff_id)
                if b.Teacher_posting=='0':
                    
                    b.id=b.id
                    b.teacherid_id=b.teacherid_id
                    b.school_id=b.school_id
                    b.Teacher_regularisation=b.Teacher_regularisation
                    b.Teacher_posting=1         
                    b.Teacher_edu=b.Teacher_edu
                    b.save()
                    
                   
                    msg = str(staff_name) + "(" + str(staff_uid)+") Posting details added successfully."
                    messages.success(request, msg ) 
                return redirect('teacher_posting_create',pk=tid)
            else:
                print form.errors  
                return render(request,'teachers/posting/teacher_posting_detail_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
 

       
class teacher_posting_update(View):
    #@never_cache
    def get(self, request,**kwargs):
        if request.user.is_authenticated():
            tid=self.kwargs.get('pk')  
            staff_id = Teacher_detail.objects.get(id = tid)     
            basic_det=Basicinfo.objects.get(school_id=staff_id.school_id)
            sch_key = basic_det.id

            desig_sub= Desig_subjects.objects.all()
            if basic_det.sch_cate_id:
                if ((basic_det.sch_cate_id==1)|(basic_det.sch_cate_id==11)):
                    posting_desg= User_desig.objects.filter((Q(user_cate='SCHOOL&OFFICE')|Q(user_cate='SCHOOL')) & Q(user_level__isnull=True)|Q(user_level='PS'))
                elif ((basic_det.sch_cate_id==2)|(basic_det.sch_cate_id==4)|(basic_det.sch_cate_id==12)):
                    posting_desg= User_desig.objects.filter((Q(user_cate='SCHOOL&OFFICE')|Q(user_cate='SCHOOL')) & Q(user_level__isnull=True)|Q(user_level='MS'))
                elif ((basic_det.sch_cate_id==6)|(basic_det.sch_cate_id==7)|(basic_det.sch_cate_id==8)) :
                    posting_desg= User_desig.objects.filter((Q(user_cate='SCHOOL&OFFICE')|Q(user_cate='SCHOOL')) & Q(user_level__isnull=True)|Q(user_level='HS')|Q(user_level='HRHS'))
                elif ((basic_det.sch_cate_id==3)|(basic_det.sch_cate_id==5)|(basic_det.sch_cate_id==9)|(basic_det.sch_cate_id==10)):
                    posting_desg= User_desig.objects.filter((Q(user_cate='SCHOOL&OFFICE')|Q(user_cate='SCHOOL')) & Q(user_level__isnull=True)|Q(user_level='HR')|Q(user_level='HRHS'))
            else:
                posting_desg= User_desig.objects.all()

            school_id = staff_id.school_id
            tid=self.kwargs.get('pk')
            pk1=self.kwargs.get('pk1')
            dategovt=staff_id.dofsed
            staffid_1=staff_id.stafs
            staff_name=staff_id.name
            staff_uid=staff_id.count
            posting_desg=User_desig.objects.all()
            dist=District.objects.all()
            block=Block.objects.all()
            post=Posting_type.objects.all()                 
            instance=Teacher_posting_entry.objects.get(id=pk1)
            form = Teacher_posting_entryform(instance=instance)
            teacherid_id = instance.teacherid_id
            designation = instance.designation
            school_name1=instance.school_name1
            district = instance.district  
            type_of_posting =instance.type_of_posting   
            period_from=instance.period_from
            period_to = instance.period_to 
            if (period_to):
                return render(request,'teachers/posting/teacher_posting_detail_form.html',locals())
            else:
                messages.success(request,'You can not update this details.')
                return redirect('teacher_posting_create',pk=tid)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    
    #@never_cache
    def post(self,request,**kwargs):
        if request.user.is_authenticated():
            school_id = request.user.account.associated_with
            tid=self.kwargs.get('pk')
            pk1=self.kwargs.get('pk1')
            staff_id = Teacher_detail.objects.get(id = tid)
            staff_name=staff_id.name
            staff_uid=staff_id.count   
            form=Teacher_posting_entryform(request.POST,request.FILES) 
            mgnt_edit = Teacher_posting_entry.objects.get(id=pk1)
            if form.is_valid():
                mgnt_edit.designation=form.cleaned_data['designation']
                mgnt_edit.school_name1=form.cleaned_data['school_name1']
                mgnt_edit.district=form.cleaned_data['district']
                mgnt_edit.block=form.cleaned_data['block']
                mgnt_edit.type_of_posting=form.cleaned_data['type_of_posting']  
                mgnt_edit.period_from=form.cleaned_data['period_from']
                mgnt_edit.period_to=form.cleaned_data['period_to']                     
                mgnt_edit.save()
                messages.success(request,'Posting Details Updated successfully')
                return redirect('teacher_posting_create',pk=tid)
            else:
                print form.errors  
                return render(request,'teachers/posting/teacher_posting_detail_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

