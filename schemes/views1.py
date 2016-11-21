from django.views.generic import View,ListView, DetailView, CreateView, \
    DeleteView, UpdateView, \
    ArchiveIndexView, DateDetailView, \
    DayArchiveView, MonthArchiveView, \
    TodayArchiveView, WeekArchiveView, \
    YearArchiveView
from django.contrib import messages
from baseapp.forms import Pool_databaseform
from schemes.forms import Student_schemesform
from django.shortcuts import render
from schemes.models import Student_schemes
from students.models import School_child_count, Child_detail
from django.db.models import Q
from baseapp.models import State, District, School, Habitation, Zone, Schemes, Class_Studying, Differently_abled, Disadvantaged_group, Child_detail_pool_database, Language, Group_code, Bank, Education_medium, Nationality, Religion, Community
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger
from datetime import datetime
from django import template
from django.contrib import messages
from excel_response import ExcelResponse






class Student_schemesView(View): 
    def get(self,request,**kwargs):
        form=Student_schemesform()
        class_id = self.kwargs.get('cl_id')
        school_code = self.kwargs.get('school_code')
        school_id = request.user.account.associated_with
        schl_id = School.objects.get(id=school_id)
        classwise_detail = Child_detail.objects.filter(school=schl_id,class_studying_id=class_id).order_by('name')
        student_schemes_list=Student_schemes.objects.filter(school=schl_id,cls=class_id)
        if class_id == '1':
            return render(request,'schemes/class/1.html',locals())
        elif class_id == '2':
            return render(request,'schemes/class/2.html',locals())
        elif class_id == '3':
            return render(request,'schemes/class/3.html',locals())
        elif class_id == '4':
            return render(request,'schemes/class/4.html',locals())
        elif class_id == '5':
            return render(request,'schemes/class/5.html',locals())
        elif class_id == '6':
            return render(request,'schemes/class/6.html',locals())
        elif class_id == '7':
            return render(request,'schemes/class/7.html',locals())
        elif class_id == '8':
            return render(request,'schemes/class/8.html',locals())
        elif class_id == '9':
            return render(request,'schemes/class/9.html',locals())
        elif class_id == '10':
            return render(request,'schemes/class/10.html',locals())
        elif class_id == '11':
            return render(request,'schemes/class/11.html',locals())
        else:
            return render(request,'schemes/class/12.html',locals())


    def post(self,request,**kwargs):
        class_id = self.kwargs.get('cl_id')
        school_code = self.kwargs.get('school_code')
        school_id = request.user.account.associated_with
        schl_id = School.objects.get(id=school_id)
        classwise_detail = Child_detail.objects.filter(school=schl_id,class_studying_id=class_id).order_by('name')
        student_schemes_list=Student_schemes.objects.filter(school=schl_id,cls=class_id)

        for i in range(len(classwise_detail)):
            school_key=request.POST.get('school_'+str(i+1))
            child_key=request.POST.get('child_'+str(i+1))
            scheme_detail = Student_schemes(
                school=School.objects.get(id=school_key),
                academic_year=request.POST.get('academic_year_'+str(i+1)),
                student=Child_detail.objects.get(id=child_key),
                cls=request.POST.get('cls_'+str(i+1)),
                uniform_1=request.POST.get('uniform_1_'+str(i+1)),
                uniform_2=request.POST.get('uniform_2_'+str(i+1)),
                uniform_3=request.POST.get('uniform_3_'+str(i+1)),
                uniform_4=request.POST.get('uniform_4_'+str(i+1)),
                textbook=request.POST.get('textbook_'+str(i+1)),
                textbook_1=request.POST.get('textbook_1_'+str(i+1)),
                textbook_2=request.POST.get('textbook_2_'+str(i+1)),
                textbook_3=request.POST.get('textbook_3_'+str(i+1)),
                notebook=request.POST.get('notebook_'+str(i+1)),
                notebook_1=request.POST.get('notebook_1_'+str(i+1)),
                notebook_2=request.POST.get('notebook_2_'+str(i+1)),
                notebook_3=request.POST.get('notebook_3_'+str(i+1)),
                bag=request.POST.get('bag_'+str(i+1)),
                footware=request.POST.get('footware_'+str(i+1)),
                sweater=request.POST.get('sweater_'+str(i+1)),
                crayon=request.POST.get('crayon_'+str(i+1)),
                colorpencil=request.POST.get('colorpencil_'+str(i+1)),
                geometrybox=request.POST.get('geometrybox_'+str(i+1)),
                atlas=request.POST.get('atlas_'+str(i+1)),
                cycle=request.POST.get('cycle_'+str(i+1)),
                laptop=request.POST.get('laptop_'+str(i+1)),
                bw=request.POST.get('bw_'+str(i+1)),
                sci=request.POST.get('sci_'+str(i+1)),
                laptop_no=request.POST.get('laptop_no_'+str(i+1)),
                laptop_date=request.POST.get('laptop_date_'+str(i+1)),)
            scheme_detail.save()

        return HttpResponseRedirect('/schemes/student_schemes')





