from django.views.generic import View
from teachers.models import Teacher_detail,completed_table,Teacher_family_detail,family_relationship,Teacher_nomini
from baseapp.models import District,School,Block
from schoolnew.models import Basicinfo
from teachers.forms import Teacher_family_detailform,Teacher_detailform
from django.shortcuts import *
from django.contrib import messages
from django.db import *
from datetime import datetime
from schoolnew.models import User_desig,Desig_subjects,Basicinfo
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache


class Teacher_family_create(View):
  #@never_cache
  def get(self,request,**kwargs):
    if request.user.is_authenticated():
      form=Teacher_family_detailform()
      import teacher_main_views
      if request.user.account.associated_with=='state' or request.user.account.associated_with=='DIPE' or request.user.account.associated_with=='CIPE' or request.user.account.associated_with=='Zone' or request.user.account.associated_with=='IAS' or request.user.account.associated_with=='IMS' :
              AEOENTRY=0
      else:
          AEOENTRY=teacher_main_views.aeoentrycheck(request.user.account.associated_with)
     
      relation1=family_relationship.objects.all()
      district_list = District.objects.all().order_by('district_name')
      tid=self.kwargs.get('pk')        
      staff_id = Teacher_detail.objects.get(id = tid)  
      basic_det=Basicinfo.objects.get(school_id=staff_id.school_id)
              
      school_id =staff_id.school_id    
      staff_name=staff_id.name
      staff_uid=staff_id.count     
      edu_list = Teacher_family_detail.objects.filter(teacherid_id=tid) 
     
      if edu_list.count()==0: 
         messages.success(request, 'No Data') 
      return render(request,'teachers/family/teacher_family_detail_form.html',locals())
    else:
      return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


  #@never_cache
  def post(self,request,**kwargs):
    if request.user.is_authenticated():
      form=Teacher_family_detailform(request.POST,request.FILES)
      tid=self.kwargs.get('pk')        
      staff_id = Teacher_detail.objects.get(id = tid)
      staff_name=staff_id.name
      staff_uid=staff_id.count    

      relation1=family_relationship.objects.all()
      if form.is_valid():            
        regular=Teacher_family_detail(teacherid_id=tid,
                    name=form.cleaned_data['name'],
                    dob=form.cleaned_data['dob'],
                    age=form.cleaned_data['age'],
                    relation=form.cleaned_data['relation'],
                    aadhaar_number = form.cleaned_data['aadhaar_number'], 
                    district = form.cleaned_data['district'],
                    block = form.cleaned_data['block'],
                    spou_gov=form.cleaned_data['spou_gov'],
                    local_body_type= form.cleaned_data['local_body_type'],
                    village_panchayat =form.cleaned_data['village_panchayat'],
                    vill_habitation = form.cleaned_data['vill_habitation'],
                    town_panchayat = form.cleaned_data['town_panchayat'],
                    town_panchayat_ward = form.cleaned_data['town_panchayat_ward'],
                    municipality = form.cleaned_data['municipality'],
                    municipal_ward = form.cleaned_data['municipal_ward'],
                    contonment = form.cleaned_data['contonment'],
                    contonment_ward = form.cleaned_data['contonment_ward'],
                    township = form.cleaned_data['township'],
                    township_ward = form.cleaned_data['township_ward'],
                    corporation = form.cleaned_data['corporation'],
                    corpn_zone = form.cleaned_data['corpn_zone'],
                    corpn_ward = form.cleaned_data['corpn_ward'],
                    )
        regular.save()
        b=completed_table.objects.get(teacherid_id=tid)       
        if b.Teacher_familyrel=='0':
          b.id=b.id
          b.teacherid_id=b.teacherid_id
          b.Teacher_familyrel=13
          b.save()
      
        msg = str(staff_name) + "(" + str(staff_uid)+") Family details added successfully." 
        messages.success(request, msg) 
        
        return redirect('teacher_family_create',pk=tid)
      else:
         print form.errors
         return render(request,'teachers/family/teacher_family_detail_form.html',locals())
    else:
      return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
 

