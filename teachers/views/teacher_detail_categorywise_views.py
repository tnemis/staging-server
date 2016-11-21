from django.views.generic import View
from teachers.models import Teacher_detail,scale_register_abstract,private_teachers_detail
from schoolnew.models import Basicinfo,Staff,User_desig,Desig_subjects
from django.db.models import Count, Sum
from django.shortcuts import render
from baseapp.models import  School
from django.contrib import messages
from django.db import connection
from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache

class teacher_detailListView(View):
    #@never_cache
    def get(self,request,**kwargs):
        if request.user.is_authenticated():
            try:
                udise_code= request.user.username
                cat_id = self.kwargs.get('cat_id')
                school_code=cat_id

                offcat_id_list=[2,3,4,5,6,7,8,9,10,11]
                management_cate_id_list=[1,2]
                management_id_list=[1,2,3]
                sch_cate_id_list=[8,9,10,11,12,13]
                ss=request.user.username
                if cat_id:
                    basic_det=Basicinfo.objects.get(school_id=cat_id)
                else:
                    if request.user.account.user_category_id >= 18:
                        basic_det=Basicinfo.objects.get(office_code=request.user.username)
                        office_chk = 'Yes'
                    else:
                        office_chk = 'No'
                        basic_det=Basicinfo.objects.get(udise_code=request.user.username)

                pups_pums=0
                off_cat=0
                sch_mgnt=0
                private_mgnt=0
                AEOENTRY=0
                check1=0
                check2=0
                check3=0
                check4=0
         
                school_entry=1
                if request.user.account.user_category_id == 2:
                    teachers_name_list_new = Teacher_detail.objects.filter(school__school_code=school_code, school__block_id= request.user.account.associated_with)
                elif request.user.account.user_category_id == 5:
                    teachers_name_list_new = Teacher_detail.objects.filter(school__school_code=school_code, school__block_id= request.user.account.associated_with)
                elif request.user.account.user_category_id == 6 or request.user.account.user_category_id == 7 or request.user.account.user_category_id == 8 or request.user.account.user_category_id == 12 or request.user.account.user_category_id == 13 or request.user.account.user_category_id == 14:
                    teachers_name_list_new = Teacher_detail.objects.filter(school__school_code=school_code, school__district_id= request.user.account.associated_with)
                elif request.user.account.user_category_id == 9 or request.user.account.user_category_id == 10 or request.user.account.user_category_id == 11 or request.user.account.user_category_id == 15 or request.user.account.user_category_id == 16 or request.user.account.user_category_id == 17 or request.user.account.user_category_id == 4:
                    teachers_name_list_new = Teacher_detail.objects.filter(school__school_code=school_code)    
                elif request.user.account.user_category_id > 18:
                    teachers_name_list_new = Teacher_detail.objects.filter(school_id=basic_det.school_id)
                else:
                    rec = Teacher_detail.objects.filter(school_id=request.user.account.associated_with).filter(transfer_flag='No').filter(ofs_flag=False)
                    school_code = request.user.account.associated_with               
                    # school_data = School.objects.get(id=school_code)               
                    sch_key = basic_det.id             
                    if (basic_det.offcat_id):
                        off_cat=int(basic_det.offcat_id)
                    if basic_det.manage_cate_id:
                        private_mgnt=int(basic_det.manage_cate_id)
                    if private_mgnt==3:
                        school_id = request.user.account.associated_with 
                        teachers_name_list_new= private_teachers_detail.objects.filter(school_name=school_id)
                        return render(request,'teachers/private/teacher_list.html',locals())

                    if basic_det.sch_management_id:
                        sch_mgnt=int(basic_det.sch_management_id)
                    if basic_det.sch_cate_id:
                        pups_pums=int(basic_det.sch_cate_id)
                  
                    if off_cat not in offcat_id_list:
                        check1=1

                    if check1==1:
                        if private_mgnt==1:
                            for item in management_id_list:
                                if item==sch_mgnt:
                                    check3=1
                            if check3==1:
                                if pups_pums in sch_cate_id_list:
                                    AEOENTRY=1
                        elif private_mgnt==2:
                            if pups_pums in sch_cate_id_list:
                                    AEOENTRY=1
                        if request.user.is_authenticated():
                            sch_key = basic_det.id
                            teaching_rec = Staff.objects.filter(school_key=sch_key)
                            
                            if teaching_rec.count()==0:
                                messages.warning(request,"FIRST MAKE SCHOOL PROFILE " )
                                return HttpResponseRedirect('/') 
                            rec1 = Staff.objects.filter(school_key=sch_key)
                            
                            filled_check = Teacher_detail.objects.filter(school_id=basic_det.school_id).filter(transfer_flag='No').filter(ofs_flag=False)    
                            teaching_sanc=0
                            teaching_filled=0
                            teaching_vac=0
                            nteaching_sanc=0
                            nteaching_filled=0
                            nteaching_vac=0
                            for i in teaching_rec:
                                if i.staff_cat == 1:
                                    if i.post_sanc:
                                        teaching_sanc=teaching_sanc+i.post_sanc
                                    if i.post_filled:
                                        teaching_filled=teaching_filled+int(i.post_filled)
                                    if i.post_vac:
                                        teaching_vac=teaching_vac +i.post_vac
                                elif  i.staff_cat == 2:         
                                    if i.post_sanc:
                                        nteaching_sanc=nteaching_sanc+i.post_sanc
                                    if i.post_filled:
                                        nteaching_filled=nteaching_filled+int(i.post_filled)
                                    if i.post_vac:
                                        nteaching_vac=nteaching_vac+int(i.post_vac)  
                if cat_id:
                    AEOENTRY=0                   
                    return render(request,'teachers/teachers_post_list.html',locals())
                return render(request,'teachers/teachers_post_list.html',locals())
       
            except Basicinfo.DoesNotExist:
                school_entry=0
                messages.info(request," First make School Entry " )
       
                return HttpResponseRedirect('/')
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path)) 