class Schemes_class_wise_count(View):

    def get(self,request,**kwargs):
        try:
            school_code = self.request.GET.get('school_code')
            if request.user.account.user_category_id == 2:
                child_detail_list = School_child_count.objects.get(school__school_code=school_code, school__block_id= request.user.account.associated_with)
            elif request.user.account.user_category_id == 5:
                child_detail_list = School_child_count.objects.get(school__school_code=school_code, school__block_id= request.user.account.associated_with)
            elif request.user.account.user_category_id == 6 or request.user.account.user_category_id == 7 or request.user.account.user_category_id == 8 or request.user.account.user_category_id == 12 or request.user.account.user_category_id == 13 or request.user.account.user_category_id == 14:
                child_detail_list = School_child_count.objects.get(school__school_code=school_code, school__district_id= request.user.account.associated_with)
            elif request.user.account.user_category_id == 9 or request.user.account.user_category_id == 10 or request.user.account.user_category_id == 11 or request.user.account.user_category_id == 15 or request.user.account.user_category_id == 16 or request.user.account.user_category_id == 17 or request.user.account.user_category_id == 4:
                child_detail_list = School_child_count.objects.get(school__school_code=school_code)    
            else:
                child_detail_list = School_child_count.objects.get(school_id=request.user.account.associated_with)

            totalcount = child_detail_list.total_count
            I = child_detail_list.one
            II = child_detail_list.two
            III = child_detail_list.three
            IV = child_detail_list.four
            V = child_detail_list.five
            VI = child_detail_list.six
            VII = child_detail_list.seven
            VIII = child_detail_list.eight
            IX = child_detail_list.nine
            X = child_detail_list.ten
            XI = child_detail_list.eleven
            XII = child_detail_list.twelve
            return render(request,'schemes/schemes_class_wise_count_table.html',{'child_detail_list':child_detail_list,'totalcount':totalcount,'I':I,'II':II,'III':III,'IV':IV,'V':V,'VI':VI,'VII':VII,'VIII':VIII,'IX':IX,'X':X,'XI':XI,'XII':XII,'school_code':school_code})
        except School_child_count.DoesNotExist:
            messages.add_message(
                self.request,
                messages.ERROR,"No School."
            )
            return render(request,'schemes/schemes_class_wise_count_table.html')
       




class Schemes_report(View):

    def get(self,request,**kwargs):
        try:
            school_code = self.request.GET.get('school_code')
            if request.user.account.user_category_id == 2:
                child_detail_list = School_child_count.objects.get(school__school_code=school_code, school__block_id= request.user.account.associated_with)
            elif request.user.account.user_category_id == 5:
                child_detail_list = School_child_count.objects.get(school__school_code=school_code, school__block_id= request.user.account.associated_with)
            elif request.user.account.user_category_id == 6 or request.user.account.user_category_id == 7 or request.user.account.user_category_id == 8 or request.user.account.user_category_id == 12 or request.user.account.user_category_id == 13 or request.user.account.user_category_id == 14:
                child_detail_list = School_child_count.objects.get(school__school_code=school_code, school__district_id= request.user.account.associated_with)
            elif request.user.account.user_category_id == 9 or request.user.account.user_category_id == 10 or request.user.account.user_category_id == 11 or request.user.account.user_category_id == 15 or request.user.account.user_category_id == 16 or request.user.account.user_category_id == 17 or request.user.account.user_category_id == 4:
                child_detail_list = School_child_count.objects.get(school__school_code=school_code)    
            else:
                child_detail_list = School_child_count.objects.get(school_id=request.user.account.associated_with)

            totalcount = child_detail_list.total_count
            I = child_detail_list.one
            II = child_detail_list.two
            III = child_detail_list.three
            IV = child_detail_list.four
            V = child_detail_list.five
            VI = child_detail_list.six
            VII = child_detail_list.seven
            VIII = child_detail_list.eight
            IX = child_detail_list.nine
            X = child_detail_list.ten
            XI = child_detail_list.eleven
            XII = child_detail_list.twelve
            return render(request,'schemes/c.html',{'child_detail_list':child_detail_list,'totalcount':totalcount,'I':I,'II':II,'III':III,'IV':IV,'V':V,'VI':VI,'VII':VII,'VIII':VIII,'IX':IX,'X':X,'XI':XI,'XII':XII,'school_code':school_code})
        except School_child_count.DoesNotExist:
            messages.add_message(
                self.request,
                messages.ERROR,"No School."
            )
            return render(request,'schemes/report_table.html',locals())
       


class Schemes_class_wise_report(View): 
    def get(self,request,**kwargs):
        form=Student_schemesform()
        class_id = self.kwargs.get('cl_id')
        school_code = self.kwargs.get('school_code')
        school_id = request.user.account.associated_with
        schl_id = School.objects.get(id=school_id)
        if request.user.account.user_category_id == 2:
            child_detail_list = Child_detail.objects.filter(staff_id=school_code, block_id=request.user.account.associated_with).exclude(transfer_flag = 1)
        elif request.user.account.user_category_id == 5:
            child_detail_list = Child_detail.objects.filter(staff_id=school_code, block_id=request.user.account.associated_with).exclude(transfer_flag = 1)
        elif request.user.account.user_category_id == 6 or request.user.account.user_category_id == 7 or request.user.account.user_category_id == 8 or request.user.account.user_category_id == 12 or request.user.account.user_category_id == 13 or request.user.account.user_category_id == 14:
            child_detail_list = Child_detail.objects.filter(staff_id=school_code, district_id= request.user.account.associated_with).exclude(transfer_flag = 1)
        elif request.user.account.user_category_id == 9 or request.user.account.user_category_id == 10 or request.user.account.user_category_id == 11 or request.user.account.user_category_id == 15 or request.user.account.user_category_id == 16 or request.user.account.user_category_id == 17 or request.user.account.user_category_id == 4:
            child_detail_list = Child_detail.objects.filter(staff_id=school_code).exclude(transfer_flag = 1)    
        else:
            child_detail_list = Child_detail.objects.filter(staff_id=schl_id.school_code).exclude(transfer_flag = 1)
        classwise_detail = child_detail_list.filter(class_studying_id=class_id).order_by('name')
        return render(request,'schemes/report.html',locals())