class teacher_family_update(View):
  #@never_cache
  def get(self, request,**kwargs):
    if request.user.is_authenticated():
      tid=self.kwargs.get('pk')
      pk1=self.kwargs.get('pk1')
      staff_id = Teacher_detail.objects.get(id = tid)          
      basic_det=Basicinfo.objects.get(school_id=staff_id.school_id)
          
      school_id =staff_id.school_id
      staff_uid=staff_id.count     
      staff_name=staff_id.name

      instance=Teacher_family_detail.objects.get(id=pk1)
      
      relation1=family_relationship.objects.all()
      form = Teacher_family_detailform(instance=instance)
      teacherid_id = instance.teacherid_id
      name = instance.name
      dob=instance.dob
      age = instance.age 
      aadhaar_number= instance.aadhaar_number
      spou_gov=instance.spou_gov
      district= instance.district
      block= instance.block
      local_body_type= instance.local_body_type
      village_panchayat= instance.village_panchayat
      vill_habitation= instance.vill_habitation
      town_panchayat= instance.town_panchayat
      town_panchayat_ward= instance.town_panchayat_ward
      municipality= instance.municipality
      municipal_ward= instance.municipal_ward
      contonment= instance.contonment
      contonment_ward= instance.contonment_ward
      township= instance.township
      township_ward= instance.township_ward
      corporation= instance.corporation
      corpn_zone= instance.corpn_zone
      corpn_ward= instance.corpn_ward
      relation = instance.relation  
      return render(request,'teachers/family/teacher_family_detail_form.html',locals())
    else:
      return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

  #@never_cache
  def post(self,request,**kwargs):
    if request.user.is_authenticated():
      tid=self.kwargs.get('pk')
      pk1=self.kwargs.get('pk1')
      staff_id = Teacher_detail.objects.get(id = tid)
      staff_name=staff_id.name
      staff_uid=staff_id.count   
          
      instance=Teacher_family_detail.objects.get(id=pk1)
      relation1=family_relationship.objects.all()
      form = Teacher_family_detailform(request.POST,request.FILES)
      mgnt_edit = Teacher_family_detail.objects.get(id=pk1)
      if form.is_valid():
          mgnt_edit.name=form.cleaned_data['name']
          mgnt_edit.dob=form.cleaned_data['dob']
          mgnt_edit.age=form.cleaned_data['age']
          mgnt_edit.relation=form.cleaned_data['relation']
          mgnt_edit.spou_gov=form.cleaned_data['spou_gov']

          mgnt_edit.aadhaar_number=form.cleaned_data['aadhaar_number']
          if mgnt_edit.spou_gov=='Yes':
            mgnt_edit.district=form.cleaned_data['district']
            mgnt_edit.block=form.cleaned_data['block']
            mgnt_edit.local_body_type=form.cleaned_data['local_body_type']
            mgnt_edit.village_panchayat=form.cleaned_data['village_panchayat']
            mgnt_edit.vill_habitation=form.cleaned_data['vill_habitation']
            mgnt_edit.town_panchayat=form.cleaned_data['town_panchayat']
            mgnt_edit.town_panchayat_ward=form.cleaned_data['town_panchayat_ward']
            mgnt_edit.municipality=form.cleaned_data['municipality']
            mgnt_edit.municipal_ward=form.cleaned_data['municipal_ward']
            mgnt_edit.contonment=form.cleaned_data['contonment']
            mgnt_edit.contonment_ward=form.cleaned_data['contonment_ward']
            mgnt_edit.township=form.cleaned_data['township']
            mgnt_edit.township_ward=form.cleaned_data['township_ward']
            mgnt_edit.corporation=form.cleaned_data['corporation']
            mgnt_edit.corpn_zone=form.cleaned_data['corpn_zone']
            mgnt_edit.corpn_ward=form.cleaned_data['corpn_ward']
          else:
            mgnt_edit.district=None
            mgnt_edit.block=None
            mgnt_edit.local_body_type=None
            mgnt_edit.village_panchayat=None
            mgnt_edit.vill_habitation=None
            mgnt_edit.town_panchayat=None
            mgnt_edit.town_panchayat_ward=None
            mgnt_edit.municipality=None
            mgnt_edit.municipal_ward=None
            mgnt_edit.contonment=None
            mgnt_edit.contonment_ward=None
            mgnt_edit.township=None
            mgnt_edit.township_ward=None
            mgnt_edit.corporation=None
            mgnt_edit.corpn_zone=None
            mgnt_edit.corpn_ward=None
          mgnt_edit.save()
          messages.success(request,'Family details Details Updated successfully')
          return redirect('teacher_family_create',pk=tid)
      else:
          print form.errors
          return render(request,'teachers/family/teacher_family_detail_form.html',locals())
    else:
      return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
  
class teacher_family_delete(View):
  #@never_cache
  def get(self, request,**kwargs):
    if request.user.is_authenticated():
      tid=self.kwargs.get('pk')
      pk1=self.kwargs.get('pk1')
      staff_id = Teacher_detail.objects.get(id = tid)
      import teacher_main_views
      AEOENTRY=teacher_main_views.aeoentrycheck(request.user.account.associated_with)   
      basic_det=Basicinfo.objects.get(school_id=staff_id.school_id)
          
      school_id =staff_id.school_id
      flag=0
      staff_name=request.session['staffname']
      data=Teacher_family_detail.objects.get(id=pk1)
      instance=Teacher_nomini.objects.filter(teacherid_id=tid)  
      for entry in instance:
        if data.id==entry.nominee_name_id:
          flag=1
      if flag==1:
          messages.warning(request, 'Relation Reffered in Nomination. First Update Financial Nomination' )       

          return redirect('teacher_nomini_create',pk=tid)
      else:
        staff_id=request.session['staffid']
        count=Teacher_family_detail.objects.filter(teacherid_id=staff_id).count()
        if count == 1 :
            data.delete()
            b=completed_table.objects.get(teacherid_id=staff_id)
            b.id=b.id
            b.teacherid_id=b.teacherid_id
            b.Teacher_immovabl=0
            b.save()
        else :
            data.delete()        
        msg=   " Data Removed successfully"
        messages.success(request, msg )       
        return redirect('teacher_family_create',pk=tid)
    else:
      return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        

