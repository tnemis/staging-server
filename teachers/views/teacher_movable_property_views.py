from django.views.generic import View
from teachers.models import Teacher_detail,completed_table,Teacher_movable_property
from teachers.forms import Teacher_movable_propertyform
from django.shortcuts import *
from django.contrib import messages
from schoolnew.models import Basicinfo
from django.db import *
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache


class Teacher_movable_property_create(View):
    #@never_cache
    def get(self,request,**kwargs):
        if request.user.is_authenticated():
            import teacher_main_views
            if request.user.account.associated_with=='state' or request.user.account.associated_with=='DIPE' or request.user.account.associated_with=='CIPE' or request.user.account.associated_with=='Zone' or request.user.account.associated_with=='IAS' or request.user.account.associated_with=='IMS' :
                AEOENTRY=0
            else:
                AEOENTRY=teacher_main_views.aeoentrycheck(request.user.account.associated_with)
            form=Teacher_movable_propertyform()
            tid=self.kwargs.get('pk')        
            staff_id = Teacher_detail.objects.get(id = tid)          
            basic_det=Basicinfo.objects.get(school_id=staff_id.school_id)
            school_id =staff_id.school_id            
            dategovt=staff_id.dofsed    
            staff_name=staff_id.name
            staff_uid=staff_id.count   
            edu_list = Teacher_movable_property.objects.filter(teacherid_id=tid)
            if edu_list.count()==0:
                messages.success(request, 'No Data')
            return render(request,'teachers/movable/teacher_movable_property_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    #@never_cache
    def post(self,request,**kwargs):
        if request.user.is_authenticated():
            form = Teacher_movable_propertyform(request.POST,request.FILES)        
            school_id = request.user.account.associated_with
            tid=self.kwargs.get('pk')        
            staff_id = Teacher_detail.objects.get(id = tid)
            staff_name=staff_id.name
            staff_uid=staff_id.count     
            if form.is_valid():      
                regular=Teacher_movable_property(teacherid_id=tid,
                        prop_description=form.cleaned_data['prop_description'],
                        purchase_value=form.cleaned_data['purchase_value'],
                        source=form.cleaned_data['source'],                      
                        purchase_doc_date=form.cleaned_data['purchase_doc_date'],                  
                        present_value=form.cleaned_data['present_value'],                   
                        order_date=form.cleaned_data['order_date']
                        )
                regular.save()  
               
                b=completed_table.objects.get(teacherid_id=staff_id)
            
                if b.Teacher_movabl=='0':
                    b.id=b.id
                    b.teacherid_id=b.teacherid_id
                    b.Teacher_movabl=15
                    b.save()
                msg = str(staff_name) + "(" + str(staff_uid)+") Movable Property details added successfully."
                messages.success(request, msg )      
                return redirect('teacher_movable_property_create',pk=tid) 
            else:
                print form.errors
                return render(request,'teachers/movable/teacher_movable_property_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class teacher_movable_update(View):
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
            instance=Teacher_movable_property.objects.get(id=pk1)
           
            form = Teacher_movable_propertyform(instance=instance)
            teacherid_id = instance.teacherid_id
            prop_description = instance.prop_description
            purchase_value=instance.purchase_value       
            source = instance.source         
            purchase_doc_date = instance.purchase_doc_date      
            present_value = instance.present_value  
            order_date =instance.order_date
            return render(request,'teachers/movable/teacher_movable_property_form.html',locals())
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
            instance=Teacher_movable_property.objects.get(id=pk1)
            form = Teacher_movable_propertyform(request.POST,request.FILES)
         
            mgnt_edit = Teacher_movable_property.objects.get(id=pk1)
            if form.is_valid():
                mgnt_edit.prop_description=form.cleaned_data['prop_description']
                mgnt_edit.purchase_value=form.cleaned_data['purchase_value']
                mgnt_edit.source=form.cleaned_data['source']
                mgnt_edit.order_date=form.cleaned_data['order_date']
                mgnt_edit.purchase_doc_date=form.cleaned_data['purchase_doc_date']            
                mgnt_edit.present_value=form.cleaned_data['present_value']                 
                mgnt_edit.save()
                messages.success(request,'Movable Property Details Updated successfully')
                return redirect('teacher_movable_property_create',pk=tid) 
            else:
                print form.errors
                return render(request,'teachers/movable/teacher_movable_property_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