class Teacher_detailList(View):
    #@never_cache
    def get(self,request,**kwargs):
        if request.user.is_authenticated():
            cat_id = self.kwargs.get('cat_id')
            school_code=cat_id
            AEOENTRY=0
            office_enter=scale_register_abstract.objects.filter(udise_code=cat_id)
            flag=0
            for i in office_enter:
                print i.office_entry
                flag=i.office_entry

            if request.user.account.user_category_id==2 or request.user.account.user_category_id==3 or request.user.account.user_category_id==18:
                if flag==0:
                    basic_det=Basicinfo.objects.get(school_id=cat_id)
                elif flag==1:
                    basic_det=Basicinfo.objects.get(udise_code=cat_id)            
                
                teaching_staff_records=Teachingstaff.objects.filter(school_key=basic_det.id).values('tpost_name').annotate(dcount=Sum('tpost_sanc'))
                non_teaching_staff_records=NonTeachingstaff.objects.filter(school_key=basic_det.id).values('ntpost_name').annotate(dcount1=Sum('ntpost_sanc'))
                filled_check = Teacher_detail.objects.filter(school_id=basic_det.school_id).filter(transfer_flag='No').filter(ofs_flag=False)
                scale_register_abstract.objects.filter(udise_code=basic_det.udise_code).delete()
                teaching_count=0

                for i in teaching_staff_records:
                    desig=User_desig.objects.get(id=i.get('tpost_name'))                
                    subjectwise_records=Teachingstaff.objects.filter(school_key=basic_det.id).filter(tpost_name=i.get('tpost_name')).values('tpost_sub').annotate(dcount1=Sum('tpost_sanc'))
                    teaching_count=teaching_count+ i.get('dcount') 
                    
                    for q in subjectwise_records:
                        sub=Desig_subjects.objects.get(id=q.get('tpost_sub'))
                        records=scale_register_abstract(
                        udise_code=basic_det.udise_code,
                        management=str(basic_det.manage_cate),
                        stafs_category='Teaching',
                        designation=desig.user_desig,
                        subject=sub.desig_sub_name,
                        sanctioned_post=q.get('dcount1')
                        )
                        records.save()

                        for chk in filled_check:
                            if str(chk.designation)==str(desig.user_desig) and str(chk.subject)==str(sub.desig_sub_name):
                                records.filled_post = records.filled_post +1
                                records.vaccant_post=records.sanctioned_post - records.filled_post
                                if records.vaccant_post<0:
                                    records.vaccant_post=0
                                records.save()
                
                rec=scale_register_abstract.objects.filter(udise_code=basic_det.udise_code).filter(stafs_category='Teaching').order_by('designation')
                rec_filled=scale_register_abstract.objects.filter(udise_code=basic_det.udise_code).filter(stafs_category='Teaching').values('stafs_category').annotate(dcount1=Sum('filled_post'))
                if rec_filled.count()==0:
                    a=0
                else:
                    a=rec_filled[0].get('dcount1',None)   
                nteaching_count=0
                
                for i in non_teaching_staff_records:
                    desig=User_desig.objects.get(id=i.get('ntpost_name'))                
                    nteaching_count= nteaching_count + int(i.get('dcount1'))
                    records=scale_register_abstract(
                    udise_code=basic_det.udise_code,
                    management=str(basic_det.manage_cate),
                    stafs_category='Non Teaching',
                    designation=desig.user_desig,
                    subject='Not Applicable',
                    sanctioned_post=i.get('dcount1'), 
                    )
                    records.save()
                    for chk in filled_check:
                        if str(chk.designation)==str(desig.user_desig):
                            records.filled_post = records.filled_post +1
                            records.vaccant_post=records.sanctioned_post - records.filled_post
                            if records.vaccant_post<0:
                                records.vaccant_post=0
                            records.save()
               
                rec1=scale_register_abstract.objects.filter(udise_code=basic_det.udise_code).filter(stafs_category='Non Teaching').order_by('designation')
                rec_filled1=scale_register_abstract.objects.filter(udise_code=basic_det.udise_code).filter(stafs_category='Non Teaching').values('stafs_category').annotate(dcount1=Sum('filled_post'))
                if rec_filled1.count()==0:
                    b=0
                else:
                    b=rec_filled1[0].get('dcount1',None)     
                return render(request,'teachers/teachers_post_list.html',locals())

            elif request.user.account.user_category_id == 5:
                teachers_name_list_new = Teacher_detail.objects.filter(school__school_code=school_code, school__block_id= request.user.account.associated_with)
            elif request.user.account.user_category_id == 6 or request.user.account.user_category_id == 7 or request.user.account.user_category_id == 8 or request.user.account.user_category_id == 12 or request.user.account.user_category_id == 13 or request.user.account.user_category_id == 14:
                teachers_name_list_new = Teacher_detail.objects.filter(school__school_code=school_code, school__district_id= request.user.account.associated_with)
            elif request.user.account.user_category_id == 9 or request.user.account.user_category_id == 10 or request.user.account.user_category_id == 11 or request.user.account.user_category_id == 15 or request.user.account.user_category_id == 16 or request.user.account.user_category_id == 17 or request.user.account.user_category_id == 4:
                teachers_name_list_new = Teacher_detail.objects.filter(school__school_code=school_code)    
            
            return render(request,'teachers/teachers_post_list.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class teacher_detailListView1(View):
    #@never_cache
    def get(self,request,**kwargs):
        if request.user.is_authenticated():
            try:
                cat_id = self.kwargs.get('cat_id')
                school_code=cat_id
                rec = Teacher_detail.objects.filter(school_id=school_code).filter(transfer_flag='No').filter(ofs_flag=False)
                sch_id_chk = School.objects.get(id=school_code)
                a=Basicinfo.objects.all()
                for i in a:
                    print i.school_id
                    print school_code
                basic_det=Basicinfo.objects.get(school_id=school_code)
                
                if (Basicinfo.objects.filter(school_id=school_code).count())>0:
                    basic_det=Basicinfo.objects.get(udise_code=sch_id_chk.school_code)
                    sch_key = basic_det.id
                    print basic_det.sch_management.id
                    teaching_staff_records=Teachingstaff.objects.filter(school_key=sch_key).values('tpost_name').annotate(dcount=Sum('tpost_sanc'))
                    non_teaching_staff_records=NonTeachingstaff.objects.filter(school_key=sch_key).values('ntpost_name').annotate(dcount1=Sum('ntpost_sanc'))
                    filled_check = Teacher_detail.objects.filter(school_id=request.user.account.associated_with).filter(transfer_flag='No').filter(ofs_flag=False)
                    scale_register_abstract.objects.filter(udise_code=basic_det.udise_code).delete()
                    teaching_count=0
                    for i in teaching_staff_records:
                        desig=User_desig.objects.get(id=i.get('tpost_name'))
                        subjectwise_records=Teachingstaff.objects.filter(school_key=basic_det.id).filter(tpost_name=i.get('tpost_name')).values('tpost_sub').annotate(dcount1=Sum('tpost_sanc'))
                        teaching_count=teaching_count+ i.get('dcount') 
                        
                        for q in subjectwise_records:
                            sub=Desig_subjects.objects.get(id=q.get('tpost_sub'))
                            records=scale_register_abstract(
                            udise_code=basic_det.udise_code,
                            management=str(basic_det.manage_cate),
                            stafs_category='Teaching',
                            designation=desig.user_desig,
                            subject=sub.desig_sub_name,
                            sanctioned_post=q.get('dcount1')
                            )
                            records.save()
                            for chk in filled_check:
                        
                                if str(chk.designation)==str(desig.user_desig) and str(chk.subject)==str(sub.desig_sub_name):

                                    records.filled_post = records.filled_post +1
                                    records.vaccant_post=records.sanctioned_post - records.filled_post
                                    if records.vaccant_post<0:
                                            records.vaccant_post=0
                                    records.save()
                    
                    rec=scale_register_abstract.objects.filter(udise_code=basic_det.udise_code,stafs_category='Teaching').order_by('designation')
                    rec_filled=scale_register_abstract.objects.filter(udise_code=basic_det.udise_code,stafs_category='Teaching').values('stafs_category').annotate(dcount1=Sum('filled_post'))
                    if rec_filled.count()==0:
                        a=0
                    else:
                        a=rec_filled[0].get('dcount1',None)   
                        
                    nteaching_count=0
                    
                    for i in non_teaching_staff_records:
                        desig=User_desig.objects.get(id=i.get('ntpost_name'))                 
                        nteaching_count= nteaching_count + int(i.get('dcount1'))
                    
                        records=scale_register_abstract(
                        udise_code=basic_det.udise_code,
                        management=str(basic_det.manage_cate),
                        stafs_category='Non Teaching',
                        designation=desig.user_desig,
                        subject='Not Applicable',
                        sanctioned_post=i.get('dcount1'), 
                        )
                        records.save()
                        for chk in filled_check:
                            if str(chk.designation)==str(desig.user_desig):
                                records.filled_post = records.filled_post +1
                                records.vaccant_post=records.sanctioned_post - records.filled_post
                                if records.vaccant_post<0:
                                            records.vaccant_post=0
                                records.save()
                   
                    rec1=scale_register_abstract.objects.filter(udise_code=basic_det.udise_code).filter(stafs_category='Non Teaching').order_by('designation')
                    rec_filled1=scale_register_abstract.objects.filter(udise_code=basic_det.udise_code).filter(stafs_category='Non Teaching').values('stafs_category').annotate(dcount1=Sum('filled_post'))
                    if rec_filled1.count()==0:
                        b=0
                    else:
                        b=rec_filled1[0].get('dcount1',None)     
                            
                return render(request,'teachers/teachers_post_list.html',locals())
            except Basicinfo.DoesNotExist:
                messages.info(request," First make entries in Schools Basic Information" )
                return render(request,'teachers/teachers_post_list.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class staff_detailListView(View):
    #@never_cache
    def get(self,request,**kwargs):
        if request.user.is_authenticated():
            try:
                AEOENTRY=0
                abstract_page = 0
                school_code = request.user.account.associated_with
                if request.user.is_authenticated():
                        basic_det=Basicinfo.objects.get(office_code=request.user.username)
                        sch_key = basic_det.id
                        nonteaching_rec = Staff.objects.filter(school_key=sch_key).filter(staff_cat=2)
                        nteaching_sanc=0
                        nteaching_filled=0
                        nteaching_vac=0
                       
                        for i in nonteaching_rec:
                            if i.post_sanc:
                                nteaching_sanc=nteaching_sanc+i.post_sanc
                            if i.post_filled:
                                nteaching_filled=nteaching_filled+int(i.post_filled)
                            if i.post_vac:
                                nteaching_vac=nteaching_vac+int(i.post_vac)
                return render(request,'teachers/staffs_post_list.html',locals())
                 
            except Basicinfo.DoesNotExist:
                messages.info(request," First make entries in Office Basic Information" )
                
                return render(request,'teachers/staffs_post_list.html',locals())
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

