from django.views.generic import View
from teachers.models import *
from baseapp.models import *
from teachers.forms import *
from django.shortcuts import *
from django.db import *
from datetime import datetime
from django.contrib import messages
import cStringIO as StringIO
from xhtml2pdf import pisa
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache



#@never_cache
def generate(i):
	mag_code=int(i)
	if (mag_code==33):
		x=int(mag_code)*10000000+count_private_Teaching.objects.all().count()
		x+=1
		m=count_private_Teaching(count_private_Teaching=x)
		m.save()
	d=Count_private.objects.all().count()
	d+=1
	f=Count_private(count_stand=d)
	f.save()
	return x


class private_teachers_create(View):
	#@never_cache
	def get(self,request,**kwargs):
		if request.user.is_authenticated():
			form=private_teachers_detailform()
			private_mgnt=3
			school_id = request.user.account.associated_with
			designation_1=private_designation.objects.all()
			classes=class_assigned_master.objects.all()
			subjects=Subject.objects.order_by('subject_name').values('subject_name').distinct()
			return render(request,'teachers/private/private_teacher_form.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
   
	#@never_cache
	def post(self,request,**kwargs):
		if request.user.is_authenticated():
			form=private_teachers_detailform(request.POST,request.FILES)
			school_id = request.user.account.associated_with
			management=33
   			x=generate(management)
   			if form.is_valid():            
   				loan=private_teachers_detail(pri_tea_id=x,
   					name=form.cleaned_data['name'],
   					school_name=school_id,
   					dob=form.cleaned_data['dob'],
   					gender=form.cleaned_data['gender'],
   					father_name=form.cleaned_data['father_name'],
   					designation_typeno=form.cleaned_data['designation_typeno'],
   					designation=form.cleaned_data['designation'],
   					subject=form.cleaned_data['subject'],
   					doa=form.cleaned_data['doa'],
   					class_assigned=form.cleaned_data['class_assigned'],
   					teaching_experience=form.cleaned_data['teaching_experience'],
   					train_untrain=form.cleaned_data['train_untrain'],
   					scaleofpay=form.cleaned_data['scaleofpay'],
   					grossofpay=form.cleaned_data['grossofpay'],
   					whethertet=form.cleaned_data['whethertet'],
   					date_of_pass=form.cleaned_data['date_of_pass'],
   					reg_no=form.cleaned_data['reg_no'],
   					esino=form.cleaned_data['esino'],
   					epfno=form.cleaned_data['epfno'],
   					epfreceipt=form.cleaned_data['epfreceipt']
   					)
				loan.save()     
				return  HttpResponseRedirect('/teachers/private_teachers_school_level_name_list/') 
			else:
				print form.errors
				return render(request,'teachers/private/private_teacher_form.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class private_teacher_update(View):
	#@never_cache
	def get(self, request,**kwargs):
		if request.user.is_authenticated():
			school_id = request.user.account.associated_with
			subjects=Subject.objects.order_by('subject_name').values('subject_name').distinct()
			tid=self.kwargs.get('pk')        
			instance = private_teachers_detail.objects.get(pri_tea_id = tid)          
			staff_name=instance.name
			staff_uid=instance.pri_tea_id   
			form = private_teachers_detailform(instance=instance)        
			pri_tea_id = instance.pri_tea_id
			name=instance.name
			school_name=instance.school_name
			dob=instance.dob
			gender=instance.gender
			father_name=instance.father_name
			designation_typeno=instance.designation_typeno
			designation=instance.designation
			subject=instance.subject
			doa=instance.doa
			class_assigned=instance.class_assigned
			teaching_experience=instance.teaching_experience
			train_untrain=instance.train_untrain
			scaleofpay=instance.scaleofpay
			grossofpay=instance.grossofpay
			whethertet=instance.whethertet

			date_of_pass=instance.date_of_pass
			reg_no =instance.reg_no
			esino=instance.esino
			epfno=instance.epfno
			private_mgnt=3
			return render(request,'teachers/private/private_teacher_form.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

	#@never_cache
	def post(self,request,**kwargs):
		if request.user.is_authenticated():
			school_id = request.user.account.associated_with
			tid=self.kwargs.get('pk')
			mgnt_edit = private_teachers_detail.objects.get(pri_tea_id=tid) 		
			form = private_teachers_detailform(request.POST,request.FILES)  
			staff_name=mgnt_edit.name
			staff_uid=mgnt_edit.pri_tea_id         
			if form.is_valid():
				mgnt_edit.pri_tea_id=mgnt_edit.pri_tea_id
				mgnt_edit.name=form.cleaned_data['name']
				mgnt_edit.dob=form.cleaned_data['dob']
				mgnt_edit.gender=form.cleaned_data['gender']  
				mgnt_edit.father_name=form.cleaned_data['father_name']
				mgnt_edit.designation_typeno=form.cleaned_data['designation_typeno']
				mgnt_edit.designation=form.cleaned_data['designation']
				mgnt_edit.subject=form.cleaned_data['subject']
				mgnt_edit.doa=form.cleaned_data['doa'] 
				mgnt_edit.class_assigned=form.cleaned_data['class_assigned']
				mgnt_edit.teaching_experience=form.cleaned_data['teaching_experience']
				mgnt_edit.train_untrain=form.cleaned_data['train_untrain']
				mgnt_edit.scaleofpay=form.cleaned_data['scaleofpay']
				mgnt_edit.grossofpay=form.cleaned_data['grossofpay']
				mgnt_edit.whethertet=form.cleaned_data['whethertet'] 
				mgnt_edit.date_of_pass=form.cleaned_data['date_of_pass']
				mgnt_edit.reg_no=form.cleaned_data['reg_no']
				mgnt_edit.esino=form.cleaned_data['esino']
				mgnt_edit.epfno=form.cleaned_data['epfno']  
				mgnt_edit.save()
				messages.success(request,'Details Updated successfully')
				return HttpResponseRedirect('/teachers/private_teachers_school_level_name_list/' )
			else:
				print form.errors
				return render(request,'teachers/private/private_teacher_form.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
			
class private_teachers_school_level_name_list(View):
	#@never_cache
	def get(self,request,**kwargs):
		if request.user.is_authenticated():
			private_mgnt=3
			school_id = request.user.account.associated_with 
			teachers_name_list_new= private_teachers_detail.objects.filter(school_name=school_id).filter(outofservice=False)
			return render(request,'teachers/private/teacher_list.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


class edu_qualifaction_create(View):
	#@never_cache
	def get(self,request,**kwargs):
		if request.user.is_authenticated():
			private_mgnt=3
			tid=self.kwargs.get('pk')        
			staff_id = private_teachers_detail.objects.get(pri_tea_id = tid)          
			staff_name=staff_id.name
			staff_uid=staff_id.pri_tea_id 
			dob=staff_id.dob       
			form=private_educationform()        
			qualification=Qualification.objects.all()
			subject=Edu_subjects.objects.all()
			medium_value=Medium.objects.all()
			month_value=Months.objects.all()
			class_value=Distinction.objects.all()
			edu_list = Teacher_edu_private.objects.filter(unique_id=tid)
			if edu_list.count()==0:
				messages.success(request,'No Data')        
			return render(request,'teachers/private/teacher_education_form_private.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

	#@never_cache
	def post(self,request,**kwargs): 
		if request.user.is_authenticated():
			tid=self.kwargs.get('pk')        
			form=private_educationform(request.POST,request.FILES)
			edu_list = private_teachers_detail.objects.get(pri_tea_id=tid)
			staff_name=edu_list.name   
			staff_uid=edu_list.pri_tea_id  
			try:
				if form.is_valid():            
					education=Teacher_edu_private(private_tea_id_id=edu_list.id,
						unique_id=edu_list.pri_tea_id,
						qualification=form.cleaned_data['qualification'],
						subject=form.cleaned_data['subject'],
						medium_of_instruction=form.cleaned_data['medium_of_instruction'],
						month=form.cleaned_data['month'],
						year=form.cleaned_data['year'],
						university=form.cleaned_data['university'],
						remarks=form.cleaned_data['remarks'],
					)
					education.save()
				msg = str(staff_name) + "(" + str(staff_uid)+") Education details added successfully."
				messages.success(request, msg )
				
				return redirect('edu_qualifaction_create',pk=tid)

			except:

				messages.success(request, "Invalid Data. Please Try Again" )
				return redirect('edu_qualifaction_create',pk=tid)
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


class edu_qualifaction_update(View):
	#@never_cache
	def get(self, request,**kwargs):
		if request.user.is_authenticated():
			private_mgnt=3
			school_id = request.user.account.associated_with
			tid=self.kwargs.get('pk')
			pk1=self.kwargs.get('pk1')
			staff_id = private_teachers_detail.objects.get(pri_tea_id = tid )          
			staff_name=staff_id.name
			staff_uid=staff_id.pri_tea_id  
			instance=Teacher_edu_private.objects.get(id=pk1)     
			qualification=Qualification.objects.all()
			subject=Edu_subjects.objects.all()
			medium_value=Medium.objects.all()
			month_value=Months.objects.all()
			class_value=Distinction.objects.all()        
			form = private_educationform(instance=instance)
			unique_id = instance.private_tea_id
			qualification = instance.qualification
			subject=instance.subject
			medium_of_instruction = instance.medium_of_instruction  
			month =instance.month  
			year =instance.year
			university =instance.university
			remarks =instance.remarks       
			return render(request,'teachers/private/teacher_education_form_private.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


	#@never_cache
	def post(self,request,**kwargs):
		if request.user.is_authenticated():
			school_id = request.user.account.associated_with
			tid=self.kwargs.get('pk')
			pk1=self.kwargs.get('pk1')
			staff_id = private_teachers_detail.objects.get(pri_tea_id = tid)     
			staff_name=staff_id.name
			staff_uid=staff_id.pri_tea_id    
			instance=Teacher_edu_private.objects.get(id=pk1)
			form = private_educationform(request.POST,request.FILES)
			mgnt_edit = Teacher_edu_private.objects.get(id=pk1)
			if form.is_valid():
				mgnt_edit.qualification=form.cleaned_data['qualification']
				mgnt_edit.medium_of_instruction=form.cleaned_data['medium_of_instruction']
				mgnt_edit.month=form.cleaned_data['month']
				mgnt_edit.year=form.cleaned_data['year']            
				mgnt_edit.university=form.cleaned_data['university']
				mgnt_edit.remarks=form.cleaned_data['remarks']            
				mgnt_edit.save()
				messages.success(request,'Education Qualification Details Updated successfully')
				return redirect('edu_qualifaction_create',pk=tid)
			else:
				print form.errors
				return render(request,'teachers/private/teacher_education_form_private.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class private_teacher_delete(View):
	#@never_cache
	def get(self, request,**kwargs):
		if request.user.is_authenticated():
			private_mgnt=3
			tid=self.kwargs.get('pk')
			data= private_teachers_detail.objects.get(pri_tea_id = tid)
			return render(request,'teachers/private_teacher_delete.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

#@never_cache
def post(self, request,**kwargs):
	if request.user.is_authenticated():
		tid=self.kwargs.get('pk')
		data=private_teachers_detail.objects.get(pri_tea_id = tid)
		data1=Teacher_edu_private.objects.filter(private_tea_id_id=data.id)
		if data.epfno:
			data.outofservice = True;
			data.save()
			msg = data.name +" with "+ str(data.designation) + "  details removed successfully."
		else:
			msg = data.name +" with "+ str(data.designation) + "  details removed successfully." 
			data.delete()
			if data1.count()>0:
				for i in data1:
					i.delete()
			messages.success(request,msg)
			return HttpResponseRedirect('/teachers/private_teachers_school_level_name_list')

class teacher_full_detail_private(View):
	#@never_cache
	def get(self,request,**kwargs):
	    if request.user.is_authenticated():   	
			tid=self.kwargs.get('pk')        
			private_mgnt=3
			instancee=private_teachers_detail.objects.get(pri_tea_id = tid) 
			edu_list = Teacher_edu_private.objects.filter(unique_id=tid)
			return render(request,'teachers/private/private_teacher_full_detail.html',locals())
		# else:
		# 	return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class private_teacher_view(View):
	#@never_cache
	def get(self,request,**kwargs):
		if request.user.is_authenticated():
			pk=self.kwargs.get('pk')
			teacher=private_teachers_detail.objects.get(pri_tea_id = pk)
			edu_list = Teacher_edu_private.objects.filter(unique_id=pk)
			a=teacher.pri_tea_id
			response = HttpResponse(content_type='application/pdf')
			filename = str(a)
			photo=settings.MEDIA_URL
			root=settings.MEDIA_ROOT
			response['Content-Disposition'] = 'attachement; filename={0}.pdf'.format(filename)
	    	pdf=render_to_private_pdf(
	               'teachers/private/pdfprivate.html',
	                {
	                  
	                    'teacher':teacher,
	                    'edu_list':edu_list,
	                    
	                    'pagesize':'A4',
	                    'MEDIA_URL':root,
	                    
	                }
	            )
	    	response.write(pdf)
	    	return response
		# else:
		# 	return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


#@never_cache
def render_to_private_pdf(template_src, context_dict):
	template = get_template(template_src)
	context = Context(context_dict)
	html  = template.render(context)
	result = StringIO.StringIO()

	pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
