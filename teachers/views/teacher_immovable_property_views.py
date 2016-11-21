from django.views.generic import View
from teachers.models import Teacher_detail,completed_table,Teacher_immovalble_property
from teachers.forms import Teacher_immovalble_propertyform
from django.shortcuts import *
from schoolnew.models import Basicinfo
from django.contrib import messages
from django.db import *
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache


class Teacher_immovable_delete(View):
    #@never_cache
    def get(self, request,**kwargs):
        if request.user.is_authenticated():
            tid=self.kwargs.get('pk')
            import teacher_main_views
            if request.user.account.associated_with=='state' or request.user.account.associated_with=='DIPE' or request.user.account.associated_with=='CIPE' or request.user.account.associated_with=='Zone' or request.user.account.associated_with=='IAS' or request.user.account.associated_with=='IMS' :
                AEOENTRY=0
            else:
                AEOENTRY=teacher_main_views.aeoentrycheck(request.user.account.associated_with)
            
            staff_name=request.session['staffname']
            data=Teacher_immovalble_property.objects.get(id=tid)
            staff_id=request.session['staffid']
            basic_det=Basicinfo.objects.get(school_id=data.school_id)
                
            school_id =data.school_id       
            count=Teacher_immovalble_property.objects.filter(teacherid_id=staff_id).count()
            if count == 1 :
                data.delete()
                b=completed_table.objects.get(teacherid_id=staff_id)
                b.id=b.id
                b.teacherid_id=b.teacherid_id
                b.Teacher_immovabl=0
                b.save()
            else :
                data.delete()        
            msg= data.prop_description +  " Removed successfully"
            messages.success(request, msg )       
            return HttpResponseRedirect('/teachers/teacher_immovable_property_create/')
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))



class Teacher_immovable_property_create(View):
    #@never_cache
    def get(self,request,**kwargs):
        if request.user.is_authenticated():
            form=Teacher_immovalble_propertyform()
            tid=self.kwargs.get('pk')        
            staff_id = Teacher_detail.objects.get(id = tid)  
            basic_det=Basicinfo.objects.get(school_id=staff_id.school_id)
            school_id =staff_id.school_id               
            dategovt=staff_id.dofsed
            staff_name=staff_id.name
            staff_uid=staff_id.count    
            
            edu_list = Teacher_immovalble_property.objects.filter(teacherid_id=tid)
            if edu_list.count()==0:
                messages.success(request, 'No Data')
            return render(request,'teachers/immovable/teacher_immovable_property_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

 
    #@never_cache
    def post(self,request,**kwargs):
        if request.user.is_authenticated():
            form = Teacher_immovalble_propertyform(request.POST,request.FILES)
            tid=self.kwargs.get('pk')        
            staff_id = Teacher_detail.objects.get(id = tid)
                  
            staff_name=staff_id.name
            staff_uid=staff_id.count    

            if form.is_valid():            
                regular=Teacher_immovalble_property(teacherid_id=tid,
                        prop_description=form.cleaned_data['prop_description'],
                        purchase_value=form.cleaned_data['purchase_value'],
                        acquired_source=form.cleaned_data['acquired_source'],
                        doc_number=form.cleaned_data['doc_number'],
                        doc_date=form.cleaned_data['doc_date'],
                        place=form.cleaned_data['place'],
                        order_no=form.cleaned_data['order_no'],
                        present_value=form.cleaned_data['present_value'],
                        order_date=form.cleaned_data['order_date'],
                        )
                regular.save()   

                b=completed_table.objects.get(teacherid_id=staff_id)
                
                if b.Teacher_immovabl=='0':
                    b.id=b.id
                    b.teacherid_id=b.teacherid_id
                    b.Teacher_immovabl=16
                    b.save()

                msg = str(staff_name) + "(" + str(staff_uid)+") Immovable Property details added successfully."
                messages.success(request, msg )       
                # return HttpResponseRedirect('/teachers/teacher_immovable_property_create/')
                return redirect('teacher_immovable_property_create',pk=tid)
            else:
                print form.errors
                return render(request,'teachers/immovable/teacher_immovable_property_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class teacher_immovable_update(View):
    #@never_cache
    def get(self, request,**kwargs):
        if request.user.is_authenticated():
            # school_id = request.user.account.associated_with
            tid=self.kwargs.get('pk')
            pk1=self.kwargs.get('pk1')
            staff_id = Teacher_detail.objects.get(id = tid)    
            basic_det=Basicinfo.objects.get(school_id=staff_id.school_id)
                
            school_id =staff_id.school_id             
            dategovt=staff_id.dofsed
            staff_name=staff_id.name
            staff_uid=staff_id.count    
            instance=Teacher_immovalble_property.objects.get(id=pk1)
            form = Teacher_immovalble_propertyform(instance=instance)
            teacherid_id = instance.teacherid_id
            prop_description = instance.prop_description
            purchase_value=instance.purchase_value
            acquired_source = instance.acquired_source  
            doc_number =instance.doc_number
            doc_date = instance.doc_date
            place=instance.place
            order_no=instance.order_no
            present_value = instance.present_value  
            order_date =instance.order_date            
            return render(request,'teachers/immovable/teacher_immovable_property_form.html',locals())
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
            
            form = Teacher_immovalble_propertyform(request.POST,request.FILES)
            
            mgnt_edit = Teacher_immovalble_property.objects.get(id=pk1)
            if form.is_valid():
                mgnt_edit.prop_description=form.cleaned_data['prop_description']
                mgnt_edit.purchase_value=form.cleaned_data['purchase_value']
                mgnt_edit.acquired_source=form.cleaned_data['acquired_source']
                mgnt_edit.doc_number=form.cleaned_data['doc_number'] 
                mgnt_edit.doc_date=form.cleaned_data['doc_date']
                mgnt_edit.place=form.cleaned_data['place']
                mgnt_edit.order_no=form.cleaned_data['order_no']
                mgnt_edit.present_value=form.cleaned_data['present_value']
                mgnt_edit.order_date=form.cleaned_data['order_date']           
                mgnt_edit.save()
                messages.success(request,'Immovable Property Details Updated successfully')
                return redirect('teacher_immovable_property_create',pk=tid)
            else:
                print form.errors
                return render(request,'teachers/immovable/teacher_immovable_property_form.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


