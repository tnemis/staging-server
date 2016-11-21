from django.views.generic import ListView, DetailView, CreateView, \
                                 DeleteView, UpdateView, \
                                 ArchiveIndexView, DateDetailView, \
                                 DayArchiveView, MonthArchiveView, \
                                 TodayArchiveView, WeekArchiveView, \
                                 YearArchiveView, View


from schoolnew.models import *
from schoolnew.forms import *
from django.db.models import *
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.contrib import messages
from itertools import *
from datetime import datetime
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect
import reportlab
import cStringIO as StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from cgi import escape
from excel_response import ExcelResponse
import json 
from django.utils import simplejson
import os
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.core.cache import cache

class myview1(View):

	def get(self,request,**kwargs):
		if request.user.is_authenticated():
			pk=self.kwargs.get('pk')
			basic=Basicinfo.objects.get(id=pk)
			school=School.objects.get(id=request.user.account.associated_with)
			admin = Academicinfo.objects.get(school_key=basic.id)
			academic = Academicinfo.objects.get(school_key=basic.id)
			infra = Infradet.objects.get(school_key=basic.id)
			class_det = Class_section.objects.filter(school_key=basic.id)
			schgroup_det = Sch_groups.objects.filter(school_key=basic.id)
			post_det = Staff.objects.filter(Q(school_key=basic.id))
			parttime_det = Parttimestaff.objects.filter(school_key=basic.id)
			land_det = Land.objects.filter(school_key=basic.id)
			build_det = Building.objects.filter(school_key=basic.id)
			buildabs_det = Building_abs.objects.filter(school_key=basic.id)
			sports_det = Sports.objects.filter(school_key=basic.id)
			ict_det = Ictentry.objects.filter(school_key=basic.id)
			passper_det=Passpercent.objects.filter(school_key=basic.id)

			infra
			a=basic.udise_code
			response = HttpResponse(content_type='application/pdf')
			filename = str(a)
			infra_edit_chk='Yes'
			response['Content-Disposition'] = 'attachement'; 'filename={0}.pdf'.format(filename)
			pdf=render_to_pdf(
				'printpdfschool.html',
					{
						'basic':basic,
						'admin':admin,
						'academic':academic,
						'infra': infra,
						'class_det':class_det,
						'schgroup_det':schgroup_det,
						'post_det':post_det,
						'parttime_det':parttime_det,
						'land_det':land_det,
						'build_det':build_det,
						'buildabs_det':buildabs_det,
						'sports_det':sports_det,
						'ict_det':ict_det,
						'passper_det':passper_det,
						'pagesize':'A4'
					}
				)

			response.write(pdf)
			return response
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))	


def render_to_pdf(template_src, context_dict):
	template = get_template(template_src)
	context = Context(context_dict)
	html  = template.render(context)
	result = StringIO.StringIO()
	infra_edit_chk='Yes'
	# "UTF-8"
	# The only thing was to replace html.encode("ISO-8859-1") by html.decode("utf-8")
	pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
	if not pdf.err:      
		return HttpResponse(result.getvalue(), content_type='application/pdf')        
	return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))



class home_page(View):

	def get(self,request,**kwargs):

		if request.user.is_authenticated():
			if (Basicinfo.objects.filter(udise_code=request.user.username).count())>0:
				# chk_ss=Basicinfo.objects.filter(udise_code=request.user.username)
				# slno=District.objects.filter(id__lt=15)
				basic_det=Basicinfo.objects.get(udise_code=request.user.username)
				basic_det = Basicinfo.objects.get(id=basic_det.id)
				sch_key = basic_det.id			
				new_sch_id = basic_det.id
				govchk=basic_det.sch_management
				sch_dir=basic_det.sch_directorate
				sch_cat_chk=basic_det.sch_cate
				chk_user=Basicinfo.objects.get(udise_code=request.user.username)

				if ((str(govchk)=='School Education Department School')|(str(govchk)=='Corporation School')|(str(govchk)=='Municipal School')|(str(govchk)=='Fully Aided School')|(str(govchk)=='Partly Aided School')|(str(govchk)=='Anglo Indian (Fully Aided) School')|(str(govchk)=='Anglo Indian (Partly Aided) School')|(str(govchk)=='Oriental (Fully Aided) Sanskrit School')|(str(govchk)=='Oriental (Partly Aided) Sanskrit School')|(str(govchk)=='Oriental (Fully Aided) Arabic School')|(str(govchk)=='Oriental (Partly Aided) Arabic School')):
					if ((basic_det.sch_directorate.department_code=='001')|(basic_det.sch_directorate.department_code=='002')):
						govaid_ent='Yes'
					else:
						govaid_ent=''
				else:
					govaid_ent=''

				if (Academicinfo.objects.filter(school_key=basic_det.id).count())>0:
					acade_det = Academicinfo.objects.get(school_key=basic_det.id)
					acade_det = Academicinfo.objects.get(id=acade_det.id)
					if basic_det.sch_cate:
						if (basic_det.sch_cate.category_code in ('3,5,6,7,8,10,11')):
							pass_ent='Yes'
						else:
							pass_ent=''
					else:
						pass_ent=''

				if (Infradet.objects.filter(school_key=basic_det.id).count())>0:
					infra_det = Infradet.objects.get(school_key=basic_det.id)				
				if (Class_section.objects.filter(school_key=basic_det.id).count())>0:
					class_det = Class_section.objects.filter(school_key=basic_det.id)

				if (Staff.objects.filter(Q(school_key=basic_det.id) & Q(staff_cat=1)))>0:
					teach_det = Staff.objects.filter(Q(school_key=basic_det.id) & Q(staff_cat=1))
				if (Staff.objects.filter(Q(school_key=basic_det.id) & Q(staff_cat=2)).count())>0:
					nonteach_det = Staff.objects.filter(Q(school_key=basic_det.id) & Q(staff_cat=2))
				if (Parttimestaff.objects.filter(school_key=basic_det.id).count())>0:
					parttime_det = Parttimestaff.objects.filter(school_key=basic_det.id)
				if (Land.objects.filter(school_key=basic_det.id).count())>0:
					land_det = Land.objects.filter(school_key=basic_det.id)
				if (Building.objects.filter(school_key=basic_det.id).count())>0:
					building_det = Building.objects.filter(school_key=basic_det.id)
				if (Building_abs.objects.filter(school_key=basic_det.id).count())>0:
					buildabs_det = Building_abs.objects.filter(school_key=basic_det.id)
				if (Sports.objects.filter(school_key=basic_det.id).count())>0:
					sports_det = Sports.objects.filter(school_key=basic_det.id)
				if (Ictentry.objects.filter(school_key=basic_det.id).count())>0:
					ict_det = Ictentry.objects.filter(school_key=basic_det.id)
				if (Sch_groups.objects.filter(school_key=basic_det.id).count())>0:
					schgroup_det = Sch_groups.objects.filter(school_key=basic_det.id)
				basic_mdate=basic_det.modified_date.strftime('%d-%m-%Y --  %H:%M %p')
				grp=basic_det.sch_cate
				if ((str(grp)=='Hr.Sec School (I-XII)')|(str(grp)=='Hr.Sec School (VI-XII)')|(str(grp)=='Hr.Sec School (IX-XII)')|(str(grp)=='Hr.Sec School (XI-XII)')|(str(grp)=='Matriculation Hr.Sec School (I-XII)')):
					
					grp_chk='Yes'
				else:
					grp_chk=''		


				if (Academicinfo.objects.filter(school_key=basic_det.id).count())>0:
					acade_mdate=Academicinfo.objects.get(school_key=basic_det.id)

				if (Infradet.objects.filter(school_key=basic_det.id).count())>0:
					infra_mdate=Infradet.objects.get(school_key=basic_det.id)


				if (Staff.objects.filter(Q(school_key=basic_det.id) & Q(staff_cat=1)))>0:
					teach_mdate=Staff.objects.filter(Q(school_key=basic_det.id) & Q(staff_cat=1))

				return render (request,'home_edit1.html',locals())
			else:
				return render (request,'home_edit1.html',locals())

		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))		

class basic_edit(UpdateView):			

	def get(self,request,**kwargs):
		if request.user.is_authenticated():
			chk_user1=self.kwargs.get('pk')

			district_list = District.objects.all().order_by('district_name')
			chk_udise_block=int((str(request.user.username)[:6])) 
			latlong_det= Gis_block_code.objects.get(udise_block_code=chk_udise_block)
			acadyr_lst=Acadyr_mas.objects.all()
			if Basicinfo.objects.filter(udise_code=int(request.user.username)).count()>0:
				basic_det=Basicinfo.objects.get(udise_code=request.user.username)
				basic_det = Basicinfo.objects.get(id=basic_det.id)
				instance = Basicinfo.objects.get(udise_code=request.user.username)
				form=BasicForm(instance=instance)

				school_id=instance.school_id
				school_name = instance.school_name
				if instance.school_name_tamil:
					word = instance.school_name_tamil
				else:
					word=''
				udise_code = instance.udise_code
				district = instance.district
				block = instance.block
				local_body_type= instance.local_body_type
				village_panchayat =instance.village_panchayat
				vill_habitation = instance.vill_habitation
				town_panchayat = instance.town_panchayat
				town_panchayat_ward = instance.town_panchayat_ward
				municipality = instance.municipality
				municipal_ward = instance.municipal_ward
				cantonment = instance.cantonment
				cantonment_ward = instance.cantonment_ward
				township = instance.township
				township_ward = instance.township_ward
				corporation = instance.corporation
				corpn_zone = instance.corpn_zone
				corpn_ward = instance.corpn_ward
				edu_district = instance.edu_district
				address  = instance.address
				stdcode = instance.stdcode
				landline = instance.landline
				landline2 = instance.landline2
				mobile = instance.mobile
				sch_email = instance.sch_email
				website = instance.website
				bank_dist=instance.bank_dist
				bank = instance.bank
				branch = instance.branch
				bankaccno = instance.bankaccno
				parliament = instance.parliament
				assembly = instance.assembly
				manage_cate = instance.manage_cate
				sch_management=instance.sch_management
				sch_cate = instance.sch_cate
				sch_directorate = instance.sch_directorate	
				pta_esta = instance.pta_esta
				pta_no= instance.pta_no
				pta_sub_yr= instance.pta_sub_yr		
				prekg=instance.prekg
				kgsec=instance.kgsec
				cluster=instance.cluster
				mgt_opn_year=instance.mgt_opn_year
				mgt_type=instance.mgt_type
				mgt_name=instance.mgt_name
				mgt_address=instance.mgt_address
				mgt_regis_no=instance.mgt_regis_no
				mgt_regis_dt=instance.mgt_regis_dt
				draw_off_code=instance.draw_off_code
				regis_by_office=instance.regis_by_office
				pincode=instance.pincode
				chk_dept=instance.chk_dept
				chk_manage=instance.chk_manage
				if instance.latitude:
					latitude = instance.latitude
					longitude = instance.longitude
					latlong='Yes'
				else:	
					latlong_det= Gis_block_code.objects.get(udise_block_code=chk_udise_block)
					latlong=''					

				return render (request,'basicinfo_edit.html',locals())				
			else:
				form=BasicForm()
				chk_udise_block=int((str(request.user.username)[:6])) 
				latlong_det= Gis_block_code.objects.get(udise_block_code=chk_udise_block)
				latlong=''				
			return render (request,'basicinfo_edit.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			



	def post(self, request, **kwargs):
		if request.user.is_authenticated():
			if Basicinfo.objects.filter(udise_code=request.user.username).count()>0:	
				instance = Basicinfo.objects.get(udise_code=request.user.username)
				basic_editsave=Basicinfo.objects.get(udise_code=request.user.username)	
				form = BasicForm(request.POST,request.FILES)
				if form.is_valid():
					basic_editsave.school_id = form.cleaned_data['school_id']				
					basic_editsave.school_name = form.cleaned_data['school_name'].upper()
					basic_editsave.school_name_tamil = request.POST['word']
					basic_editsave.udise_code = form.cleaned_data['udise_code']
					basic_editsave.district = form.cleaned_data['district']
					basic_editsave.district1 = form.cleaned_data['district']
					basic_editsave.block = form.cleaned_data['block']
					basic_editsave.block1 = form.cleaned_data['block']
					basic_editsave.local_body_type= form.cleaned_data['local_body_type']
					chk_local_body=Local_body.objects.get(id=request.POST['local_body_type'])			
					if str(chk_local_body)=='Village Panchayat':	
						basic_editsave.village_panchayat =form.cleaned_data['village_panchayat']
						basic_editsave.vill_habitation = form.cleaned_data['vill_habitation']
						basic_editsave.town_panchayat = None
						basic_editsave.town_panchayat_ward = None
						basic_editsave.municipality = None
						basic_editsave.municipal_ward = None
						basic_editsave.cantonment = None
						basic_editsave.cantonment_ward = None
						basic_editsave.township = None
						basic_editsave.township_ward = None
						basic_editsave.corporation = None
						basic_editsave.corpn_zone = None
						basic_editsave.corpn_ward = None
					elif str(chk_local_body)=="Town Panchayat":
						basic_editsave.village_panchayat =None
						basic_editsave.vill_habitation = None
						basic_editsave.town_panchayat = form.cleaned_data['town_panchayat']
						basic_editsave.town_panchayat_ward = form.cleaned_data['town_panchayat_ward']				
						basic_editsave.municipality = None
						basic_editsave.municipal_ward = None
						basic_editsave.cantonment = None
						basic_editsave.cantonment_ward = None
						basic_editsave.township = None
						basic_editsave.township_ward = None
						basic_editsave.corporation = None
						basic_editsave.corpn_zone = None
						basic_editsave.corpn_ward = None				
					elif str(chk_local_body)=="Municipality":
						basic_editsave.village_panchayat =None
						basic_editsave.vill_habitation = None
						basic_editsave.town_panchayat = None
						basic_editsave.town_panchayat_ward = None
						basic_editsave.municipality = form.cleaned_data['municipality']
						basic_editsave.municipal_ward = form.cleaned_data['municipal_ward']
						basic_editsave.cantonment = None
						basic_editsave.cantonment_ward = None
						basic_editsave.township = None
						basic_editsave.township_ward = None
						basic_editsave.corporation = None
						basic_editsave.corpn_zone = None
						basic_editsave.corpn_ward = None				
					elif str(chk_local_body)=="cantonment":
						basic_editsave.village_panchayat =None
						basic_editsave.vill_habitation = None
						basic_editsave.town_panchayat = None
						basic_editsave.town_panchayat_ward = None
						basic_editsave.municipality = None
						basic_editsave.municipal_ward = None
						basic_editsave.cantonment = form.cleaned_data['cantonment']
						basic_editsave.cantonment_ward = form.cleaned_data['cantonment_ward']
						basic_editsave.township = None
						basic_editsave.township_ward = None
						basic_editsave.corporation = None
						basic_editsave.corpn_zone = None
						basic_editsave.corpn_ward = None				
					elif str(chk_local_body)=="Township":
						basic_editsave.village_panchayat =None
						basic_editsave.vill_habitation = None
						basic_editsave.town_panchayat = None
						basic_editsave.town_panchayat_ward = None
						basic_editsave.municipality = None
						basic_editsave.municipal_ward = None
						basic_editsave.cantonment = None
						basic_editsave.cantonment_ward = None
						basic_editsave.township = form.cleaned_data['township']
						basic_editsave.township_ward = form.cleaned_data['township_ward']
						basic_editsave.corporation = None
						basic_editsave.corpn_zone = None
						basic_editsave.corpn_ward = None				
					elif str(chk_local_body)=="Corporation":
						basic_editsave.village_panchayat =None
						basic_editsave.vill_habitation = None
						basic_editsave.town_panchayat = None
						basic_editsave.town_panchayat_ward = None
						basic_editsave.municipality = None
						basic_editsave.municipal_ward = None
						basic_editsave.cantonment = None
						basic_editsave.cantonment_ward = None
						basic_editsave.township = None
						basic_editsave.township_ward = None
						basic_editsave.corporation = form.cleaned_data['corporation']
						basic_editsave.corpn_zone = form.cleaned_data['corpn_zone']
						basic_editsave.corpn_ward = form.cleaned_data['corpn_ward']	

					if request.POST['prekg']=='Yes':
						basic_editsave.prekg = form.cleaned_data['prekg']
						basic_editsave.kgsec = 'Yes'
					else:
						basic_editsave.prekg = 'No'
						if request.POST['kgsec']=='Yes':
							basic_editsave.kgsec = form.cleaned_data['kgsec']		
						else:
							basic_editsave.kgsec = 'No'
					basic_editsave.edu_district = form.cleaned_data['edu_district']
					basic_editsave.address  = form.cleaned_data['address']
					basic_editsave.pincode = form.cleaned_data['pincode']
					basic_editsave.stdcode = form.cleaned_data['stdcode']
					basic_editsave.landline = form.cleaned_data['landline']
					basic_editsave.landline2 = form.cleaned_data['landline2']
					basic_editsave.mobile = form.cleaned_data['mobile']
					basic_editsave.sch_email = form.cleaned_data['sch_email']
					basic_editsave.website = form.cleaned_data['website']
					basic_editsave.bank_dist=form.cleaned_data['bank_dist']
					basic_editsave.bank = form.cleaned_data['bank']
					basic_editsave.branch = form.cleaned_data['branch']
					basic_editsave.bankaccno = form.cleaned_data['bankaccno']
					basic_editsave.parliament = form.cleaned_data['parliament']
					basic_editsave.assembly = form.cleaned_data['assembly']
					basic_editsave.latitude = form.cleaned_data['latitude']
					basic_editsave.longitude = form.cleaned_data['longitude']
					basic_editsave.manage_cate = form.cleaned_data['manage_cate']
					basic_editsave.sch_management=form.cleaned_data['sch_management']
					basic_editsave.sch_directorate = form.cleaned_data['sch_directorate']
					basic_editsave.sch_cate = form.cleaned_data['sch_cate']

					if request.POST['pta_esta']=='Yes':
						basic_editsave.pta_esta = form.cleaned_data['pta_esta']
						basic_editsave.pta_no= form.cleaned_data['pta_no']
						basic_editsave.pta_sub_yr= form.cleaned_data['pta_sub_yr']
					else:
						basic_editsave.pta_esta = form.cleaned_data['pta_esta']
						basic_editsave.pta_no= None
						basic_editsave.pta_sub_yr= None

					basic_editsave.cluster=form.cleaned_data['cluster']
					if basic_editsave.manage_cate_id==1:
						basic_editsave.mgt_opn_year=None
						basic_editsave.mgt_type=None
						basic_editsave.mgt_name=None
						basic_editsave.mgt_address=None
						basic_editsave.mgt_regis_no=None
						basic_editsave.mgt_regis_dt=None
						basic_editsave.regis_by_office=None
						basic_editsave.draw_off_code = form.cleaned_data['draw_off_code']
					elif basic_editsave.manage_cate_id==2:
						basic_editsave.mgt_opn_year=None
						basic_editsave.mgt_type=None
						basic_editsave.mgt_name=None
						basic_editsave.mgt_address=None
						basic_editsave.mgt_regis_no=None
						basic_editsave.mgt_regis_dt=None
						basic_editsave.regis_by_office=None
						basic_editsave.draw_off_code = form.cleaned_data['draw_off_code']
					else:
						basic_editsave.mgt_opn_year=form.cleaned_data['mgt_opn_year']
						basic_editsave.mgt_type=form.cleaned_data['mgt_type']
						basic_editsave.mgt_name=form.cleaned_data['mgt_name']
						basic_editsave.mgt_address=form.cleaned_data['mgt_address']
						basic_editsave.mgt_regis_no=form.cleaned_data['mgt_regis_no']
						basic_editsave.mgt_regis_dt=form.cleaned_data['mgt_regis_dt']
						basic_editsave.regis_by_office=form.cleaned_data['regis_by_office']
						basic_editsave.draw_off_code = None	
			
					if basic_editsave.manage_cate_id==1:
						basic_editsave.chk_manage=1
					elif basic_editsave.manage_cate_id==2:
						basic_editsave.chk_manage=2
					else:
						basic_editsave.chk_manage=3

					if basic_editsave.sch_directorate_id==28:
						basic_editsave.chk_dept=3
					elif basic_editsave.sch_directorate_id in (2,3,16,18,27,29,32,34,42):
						basic_editsave.chk_dept=2
					else:

						if basic_editsave.sch_cate.category_code in ('1','2','4'):
							basic_editsave.chk_dept=2
						elif basic_editsave.sch_cate.category_code in ('10','11','5','7','8'):
							basic_editsave.chk_dept=1
						else:
							basic_editsave.chk_dept=3					
					basic_editsave.save()

					govchk=basic_editsave.sch_management
					if (str(govchk)=='Un-Aided (Private) School - Other than State Board School'):
						board_id = basic_editsave.sch_directorate
						oth_board=School_department.objects.get(id=board_id.id)
						board=oth_board.department
						
						
					elif (str(govchk)=='Army Public School'):
						board ='CBSE'
						
					elif (str(govchk)=='Kendra Vidyalaya - Central Government School'):
						board ='CBSE'

					elif (str(govchk)=='Sainik School'):
						board ='CBSE'	
					else:
						board ='State Board'
					if Academicinfo.objects.filter(school_key=basic_editsave.id).count()>0:
						acade_det1 = Academicinfo.objects.get(school_key=basic_editsave.id)
						acade_det1.board=board
						acade_det1.save()

					messages.success(request,'Basic Informations Updated Successfully')
					return HttpResponseRedirect('/schoolnew/school_registration')
				else:
					messages.warning(request,'Basic Informations Not Updated')
					return HttpResponseRedirect('/schoolnew/school_registration')

			else:
				form = BasicForm(request.POST,request.FILES)
				if form.is_valid():

					basicinfo = Basicinfo(
						school_id=form.cleaned_data['school_id'],
						school_name = form.cleaned_data['school_name'].upper(),
						school_name_tamil = request.POST['word'],
						udise_code = form.cleaned_data['udise_code'],
						district = form.cleaned_data['district'],
						block = form.cleaned_data['block'],
						local_body_type= form.cleaned_data['local_body_type'],
						village_panchayat =form.cleaned_data['village_panchayat'],
						vill_habitation = form.cleaned_data['vill_habitation'],
						town_panchayat = form.cleaned_data['town_panchayat'],
						town_panchayat_ward = form.cleaned_data['town_panchayat_ward'],
						municipality = form.cleaned_data['municipality'],
						municipal_ward = form.cleaned_data['municipal_ward'],
						cantonment = form.cleaned_data['cantonment'],
						cantonment_ward = form.cleaned_data['cantonment_ward'],
						township = form.cleaned_data['township'],
						township_ward = form.cleaned_data['township_ward'],
						corporation = form.cleaned_data['corporation'],
						corpn_zone = form.cleaned_data['corpn_zone'],
						corpn_ward = form.cleaned_data['corpn_ward'],
						edu_district = form.cleaned_data['edu_district'],
						address  = form.cleaned_data['address'],
						pincode = form.cleaned_data['pincode'],
						stdcode = form.cleaned_data['stdcode'],
						landline = form.cleaned_data['landline'],
						landline2 = form.cleaned_data['landline2'],
						mobile = form.cleaned_data['mobile'],
						sch_email = form.cleaned_data['sch_email'],
						website = form.cleaned_data['website'],
						bank_dist=form.cleaned_data['bank_dist'],
						bank = form.cleaned_data['bank'],
						branch = form.cleaned_data['branch'],
						bankaccno = form.cleaned_data['bankaccno'],			
						parliament = form.cleaned_data['parliament'],
						assembly = form.cleaned_data['assembly'],
						latitude = form.cleaned_data['latitude'],
						longitude = form.cleaned_data['longitude'],
						manage_cate = form.cleaned_data['manage_cate'],
						sch_management=form.cleaned_data['sch_management'],
						sch_cate = form.cleaned_data['sch_cate'],
						sch_directorate = form.cleaned_data['sch_directorate'],		
						pta_esta = form.cleaned_data['pta_esta'],
						pta_no= form.cleaned_data['pta_no'],
						pta_sub_yr= form.cleaned_data['pta_sub_yr'],
						prekg = form.cleaned_data['prekg'],
						kgsec = form.cleaned_data['kgsec'],
						cluster=form.cleaned_data['cluster'],					
						mgt_opn_year=form.cleaned_data['mgt_opn_year'],
						mgt_type=form.cleaned_data['mgt_type'],
						mgt_name=form.cleaned_data['mgt_name'],
						mgt_address=form.cleaned_data['mgt_address'],
						mgt_regis_no=form.cleaned_data['mgt_regis_no'],
						mgt_regis_dt=form.cleaned_data['mgt_regis_dt'],
						draw_off_code=form.cleaned_data['draw_off_code'],
						regis_by_office=form.cleaned_data['regis_by_office'],
					)
					basicinfo.save()

					messages.success(request,'Basic Informations Added Successfully')
					return HttpResponseRedirect('/schoolnew/school_registration')
				else:
					messages.warning(request,'Basic Informations Not Saved')
					return HttpResponseRedirect('/schoolnew/school_registration')
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			



class admin_edit(View):
	
	def get(self,request,**kwargs):
		chk_user2=self.kwargs.get('code2')		
		if request.user.is_authenticated():		
			if (Basicinfo.objects.filter(udise_code=request.user.username).count())>0:
				basic_det=Basicinfo.objects.get(udise_code=request.user.username)
				basic_det = Basicinfo.objects.get(id=basic_det.id)
				sch_key = basic_det.id
				new_sch_id = basic_det.id
				govchk=basic_det.sch_management

				if ((str(govchk)=='School Education Department School')|(str(govchk)=='Corporation School')|(str(govchk)=='Municipal School')|(str(govchk)=='Adi-Dravida Welfare School')|(str(govchk)=='Forest Department School')|(str(govchk)=='Differently Abled Department School')|(str(govchk)=='Kallar BC/MBC Department School')|(str(govchk)=='Rubber Board School')|(str(govchk)=='Tribal Welfare School')|(str(govchk)=='Aranilayam HR&C Department School')|(str(govchk)=='Fully Aided School')|(str(govchk)=='Partly Aided School')|(str(govchk)=='Anglo Indian (Fully Aided) School')|(str(govchk)=='Anglo Indian (Partly Aided) School')|(str(govchk)=='Oriental (Fully Aided) Sanskrit School')|(str(govchk)=='Oriental (Partly Aided) Sanskrit School')|(str(govchk)=='Oriental (Fully Aided) Arabic School')|(str(govchk)=='Oriental (Partly Aided) Arabic School')|(str(govchk)=='Differently Abled Department Aided School')):
					govaid_chk='Yes'
				else:
					govaid_chk=''
				grp=basic_det.sch_cate
				if ((str(grp)=='Hr.Sec School (I-XII)')|(str(grp)=='Hr.Sec School (VI-XII)')|(str(grp)=='Hr.Sec School (IX-XII)')|(str(grp)=='Hr.Sec School (XI-XII)')|(str(grp)=='Matriculation Hr.Sec School (I-XII)')):
					grp_chk='Yes'
				else:
					grp_chk=''		
				if ((str(govchk)=='Fully Aided School')|(str(govchk)=='Partly Aided School')|(str(govchk)=='Anglo Indian (Fully Aided) School')|(str(govchk)=='Anglo Indian (Partly Aided) School')|(str(govchk)=='Oriental (Fully Aided) Sanskrit School')|(str(govchk)=='Oriental (Partly Aided) Sanskrit School')|(str(govchk)=='Oriental (Fully Aided) Arabic School')|(str(govchk)=='Oriental (Partly Aided) Arabic School')|(str(govchk)=='Differently Abled Department Aided School')):
					aid_chk='Yes'
				else:
					aid_chk=''	
				if ((str(govchk)=='School Education Department School')|(str(govchk)=='Corporation School')|(str(govchk)=='Municipal School')|(str(govchk)=='Adi-Dravida Welfare School')|(str(govchk)=='Forest Department School')|(str(govchk)=='Differently Abled Department School')|(str(govchk)=='Kallar BC/MBC Department School')|(str(govchk)=='Rubber Board School')|(str(govchk)=='Tribal Welfare School')|(str(govchk)=='Aranilayam HR&C Department School')):	
					gov_chk='Yes'
				else:
					gov_chk='No'

				if basic_det.sch_cate.category_code=='1':
					sch_cat_chk=['I Std','II Std','III Std','IV Std','V Std']
					low_class = 'I Std'
					high_class = 'V Std'
				elif basic_det.sch_cate.category_code=='2':
					sch_cat_chk=['I Std','II Std','III Std','IV Std','V Std','VI Std','VII Std','VIII Std']
					low_class = 'I Std'
					high_class = 'VIII Std'
				elif basic_det.sch_cate.category_code=='3':
					sch_cat_chk=['I Std','II Std','III Std','IV Std','V Std','VI Std','VII Std','VIII Std','IX Std','X Std','XI Std','XII Std']
					low_class = 'I Std'
					high_class = 'XII Std'
				elif basic_det.sch_cate.category_code=='4':
					sch_cat_chk=['VI Std','VII Std','VIII Std']
					low_class = 'VI Std'
					high_class = 'VIII Std'
				elif basic_det.sch_cate.category_code=='5':
					sch_cat_chk=['VI Std','VII Std','VIII Std','IX Std','X Std','XI Std','XII Std',]
					low_class = 'VI Std'
					high_class = 'XII Std'
				elif basic_det.sch_cate.category_code=='6':
					sch_cat_chk=['I Std','II Std','III Std','IV Std','V Std','VI Std','VII Std','VIII Std','IX Std','X Std']
					low_class = 'I Std'
					high_class = 'X Std'
				elif basic_det.sch_cate.category_code=='7':
					sch_cat_chk=['VI Std','VII Std','VIII Std','IX Std','X Std']
					low_class = 'VI Std'
					high_class = 'X Std'
				elif basic_det.sch_cate.category_code=='8':
					sch_cat_chk=['IX Std','X Std']
					low_class = 'IX Std'
					high_class = 'X Std'
				elif basic_det.sch_cate.category_code=='10':
					sch_cat_chk=['IX Std','X Std','XI Std','XII Std']
					low_class = 'IX Std'
					high_class = 'XII Std'
				elif basic_det.sch_cate.category_code=='11':
					sch_cat_chk=['XI Std','XII Std']
					low_class = 'XI Std'
					high_class = 'XII Std'
				elif basic_det.sch_cate.category_code=='14':
					sch_cat_chk=['I Std','II Std','III Std','IV Std','V Std']
					low_class = 'I Std'
					high_class = 'V Std'			
				elif basic_det.sch_cate.category_code=='12':
					sch_cat_chk=['VI Std','VII Std','VIII Std']
					low_class = 'VI Std'
					high_class = 'VIII Std'
				else:
					sch_cat_chk=['I Std','II Std','III Std','IV Std','V Std','VI Std','VII Std','VIII Std','IX Std','X Std','XI Std','XII Std',]
					low_class = 'I Std'
					high_class = 'XII Std'
		

			if Academicinfo.objects.filter(school_key=basic_det.id).count()>0:
				acade_det = Academicinfo.objects.get(school_key=basic_det.id)
				acade_det = Academicinfo.objects.get(id=acade_det.id)
				instance = Academicinfo.objects.get(school_key=basic_det)
					
				if Class_section.objects.filter(school_key=basic_det.id).count()>0:
					class_det = Class_section.objects.filter(school_key=basic_det.id)
				if Staff.objects.filter(Q(school_key=basic_det.id) & Q(staff_cat=1)).count()>0:	
					teach_det = Staff.objects.filter(Q(school_key=basic_det.id) & Q(staff_cat=1))
				if Staff.objects.filter(Q(school_key=basic_det.id) & Q(staff_cat=2)).count()>0:
					nonteach_det = Staff.objects.filter(Q(school_key=basic_det.id) & Q(staff_cat=2))
				if Parttimestaff.objects.filter(school_key=basic_det.id).count()>0:
					ptime_det = Parttimestaff.objects.filter(school_key=basic_det.id)
				if Sch_groups.objects.filter(school_key=basic_det.id)>0:
					group_det = Sch_groups.objects.filter(school_key=basic_det.id)				
				
				if acade_det.recog_dt_fm!=None:
					recog_dtfm=acade_det.recog_dt_fm.strftime('%Y-%m-%d')
				if acade_det.recog_dt_to!=None:
					recog_dtto=acade_det.recog_dt_to.strftime('%Y-%m-%d')
				if acade_det.min_dt_iss!=None:
					mino_dt=acade_det.min_dt_iss.strftime('%Y-%m-%d')
				form=academicinfo_form(instance=instance)
				school_key = basic_det.id	
				schooltype = instance.schooltype
				board = instance.board
				tamil_med = instance.tamil_med
				eng_med = instance.eng_med
				tel_med = instance.tel_med
				mal_med = instance.mal_med
				kan_med = instance.kan_med
				urdu_med = instance.urdu_med
				oth_med=instance.oth_med
				other_med = instance.other_med
				minority = instance.minority
				rel_minority = instance.rel_minority
				ling_minority = instance.ling_minority
				min_ord_no = instance.min_ord_no
				min_dt_iss = instance.min_dt_iss
				recog_dt_fm = instance.recog_dt_fm
				recog_dt_to = instance.recog_dt_to
				min_dt_iss=instance.min_dt_iss
				recog_dt_fm=instance.recog_dt_fm
				recog_dt_to=instance.recog_dt_to
				iss_auth = instance.iss_auth
				start_order = instance.start_order
				start_yr=instance.start_yr
				recog_typ = instance.recog_typ
				recog_ord = instance.recog_ord
				hssstart_order = instance.hssstart_order
				hssstart_yr=instance.hssstart_yr
				hssrecog_typ = instance.hssrecog_typ
				hssrecog_ord = instance.hssrecog_ord
				hssrecog_dt_fm = instance.hssrecog_dt_fm
				hssrecog_dt_to = instance.hssrecog_dt_to
				upgr_det = instance.upgr_det
				other_board_aff = instance.other_board_aff
				spl_school = instance.spl_school
				spl_type = instance.spl_type
				boarding = instance.boarding
				hostel_floor = instance.hostel_floor
				hostel_rooms = instance.hostel_rooms
				hostel_boys = instance.hostel_boys
				hostel_girls = instance.hostel_girls
				hostel_staff = instance.hostel_staff
				extra_scout=instance.extra_scout
				extra_jrc=instance.extra_jrc
				extra_nss=instance.extra_nss
				extra_ncc=instance.extra_ncc
				extra_rrc=instance.extra_rrc
				extra_ec=instance.extra_ec
				extra_cub=instance.extra_cub
				nrstc=instance.nrstc
				hssboard=instance.hssboard			
				smc_smdc = instance.smc_smdc
				noof_med=instance.noof_med	
				dge_no_ten= instance.dge_no_ten	
				dge_no_twelve= instance.dge_no_twelve			

				return render (request,'admin_edit_new.html',locals())
			else:
				form=academicinfo_form()

				if (str(govchk)=='Un-Aided (Private) School - Other than State Board School'):
					board = basic_det.sch_directorate
					
				elif (str(govchk)=='Army Public School'):
					board ='CBSE'
					
				elif (str(govchk)=='Kendra Vidyalaya - Central Government School'):
					board ='CBSE'

				elif (str(govchk)=='Sainik School'):
					board ='CBSE'	
				else:
					board ='State Board'						
				groups_list=Groups.objects.all()	
				district_list = District.objects.all().order_by('district_name')
				noof_med=0
				return render (request,'admin_edit_new.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
	
	def post(self,request,**kwargs):
		if request.user.is_authenticated():
			pk=self.kwargs.get('pk')

			basic_det=Basicinfo.objects.get(udise_code=request.user.username)		
			form = academicinfo_form(request.POST,request.FILES)
			if Academicinfo.objects.filter(school_key=basic_det.id).count()>0:
				academic_edit=Academicinfo.objects.get(school_key=basic_det.id)

				if form.is_valid():

					if form.cleaned_data['recog_dt_fm']:
						chk_recfmdt=form.cleaned_data['recog_dt_fm']
					else:
						chk_recfmdt=None
					if form.cleaned_data['recog_dt_to']:
						chk_rectodt=form.cleaned_data['recog_dt_to']
					else:
						chk_rectodt=None

					class_sec_del = Class_section.objects.filter(school_key=basic_det.id)
					sch_key=form.cleaned_data['school_key']
					academic_edit.schooltype = form.cleaned_data['schooltype']
					academic_edit.board = form.cleaned_data['board']
					academic_edit.tamil_med = form.cleaned_data['tamil_med']
					academic_edit.eng_med = form.cleaned_data['eng_med']
					academic_edit.tel_med = form.cleaned_data['tel_med']
					academic_edit.mal_med = form.cleaned_data['mal_med']
					academic_edit.kan_med = form.cleaned_data['kan_med']
					academic_edit.urdu_med = form.cleaned_data['urdu_med']

					if request.POST['oth_med']== 'Yes':
						academic_edit.oth_med = True
						academic_edit.other_med = form.cleaned_data['other_med']
					else:
						academic_edit.oth_med = False
						academic_edit.other_med = ''	
					if form.cleaned_data['minority']==True:
						academic_edit.minority = form.cleaned_data['minority']
						academic_edit.min_ord_no = form.cleaned_data['min_ord_no']
						academic_edit.min_dt_iss = form.cleaned_data['min_dt_iss']
						academic_edit.iss_auth = form.cleaned_data['iss_auth']
						if request.POST['mino_type']=='Religious Minority':
							academic_edit.rel_minority = True
							academic_edit.ling_minority = False

						if request.POST['mino_type']=='Linguistic Minority':
							academic_edit.ling_minority = True
							academic_edit.rel_minority =False

					else:
						academic_edit.minority = False
						academic_edit.rel_minority = False
						academic_edit.ling_minority = False
						academic_edit.min_ord_no=''
						academic_edit.min_dt_iss =None
						academic_edit.iss_auth =''

					academic_edit.start_order = form.cleaned_data['start_order']
					academic_edit.start_yr = form.cleaned_data['start_yr']
					academic_edit.recog_typ = form.cleaned_data['recog_typ']
					academic_edit.recog_ord = form.cleaned_data['recog_ord']
					academic_edit.recog_dt_fm = chk_recfmdt
					academic_edit.recog_dt_to = chk_rectodt
					academic_edit.low_class = form.cleaned_data['low_class']
					academic_edit.high_class = form.cleaned_data['high_class']

					if (request.POST['high_class'] == 'XII Std'):
						academic_edit.hssstart_order = form.cleaned_data['hssstart_order']
						academic_edit.hssrecog_typ = form.cleaned_data['hssrecog_typ']
						academic_edit.hssrecog_ord = form.cleaned_data['hssrecog_ord']
						academic_edit.hssstart_yr = form.cleaned_data['hssstart_yr']
						academic_edit.hssrecog_dt_fm = form.cleaned_data['hssrecog_dt_fm']
						academic_edit.hssrecog_dt_to = form.cleaned_data['hssrecog_dt_to']	
						academic_edit.hssboard = form.cleaned_data['hssboard']

					academic_edit.upgr_det = form.cleaned_data['upgr_det']
					academic_edit.other_board_aff = form.cleaned_data['other_board_aff']

					if request.POST['spl_school']== 'True':
						academic_edit.spl_school = True
						academic_edit.spl_type = form.cleaned_data['spl_type']
					else:
						academic_edit.spl_school = False
						academic_edit.spl_type = ''
					if request.POST['boarding']== 'True':
						academic_edit.boarding = True
						academic_edit.hostel_floor = form.cleaned_data['hostel_floor']
						academic_edit.hostel_rooms = form.cleaned_data['hostel_rooms']
						academic_edit.hostel_boys = form.cleaned_data['hostel_boys']
						academic_edit.hostel_girls = form.cleaned_data['hostel_girls']
						academic_edit.hostel_staff = form.cleaned_data['hostel_staff']
					else:
						academic_edit.boarding = False
						academic_edit.hostel_floor = 0
						academic_edit.hostel_rooms = 0
						academic_edit.hostel_boys = 0
						academic_edit.hostel_girls = 0
						academic_edit.hostel_staff = 0

					academic_edit.extra_scout=form.cleaned_data['extra_scout']
					academic_edit.extra_jrc=form.cleaned_data['extra_jrc']
					academic_edit.extra_nss=form.cleaned_data['extra_nss']
					academic_edit.extra_ncc=form.cleaned_data['extra_ncc']
					academic_edit.extra_rrc=form.cleaned_data['extra_rrc']
					academic_edit.extra_ec=form.cleaned_data['extra_ec']
					academic_edit.extra_cub=form.cleaned_data['extra_cub']
					academic_edit.smc_smdc = form.cleaned_data['smc_smdc']
					academic_edit.noof_med=form.cleaned_data['noof_med']
					academic_edit.dge_no_ten=form.cleaned_data['dge_no_ten']
					academic_edit.dge_no_twelve=form.cleaned_data['dge_no_twelve']
					if form.cleaned_data['nrstc']== True:
						academic_edit.nrstc = True
					else:
						academic_edit.nrstc = False

					academic_edit.save()		

					messages.success(request,'Admininstration Details Updated successfully')
					return HttpResponseRedirect('/schoolnew/school_registration')
				else:
					print form.errors
					messages.warning(request,'Admininstration Details Not Updated')
					return HttpResponseRedirect('/schoolnew/school_registration')		
			else:

				if form.is_valid():

					sch_key=form.cleaned_data['school_key']
					if request.POST['min_dt_iss']:
						chk_dtiss=form.cleaned_data['min_dt_iss']
					else:
						chk_dtiss=None
					if request.POST['recog_dt_fm']:
						chk_recfmdt=form.cleaned_data['recog_dt_fm']
					else:
						chk_recfmdt=None
					if request.POST['recog_dt_to']:
						chk_rectodt=form.cleaned_data['recog_dt_to']
					else:
						chk_rectodt=None
					if request.POST['gov_chk']=='No':
						if request.POST['hssrecog_dt_fm']:
							chk_hssrecfmdt=form.cleaned_data['hssrecog_dt_fm']
						else:
							chk_hssrecfmdt=None
						if request.POST['hssrecog_dt_to']:
							chk_hssrectodt=form.cleaned_data['hssrecog_dt_to']
						else:
							chk_hssrectodt=None
					else:
						chk_hssrecfmdt=None
						chk_hssrectodt=None
					if request.POST['boarding'] == 'True':
						boarding_chk=True
					else:
						boarding_chk=False
						
					if request.POST['mino_type']=='Religious Minority':
						rel_minority=True
					else:
						rel_minority=False
					if request.POST['mino_type']=='Linguistic Minority':
						ling_minority=True
					else:
						ling_minority=False		

					if request.POST['oth_med']=='Yes':
						oth_med=True
					else:
						oth_med=False	

					if (request.POST['high_class'] == 'XII Std'):
						thssstart_order = request.POST['hssstart_order'],
						thssstart_yr = request.POST['hssstart_yr'],
						thssrecog_typ = request.POST['hssrecog_typ'],
						thssrecog_ord = request.POST['hssrecog_ord'],
						thssboard = request.POST['hssboard'],
					else:
						thssstart_order = ''
						thssstart_yr = ''
						thssrecog_typ = ''
						thssrecog_ord = ''
						thssboard = ''						

					academicinfo = Academicinfo(
					school_key = sch_key,			
					schooltype = form.cleaned_data['schooltype'],
					board = form.cleaned_data['board'],
					tamil_med = form.cleaned_data['tamil_med'],
					eng_med = form.cleaned_data['eng_med'],
					tel_med = form.cleaned_data['tel_med'],
					mal_med = form.cleaned_data['mal_med'],
					kan_med = form.cleaned_data['kan_med'],
					urdu_med = form.cleaned_data['urdu_med'],
					oth_med = oth_med,				
					other_med = form.cleaned_data['other_med'],
					minority = form.cleaned_data['minority'],
					rel_minority = rel_minority,
					ling_minority = ling_minority,
					min_ord_no = form.cleaned_data['min_ord_no'],
					min_dt_iss = chk_dtiss,
					iss_auth = form.cleaned_data['iss_auth'],
					start_order = form.cleaned_data['start_order'],
					start_yr = form.cleaned_data['start_yr'],
					recog_typ = form.cleaned_data['recog_typ'],
					recog_ord = form.cleaned_data['recog_ord'],
					recog_dt_fm = chk_recfmdt,
					recog_dt_to = chk_rectodt,
					low_class = form.cleaned_data['low_class'],
					high_class = form.cleaned_data['high_class'],
					hssstart_order = thssstart_order,
					hssstart_yr = thssstart_yr,
					hssrecog_typ = thssrecog_typ,
					hssrecog_ord = thssrecog_ord,
					hssrecog_dt_fm = chk_hssrecfmdt,
					hssrecog_dt_to = chk_hssrectodt,
					hssboard = thssboard,
					upgr_det = form.cleaned_data['upgr_det'],
					other_board_aff = form.cleaned_data['other_board_aff'],
					spl_school = form.cleaned_data['spl_school'],
					spl_type = form.cleaned_data['spl_type'],
					boarding = boarding_chk,
					hostel_floor = form.cleaned_data['hostel_floor'],
					hostel_rooms = form.cleaned_data['hostel_rooms'],
					hostel_boys = form.cleaned_data['hostel_boys'],
					hostel_girls = form.cleaned_data['hostel_girls'],
					hostel_staff = form.cleaned_data['hostel_staff'],
					extra_scout=form.cleaned_data['extra_scout'],
					extra_jrc=form.cleaned_data['extra_jrc'],
					extra_nss=form.cleaned_data['extra_nss'],
					extra_ncc=form.cleaned_data['extra_ncc'],
					extra_rrc=form.cleaned_data['extra_rrc'],
					extra_ec=form.cleaned_data['extra_ec'],
					extra_cub=form.cleaned_data['extra_cub'],
					nrstc = form.cleaned_data['nrstc'],
					smc_smdc = form.cleaned_data['smc_smdc'],
					noof_med = form.cleaned_data['noof_med'],
					dge_no_ten= form.cleaned_data['dge_no_ten'],
					dge_no_twelve= form.cleaned_data['dge_no_twelve'],				
					
					)
					academicinfo.save()
					messages.success(request,'Admininstration Details Added successfully')
					return HttpResponseRedirect('/schoolnew/school_registration')
					
				else:
					print form.errors
					messages.warning(request,'Admininstration Details Not Saved')

					return HttpResponseRedirect('/schoolnew/school_registration')
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	

				


class infra_edit(View):
	
	def get(self,request,**kwargs):	
		if request.user.is_authenticated():		
			district_list = District.objects.all().order_by('district_name')
			concre_chk="Yes"
			if Basicinfo.objects.filter(udise_code=request.user.username).count()>0:
				basic_det=Basicinfo.objects.get(udise_code=request.user.username)
				new_sch_id = basic_det.id

			if Academicinfo.objects.filter(school_key=basic_det.id).count()>0:
				acade_det = Academicinfo.objects.get(school_key=basic_det.id)
				if ((acade_det.high_class=='XII Std') | (acade_det.high_class=='X Std')):
					lab_chk='Yes'
				else:
					lab_chk='No'

			if Infradet.objects.filter(school_key=basic_det.id).count()>0:
				infra_det = Infradet.objects.filter(school_key=basic_det.id)
				infra_det = Infradet.objects.filter(id=infra_det)

				instance = Infradet.objects.get(school_key=basic_det)
				form=infradet_form(instance=instance)
				school_key = basic_det.id	
				electricity = instance.electricity
				tot_area= instance.tot_area
				tot_type=instance.tot_type
				cov= instance.cov
				cov_type=instance.cov_type
				opn= instance.opn
				opn_type=instance.opn_type
				play= instance.play
				play_type=instance.play_type
				tot_ft = instance.tot_ft
				tot_mt = instance.tot_mt
				covered_ft = instance.covered_ft
				covered_mt = instance.covered_mt
				open_ft = instance.open_ft
				open_mt = instance.open_mt
				play_ft = instance.play_ft
				play_mt = instance.play_mt

				cwall = instance.cwall
				cwall_concre = instance.cwall_concre
				cwall_fence = instance.cwall_fence
				cwall_existbu = instance.cwall_existbu
				cwall_nbarr = instance.cwall_nbarr
				chk_cwall=cwall

				cwall_concre_len = instance.cwall_concre_len
				cwall_fence_len = instance.cwall_fence_len
				cwall_existbu_len = instance.cwall_existbu_len
				cwall_nbarr_len = instance.cwall_nbarr_len
				cwall_notcon_len = instance.cwall_notcon_len

				fireext= instance.fireext
				fireext_no = instance.fireext_no
				fireext_w = instance.fireext_w	
				firstaid_box=instance.firstaid_box
				rainwater = instance.rainwater
				kitchenshed= instance.kitchenshed
				furn_desk_no = instance.furn_desk_no
				furn_desk_use = instance.furn_desk_use
				furn_bench_no = instance.furn_bench_no
				furn_bench_use = instance.furn_bench_use	
				fans = instance.fans
				fans_work = instance.fans_work
				tubelights = instance.tubelights
				tlights_work = instance.tlights_work
				bu_no = instance.bu_no
				bu_usable =instance.bu_usable
				bu_minrep =instance.bu_minrep
				bu_majrep =instance.bu_majrep
				gu_no =instance.gu_no
				gu_usable = instance.gu_usable
				gu_minrep =instance.gu_minrep
				gu_majrep = instance.gu_majrep
				bl_no = instance.bl_no
				bl_usable = instance.bl_usable
				bl_minrep = instance.bl_minrep
				bl_majrep = instance.bl_majrep
				gl_no = instance.gl_no
				gl_usable = instance.gl_usable
				gl_minrep =instance.gl_minrep
				gl_majrep = instance.gl_majrep
				gentsu_no = instance.gentsu_no
				gentsu_usable = instance.gentsu_usable
				gentsu_minrep = instance.gentsu_minrep
				gentsu_majrep = instance.gentsu_majrep
				ladiesu_no = instance.ladiesu_no
				ladiesu_usable = instance.ladiesu_usable
				ladiesu_minrep = instance.ladiesu_minrep
				ladiesu_majrep = instance.ladiesu_majrep
				gentsl_no = instance.gentsl_no
				gentsl_usable = instance.gentsl_usable
				gentsl_minrep = instance.gentsl_minrep
				gentsl_majrep = instance.gentsl_majrep
				ladiesl_no = instance.ladiesl_no
				ladiesl_usable = instance.ladiesl_usable
				ladiesl_minrep = instance.ladiesl_minrep
				ladiesl_majrep = instance.ladiesl_majrep
				incinirator=instance.incinirator
				water_toilet=instance.water_toilet
				cwsn_toilet = instance.cwsn_toilet
				cwsn_toilet_no = instance.cwsn_toilet_no
				water_facility=instance.water_facility
				water_source=instance.water_source
				well_dia=instance.well_dia
				well_close=instance.well_close
				water_puri=instance.water_puri
				water_access  = instance.water_access
				internet_yes = instance.internet_yes
				lightning_arest= instance.lightning_arest
				lib_tamil=instance.lib_tamil
				lib_eng=instance.lib_eng
				lib_others=instance.lib_others
				lib_tamil_news =instance.lib_tamil_news
				lib_eng_news =instance.lib_eng_news
				lib_periodic =instance.lib_periodic
				trans_faci=instance.trans_faci
				trans_bus=instance.trans_bus
				trans_van=instance.trans_van
				trans_stud=instance.trans_stud
				trans_rules=instance.trans_rules
				award_recd=instance.award_recd
				award_info =instance.award_info
				phy_lab=instance.phy_lab
				che_lab=instance.che_lab
				bot_lab=instance.bot_lab
				zoo_lab=instance.zoo_lab
				gas_cylin=instance.gas_cylin
				suffi_equip=instance.suffi_equip
				eb_ht_line=instance.eb_ht_line
				infra_edit_chk='Yes'
				if lightning_arest=="Yes":
					light_arest="Yes"
				else:
					light_arest=""

				if water_facility=="Yes":
					water_chk="Yes"
				else:
					water_chk=""

				if water_source=="Well":
					well_chk="Yes"
				else:
					well_chk=""
				govchk=basic_det.sch_management
				grp=basic_det.sch_cate
				schtype=acade_det.schooltype
				if ((str(govchk)=='School Education Department School')|(str(govchk)=='Corporation School')|(str(govchk)=='Municipal School')|(str(govchk)=='Adi-Dravida Welfare School')|(str(govchk)=='Forest Department School')|(str(govchk)=='Differently Abled Department School')|(str(govchk)=='Kallar BC/MBC Department School')|(str(govchk)=='Rubber Board School')|(str(govchk)=='Tribal Welfare School')|(str(govchk)=='Aranilayam HR&C Department School')|(str(govchk)=='Fully Aided School')|(str(govchk)=='Partly Aided School')|(str(govchk)=='Anglo Indian (Fully Aided) School')|(str(govchk)=='Anglo Indian (Partly Aided) School')|(str(govchk)=='Oriental (Fully Aided) Sanskrit School')|(str(govchk)=='Oriental (Partly Aided) Sanskrit School')|(str(govchk)=='Oriental (Fully Aided) Arabic School')|(str(govchk)=='Oriental (Partly Aided) Arabic School')|(str(govchk)=='Differently Abled Department Aided School')):
					govaid_chk='Yes'
				else:
					govaid_chk=''
				if ((str(govchk)=='School Education Department School')|(str(govchk)=='Corporation School')|(str(govchk)=='Municipal School')|(str(govchk)=='Adi-Dravida Welfare School')|(str(govchk)=='Forest Department School')|(str(govchk)=='Differently Abled Department School')|(str(govchk)=='Kallar BC/MBC Department School')|(str(govchk)=='Rubber Board School')|(str(govchk)=='Tribal Welfare School')|(str(govchk)=='Aranilayam HR&C Department School')):	
					gov_chk='Yes'
				else:
					gov_chk='No'				
					
				if ((str(grp)=='Hr.Sec School (I-XII)')|(str(grp)=='Hr.Sec School (VI-XII)')|(str(grp)=='Hr.Sec School (IX-XII)')|(str(grp)=='Hr.Sec School (XI-XII)')|(str(grp)=='Middle School (I-VIII)')|(str(grp)=='Middle School (VI-VIII)')|(str(grp)=='High Schools (I-X)')|(str(grp)=='High Schools (VI-X)')|(str(grp)=='High Schools (IX-X)')|(str(grp)=='KGBV')):
					if acade_det.schooltype<>'Boys':
						inci_chk='Yes'
					else:
						inci_chk=''	
				else:
					inci_chk=''	

				return render (request,'infra_edit_new.html',locals())			
			else: 
				form=infradet_form()
				govchk=basic_det.sch_management
				grp=basic_det.sch_cate
				hi_class=acade_det.high_class
				schtype=acade_det.schooltype			
				if ((str(govchk)=='School Education Department School')|(str(govchk)=='Corporation School')|(str(govchk)=='Municipal School')|(str(govchk)=='Adi-Dravida Welfare School')|(str(govchk)=='Forest Department School')|(str(govchk)=='Differently Abled Department School')|(str(govchk)=='Kallar BC/MBC Department School')|(str(govchk)=='Rubber Board School')|(str(govchk)=='Tribal Welfare School')|(str(govchk)=='Aranilayam HR&C Department School')|(str(govchk)=='Fully Aided School')|(str(govchk)=='Partly Aided School')|(str(govchk)=='Anglo Indian (Fully Aided) School')|(str(govchk)=='Anglo Indian (Partly Aided) School')|(str(govchk)=='Oriental (Fully Aided) Sanskrit School')|(str(govchk)=='Oriental (Partly Aided) Sanskrit School')|(str(govchk)=='Oriental (Fully Aided) Arabic School')|(str(govchk)=='Oriental (Partly Aided) Arabic School')|(str(govchk)=='Differently Abled Department Aided School')):
					govaid_chk='Yes'
				else:
					govaid_chk=''
					
				if ((str(grp)=='Hr.Sec School (I-XII)')|(str(grp)=='Hr.Sec School (VI-XII)')|(str(grp)=='Hr.Sec School (IX-XII)')|(str(grp)=='Hr.Sec School (XI-XII)')|(str(grp)=='Middle School (I-VIII)')|(str(grp)=='Middle School (VI-VIII)')|(str(grp)=='High Schools (I-X)')|(str(grp)=='High Schools (VI-X)')|(str(grp)=='High Schools (IX-X)')|(str(grp)=='KGBV')):
					if acade_det.schooltype<>'Boys':
						inci_chk='Yes'
					else:
						inci_chk=''	
				else:
					inci_chk=''	
				infra_edit_chk=''
				if ((str(govchk)=='School Education Department School')|(str(govchk)=='Corporation School')|(str(govchk)=='Municipal School')|(str(govchk)=='Adi-Dravida Welfare School')|(str(govchk)=='Forest Department School')|(str(govchk)=='Differently Abled Department School')|(str(govchk)=='Kallar BC/MBC Department School')|(str(govchk)=='Rubber Board School')|(str(govchk)=='Tribal Welfare School')|(str(govchk)=='Aranilayam HR&C Department School')):	
					gov_chk='Yes'
				else:
					gov_chk='No'					
				return render (request,'infra_edit_new.html',locals())
	
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
	def post(self,request,**kwargs):
		if request.user.is_authenticated():		
			basic_det=Basicinfo.objects.get(udise_code=request.user.username)	
			form = infradet_form(request.POST,request.FILES)	
			if Infradet.objects.filter(school_key=basic_det.id).count()>0:	
				infra_edit=Infradet.objects.get(school_key=basic_det.id)

				if form.is_valid():

					infra_edit.electricity = form.cleaned_data['electricity']
					infra_edit.tot_area= form.cleaned_data['tot_area']
					infra_edit.tot_type=form.cleaned_data['tot_type']
					infra_edit.cov= form.cleaned_data['cov']
					infra_edit.cov_type=form.cleaned_data['cov_type']
					infra_edit.opn= form.cleaned_data['opn']
					infra_edit.opn_type=form.cleaned_data['opn_type']
					infra_edit.play= form.cleaned_data['play']
					infra_edit.play_type=form.cleaned_data['play_type']
					infra_edit.tot_ft = form.cleaned_data['tot_ft']
					infra_edit.tot_mt = form.cleaned_data['tot_mt']
					infra_edit.covered_ft = form.cleaned_data['covered_ft']
					infra_edit.covered_mt = form.cleaned_data['covered_mt']
					infra_edit.open_ft = form.cleaned_data['open_ft']
					infra_edit.open_mt = form.cleaned_data['open_mt']
					infra_edit.play_ft = form.cleaned_data['play_ft']
					infra_edit.play_mt = form.cleaned_data['play_mt']
					infra_edit.cwall_notcon_len = form.cleaned_data['cwall_notcon_len']
					chk_cwal=request.POST['cwall']
					if request.POST['cwall']=='Yes':
						infra_edit.cwall = True
						if form.cleaned_data['cwall_concre']==True:
							infra_edit.cwall_concre = form.cleaned_data['cwall_concre']
							infra_edit.cwall_concre_len = form.cleaned_data['cwall_concre_len']
						else:
							infra_edit.cwall_concre = form.cleaned_data['cwall_concre']
							infra_edit.cwall_concre_len = 0
						if form.cleaned_data['cwall_fence']==True:
							infra_edit.cwall_fence = form.cleaned_data['cwall_fence']
							infra_edit.cwall_fence_len = form.cleaned_data['cwall_fence_len']
						else:
							infra_edit.cwall_fence = form.cleaned_data['cwall_fence']
							infra_edit.cwall_fence_len = 0
						if 	form.cleaned_data['cwall_existbu']==True:
							infra_edit.cwall_existbu = form.cleaned_data['cwall_existbu']
							infra_edit.cwall_existbu_len = form.cleaned_data['cwall_existbu_len']
						else:
							infra_edit.cwall_existbu = form.cleaned_data['cwall_existbu']
							infra_edit.cwall_existbu_len = 0						
						if form.cleaned_data['cwall_nbarr']==True:
							infra_edit.cwall_nbarr = form.cleaned_data['cwall_nbarr']
							infra_edit.cwall_nbarr_len = form.cleaned_data['cwall_nbarr_len']
						else:
							infra_edit.cwall_nbarr = form.cleaned_data['cwall_nbarr']
							infra_edit.cwall_nbarr_len = 0
					else:
						infra_edit.cwall = False
						infra_edit.cwall_concre = False
						infra_edit.cwall_fence = False
						infra_edit.cwall_existbu = False
						infra_edit.cwall_nbarr = False
						infra_edit.cwall_concre_len = 0
						infra_edit.cwall_fence_len = 0
						infra_edit.cwall_existbu_len = 0
						infra_edit.cwall_nbarr_len = 0


					if form.cleaned_data['fireext']==True:
						infra_edit.fireext= True
						infra_edit.fireext_no = form.cleaned_data['fireext_no']
						infra_edit.fireext_w = form.cleaned_data['fireext_w']
					else:
						infra_edit.fireext= False
						infra_edit.fireext_no = 0
						infra_edit.fireext_w = 0

					infra_edit.firstaid_box=form.cleaned_data['firstaid_box']
					infra_edit.rainwater = form.cleaned_data['rainwater']
					infra_edit.kitchenshed= form.cleaned_data['kitchenshed']
					infra_edit.furn_desk_no = form.cleaned_data['furn_desk_no']
					infra_edit.furn_desk_use = form.cleaned_data['furn_desk_use']
					infra_edit.furn_bench_no = form.cleaned_data['furn_bench_no']
					infra_edit.furn_bench_use = form.cleaned_data['furn_bench_use']
					infra_edit.fans = form.cleaned_data['fans']
					infra_edit.fans_work = form.cleaned_data['fans_work']
					infra_edit.tubelights = form.cleaned_data['tubelights']
					infra_edit.tlights_work = form.cleaned_data['tlights_work']
					infra_edit.bu_no = form.cleaned_data['bu_no']
					infra_edit.bu_usable =form.cleaned_data['bu_usable']
					infra_edit.bu_minrep =form.cleaned_data['bu_minrep']
					infra_edit.bu_majrep =form.cleaned_data['bu_majrep']
					infra_edit.gu_no =form.cleaned_data['gu_no']
					infra_edit.gu_usable = form.cleaned_data['gu_usable']
					infra_edit.gu_minrep =form.cleaned_data['gu_minrep']
					infra_edit.gu_majrep = form.cleaned_data['gu_majrep']
					infra_edit.bl_no = form.cleaned_data['bl_no']
					infra_edit.bl_usable = form.cleaned_data['bl_usable']
					infra_edit.bl_minrep = form.cleaned_data['bl_minrep']
					infra_edit.bl_majrep = form.cleaned_data['bl_majrep']
					infra_edit.gl_no = form.cleaned_data['gl_no']
					infra_edit.gl_usable = form.cleaned_data['gl_usable']
					infra_edit.gl_minrep =form.cleaned_data['gl_minrep']
					infra_edit.gl_majrep = form.cleaned_data['gl_majrep']
					infra_edit.gentsu_no = form.cleaned_data['gentsu_no']
					infra_edit.gentsu_usable = form.cleaned_data['gentsu_usable']
					infra_edit.gentsu_minrep = form.cleaned_data['gentsu_minrep']
					infra_edit.gentsu_majrep = form.cleaned_data['gentsu_majrep']
					infra_edit.ladiesu_no = form.cleaned_data['ladiesu_no']
					infra_edit.ladiesu_usable = form.cleaned_data['ladiesu_usable']
					infra_edit.ladiesu_minrep = form.cleaned_data['ladiesu_minrep']
					infra_edit.ladiesu_majrep = form.cleaned_data['ladiesu_majrep']
					infra_edit.gentsl_no = form.cleaned_data['gentsl_no']
					infra_edit.gentsl_usable = form.cleaned_data['gentsl_usable']
					infra_edit.gentsl_minrep = form.cleaned_data['gentsl_minrep']
					infra_edit.gentsl_majrep = form.cleaned_data['gentsl_majrep']
					infra_edit.ladiesl_no = form.cleaned_data['ladiesl_no']
					infra_edit.ladiesl_usable = form.cleaned_data['ladiesl_usable']
					infra_edit.ladiesl_minrep = form.cleaned_data['ladiesl_minrep']
					infra_edit.ladiesl_majrep = form.cleaned_data['ladiesl_majrep']
					infra_edit.incinirator=form.cleaned_data['incinirator']
					infra_edit.water_toilet=form.cleaned_data['water_toilet']
					infra_edit.internet_yes=form.cleaned_data['internet_yes']

					if request.POST['cwsn_toilet']==True:
						infra_edit.cwsn_toilet = True
						infra_edit.cwsn_toilet_no = form.cleaned_data['cwsn_toilet_no']
					else:
						infra_edit.cwsn_toilet = False
						infra_edit.cwsn_toilet_no = 0
					infra_edit.water_facility=form.cleaned_data['water_facility']
					infra_edit.water_source=form.cleaned_data['water_source']
					infra_edit.well_dia=form.cleaned_data['well_dia']
					infra_edit.well_close=form.cleaned_data['well_close']
					infra_edit.water_puri=form.cleaned_data['water_puri']
					infra_edit.water_access  = form.cleaned_data['water_access']
					infra_edit.lightning_arest= form.cleaned_data['lightning_arest']
					infra_edit.lib_tamil = form.cleaned_data['lib_tamil']
					infra_edit.lib_eng = form.cleaned_data['lib_eng']
					infra_edit.lib_others = form.cleaned_data['lib_others']
					infra_edit.lib_tamil_news = form.cleaned_data['lib_tamil_news']
					infra_edit.lib_eng_news = form.cleaned_data['lib_eng_news']
					infra_edit.lib_periodic = form.cleaned_data['lib_periodic']
						
					if request.POST['gov_chk']=='No':	
						if request.POST['trans_faci']=='True':
							infra_edit.trans_faci = True
							infra_edit.trans_bus= form.cleaned_data['trans_bus']
							infra_edit.trans_van= form.cleaned_data['trans_van']
							infra_edit.trans_stud= form.cleaned_data['trans_stud']
							infra_edit.trans_rules= form.cleaned_data['trans_rules']
						else:
							infra_edit.trans_faci = False
							infra_edit.trans_bus= None
							infra_edit.trans_van= None
							infra_edit.trans_stud= None
							infra_edit.trans_rules= False
					else:
						infra_edit.trans_faci = False
						infra_edit.trans_bus= None
						infra_edit.trans_van= None
						infra_edit.trans_stud= None
						infra_edit.trans_rules= False

					if request.POST['award_recd']=='True':
						infra_edit.award_recd = True
						infra_edit.award_info = form.cleaned_data['award_info']
					else:
						infra_edit.award_recd = False
						infra_edit.award_info = ''			
					infra_edit.phy_lab= form.cleaned_data['phy_lab']
					infra_edit.che_lab= form.cleaned_data['che_lab']
					infra_edit.bot_lab= form.cleaned_data['bot_lab']
					infra_edit.zoo_lab= form.cleaned_data['zoo_lab']
					infra_edit.gas_cylin= form.cleaned_data['gas_cylin']
					infra_edit.suffi_equip= form.cleaned_data['suffi_equip']
					infra_edit.eb_ht_line= form.cleaned_data['eb_ht_line']
					infra_edit.save()
					messages.success(request,'Infrastructure Details Updated successfully')
					return HttpResponseRedirect('/schoolnew/school_registration')
				else:
					messages.warning(request,'Infrastructure Details Not Updated')

					return HttpResponseRedirect('/schoolnew/school_registration')		
			else:

				if form.is_valid():

					if form.cleaned_data['cwall']=='Yes':
						post_cwall=True
						if form.cleaned_data['cwall_concre']==True:
							cwall_concre = form.cleaned_data['cwall_concre']
							cwall_concre_len = form.cleaned_data['cwall_concre_len']
						else:
							cwall_concre = form.cleaned_data['cwall_concre']
							cwall_concre_len = 0
						if form.cleaned_data['cwall_fence']==True:
							cwall_fence = form.cleaned_data['cwall_fence']
							cwall_fence_len = form.cleaned_data['cwall_fence_len']
						else:
							cwall_fence = form.cleaned_data['cwall_fence']
							cwall_fence_len = 0
						if 	form.cleaned_data['cwall_existbu']==True:
							cwall_existbu = form.cleaned_data['cwall_existbu']
							cwall_existbu_len = form.cleaned_data['cwall_existbu_len']
						else:
							cwall_existbu = form.cleaned_data['cwall_existbu']
							cwall_existbu_len = 0						
						if form.cleaned_data['cwall_nbarr']==True:
							cwall_nbarr = form.cleaned_data['cwall_nbarr']
							cwall_nbarr_len = form.cleaned_data['cwall_nbarr_len']
						else:
							cwall_nbarr = form.cleaned_data['cwall_nbarr']
							cwall_nbarr_len = 0
					else:
						post_cwall=False
						cwall_concre = False
						cwall_fence = False
						cwall_existbu = False
						cwall_nbarr = False
						cwall_concre_len = 0
						cwall_fence_len = 0
						cwall_existbu_len = 0
						cwall_nbarr_len = 0



					sch_key=form.cleaned_data['school_key']
					ss=form.cleaned_data['open_ft']
					ss1=form.cleaned_data['open_mt']
					if request.POST['gov_chk']=='No':
						if request.POST['trans_faci']=='True':
							chktrans_faci = True
							chktrans_bus= form.cleaned_data['trans_bus']
							chktrans_van= form.cleaned_data['trans_van']
							chktrans_stud= form.cleaned_data['trans_stud']
							chktrans_rules= form.cleaned_data['trans_rules']
						else:
							chktrans_faci = False
							chktrans_bus= None
							chktrans_van= None
							chktrans_stud= None
							chktrans_rules= False	
					else:
						chktrans_faci = False
						chktrans_bus= None
						chktrans_van= None
						chktrans_stud= None
						chktrans_rules= False
					infradet=Infradet(
					school_key = sch_key,
					electricity = form.cleaned_data['electricity'],
					tot_area= form.cleaned_data['tot_area'],
					tot_type=form.cleaned_data['tot_type'],
					cov= form.cleaned_data['cov'],
					cov_type=form.cleaned_data['cov_type'],
					opn= form.cleaned_data['opn'],
					opn_type=form.cleaned_data['opn_type'],
					play= form.cleaned_data['play'],
					play_type=form.cleaned_data['play_type'],

					tot_ft = form.cleaned_data['tot_ft'],
					tot_mt = form.cleaned_data['tot_mt'],
					covered_ft = form.cleaned_data['covered_ft'],
					covered_mt = form.cleaned_data['covered_mt'],
					open_ft = form.cleaned_data['open_ft'],
					open_mt = form.cleaned_data['open_mt'],
					play_ft = form.cleaned_data['play_ft'],
					play_mt = form.cleaned_data['play_mt'],
					cwall = post_cwall,
					cwall_concre = cwall_concre,
					cwall_fence = cwall_fence,
					cwall_existbu = cwall_existbu ,
					cwall_nbarr = cwall_nbarr,
					cwall_concre_len = cwall_concre_len,
					cwall_fence_len = cwall_fence_len,
					cwall_existbu_len = cwall_existbu_len,
					cwall_nbarr_len = cwall_nbarr_len,
					cwall_notcon_len = form.cleaned_data['cwall_notcon_len'],
					fireext= form.cleaned_data['fireext'],
					fireext_no = form.cleaned_data['fireext_no'],
					fireext_w = form.cleaned_data['fireext_w'],
					firstaid_box=form.cleaned_data['firstaid_box'],
					rainwater = form.cleaned_data['rainwater'],
					kitchenshed= form.cleaned_data['kitchenshed'],
					furn_desk_no = form.cleaned_data['furn_desk_no'],
					furn_desk_use = form.cleaned_data['furn_desk_use'],
					furn_bench_no = form.cleaned_data['furn_bench_no'],
					furn_bench_use = form.cleaned_data['furn_bench_use'],
					fans = form.cleaned_data['fans'],
					fans_work = form.cleaned_data['fans_work'],
					tubelights = form.cleaned_data['tubelights'],
					tlights_work = form.cleaned_data['tlights_work'],
					bu_no = form.cleaned_data['bu_no'],
					bu_usable =form.cleaned_data['bu_usable'],
					bu_minrep =form.cleaned_data['bu_minrep'],
					bu_majrep =form.cleaned_data['bu_majrep'],
					gu_no =form.cleaned_data['gu_no'],
					gu_usable = form.cleaned_data['gu_usable'],
					gu_minrep =form.cleaned_data['gu_minrep'],
					gu_majrep = form.cleaned_data['gu_majrep'],
					bl_no = form.cleaned_data['bl_no'],
					bl_usable = form.cleaned_data['bl_usable'],
					bl_minrep = form.cleaned_data['bl_minrep'],
					bl_majrep = form.cleaned_data['bl_majrep'],
					gl_no = form.cleaned_data['gl_no'],
					gl_usable = form.cleaned_data['gl_usable'],
					gl_minrep =form.cleaned_data['gl_minrep'],
					gl_majrep = form.cleaned_data['gl_majrep'],
					gentsu_no = form.cleaned_data['gentsu_no'],
					gentsu_usable = form.cleaned_data['gentsu_usable'],
					gentsu_minrep = form.cleaned_data['gentsu_minrep'],
					gentsu_majrep = form.cleaned_data['gentsu_majrep'],
					ladiesu_no = form.cleaned_data['ladiesu_no'],
					ladiesu_usable = form.cleaned_data['ladiesu_usable'],
					ladiesu_minrep = form.cleaned_data['ladiesu_minrep'],
					ladiesu_majrep = form.cleaned_data['ladiesu_majrep'],
					gentsl_no = form.cleaned_data['gentsl_no'],
					gentsl_usable = form.cleaned_data['gentsl_usable'],
					gentsl_minrep = form.cleaned_data['gentsl_minrep'],
					gentsl_majrep = form.cleaned_data['gentsl_majrep'],
					ladiesl_no = form.cleaned_data['ladiesl_no'],
					ladiesl_usable = form.cleaned_data['ladiesl_usable'],
					ladiesl_minrep = form.cleaned_data['ladiesl_minrep'],
					ladiesl_majrep = form.cleaned_data['ladiesl_majrep'],
					incinirator=form.cleaned_data['incinirator'],
					water_toilet = form.cleaned_data['water_toilet'],			
					cwsn_toilet = form.cleaned_data['cwsn_toilet'],
					cwsn_toilet_no = form.cleaned_data['cwsn_toilet_no'],
					water_facility=form.cleaned_data['water_facility'],
					water_source=form.cleaned_data['water_source'],
					well_dia=form.cleaned_data['well_dia'],
					well_close=form.cleaned_data['well_close'],
					water_puri=form.cleaned_data['water_puri'],
					water_access  = form.cleaned_data['water_access'],
					internet_yes = form.cleaned_data['internet_yes'],
					lightning_arest= form.cleaned_data['lightning_arest'],
					lib_tamil = form.cleaned_data['lib_tamil'],
					lib_eng = form.cleaned_data['lib_eng'],
					lib_others = form.cleaned_data['lib_others'],
					lib_tamil_news = form.cleaned_data['lib_tamil_news'],
					lib_eng_news = form.cleaned_data['lib_eng_news'],
					lib_periodic = form.cleaned_data['lib_periodic'],
					trans_faci= chktrans_faci,
					trans_bus= chktrans_bus,
					trans_van= chktrans_van,
					trans_stud= chktrans_stud,
					trans_rules= chktrans_rules,
					award_recd= form.cleaned_data['award_recd'],
					award_info = form.cleaned_data['award_info'],
					phy_lab= form.cleaned_data['phy_lab'],
					che_lab= form.cleaned_data['che_lab'],
					bot_lab= form.cleaned_data['bot_lab'],
					zoo_lab= form.cleaned_data['zoo_lab'],
					gas_cylin= form.cleaned_data['gas_cylin'],
					suffi_equip= form.cleaned_data['suffi_equip'],
					eb_ht_line= form.cleaned_data['eb_ht_line'],

					)
					infradet.save()

					messages.success(request,'Infrastructure Details Added successfully')

					return HttpResponseRedirect('/schoolnew/school_registration')				
				else:
					messages.warning(request,'Infrastructure Details Not Saved')
					return HttpResponseRedirect('/schoolnew/school_registration')
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
class class_section_edit(View):
	
	def get(self,request,**kwargs):
		if request.user.is_authenticated():
			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			acade_det = Academicinfo.objects.get(school_key=basic_det.id)
			sch_key = basic_det.id
			sch_clas_exist=School_category.objects.get(id=basic_det.sch_cate_id)
			class_det = Class_section.objects.filter(school_key=sch_key)
			govchk=basic_det.sch_management
			if ((str(govchk)=='Fully Aided School')|(str(govchk)=='Partly Aided School')|(str(govchk)=='Anglo Indian (Fully Aided) School')|(str(govchk)=='Anglo Indian (Partly Aided) School')|(str(govchk)=='Oriental (Fully Aided) Sanskrit School')|(str(govchk)=='Oriental (Partly Aided) Sanskrit School')|(str(govchk)=='Oriental (Fully Aided) Arabic School')|(str(govchk)=='Oriental (Partly Aided) Arabic School')|(str(govchk)=='Differently Abled Department Aided School')):
				aid_chk='Yes'
			else:
				aid_chk=''

			if basic_det.prekg=='Yes':
				prekg_chk='Yes'
			else:
				prekg_chk='No'

			if basic_det.kgsec=='Yes':
				kgsec_chk='Yes'
			else:
				kgsec_chk='No'		

			if sch_clas_exist.category_code=='1':
				sch_cat_chk=['I Std','II Std','III Std','IV Std','V Std']
			elif sch_clas_exist.category_code=='2':
				sch_cat_chk=['I Std','II Std','III Std','IV Std','V Std','VI Std','VII Std','VIII Std']
			elif sch_clas_exist.category_code=='3':
				sch_cat_chk=['I Std','II Std','III Std','IV Std','V Std','VI Std','VII Std','VIII Std','IX Std','X Std','XI Std','XII Std']
			elif sch_clas_exist.category_code=='4':
				sch_cat_chk=['VI Std','VII Std','VIII Std']
			elif sch_clas_exist.category_code=='5':
				sch_cat_chk=['VI Std','VII Std','VIII Std','IX Std','X Std','XI Std','XII Std',]
			elif sch_clas_exist.category_code=='6':
				sch_cat_chk=['I Std','II Std','III Std','IV Std','V Std','VI Std','VII Std','VIII Std','IX Std','X Std']
			elif sch_clas_exist.category_code=='7':
				sch_cat_chk=['VI Std','VII Std','VIII Std','IX Std','X Std']
			elif sch_clas_exist.category_code=='8':
				sch_cat_chk=['IX Std','X Std']
			elif sch_clas_exist.category_code=='10':
				sch_cat_chk=['IX Std','X Std','XI Std','XII Std']
			elif sch_clas_exist.category_code=='11':
				sch_cat_chk=['XI Std','XII Std']
			elif sch_clas_exist.category_code=='14':
				sch_cat_chk=['I Std','II Std','III Std','IV Std','V Std']
			elif sch_clas_exist.category_code=='12':
				sch_cat_chk=['VI Std','VII Std','VIII Std']
			else:
				sch_cat_chk=['I Std','II Std','III Std','IV Std','V Std','VI Std','VII Std','VIII Std','IX Std','X Std','XI Std','XII Std',]
			form=class_section_form()

			if (Class_section.objects.filter(school_key=sch_key).count())>0:
				class_det = Class_section.objects.filter(school_key=sch_key).order_by('id')
				
			else:
				if basic_det.prekg=='Yes':
						newclass = Class_section(
							school_key=basic_det,
							class_id = 'Pre-KG',
							sections = 0,
							no_sec_aided=0,
							no_stud=0,
							)
						newclass.save()	
										
				if basic_det.kgsec=='Yes':
						newclass = Class_section(
							school_key=basic_det,
							class_id = 'LKG',
							sections = 0,
							no_sec_aided=0,
							no_stud=0,
							)
						newclass.save()
						newclass = Class_section(
							school_key=basic_det,
							class_id = 'UKG',
							sections = 0,
							no_sec_aided=0,
							no_stud=0,
							)
						newclass.save()
					
				for entry in range(len(sch_cat_chk)):
						newclass = Class_section(
							school_key=basic_det,
							class_id = sch_cat_chk[entry],
							sections = 0,
							no_sec_aided=0,
							no_stud=0,
							)
						newclass.save()	
				class_det = Class_section.objects.filter(school_key=sch_key)

		
			if (acade_det.tel_med | acade_det.mal_med| acade_det.kan_med| acade_det.urdu_med | acade_det.oth_med):
				oth_med_stren=True
			else:
				oth_med_stren=False	
			return render (request,'class_section_table_edit.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	

	
	def post(self,request,**kwargs):
		if request.user.is_authenticated():

			tid=self.kwargs.get('pk')
			form = class_section_form(request.POST,request.FILES)

			basic_det=Basicinfo.objects.get(udise_code=request.user.username)		
			academic_edit=Academicinfo.objects.get(school_key=basic_det.id)	
			sch_key = basic_det.id
			class_det = Class_section.objects.filter(school_key=sch_key).order_by('id')
			try:	
				if form.is_valid():
					sch_key=form.cleaned_data['school_key']
					schsec = request.POST.getlist('sections')
					schaid = request.POST.getlist('no_sec_aided')
					stud_coun = request.POST.getlist('no_stud')
					tamstu=request.POST.getlist('tam_stud')
					engstu=request.POST.getlist('eng_stud')
					othstu=request.POST.getlist('oth_stud')
					cwsnstu=request.POST.getlist('cwsn_stud_no')
					counter=0			
					for i in class_det:
						class_edit = Class_section.objects.get(id=i.id)
						class_edit.sections=schsec[counter]
						if len(schaid)>0:
							class_edit.no_sec_aided=schaid[counter]
						class_edit.no_stud=stud_coun[counter]
						if len(tamstu)>0:
							class_edit.tam_stud=tamstu[counter]
						if len(engstu)>0:
							class_edit.eng_stud=engstu[counter]
						if len(othstu)>0:
							class_edit.oth_stud=othstu[counter]	
						class_edit.cwsn_stud_no=cwsnstu[counter]																
						class_edit.save()
						counter+=1
					messages.success(request,'Class & Section Details Updated successfully')
					return HttpResponseRedirect('/schoolnew/school_registration')

				else:
					messages.warning(request,'No. sections allowed is Min. 1 Max.30 - Hence Not Saved')
					return HttpResponseRedirect('/schoolnew/class_section_edit')
			except Exception:
				pass
			return HttpResponseRedirect('/schoolnew/class_section_edit/')
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
			
class Teaching_edit(View):
	
	def get(self,request,**kwargs):
		if request.user.is_authenticated():
			tid=self.kwargs.get('pk')
			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			sch_key = basic_det.id
			post_det = Staff.objects.filter(Q(school_key=sch_key) & Q(staff_cat=1))
			form=staff_form()
			chk_catid=School_category.objects.get(id=basic_det.sch_cate_id)
			pg_head='Teaching'
			if ((chk_catid.category_code=='1')|(chk_catid=='11')):			
				desig_det= User_desig.objects.filter(Q(user_cate='SCHOOL') & Q(user_level__isnull=True)|Q(user_level='PS')).exclude(user_cate='SCHOOL&OFFICE') 
			elif ((chk_catid.category_code=='2')|(chk_catid.category_code=='4')|(chk_catid.category_code=='12')):
				desig_det= User_desig.objects.filter(Q(user_cate='SCHOOL') & Q(user_level__isnull=True)|Q(user_level='MS')|Q(user_level='HRHSMS')).exclude(user_cate='SCHOOL&OFFICE')
			elif ((chk_catid.category_code=='6')|(chk_catid.category_code=='7')|(chk_catid.category_code=='8')) :
				desig_det= User_desig.objects.filter(Q(user_cate='SCHOOL') & Q(user_level__isnull=True)|Q(user_level='HS')|Q(user_level='HRHS')|Q(user_level='HRHSMS')).exclude(user_cate='SCHOOL&OFFICE')
			elif ((chk_catid.category_code=='3')|(chk_catid.category_code=='5')|(chk_catid.category_code=='9')|(chk_catid.category_code=='10')):
				desig_det= User_desig.objects.filter(Q(user_cate='SCHOOL') & Q(user_level__isnull=True)|Q(user_level='HR')|Q(user_level='HRHS')|Q(user_level='HRHSMS')).exclude(user_cate='SCHOOL&OFFICE')
			else:
				desig_det= User_desig.objects.filter(Q(user_cate='SCHOOL') & Q(user_level__isnull=True)).exclude(user_cate='SCHOOL&OFFICE')

			return render (request,'post_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
	def post(self,request,**kwargs):
		if request.user.is_authenticated():		
			pk=self.kwargs.get('pk')
		
			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			form = staff_form(request.POST,request.FILES)
			if form.is_valid():
				sch_key=form.cleaned_data['school_key']
				chk_post=form.cleaned_data['post_name']
				
				if (Staff.objects.filter(school_key=sch_key).count())>0:
					
					if(chk_post.id in(85,70,50,51)):
						if Staff.objects.filter(school_key=basic_det.id).filter(post_name=form.cleaned_data['post_name']).exists():
							messages.warning(request,'Headmaster post santion details already entered, if you want to correct pl. use Update option')						
							return HttpResponseRedirect('/schoolnew/teaching_edit/')
						else:
							if request.POST['post_mode']=='Permanent':
								tpost_GO_pd = ''
								ttemgofm_dt = None
								ttemgoto_dt = None
							else:
								tpost_GO_pd = form.cleaned_data['post_GO_pd']
								ttemgofm_dt = form.cleaned_data['temgofm_dt']
								ttemgoto_dt = form.cleaned_data['temgoto_dt']	

							newteachpost = Staff(
							school_key=sch_key,	
							post_name = form.cleaned_data['post_name'],
							post_sub = form.cleaned_data['post_sub'],					
							post_sanc = form.cleaned_data['post_sanc'],
							post_mode = form.cleaned_data['post_mode'],
							post_GO = form.cleaned_data['post_GO'],
							post_GO_dt = form.cleaned_data['post_GO_dt'],
							post_filled = 0,
							post_vac = form.cleaned_data['post_sanc'],
							post_GO_pd = tpost_GO_pd,
							temgofm_dt = ttemgofm_dt,
							temgoto_dt = ttemgoto_dt,
							staff_cat = 1,
							)
							newteachpost.save()
							messages.success(request,'Post Sanction Details addedded successfully')
							return HttpResponseRedirect('/schoolnew/teaching_edit/')	
					else:
						if request.POST['post_mode']=='Permanent':
							tpost_GO_pd = ''
							ttemgofm_dt = None
							ttemgoto_dt = None
						else:
							tpost_GO_pd = form.cleaned_data['post_GO_pd']
							ttemgofm_dt = form.cleaned_data['temgofm_dt']
							ttemgoto_dt = form.cleaned_data['temgoto_dt']	

						newteachpost = Staff(
						school_key=sch_key,
						post_name = form.cleaned_data['post_name'],
						post_sub = form.cleaned_data['post_sub'],					
						post_sanc = form.cleaned_data['post_sanc'],
						post_mode = form.cleaned_data['post_mode'],
						post_GO = form.cleaned_data['post_GO'],
						post_GO_dt = form.cleaned_data['post_GO_dt'],
						post_filled = 0,
						post_vac = form.cleaned_data['post_sanc'],						
						post_GO_pd = tpost_GO_pd,
						temgofm_dt = ttemgofm_dt,
						temgoto_dt = ttemgoto_dt,
						staff_cat = 1,
						)
						newteachpost.save()
						messages.success(request,'Post Sanction Details addedded successfully')
						return HttpResponseRedirect('/schoolnew/teaching_edit/')

				else:
					if request.POST['post_mode']=='Permanent':
						tpost_GO_pd = ''
						ttemgofm_dt = None
						ttemgoto_dt = None
					else:
						tpost_GO_pd = form.cleaned_data['post_GO_pd']
						ttemgofm_dt = form.cleaned_data['temgofm_dt']
						ttemgoto_dt = form.cleaned_data['temgoto_dt']				
					newteachpost = Staff(
					school_key=sch_key,
					post_name = form.cleaned_data['post_name'],
					post_sub = form.cleaned_data['post_sub'],
					post_sanc = form.cleaned_data['post_sanc'],
					post_mode = form.cleaned_data['post_mode'],
					post_GO = form.cleaned_data['post_GO'],
					post_GO_dt = form.cleaned_data['post_GO_dt'],
					post_filled = 0,
					post_vac = form.cleaned_data['post_sanc'],					
					post_GO_pd = tpost_GO_pd,
					temgofm_dt = ttemgofm_dt,
					temgoto_dt = ttemgoto_dt,
					staff_cat = 1,
					)
					newteachpost.save()
					messages.success(request,'Post Sanction Details addedded successfully')
					return HttpResponseRedirect('/schoolnew/teaching_edit/')
			else:
				print form.errors
				messages.warning(request,'Post Sanction Details Not Saved')
				return render (request,'post_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
class Teaching_delete(View):
	
	def get(self, request,**kwargs):
		if request.user.is_authenticated():  	
			tid=self.kwargs.get('pk')
			data=Staff.objects.get(id=tid)
			data.delete()
			msg= str(data.post_name)+" - Posts has been successfully removed "
			messages.success(request, msg ) 
			return HttpResponseRedirect('/schoolnew/teaching_edit/')
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
class Teaching_update(View):
	
	def get(self,request,**kwargs):
		if request.user.is_authenticated():	
			tid=self.kwargs.get('pk')
			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			instance=Staff.objects.get(id=tid)
			staff_det_dt=Staff.objects.get(id=tid)
			form=staff_form(instance=instance)
			post_name= instance.post_name
			post_sub= instance.post_sub
			id_tpost_sub=post_sub.id	
			post_sanc=instance.post_sanc
			post_mode= instance.post_mode
			post_GO= instance.post_GO
			go_dt= instance.post_GO_dt		
			post_GO_dt= instance.post_GO_dt
			post_GO_pd= instance.post_GO_pd
			post_filled= instance.post_filled
			post_vac= instance.post_vac
			post_filled = instance.post_filled
			post_vac = instance.post_vac
			staff_cat = instance.staff_cat
			temgofm_dt = instance.temgofm_dt
			temgoto_dt = instance.temgoto_dt	
			pg_head='Teaching'			
			if staff_det_dt.post_GO_dt:
				go_dt=staff_det_dt.post_GO_dt.strftime('%Y-%m-%d')
			chk_catid=School_category.objects.get(id=basic_det.sch_cate_id)
			if ((chk_catid.category_code=='1')|(chk_catid=='11')):
				desig_det= User_desig.objects.filter(Q(user_cate='SCHOOL') & Q(user_level__isnull=True)|Q(user_level='PS')).exclude(user_cate='SCHOOL&OFFICE') 
			elif ((chk_catid.category_code=='2')|(chk_catid.category_code=='4')|(chk_catid.category_code=='12')):
				desig_det= User_desig.objects.filter(Q(user_cate='SCHOOL') & Q(user_level__isnull=True)|Q(user_level='MS')|Q(user_level='HRHSMS')).exclude(user_cate='SCHOOL&OFFICE') 
			elif ((chk_catid.category_code=='6')|(chk_catid.category_code=='7')|(chk_catid.category_code=='8')) :
				desig_det= User_desig.objects.filter(Q(user_cate='SCHOOL') & Q(user_level__isnull=True)|Q(user_level='HS')|Q(user_level='HRHS')|Q(user_level='HRHSMS')).exclude(user_cate='SCHOOL&OFFICE') 
			elif ((chk_catid.category_code=='3')|(chk_catid.category_code=='5')|(chk_catid.category_code=='9')|(chk_catid.category_code=='10')):
				desig_det= User_desig.objects.filter(Q(user_cate='SCHOOL') & Q(user_level__isnull=True)|Q(user_level='HR')|Q(user_level='HRHS')|Q(user_level='HRHSMS')).exclude(user_cate='SCHOOL&OFFICE')
			else:
				desig_det= User_desig.objects.filter(Q(user_cate='SCHOOL') & Q(user_level__isnull=True)).exclude(user_cate='SCHOOL&OFFICE') 

			sch_key = basic_det.id
			staff_det = Staff.objects.filter(school_key=sch_key)	
			return render (request,'post_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
		
	def post(self,request,**kwargs):
		if request.user.is_authenticated():

			tid=self.kwargs.get('pk')

			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			form = staff_form(request.POST,request.FILES)
			instance=Staff.objects.get(id=tid)
			newteachpost = Staff.objects.get(id=tid)

			if form.is_valid():
				chk_post=form.cleaned_data['post_name']
				if(chk_post.user_desig in("85","70","50","51")):
					if Staff.objects.filter(school_key=basic_det.id).filter(post_name=form.cleaned_data['post_name']).exclude(id=tid).exists():
						messages.warning(request,'Headmaster post santion details already entered, if you want to correct pl. use Update option')
						return HttpResponseRedirect('/schoolnew/teaching_edit/')
					else:
						newteachpost.post_name = form.cleaned_data['post_name']
						newteachpost.post_sub = form.cleaned_data['post_sub']				
						newteachpost.post_sanc = form.cleaned_data['post_sanc']
						newteachpost.post_mode = form.cleaned_data['post_mode']
						newteachpost.post_GO = form.cleaned_data['post_GO']
						newteachpost.post_GO_dt = form.cleaned_data['post_GO_dt']
						newteachpost.post_GO_pd = form.cleaned_data['post_GO_pd']
						newteachpost.post_vac = (form.cleaned_data['post_sanc']-newteachpost.post_filled)
						newteachpost.staff_cat = 1

						if newteachpost.post_mode=='Permanent':
							newteachpost.temgofm_dt = None
							newteachpost.temgoto_dt = None
						else:
							newteachpost.ttemgofm_dt = form.cleaned_data['temgofm_dt']
							newteachpost.ttemgoto_dt = form.cleaned_data['temgoto_dt']

						newteachpost.save()
						messages.success(request,'Teaching Post Sanction Details Updated successfully')
						return HttpResponseRedirect('/schoolnew/teaching_edit/')
				else:	
					newteachpost.post_name = form.cleaned_data['post_name']
					newteachpost.post_sub = form.cleaned_data['post_sub']				
					newteachpost.post_sanc = form.cleaned_data['post_sanc']
					newteachpost.post_mode = form.cleaned_data['post_mode']
					newteachpost.post_GO = form.cleaned_data['post_GO']
					newteachpost.post_GO_dt = form.cleaned_data['post_GO_dt']
					newteachpost.post_GO_pd = form.cleaned_data['post_GO_pd']
					newteachpost.post_vac = (form.cleaned_data['post_sanc']-newteachpost.post_filled)
					newteachpost.staff_cat = 1			
					if newteachpost.post_mode=='Permanent':
						newteachpost.temgofm_dt = None
						newteachpost.temgoto_dt = None
					else:
						newteachpost.temgofm_dt = form.cleaned_data['temgofm_dt']
						newteachpost.temgoto_dt = form.cleaned_data['temgoto_dt']
					newteachpost.save()
				messages.success(request,'Teaching Post Sanction Details Updated successfully')
				return HttpResponseRedirect('/schoolnew/teaching_edit/')
			else:
				messages.warning(request,'Teaching Post Sanction Details Not Updated')
				return render (request,'post_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	


class Nonteaching_edit(View):
	
	def get(self,request,**kwargs):
		if request.user.is_authenticated():		
			tid=self.kwargs.get('pk')

			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			sch_key = basic_det.id
			post_det = Staff.objects.filter(Q(school_key=sch_key) & Q(staff_cat=2))


			form=staff_form()
			chk_catid=School_category.objects.get(id=basic_det.sch_cate_id)
			pg_head='Non-Teaching'
			if ((chk_catid.category_code=='1')|(chk_catid.category_code=='11')):
				desig_det= User_desig.objects.filter(Q(user_cate='SCHOOL&OFFICE') & Q(user_level__isnull=True))
			elif ((chk_catid.category_code=='2')|(chk_catid.category_code=='4')|(chk_catid.category_code=='12')):
				desig_det= User_desig.objects.filter(Q(user_cate='SCHOOL&OFFICE') & Q(user_level__isnull=True))
			elif ((chk_catid.category_code=='6')|(chk_catid.category_code=='7')|(chk_catid.category_code=='8')) :
				desig_det= User_desig.objects.filter(Q(user_cate='SCHOOL&OFFICE') & Q(user_level__isnull=True))
			elif ((chk_catid.category_code=='3')|(chk_catid.category_code=='5')|(chk_catid.category_code=='9')|(chk_catid.category_code=='10')):
				desig_det= User_desig.objects.filter(Q(user_cate='SCHOOL&OFFICE') )
			else:
				desig_det= User_desig.objects.filter((Q(user_cate='SCHOOL&OFFICE')|Q(user_cate='OFFICE')) & Q(user_level__isnull=True))
			return render (request,'post_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
	
	def post(self,request,**kwargs):
		if request.user.is_authenticated():
			pk=self.kwargs.get('pk')
		
			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			form = staff_form(request.POST,request.FILES)
			if form.is_valid():

				sch_key=form.cleaned_data['school_key']
				if request.POST['post_mode']=='Permanent':
					tpost_GO_pd = ''
					ttemgofm_dt = None
					ttemgoto_dt = None
				else:
					tpost_GO_pd = form.cleaned_data['post_GO_pd']
					ttemgofm_dt = form.cleaned_data['temgofm_dt']
					ttemgoto_dt = form.cleaned_data['temgoto_dt']
				newnnonteachpost = Staff(
					school_key=sch_key,
					post_name = form.cleaned_data['post_name'],	
					post_sub = form.cleaned_data['post_sub'],				
					post_sanc = form.cleaned_data['post_sanc'],
					post_mode = form.cleaned_data['post_mode'],
					post_GO = form.cleaned_data['post_GO'],
					post_GO_dt = form.cleaned_data['post_GO_dt'],
					post_filled = 0,
					post_vac = form.cleaned_data['post_sanc'],
					post_GO_pd = tpost_GO_pd,
					temgofm_dt = ttemgofm_dt,
					temgoto_dt = ttemgoto_dt,
					staff_cat = 2,

					)
				newnnonteachpost.save()
				messages.success(request,'Non-Teaching Post Details Added successfully')
				return HttpResponseRedirect('/schoolnew/nonteaching_edit/')
			else:
				print form.errors
				messages.warning(request,'Non-Teaching Post Details Not Saved')
				return render (request,'post_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	


class Nonteaching_update(View):
	
	def get(self,request,**kwargs):
		if request.user.is_authenticated():		
			tid=self.kwargs.get('pk')

			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			instance=Staff.objects.get(id=tid)
			sch_key = basic_det.id
			nonteach_det_dt=Staff.objects.get(id=tid)
			form=staff_form(instance=instance)
			post_name= instance.post_name
			post_sub= instance.post_sub
			id_tpost_sub=post_sub.id	
			post_sanc=instance.post_sanc
			post_mode= instance.post_mode
			post_GO= instance.post_GO
			go_dt= instance.post_GO_dt		
			post_GO_dt= instance.post_GO_dt
			post_GO_pd= instance.post_GO_pd
			post_filled= instance.post_filled
			post_vac= instance.post_vac
			post_filled = instance.post_filled
			post_vac = instance.post_vac
			staff_cat = instance.staff_cat
			temgofm_dt = instance.temgofm_dt
			temgoto_dt = instance.temgoto_dt		
			pg_head='Non-Teaching'
			if nonteach_det_dt.post_GO_dt:
				go_dt=nonteach_det_dt.post_GO_dt.strftime('%Y-%m-%d')	
			chk_catid=School_category.objects.get(id=basic_det.sch_cate_id)
			if ((chk_catid.category_code=='1')|(chk_catid.category_code=='11')):
				desig_det= User_desig.objects.filter(Q(user_cate='SCHOOL&OFFICE') & Q(user_level__isnull=True))
			elif ((chk_catid.category_code=='2')|(chk_catid.category_code=='4')|(chk_catid.category_code=='12')):
				desig_det= User_desig.objects.filter(Q(user_cate='SCHOOL&OFFICE') & Q(user_level__isnull=True))
			elif ((chk_catid.category_code=='6')|(chk_catid.category_code=='7')|(chk_catid.category_code=='8')) :
				desig_det= User_desig.objects.filter(Q(user_cate='SCHOOL&OFFICE') & Q(user_level__isnull=True))
			elif ((chk_catid.category_code=='3')|(chk_catid.category_code=='5')|(chk_catid.category_code=='9')|(chk_catid.category_code=='10')):
				desig_det= User_desig.objects.filter(Q(user_cate='SCHOOL&OFFICE') )
			else:
				desig_det= User_desig.objects.filter((Q(user_cate='SCHOOL&OFFICE')|Q(user_cate='OFFICE')) & Q(user_level__isnull=True))
			sch_key = basic_det.id
			return render (request,'post_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
	def post(self,request,**kwargs):
		if request.user.is_authenticated():		
			tid=self.kwargs.get('pk')

			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			form = staff_form(request.POST,request.FILES)
			instance=Staff.objects.get(id=tid)
		
			newnonteachpost = Staff.objects.get(id=tid)


			if form.is_valid():

				newnonteachpost.post_name = form.cleaned_data['post_name']			
				newnonteachpost.post_sanc = form.cleaned_data['post_sanc']
				newnonteachpost.post_mode = form.cleaned_data['post_mode']
				newnonteachpost.post_GO = form.cleaned_data['post_GO']
				newnonteachpost.post_GO_dt = form.cleaned_data['post_GO_dt']
				newnonteachpost.post_GO_pd = form.cleaned_data['post_GO_pd']
				newnonteachpost.post_sub = form.cleaned_data['post_sub']
				newnonteachpost.post_vac = (form.cleaned_data['post_sanc']-newnonteachpost.post_filled)
				newnonteachpost.staff_cat = 2
				if newnonteachpost.post_mode=='Permanent':
					newnonteachpost.temgofm_dt = None
					newnonteachpost.temgoto_dt = None
				else:
					newnonteachpost.temgofm_dt = form.cleaned_data['temgofm_dt']
					newnonteachpost.temgoto_dt = form.cleaned_data['temgoto_dt']
				newnonteachpost.save()
				messages.success(request,'Non-Teaching Post Details Updated successfully')
				return HttpResponseRedirect('/schoolnew/nonteaching_edit/')
			else:
				messages.warning(request,'Non-Teaching Post Details Not Updated')
				return render (request,'post_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	


class Nonteaching_delete(View):
	
	def get(self, request,**kwargs):
		if request.user.is_authenticated():   	
			tid=self.kwargs.get('pk')
			data=Staff.objects.get(id=tid)
			data.delete()
			print data.school_key
			msg= str(data.post_name)+" - Posts has been successfully removed "
			messages.success(request, msg ) 
			return HttpResponseRedirect('/schoolnew/nonteaching_edit/')
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	

class Parttime_edit(View):
	
	def get(self,request,**kwargs):
		if request.user.is_authenticated():		
			tid=self.kwargs.get('pk')

			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			acade_det = Academicinfo.objects.filter(school_key=basic_det.id)
			sch_key = basic_det.id
			parttime_det = Parttimestaff.objects.filter(school_key=sch_key)
			part_time_sub=Part_time_Subjects.objects.all()
			form = parttimestaff_form()
			return render (request,'parttime_staff_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
	
	def post(self,request,**kwargs):
		if request.user.is_authenticated():		
			pk=self.kwargs.get('pk')
		
			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			form = parttimestaff_form(request.POST,request.FILES)

			if form.is_valid():
				sch_key=form.cleaned_data['school_key']
				newnpartime = Parttimestaff(
					school_key=sch_key,
					part_instr = form.cleaned_data['part_instr'],
					part_instr_sub = form.cleaned_data['part_instr_sub'],)
				newnpartime.save()
				messages.success(request,'Part-time Teacher Details Added successfully')
				return HttpResponseRedirect('/schoolnew/parttime_edit/')
			else:
				messages.success(request,'Part-time Teacher Details Not Saved')
				return render (request,'parttime_staff_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	


class Parttime_update(View):
	
	def get(self,request,**kwargs):
		if request.user.is_authenticated():
			tid=self.kwargs.get('pk')

			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			sch_key = basic_det.id
			parttime_det = Parttimestaff.objects.filter(school_key=sch_key)
			part_time_sub=Part_time_Subjects.objects.all()
			instance=Parttimestaff.objects.get(id=tid)		
			form = parttimestaff_form(instance=instance)
			instance=Parttimestaff.objects.get(id=tid)
			part_instr = instance.part_instr
			part_instr_sub = instance.part_instr_sub
			return render (request,'parttime_staff_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
	def post(self,request,**kwargs):
		if request.user.is_authenticated():			
			tid=self.kwargs.get('pk')

			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			form = parttimestaff_form(request.POST,request.FILES)
			instance=Parttimestaff.objects.get(id=tid)
		
			newparttimestaff = Parttimestaff.objects.get(id=tid)


			if form.is_valid():
				newparttimestaff.part_instr = form.cleaned_data['part_instr']			
				newparttimestaff.part_instr_sub = form.cleaned_data['part_instr_sub']
				newparttimestaff.save()
				messages.success(request,'Part-time Teacher Details Updated successfully')
				return HttpResponseRedirect('/schoolnew/parttime_edit/')
			else:
				messages.warning(request,'Part-time Teacher Details Not Added')
				return render (request,'parttime_staff_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	

class Parttime_delete(View):
	
	def get(self, request,**kwargs):
		if request.user.is_authenticated():
			tid=self.kwargs.get('pk')
			data=Parttimestaff.objects.get(id=tid)
			data.delete()
			msg= data.part_instr+" - Part Time Teacher has been successfully removed "
			messages.success(request, msg ) 
			return HttpResponseRedirect('/schoolnew/parttime_edit/')
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	


class Group_edit(View):
	
	def get(self,request,**kwargs):
		if request.user.is_authenticated():		
			tid=self.kwargs.get('pk')
			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			sch_key = basic_det.id
			group_det = Sch_groups.objects.filter(school_key=sch_key)
			gropu_mas= Groups.objects.all()
			form=sch_groups_form()	
			govchk=basic_det.sch_management
			if ((str(govchk)=='Fully Aided School')|(str(govchk)=='Partly Aided School')|(str(govchk)=='Anglo Indian (Fully Aided) School')|(str(govchk)=='Anglo Indian (Partly Aided) School')|(str(govchk)=='Oriental (Fully Aided) Sanskrit School')|(str(govchk)=='Oriental (Partly Aided) Sanskrit School')|(str(govchk)=='Oriental (Fully Aided) Arabic School')|(str(govchk)=='Oriental (Partly Aided) Arabic School')|(str(govchk)=='Differently Abled Department Aided School')):
				aid_chk='Yes'
			else:
				aid_chk=''
			return render (request,'group_edit_upd.html',locals())			
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
	
	def post(self,request,**kwargs):
		if request.user.is_authenticated():
			form = sch_groups_form(request.POST,request.FILES)


			basic_det=Basicinfo.objects.get(udise_code=request.user.username)

			if form.is_valid():
				if Sch_groups.objects.filter(school_key=basic_det.id).filter(group_name=request.POST['group_name']).exists():
					messages.warning(request,'This Group already Exist. Pleae check & update the same if necessary')
					return HttpResponseRedirect('/schoolnew/group_edit')
				else:
					sch_key=form.cleaned_data['school_key']
					newgroup = Sch_groups(
						school_key =sch_key,
						group_name=form.cleaned_data['group_name'],
						sec_in_group=form.cleaned_data['sec_in_group'],
						sec_in_group_aid=form.cleaned_data['sec_in_group_aid'],
						permis_ordno=form.cleaned_data['permis_ordno'],
						permis_orddt=form.cleaned_data['permis_orddt'],										
						)
					newgroup.save()

					messages.success(request,'Group Details Added successfully')
					return HttpResponseRedirect('/schoolnew/group_edit/')
			else:

				messages.warning(request,'Group Details Not Saved')

			return render (request,'group_edit_upd.html',locals())

		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	




class Group_delete(View):
	
	def get(self, request,**kwargs):
		if request.user.is_authenticated():   	
			tid=self.kwargs.get('pk')
			data=Sch_groups.objects.get(id=tid)
			data.delete()
			msg= data.group_name+" - Group has been successfully removed "
			messages.success(request, msg ) 
			return HttpResponseRedirect('/schoolnew/group_edit/')
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	



class Group_update(View):
	
	def get(self, request,**kwargs):
		if request.user.is_authenticated():
			tid=self.kwargs.get('pk')

			basic_det=Basicinfo.objects.get(udise_code=request.user.username)		
			instance=Sch_groups.objects.get(id=tid)
			sch_key = basic_det.id
			group_det = Sch_groups.objects.filter(school_key=sch_key)		
			group_name=instance.group_name
			sec_in_group=instance.sec_in_group
			sec_in_group_aid=instance.sec_in_group_aid
			permis_ordno=instance.permis_ordno
			permis_orddt=instance.permis_orddt
			gropu_mas= Groups.objects.all()
			govchk=basic_det.sch_management
			if ((str(govchk)=='Fully Aided School')|(str(govchk)=='Partly Aided School')|(str(govchk)=='Anglo Indian (Fully Aided) School')|(str(govchk)=='Anglo Indian (Partly Aided) School')|(str(govchk)=='Oriental (Fully Aided) Sanskrit School')|(str(govchk)=='Oriental (Partly Aided) Sanskrit School')|(str(govchk)=='Oriental (Fully Aided) Arabic School')|(str(govchk)=='Oriental (Partly Aided) Arabic School')|(str(govchk)=='Differently Abled Department Aided School')):
				aid_chk='Yes'
			else:
				aid_chk=''
			return render(request,'group_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
	def post(self,request,**kwargs):
		if request.user.is_authenticated():		
			tid=self.kwargs.get('pk')

			basic_det=Basicinfo.objects.get(udise_code=request.user.username)		
			form = sch_groups_form(request.POST,request.FILES)
			instance=Sch_groups.objects.get(id=tid)
			group_edit = Sch_groups.objects.get(id=tid)

			if form.is_valid():	

				if Sch_groups.objects.filter(school_key=basic_det.id).filter(group_name=request.POST['group_name']).exclude(id=tid).exists():
					messages.success(request,'This Group already exist. Please update the same')
					return HttpResponseRedirect('/schoolnew/group_edit')
				else:
					group_edit.group_name=form.cleaned_data['group_name']	
					group_edit.sec_in_group=form.cleaned_data['sec_in_group']	
					group_edit.sec_in_group_aid=form.cleaned_data['sec_in_group_aid']			
					group_edit.permis_ordno=form.cleaned_data['permis_ordno']
					group_edit.permis_orddt=form.cleaned_data['permis_orddt']
					group_edit.save()
					messages.success(request,'Group Details Updated successfully')
					return HttpResponseRedirect('/schoolnew/group_edit')
			else:
				messages.warning(request,'Group Details Not Updated')
				return render(request,'group_edit_upd.html',locals()) 
	 
			return HttpResponseRedirect('/schoolnew/group_edit/')
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	


class Buildabs_edit(View):
	
	def get(self,request,**kwargs):
		if request.user.is_authenticated():		
			tid=self.kwargs.get('pk')
			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			buildabs_det = Building_abs.objects.filter(school_key=basic_det.id)
			sch_key = basic_det.id
			Build_abs = Building_abs.objects.filter(school_key=sch_key)
			form=building_abs_form()
			govchk=basic_det.sch_management
			print govchk
			if ((str(govchk)=='School Education Department School')|(str(govchk)=='Corporation School')|(str(govchk)=='Municipal School')|(str(govchk)=='Adi-Dravida Welfare School')|(str(govchk)=='Forest Department School')|(str(govchk)=='Differently Abled Department School')|(str(govchk)=='Kallar BC/MBC Department School')|(str(govchk)=='Rubber Board School')|(str(govchk)=='Tribal Welfare School')|(str(govchk)=='Aranilayam HR&C Department School')|(str(govchk)=='Fully Aided School')|(str(govchk)=='Partly Aided School')|(str(govchk)=='Anglo Indian (Fully Aided) School')|(str(govchk)=='Anglo Indian (Partly Aided) School')|(str(govchk)=='Oriental (Fully Aided) Sanskrit School')|(str(govchk)=='Oriental (Partly Aided) Sanskrit School')|(str(govchk)=='Oriental (Fully Aided) Arabic School')|(str(govchk)=='Oriental (Partly Aided) Arabic School')|(str(govchk)=='Differently Abled Department Aided School')):
				govaid_chk='Yes'
			else:
				govaid_chk=''	
			if ((str(govchk)=='Fully Aided School')|(str(govchk)=='Partly Aided School')|(str(govchk)=='Anglo Indian (Fully Aided) School')|(str(govchk)=='Anglo Indian (Partly Aided) School')|(str(govchk)=='Oriental (Fully Aided) Sanskrit School')|(str(govchk)=='Oriental (Partly Aided) Sanskrit School')|(str(govchk)=='Oriental (Fully Aided) Arabic School')|(str(govchk)=='Oriental (Partly Aided) Arabic School')|(str(govchk)=='Differently Abled Department Aided School')):
				aid_chk='Yes'
			else:
				aid_chk=''	
			if ((str(govchk)=='School Education Department School')|(str(govchk)=='Corporation School')|(str(govchk)=='Municipal School')|(str(govchk)=='Adi-Dravida Welfare School')|(str(govchk)=='Forest Department School')|(str(govchk)=='Differently Abled Department School')|(str(govchk)=='Kallar BC/MBC Department School')|(str(govchk)=='Rubber Board School')|(str(govchk)=='Tribal Welfare School')|(str(govchk)=='Aranilayam HR&C Department School')):	
				gov_chk='Yes'
			else:
				gov_chk=''

			return render (request,'buildabs_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
	
	def post(self,request,**kwargs):
		if request.user.is_authenticated():		
			pk=self.kwargs.get('pk')

			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			form=building_abs_form(request.POST,request.FILES)


			if form.is_valid():
				sch_key=form.cleaned_data['school_key']
				if basic_det.manage_cate_id==1:
					newbuildabs = Building_abs(
						school_key=sch_key,
						building_name = form.cleaned_data['building_name'],
						no_of_floors = form.cleaned_data['no_of_floors'],
						stair_case_no = form.cleaned_data['stair_case_no'],	
						stair_case_width = form.cleaned_data['stair_case_width'],
						building_funded = form.cleaned_data['building_funded'],
						build_pres_cond = form.cleaned_data['build_pres_cond'],
						build_cons_yr = form.cleaned_data['build_cons_yr'],
						
						)
					newbuildabs.save()
				else:
					newbuildabs = Building_abs(
						school_key=sch_key,
						building_name = form.cleaned_data['building_name'],
						no_of_floors = form.cleaned_data['no_of_floors'],
						stair_case_no = form.cleaned_data['stair_case_no'],	
						stair_case_width = form.cleaned_data['stair_case_width'],
						building_funded = form.cleaned_data['building_funded'],
						stab_cer_no = form.cleaned_data['stab_cer_no'],	
						stab_cer_date = form.cleaned_data['stab_cer_date'],
						stab_fm_dt = form.cleaned_data['stab_fm_dt'],
						stab_to_dt = form.cleaned_data['stab_to_dt'],
						stab_iss_auth = form.cleaned_data['stab_iss_auth'],
						no_stud = form.cleaned_data['no_stud'],
						lic_cer_no = form.cleaned_data['lic_cer_no'],	
						lic_cer_dt = form.cleaned_data['lic_cer_dt'],
						lic_iss_auth = form.cleaned_data['lic_iss_auth'],
						san_cer_no = form.cleaned_data['san_cer_no'],	
						san_cer_dt = form.cleaned_data['san_cer_dt'],
						san_iss_auth = form.cleaned_data['san_iss_auth'],
						fire_cer_no = form.cleaned_data['fire_cer_no'],
						fire_cer_dt = form.cleaned_data['fire_cer_dt'],
						fire_iss_auth = form.cleaned_data['fire_iss_auth'],
						build_pres_cond = form.cleaned_data['build_pres_cond'],
						build_cons_yr = form.cleaned_data['build_cons_yr'],
						
						)
					newbuildabs.save()

				messages.success(request,'Building abstract Details Added successfully')
				return HttpResponseRedirect('/schoolnew/buildabs_edit/')
			else:
				print form.errors
				messages.warning(request,'Building abstract Details Not Saved')
				return render (request,'buildabs_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
class Buildabs_update(View):
	
	def get(self,request,**kwargs):
		if request.user.is_authenticated():
			tid=self.kwargs.get('pk')
			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			instance=Building_abs.objects.get(id=tid)
			buildabs_det = Building_abs.objects.filter(school_key=basic_det.id)
			sch_key = basic_det.id
			Build_abs_det= Building_abs.objects.filter(school_key=sch_key)
			Build_sta_dt=Building_abs.objects.get(id=tid)
			form=building_abs_form(instance=instance)
			building_name = instance.building_name
			no_of_floors = instance.no_of_floors
			stair_case_no = instance.stair_case_no
			stair_case_width = instance.stair_case_width
			building_funded = instance.building_funded
			stab_cer_no = instance.stab_cer_no
			stab_cer_date= instance.stab_cer_date
			stab_fm_dt=instance.stab_fm_dt
			stab_to_dt=instance.stab_to_dt
			stab_iss_auth=instance.stab_iss_auth
			no_stud=instance.no_stud
			lic_cer_no=instance.lic_cer_no
			lic_cer_dt=instance.lic_cer_dt
			lic_iss_auth=instance.lic_iss_auth
			san_cer_no=instance.san_cer_no
			san_cer_dt=instance.san_cer_dt
			san_iss_auth=instance.san_iss_auth
			fire_cer_no=instance.fire_cer_no
			fire_cer_dt=instance.fire_cer_dt
			fire_iss_auth=instance.fire_iss_auth
			build_pres_cond=instance.build_pres_cond
			build_cons_yr=instance.build_cons_yr
			build_pres_cond = instance.build_pres_cond
			build_cons_yr = instance.build_cons_yr		
			if Build_sta_dt.stability_cer_date:
				stab_dt=Build_sta_dt.stability_cer_date.strftime('%Y-%m-%d')

			return render (request,'buildabs_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
	def post(self,request,**kwargs):
		if request.user.is_authenticated():			
			tid=self.kwargs.get('pk')

			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			form = building_abs_form(request.POST,request.FILES)
			instance=Building_abs.objects.get(id=tid)
		
			newbuildabs = Building_abs.objects.get(id=tid)
			if form.is_valid():	
				if basic_det.manage_cate_id==1:
					newbuildabs.building_name = form.cleaned_data['building_name']
					newbuildabs.no_of_floors = form.cleaned_data['no_of_floors']
					newbuildabs.stair_case_no = form.cleaned_data['stair_case_no']
					newbuildabs.stair_case_width = form.cleaned_data['stair_case_width']
					newbuildabs.building_funded = form.cleaned_data['building_funded']
					build_pres_cond = form.cleaned_data['build_pres_cond']
					build_cons_yr = form.cleaned_data['build_cons_yr']
					newbuildabs.save()					
				else:
					newbuildabs.building_name = form.cleaned_data['building_name']
					newbuildabs.no_of_floors = form.cleaned_data['no_of_floors']
					newbuildabs.stair_case_no = form.cleaned_data['stair_case_no']
					newbuildabs.stair_case_width = form.cleaned_data['stair_case_width']
					newbuildabs.building_funded = form.cleaned_data['building_funded']
					newbuildabs.stab_cer_no = form.cleaned_data['stab_cer_no']	
					newbuildabs.stab_cer_date= form.cleaned_data['stab_cer_date']
					newbuildabs.stab_fm_dt= form.cleaned_data['stab_fm_dt']
					newbuildabs.stab_to_dt= form.cleaned_data['stab_to_dt']
					newbuildabs.stab_iss_auth= form.cleaned_data['stab_iss_auth']
					newbuildabs.no_stud= form.cleaned_data['no_stud']
					newbuildabs.lic_cer_no= form.cleaned_data['lic_cer_no']
					newbuildabs.lic_cer_dt= form.cleaned_data['lic_cer_dt']
					newbuildabs.lic_iss_auth= form.cleaned_data['lic_iss_auth']
					newbuildabs.san_cer_no= form.cleaned_data['san_cer_no']
					newbuildabs.san_cer_dt= form.cleaned_data['san_cer_dt']
					newbuildabs.san_iss_auth= form.cleaned_data['san_iss_auth']
					newbuildabs.fire_cer_no= form.cleaned_data['fire_cer_no']
					newbuildabs.fire_cer_dt= form.cleaned_data['fire_cer_dt']
					newbuildabs.fire_iss_auth= form.cleaned_data['fire_iss_auth']	
					build_pres_cond = form.cleaned_data['build_pres_cond']
					build_cons_yr = form.cleaned_data['build_cons_yr']					
					newbuildabs.save()
				messages.success(request,'Building abstract Details Updated successfully')
				return HttpResponseRedirect('/schoolnew/buildabs_edit/')
			else:
				messages.warning(request,'Building abstract Details Not Updated')
				return render (request,'buildabs_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	


	

class Buildabs_delete(View):
	
	def get(self, request,**kwargs):
		if request.user.is_authenticated():	
			tid=self.kwargs.get('pk')
			data=Building_abs.objects.get(id=tid)
			data.delete()
			msg= data.building_name+" - Named building has been successfully removed "
			messages.success(request, msg ) 
			return HttpResponseRedirect('/schoolnew/buildabs_edit/')
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	

class Land_edit(View):
	
	def get(self,request,**kwargs):
		if request.user.is_authenticated():		
			tid=self.kwargs.get('pk')
			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			land_det = Land.objects.filter(school_key=basic_det.id)
			form=land_form()
			govchk=basic_det.sch_management
			if ((str(govchk)=='School Education Department School')|(str(govchk)=='Corporation School')|(str(govchk)=='Municipal School')|(str(govchk)=='Adi-Dravida Welfare School')|(str(govchk)=='Forest Department School')|(str(govchk)=='Differently Abled Department School')|(str(govchk)=='Kallar BC/MBC Department School')|(str(govchk)=='Rubber Board School')|(str(govchk)=='Tribal Welfare School')|(str(govchk)=='Aranilayam HR&C Department School')):	
				gov_chk='Yes'
			else:
				gov_chk=''

			return render (request,'land_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
	def post(self,request,**kwargs):
		if request.user.is_authenticated():		
			pk=self.kwargs.get('pk')

			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			form=land_form(request.POST,request.FILES)


			if form.is_valid():
				sch_key=form.cleaned_data['school_key']

				newland = Land(
					school_key=sch_key,
					name = form.cleaned_data['name'],
					own_type =form.cleaned_data['own_type'],
					lease_yrs=form.cleaned_data['lease_yrs'],
					lease_name=form.cleaned_data['lease_name'],
					tot_area=form.cleaned_data['tot_area'],
					area_mes_type=form.cleaned_data['area_mes_type'],
					area_cent = form.cleaned_data['area_cent'],
					area_ground = form.cleaned_data['area_ground'],
					patta_no = form.cleaned_data['patta_no'],
					survey_no = form.cleaned_data['survey_no'],
					subdiv_no=form.cleaned_data['subdiv_no'],
					land_type=form.cleaned_data['land_type'],
					doc_no=form.cleaned_data['doc_no'],
					doc_regn_dt=form.cleaned_data['doc_regn_dt'],
					place_regn=form.cleaned_data['place_regn'],
					ec_cer_no=form.cleaned_data['ec_cer_no'],
					ec_cer_dt=form.cleaned_data['ec_cer_dt'],
					ec_cer_fm=form.cleaned_data['ec_cer_fm'],
					ec_cer_to=form.cleaned_data['ec_cer_to'],
					ec_period=form.cleaned_data['ec_period'],
					
					)
				newland.save()
				messages.success(request,'Land Details Added successfully')
				return HttpResponseRedirect('/schoolnew/land_edit/')

			else:
				print form.errors
				messages.warning(request,'Land Details Not Saved')
				return render (request,'land_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	

class Land_update(View):
	
	def get(self,request,**kwargs):
		if request.user.is_authenticated():	
			tid=self.kwargs.get('pk')
			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			land_det = Land.objects.filter(school_key=basic_det.id)
			instance=Land.objects.get(id=tid)
			sch_key = basic_det.id
			land_det= Land.objects.filter(school_key=sch_key)
			form=land_form(instance=instance)
			name = instance.name
			own_type = instance.own_type
			lease_yrs = instance.lease_yrs
			lease_name = instance.lease_name
			tot_area= instance.tot_area
			area_mes_type = instance.area_mes_type
			area_cent = instance.area_cent
			area_ground = instance.area_ground
			patta_no = instance.patta_no
			survey_no = instance.survey_no
			subdiv_no = instance.subdiv_no
			land_type = instance.land_type
			doc_no=instance.doc_no
			doc_regn_dt=instance.doc_regn_dt
			place_regn=instance.place_regn
			ec_cer_no=instance.ec_cer_no
			ec_cer_dt=instance.ec_cer_dt
			ec_cer_fm=instance.ec_cer_fm
			ec_cer_to=instance.ec_cer_to
			ec_period=instance.ec_period
			
			govchk=basic_det.sch_management		
			if ((str(govchk)=='School Education Department School')|(str(govchk)=='Corporation School')|(str(govchk)=='Municipal School')|(str(govchk)=='Adi-Dravida Welfare School')|(str(govchk)=='Forest Department School')|(str(govchk)=='Differently Abled Department School')|(str(govchk)=='Kallar BC/MBC Department School')|(str(govchk)=='Rubber Board School')|(str(govchk)=='Tribal Welfare School')|(str(govchk)=='Aranilayam HR&C Department School')):	
				gov_chk='Yes'
			else:
				gov_chk=''		
			return render (request,'land_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
	def post(self,request,**kwargs):
		if request.user.is_authenticated():		
			tid=self.kwargs.get('pk')

			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			form = land_form(request.POST,request.FILES)
			instance=Land.objects.get(id=tid)
		
			newland = Land.objects.get(id=tid)
			if form.is_valid():			
				newland.name = form.cleaned_data['name']
				newland.own_type = form.cleaned_data['own_type']
				newland.lease_yrs = form.cleaned_data['lease_yrs']
				instance.lease_name = form.cleaned_data['lease_name']
				newland.tot_area = form.cleaned_data['tot_area']
				newland.area_mes_type = form.cleaned_data['area_mes_type']
				newland.area_cent = form.cleaned_data['area_cent']
				newland.area_ground = form.cleaned_data['area_ground']
				newland.patta_no = form.cleaned_data['patta_no']	
				newland.survey_no = form.cleaned_data['survey_no']
				newland.subdiv_no = form.cleaned_data['subdiv_no']
				newland.land_type = form.cleaned_data['land_type']
				newland.doc_no=form.cleaned_data['doc_no']
				newland.doc_regn_dt=form.cleaned_data['doc_regn_dt']
				newland.place_regn=form.cleaned_data['place_regn']
				newland.ec_cer_no=form.cleaned_data['ec_cer_no']
				newland.ec_cer_dt=form.cleaned_data['ec_cer_dt']
				newland.ec_cer_fm=form.cleaned_data['ec_cer_fm']
				newland.ec_cer_to=form.cleaned_data['ec_cer_to']
				newland.ec_period=form.cleaned_data['ec_period']
				newland.save()
				messages.success(request,'Land Details Updated successfully')
				return HttpResponseRedirect('/schoolnew/land_edit/')
			else:
				messages.warning(request,'Land Details Not Updated')
				return render (request,'land_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	


class Land_delete(View):
	
	def get(self, request,**kwargs):
		if request.user.is_authenticated():
			tid=self.kwargs.get('pk')
			data=Land.objects.get(id=tid)
			data.delete()
			msg= data.name+' land with patta No.'+str(data.patta_no)+" - has been successfully removed "
			messages.success(request, msg ) 
			return HttpResponseRedirect('/schoolnew/land_edit/')
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	

class Build_edit(View):
	
	def get(self,request,**kwargs):
		if request.user.is_authenticated():		
			tid=self.kwargs.get('pk')
			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			build_det = Building.objects.filter(school_key=basic_det.id)
			room_cat_chk=Room_cate.objects.all()
			sch_key = basic_det.id
			form=building_form()
			return render (request,'build_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
	
	def post(self,request,**kwargs):
		if request.user.is_authenticated():		
			pk=self.kwargs.get('pk')

			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			form=building_form(request.POST,request.FILES)

			if form.is_valid():
				sch_key=form.cleaned_data['school_key']	

				newbuild = Building(
					school_key=sch_key,
					room_cat = form.cleaned_data['room_cat'],
					room_count = form.cleaned_data['room_count'],
					roof_type = form.cleaned_data['roof_type'],
					builtup_area = form.cleaned_data['builtup_area'],
					)
				newbuild.save()
				messages.success(request,'Building Details Added successfully')
				return HttpResponseRedirect('/schoolnew/build_edit/')
			else:
				print form.errors
				return render (request,'build_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	


class Build_update(View):
	
	def get(self,request,**kwargs):
		if request.user.is_authenticated():		
			tid=self.kwargs.get('pk')
			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			build_det = Building.objects.filter(school_key=basic_det.id)
			instance=Building.objects.get(id=tid)
			sch_key = basic_det.id
			room_cat_chk=Room_cate.objects.all()
			form=building_form(instance=instance)

			room_cat = instance.room_cat
			room_count = instance.room_count
			roof_type = instance.roof_type
			builtup_area = instance.builtup_area
			return render (request,'build_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			

	
	def post(self,request,**kwargs):
		if request.user.is_authenticated():			
			tid=self.kwargs.get('pk')

			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			form = building_form(request.POST,request.FILES)
			instance=Building.objects.get(id=tid)
		
			newbuild = Building.objects.get(id=tid)

			if form.is_valid():			
				newbuild.room_cat = form.cleaned_data['room_cat']
				newbuild.room_count = form.cleaned_data['room_count']
				newbuild.roof_type = form.cleaned_data['roof_type']
				newbuild.builtup_area = form.cleaned_data['builtup_area']	
				newbuild.save()
				messages.success(request,'Building Details Updated successfully')
				return HttpResponseRedirect('/schoolnew/build_edit/')
			else:
				messages.warning(request,'Building Details Not Updated')
				return render (request,'build_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
class Build_delete(View):
	
	def get(self, request,**kwargs):
		if request.user.is_authenticated():    	
			tid=self.kwargs.get('pk')
			data=Building.objects.get(id=tid)
			data.delete()
			msg= data.room_cat+" - "+str(data.room_count)+" - has been successfully removed "
			messages.success(request, msg ) 
			return HttpResponseRedirect('/schoolnew/build_edit/')
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
class Sports_edit(View):
	
	def get(self,request,**kwargs):
		if request.user.is_authenticated():
			tid=self.kwargs.get('pk')

			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			sports_det = Sports.objects.filter(school_key=basic_det.id)
			sch_key = basic_det.id
			sport_lst=Sport_list.objects.all()
			form=sports_form()
			return render (request,'sports_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
	
	def post(self,request,**kwargs):
		if request.user.is_authenticated():		
			pk=self.kwargs.get('pk')

			basic_det=Basicinfo.objects.get(udise_code=request.user.username)

			form=sports_form(request.POST,request.FILES)
			if form.is_valid():
				sch_key=form.cleaned_data['school_key']	
				newsports = Sports(
					school_key=sch_key,
					sports_name = form.cleaned_data['sports_name'],
					play_ground = form.cleaned_data['play_ground'],
					sports_equip = form.cleaned_data['sports_equip'],	
					sports_no_sets = form.cleaned_data['sports_no_sets'],			
					)
				newsports.save()

				messages.success(request,'Sports Details Added successfully')
				return HttpResponseRedirect('/schoolnew/sports_edit/')
				
			else:
				messages.warning(request,'Sports Details Not Saved')
				return render (request,'sports_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	


class Sports_update(View):
	
	def get(self,request,**kwargs):
		if request.user.is_authenticated():		
			tid=self.kwargs.get('pk')
			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			sports_det = Sports.objects.filter(school_key=basic_det.id)
			instance=Sports.objects.get(id=tid)
			sch_key = basic_det.id
			form=sports_form(instance=instance)
			sport_lst=Sport_list.objects.all()
			sports_name = instance.sports_name
			play_ground = instance.play_ground
			sports_equip = instance.sports_equip
			sports_no_sets = instance.sports_no_sets
			return render (request,'sports_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
		
	def post(self,request,**kwargs):
		if request.user.is_authenticated():		
			tid=self.kwargs.get('pk')

			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			form = sports_form(request.POST,request.FILES)
			instance=Sports.objects.get(id=tid)
			newsports = Sports.objects.get(id=tid)
			if form.is_valid():
				newsports.sports_name = form.cleaned_data['sports_name']
				newsports.play_ground = form.cleaned_data['play_ground']
				newsports.sports_equip = form.cleaned_data['sports_equip']
				newsports.sports_no_sets = form.cleaned_data['sports_no_sets']
				newsports.save()
				messages.success(request,'Sports Details Updated successfully')
				return HttpResponseRedirect('/schoolnew/sports_edit/')
			else:
				messages.warning(request,'Sports Details Not Updated')
				return render (request,'sports_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
class Sports_delete(View):
	
	def get(self, request,**kwargs):
		if request.user.is_authenticated():    	
			tid=self.kwargs.get('pk')
			data=Sports.objects.get(id=tid)
			data.delete()
			msg= data.sports_name+" - has been successfully removed "
			messages.success(request, msg ) 
			return HttpResponseRedirect('/schoolnew/sports_edit/')
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	

	
class Ict_edit(View):
	
	def get(self,request,**kwargs):
		if request.user.is_authenticated():		
			tid=self.kwargs.get('pk')
			ss=request.user.username
			if ss.isalpha():
				basic_det=Basicinfo.objects.get(office_code=request.user.username)
				office_chk = 'Yes'
			else:
				office_chk = 'No'
				basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			ict_det = Ictentry.objects.filter(school_key=basic_det.id)
			ict_lst=Ict_list.objects.all()
			ict_suply=Ict_suppliers.objects.all()
			sch_key = basic_det.id
			form=ictentry_form()		
			return render (request,'ict_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
	
	def post(self,request,**kwargs):
		if request.user.is_authenticated():		
			pk=self.kwargs.get('pk')
			ss=request.user.username
			if ss.isalpha():
				basic_det=Basicinfo.objects.get(office_code=request.user.username)
			else:
				basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			form=ictentry_form(request.POST,request.FILES)

			if form.is_valid():
				sch_key=form.cleaned_data['school_key']	
				newict = Ictentry(
					school_key=sch_key,
					ict_type = form.cleaned_data['ict_type'],
					working_no = form.cleaned_data['working_no'],
					not_working_no = form.cleaned_data['not_working_no'],	
					supplied_by = form.cleaned_data['supplied_by'],	
					donor_ict = form.cleaned_data['donor_ict'],
					)
				newict.save()
				messages.success(request,'ICT Details Added successfully')
				return HttpResponseRedirect('/schoolnew/ict_edit/')
				
			else:
				messages.warning(request,'ICT Details Not Saved')
				print form.errors
				return render (request,'ict_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	


class Ict_update(View):
	
	def get(self,request,**kwargs):
		if request.user.is_authenticated():		
			tid=self.kwargs.get('pk')
			ss=request.user.username			
			if ss.isalpha():
				basic_det=Basicinfo.objects.get(office_code=request.user.username)
				office_chk = 'Yes'
			else:
				office_chk = 'No'
				basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			ict_det = Ictentry.objects.filter(school_key=basic_det.id)
			ict_lst=Ict_list.objects.all()
			ict_suply=Ict_suppliers.objects.all()
			instance=Ictentry.objects.get(id=tid)
			sch_key = basic_det.id
			form=ictentry_form(instance=instance)

			ict_type = instance.ict_type
			working_no = instance.working_no
			not_working_no = instance.not_working_no
			supplied_by = instance.supplied_by
			donor_ict = instance.donor_ict
			return render (request,'ict_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
	
	def post(self,request,**kwargs):
		if request.user.is_authenticated():
			tid=self.kwargs.get('pk')
			ss=request.user.username			
			if ss.isalpha():
				basic_det=Basicinfo.objects.get(office_code=request.user.username)
			else:
				basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			form = ictentry_form(request.POST,request.FILES)
			instance=Ictentry.objects.get(id=tid)
			newict = Ictentry.objects.get(id=tid)
			if form.is_valid():
				newict.ict_type = form.cleaned_data['ict_type']
				newict.working_no = form.cleaned_data['working_no']
				newict.not_working_no = form.cleaned_data['not_working_no']
				newict.supplied_by = form.cleaned_data['supplied_by']
				newict.donor_ict = form.cleaned_data['donor_ict']
				newict.save()
				messages.success(request,'ICT Details Updated successfully')
				return HttpResponseRedirect('/schoolnew/ict_edit/')
			else:
				messages.warning(request,'ICT Details Not Updated')
				return render (request,'ict_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	


class Ict_delete(View):
	
	def get(self, request,**kwargs):
		if request.user.is_authenticated():
			tid=self.kwargs.get('pk')
			data=Ictentry.objects.get(id=tid)
			data.delete()
			msg= data.ict_type+" - has been successfully removed "
			messages.success(request, msg ) 
			return HttpResponseRedirect('/schoolnew/ict_edit/')
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
class Passpercent_edit(View):
	
	def get(self,request,**kwargs):
		if request.user.is_authenticated():		
			tid=self.kwargs.get('pk')
			basic_det=Basicinfo.objects.get(udise_code=request.user.username)	
			acadyr_lst=Acadyr_mas.objects.all()
			sch_key = basic_det.id
			passper_det=Passpercent.objects.filter(school_key=sch_key)
			sch_key = basic_det.id
			form=pass_form()
			acade_det = Academicinfo.objects.get(school_key=basic_det.id)
			return render (request,'pass_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
	
	def post(self,request,**kwargs):
		if request.user.is_authenticated():		
			pk=self.kwargs.get('pk')

			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			form=pass_form(request.POST,request.FILES)

			if form.is_valid():
				sch_key=form.cleaned_data['school_key']	
				chk_ayr=form.cleaned_data['acad_yr']

				if Passpercent.objects.filter(school_key=basic_det.id).filter(acad_yr=form.cleaned_data['acad_yr']).exists():
					messages.warning(request,'This academic year information already fed. If you want to correct pl. use Update option')			
					return HttpResponseRedirect('/schoolnew/pass_edit/')
				else:
					newpass = Passpercent(
						school_key=basic_det,
						acad_yr = form.cleaned_data['acad_yr'],
						ten_b_app =  form.cleaned_data['ten_b_app'],
						ten_b_pass =  form.cleaned_data['ten_b_pass'],
						ten_g_app = form.cleaned_data['ten_g_app'],
						ten_g_pass =  form.cleaned_data['ten_g_pass'],
						ten_app =  form.cleaned_data['ten_app'],
						ten_pass =  form.cleaned_data['ten_pass'],
						twelve_b_app = form.cleaned_data['twelve_b_app'],
						twelve_b_pass = form.cleaned_data['twelve_b_pass'],
						twelve_g_app = form.cleaned_data['twelve_g_app'],
						twelve_g_pass = form.cleaned_data['twelve_g_pass'],
						twelve_app = form.cleaned_data['twelve_app'],
						twelve_pass = form.cleaned_data['twelve_pass'],
						ten_b_per= form.cleaned_data['ten_b_per'],
						ten_g_per= form.cleaned_data['ten_g_per'],
						ten_a_per= form.cleaned_data['ten_a_per'],
						twelve_b_per= form.cleaned_data['twelve_b_per'],
						twelve_g_per= form.cleaned_data['twelve_g_per'],
						twelve_a_per= form.cleaned_data['twelve_a_per'],
						)
					newpass.save()
					messages.success(request,'Pass Percent Details Added successfully')
				return HttpResponseRedirect('/schoolnew/pass_edit/')
			else:
				messages.warning(request,'Pass Percent Details Not Saved')
				return render (request,'pass_edit_upd.html',locals())			
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	




class Passpercent_update(View):
	
	def get(self,request,**kwargs):
		if request.user.is_authenticated():		
			tid=self.kwargs.get('pk')
			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			passper_det=Passpercent.objects.filter(school_key=basic_det.id)
			instance=Passpercent.objects.get(id=tid)
			sch_key = basic_det.id
			acadyr_lst=Acadyr_mas.objects.all()
			form=pass_form(instance=instance)
			acad_yr = instance.acad_yr
			ten_b_app =  instance.ten_b_app
			ten_b_pass =  instance.ten_b_pass
			ten_g_app = instance.ten_g_app
			ten_g_pass =  instance.ten_g_pass
			ten_app =  instance.ten_app
			ten_pass = instance.ten_pass
			twelve_b_app = instance.twelve_b_app
			twelve_b_pass = instance.twelve_b_pass
			twelve_g_app = instance.twelve_g_app
			twelve_g_pass = instance.twelve_g_pass
			twelve_app = instance.twelve_app
			twelve_pass = instance.twelve_pass
			ten_b_per= instance.ten_b_per
			ten_g_per= instance.ten_g_per
			ten_a_per= instance.ten_a_per
			twelve_b_per= instance.twelve_b_per
			twelve_g_per= instance.twelve_g_per
			twelve_a_per= instance.twelve_a_per
			acade_det = Academicinfo.objects.get(school_key=basic_det.id)			
			return render (request,'pass_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
	def post(self,request,**kwargs):
		if request.user.is_authenticated():		
			tid=self.kwargs.get('pk')

			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
			form = pass_form(request.POST,request.FILES)
			instance=Passpercent.objects.get(id=tid)
			newpassper = Passpercent.objects.get(id=tid)
			if form.is_valid():
				chk_ayr=form.cleaned_data['acad_yr']
				if Passpercent.objects.filter(school_key=basic_det.id).filter(acad_yr=form.cleaned_data['acad_yr']).exclude(id=tid).exists():
					messages.warning(request,'This academic year information already fed. If you want to correct pl. use Update option')
					return HttpResponseRedirect('/schoolnew/pass_edit/')
				else:
					newpassper.acad_yr = form.cleaned_data['acad_yr']
					newpassper.ten_b_app =  form.cleaned_data['ten_b_app']
					newpassper.ten_b_pass =  form.cleaned_data['ten_b_pass']
					newpassper.ten_g_app = form.cleaned_data['ten_g_app']
					newpassper.ten_g_pass =  form.cleaned_data['ten_g_pass']
					newpassper.ten_app =  form.cleaned_data['ten_app']
					newpassper.ten_pass =  form.cleaned_data['ten_pass']
					newpassper.twelve_b_app = form.cleaned_data['twelve_b_app']
					newpassper.twelve_b_pass = form.cleaned_data['twelve_b_pass']
					newpassper.twelve_g_app = form.cleaned_data['twelve_g_app']
					newpassper.twelve_g_pass = form.cleaned_data['twelve_g_pass']
					newpassper.twelve_app = form.cleaned_data['twelve_app']
					newpassper.twelve_pass = form.cleaned_data['twelve_pass']
					newpassper.ten_b_per= form.cleaned_data['ten_b_per']
					newpassper.ten_g_per= form.cleaned_data['ten_g_per']
					newpassper.ten_a_per= form.cleaned_data['ten_a_per']
					newpassper.twelve_b_per= form.cleaned_data['twelve_b_per']
					newpassper.twelve_g_per= form.cleaned_data['twelve_g_per']
					newpassper.twelve_a_per= form.cleaned_data['twelve_a_per']
					newpassper.save()
					messages.success(request,'Pass Percent Updated successfully')
					return HttpResponseRedirect('/schoolnew/pass_edit/')
			else:
				messages.warning(request,'Pass Percent Not Updated')
				return render (request,'pass_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	

class Passpercent_delete(View):
	
	def get(self, request,**kwargs):
		if request.user.is_authenticated():    	
			tid=self.kwargs.get('pk')
			data=Passpercent.objects.get(id=tid)
			data.delete()
			msg= data.acad_yr+" - Pass percent has been successfully removed "
			messages.success(request, msg ) 
			return HttpResponseRedirect('/schoolnew/pass_edit/')
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
class Off_home_page(View):
	
	def get(self,request,**kwargs):
		if request.user.is_authenticated():
			if (Basicinfo.objects.filter(udise_code=request.user.account.id).count())>0:
				basic_det=Basicinfo.objects.get(udise_code=request.user.account.id)
				if (Staff.objects.filter(school_key=basic_det.id).count())>0:
					offnonteach_det = Staff.objects.filter(school_key=basic_det.id)
				if (Ictentry.objects.filter(school_key=basic_det.id).count())>0:
					off_ict_det = Ictentry.objects.filter(school_key=basic_det.id)					
				return render (request,'home_edit2.html',locals())
			else:
				return render (request,'home_edit2.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	

class Office_basic_info(UpdateView):
	
	def get(self,request,**kwargs):
		if request.user.is_authenticated():		
			pk=self.kwargs.get('pk')
			district_list = District.objects.all().order_by('district_name')
			if (Basicinfo.objects.filter(udise_code=request.user.account.id).count())>0:
				basic_det=Basicinfo.objects.get(udise_code=request.user.account.id)
				if (Staff.objects.filter(school_key=basic_det.id).count())>0:
					offnonteach_det = Staff.objects.filter(school_key=basic_det.id)			
				instance = Basicinfo.objects.get(udise_code=request.user.account.id)
				form=BasicForm(instance=instance)
				udise_code=instance.udise_code
				office_code = instance.office_code			
				school_id = instance.school_id
				school_name = instance.school_name 
				school_name_tamil = instance.school_name_tamil
				if instance.school_name_tamil:
					word = instance.school_name_tamil
				else:
					word=''
				district = instance.district
				block = instance.block
				local_body_type= instance.local_body_type
				village_panchayat =instance.village_panchayat
				vill_habitation = instance.vill_habitation
				town_panchayat = instance.town_panchayat
				town_panchayat_ward = instance.town_panchayat_ward
				municipality = instance.municipality
				municipal_ward = instance.municipal_ward
				cantonment = instance.cantonment
				cantonment_ward = instance.cantonment_ward
				township = instance.township
				township_ward = instance.township_ward
				corporation = instance.corporation
				corpn_zone = instance.corpn_zone
				corpn_ward = instance.corpn_ward
				address  = instance.address
				pincode = instance.pincode
				stdcode = instance.stdcode
				landline = instance.landline
				mobile = instance.mobile
				office_email1 = instance.office_email1
				office_email2 = instance.office_email2
				sch_directorate=instance.sch_directorate
				build_status=instance.build_status
				new_build=instance.new_build
				website = instance.website
				bank_dist=instance.bank_dist
				bank = instance.bank
				branch = instance.branch
				bankaccno = instance.bankaccno
				parliament = instance.parliament
				assembly = instance.assembly
				offcat_id=instance.offcat_id
				draw_off_code=instance.draw_off_code
				offcat_id=request.user.account.user_category_id			
				return render (request,'office_basic_info.html',locals())				
			else:
				form=BasicForm()
				udise_code=request.user.account.id
				offcat_id=request.user.account.user_category_id
				office_code=request.user.username
			return render (request,'office_basic_info.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
	
	def post(self, request, **kwargs):
		if request.user.is_authenticated():		
			pk=self.kwargs.get('pk')
			if (Basicinfo.objects.filter(udise_code=request.user.account.id).count())>0:
				basic_det=Basicinfo.objects.filter(udise_code=request.user.account.id)
			if (Basicinfo.objects.filter(udise_code=request.user.account.id).count())>0:	
				instance = Basicinfo.objects.get(udise_code=request.user.account.id)
				office_editsave=Basicinfo.objects.get(udise_code=request.user.account.id)
				form=BasicForm(request.POST,request.FILES)	
				if form.is_valid():
					office_editsave.school_name = form.cleaned_data['school_name'].upper()
					office_editsave.school_name_tamil = request.POST['word']
					office_editsave.udise_code = form.cleaned_data['udise_code']
					office_editsave.school_id = form.cleaned_data['udise_code']
					office_editsave.office_code = form.cleaned_data['office_code']
					office_editsave.offcat_id = form.cleaned_data['offcat_id']
					office_editsave.draw_off_code = form.cleaned_data['draw_off_code']
					office_editsave.district = form.cleaned_data['district']
					office_editsave.block = form.cleaned_data['block']
					office_editsave.local_body_type= form.cleaned_data['local_body_type']
					chk_local_body=Local_body.objects.get(id=request.POST['local_body_type'])			
					if str(chk_local_body)=='Village Panchayat':	
						office_editsave.village_panchayat =form.cleaned_data['village_panchayat']
						office_editsave.vill_habitation = form.cleaned_data['vill_habitation']
						office_editsave.town_panchayat = None
						office_editsave.town_panchayat_ward = None
						office_editsave.municipality = None
						office_editsave.municipal_ward = None
						office_editsave.cantonment = None
						office_editsave.cantonment_ward = None
						office_editsave.township = None
						office_editsave.township_ward = None
						office_editsave.corporation = None
						office_editsave.corpn_zone = None
						office_editsave.corpn_ward = None
					elif str(chk_local_body)=="Town Panchayat":
						office_editsave.village_panchayat =None
						office_editsave.vill_habitation = None
						office_editsave.town_panchayat = form.cleaned_data['town_panchayat']
						office_editsave.town_panchayat_ward = form.cleaned_data['town_panchayat_ward']				
						office_editsave.municipality = None
						office_editsave.municipal_ward = None
						office_editsave.cantonment = None
						office_editsave.cantonment_ward = None
						office_editsave.township = None
						office_editsave.township_ward = None
						office_editsave.corporation = None
						office_editsave.corpn_zone = None
						office_editsave.corpn_ward = None				
					elif str(chk_local_body)=="Municipality":
						office_editsave.village_panchayat =None
						office_editsave.vill_habitation = None
						office_editsave.town_panchayat = None
						office_editsave.town_panchayat_ward = None
						office_editsave.municipality = form.cleaned_data['municipality']
						office_editsave.municipal_ward = form.cleaned_data['municipal_ward']
						office_editsave.cantonment = None
						office_editsave.cantonment_ward = None
						office_editsave.township = None
						office_editsave.township_ward = None
						office_editsave.corporation = None
						office_editsave.corpn_zone = None
						office_editsave.corpn_ward = None				
					elif str(chk_local_body)=="cantonment":
						office_editsave.village_panchayat =None
						office_editsave.vill_habitation = None
						office_editsave.town_panchayat = None
						office_editsave.town_panchayat_ward = None
						office_editsave.municipality = None
						office_editsave.municipal_ward = None
						office_editsave.cantonment = form.cleaned_data['cantonment']
						office_editsave.cantonment_ward = form.cleaned_data['cantonment_ward']
						office_editsave.township = None
						office_editsave.township_ward = None
						office_editsave.corporation = None
						office_editsave.corpn_zone = None
						office_editsave.corpn_ward = None				
					elif str(chk_local_body)=="Township":
						office_editsave.village_panchayat =None
						office_editsave.vill_habitation = None
						office_editsave.town_panchayat = None
						office_editsave.town_panchayat_ward = None
						office_editsave.municipality = None
						office_editsave.municipal_ward = None
						office_editsave.cantonment = None
						office_editsave.cantonment_ward = None
						office_editsave.township = form.cleaned_data['township']
						office_editsave.township_ward = form.cleaned_data['township_ward']
						office_editsave.corporation = None
						office_editsave.corpn_zone = None
						office_editsave.corpn_ward = None				
					elif str(chk_local_body)=="Corporation":
						office_editsave.village_panchayat =None
						office_editsave.vill_habitation = None
						office_editsave.town_panchayat = None
						office_editsave.town_panchayat_ward = None
						office_editsave.municipality = None
						office_editsave.municipal_ward = None
						office_editsave.cantonment = None
						office_editsave.cantonment_ward = None
						office_editsave.township = None
						office_editsave.township_ward = None
						office_editsave.corporation = form.cleaned_data['corporation']
						office_editsave.corpn_zone = form.cleaned_data['corpn_zone']
						office_editsave.corpn_ward = form.cleaned_data['corpn_ward']	

					office_editsave.address  = form.cleaned_data['address']
					office_editsave.pincode = form.cleaned_data['pincode']
					office_editsave.stdcode = form.cleaned_data['stdcode']
					office_editsave.landline = form.cleaned_data['landline']
					office_editsave.mobile = form.cleaned_data['mobile']
					office_editsave.office_email1 = form.cleaned_data['office_email1']
					office_editsave.office_email2 = form.cleaned_data['office_email2']	
					office_editsave.sch_directorate = form.cleaned_data['sch_directorate']			
					office_editsave.website = form.cleaned_data['website']
					office_editsave.build_status = form.cleaned_data['build_status']
					office_editsave.new_build = form.cleaned_data['new_build']
					office_editsave.bank_dist=form.cleaned_data['bank_dist']
					office_editsave.bank = form.cleaned_data['bank']
					office_editsave.branch = form.cleaned_data['branch']
					office_editsave.bankaccno = form.cleaned_data['bankaccno']
					office_editsave.parliament = form.cleaned_data['parliament']
					office_editsave.assembly = form.cleaned_data['assembly']

					office_editsave.save()	

					messages.success(request,'Office Basic Information Updated successfully')
					return HttpResponseRedirect('/schoolnew/office_registration')
				
				else:
					messages.warning(request,'Office Basic Information Not Updated')		
					return render (request,'basic2.html')

			else:
				form = BasicForm(request.POST,request.FILES)
				if form.is_valid():

					officeinfo = Basicinfo(
						school_id=form.cleaned_data['udise_code'],
						school_name = form.cleaned_data['school_name'],
						school_name_tamil = request.POST['word'],
						udise_code = form.cleaned_data['udise_code'],
						office_code = form.cleaned_data['office_code'],
						district = form.cleaned_data['district'],
						block = form.cleaned_data['block'],
						local_body_type= form.cleaned_data['local_body_type'],
						village_panchayat =form.cleaned_data['village_panchayat'],
						vill_habitation = form.cleaned_data['vill_habitation'],
						town_panchayat = form.cleaned_data['town_panchayat'],
						town_panchayat_ward = form.cleaned_data['town_panchayat_ward'],
						municipality = form.cleaned_data['municipality'],
						municipal_ward = form.cleaned_data['municipal_ward'],
						cantonment = form.cleaned_data['cantonment'],
						cantonment_ward = form.cleaned_data['cantonment_ward'],
						township = form.cleaned_data['township'],
						township_ward = form.cleaned_data['township_ward'],
						corporation = form.cleaned_data['corporation'],
						corpn_zone = form.cleaned_data['corpn_zone'],
						corpn_ward = form.cleaned_data['corpn_ward'],
						address  = form.cleaned_data['address'],
						pincode = form.cleaned_data['pincode'],
						stdcode = form.cleaned_data['stdcode'],
						landline = form.cleaned_data['landline'],
						mobile = form.cleaned_data['mobile'],
						office_email1 = form.cleaned_data['office_email1'],
						office_email2 = form.cleaned_data['office_email2'],
						sch_directorate = form.cleaned_data['sch_directorate'],
						website = form.cleaned_data['website'],
						build_status = form.cleaned_data['build_status'],
						new_build=form.cleaned_data['new_build'],
						bank_dist=form.cleaned_data['bank_dist'],
						bank = form.cleaned_data['bank'],
						branch = form.cleaned_data['branch'],
						bankaccno = form.cleaned_data['bankaccno'],			
						parliament = form.cleaned_data['parliament'],
						assembly = form.cleaned_data['assembly'],
						offcat_id = form.cleaned_data['offcat_id'],
						draw_off_code = form.cleaned_data['draw_off_code'],
						
					)
					officeinfo.save()
					return HttpResponseRedirect('/schoolnew/office_registration')
				else:
					return render (request,'basic2.html')
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	

class Offnonteaching_edit(View):
	
	def get(self,request,**kwargs):
		if request.user.is_authenticated():		
			tid=self.kwargs.get('pk')
			if (Basicinfo.objects.filter(udise_code=request.user.account.id).count())>0:			
				basic_det=Basicinfo.objects.get(udise_code=request.user.account.id)
				sch_key = basic_det.id					
				if (Staff.objects.filter(school_key=basic_det.id).count())>0:
					post_det = Staff.objects.filter(Q(school_key=sch_key) & Q(staff_cat=2))

			form=staff_form()
			if ((basic_det.offcat_id==2)|(basic_det.offcat_id==3)|(basic_det.offcat_id==5)|(basic_det.offcat_id==7)|(basic_det.offcat_id==6)|(basic_det.offcat_id==8)|(basic_det.offcat_id==18)|(basic_det.offcat_id==20)|(basic_det.offcat_id==21)|(basic_det.offcat_id==22)|(basic_det.offcat_id==23)|(basic_det.offcat_id==24)|(basic_det.offcat_id==25)|(basic_det.offcat_id==26)|(basic_det.offcat_id==27)):
				desig_det= User_desig.objects.filter(Q(user_cate='SCHOOL&OFFICE') | Q(user_cate='OFFICE') & Q(user_level__isnull=True))
			elif ((basic_det.offcat_id==4)|(basic_det.offcat_id==9)|(basic_det.offcat_id==10)|(basic_det.offcat_id==11)|(basic_det.offcat_id==19)):
				desig_det= User_desig.objects.filter(Q(user_cate='SCHOOL&OFFICE') | Q(user_cate='OFFICE'))
			else:
				desig_det=''
			pg_head='Office Non-Teaching'
			return render (request,'post_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
	
	def post(self,request,**kwargs):
		if request.user.is_authenticated():		
			pk=self.kwargs.get('pk')
			form=staff_form(request.POST,request.FILES)
			if form.is_valid():			
				if request.POST['post_mode']=='Permanent':
					tpost_GO_pd = ''
					ttemgofm_dt = None
					ttemgoto_dt = None
				else:
					tpost_GO_pd = form.cleaned_data['post_GO_pd']
					ttemgofm_dt = form.cleaned_data['temgofm_dt']
					ttemgoto_dt = form.cleaned_data['temgoto_dt']			
				offntpost = Staff(
					school_key = form.cleaned_data['school_key'],
					post_name = form.cleaned_data['post_name'],	
					post_sub = form.cleaned_data['post_sub'],
					post_sanc = form.cleaned_data['post_sanc'],
					post_mode = form.cleaned_data['post_mode'],
					post_GO = form.cleaned_data['post_GO'],
					post_GO_dt = form.cleaned_data['post_GO_dt'],
					post_filled = 0,
					post_vac = form.cleaned_data['post_sanc'],
					post_GO_pd = tpost_GO_pd,
					temgofm_dt = ttemgofm_dt,
					temgoto_dt = ttemgoto_dt,
					staff_cat = 2,	
					)
				offntpost.save()
				messages.success(request,'Office Non-Teaching Staff details Added successfully')			
				return HttpResponseRedirect('/schoolnew/offnonteaching_edit/')
			else:
				messages.warning(request,'Office Non-Teaching Staff details Not Updated')
				return render (request,'post_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
class Offntpost_update(View):
	
	def get(self,request,**kwargs):
		if request.user.is_authenticated():
			tid=self.kwargs.get('pk')
			basic_det=Basicinfo.objects.get(udise_code=request.user.account.id)
			instance=Staff.objects.get(id=tid)
			sch_key = basic_det.id
			nonteach_post = Staff.objects.filter(school_key=sch_key)
			nonteach_det_dt=Staff.objects.get(id=tid)
			form=staff_form(instance=instance)
			post_name= instance.post_name
			post_sub= instance.post_sub		
			post_sanc=instance.post_sanc
			post_mode= instance.post_mode
			post_GO= instance.post_GO
			go_dt= instance.post_GO_dt
			post_GO_dt= instance.post_GO_dt
			post_GO_pd= instance.post_GO_pd
			post_filled = instance.post_filled
			post_vac = instance.post_vac
			pg_head='Office Non-Teaching'
			if nonteach_det_dt.post_GO_dt:
				go_dt=nonteach_det_dt.post_GO_dt.strftime('%Y-%m-%d')	
			if ((basic_det.offcat_id==2)|(basic_det.offcat_id==3)|(basic_det.offcat_id==5)|(basic_det.offcat_id==7)|(basic_det.offcat_id==6)|(basic_det.offcat_id==8)|(basic_det.offcat_id==18)|(basic_det.offcat_id==20)|(basic_det.offcat_id==21)|(basic_det.offcat_id==22)|(basic_det.offcat_id==23)|(basic_det.offcat_id==24)|(basic_det.offcat_id==25)|(basic_det.offcat_id==26)|(basic_det.offcat_id==27)):
				desig_det= User_desig.objects.filter(Q(user_cate='SCHOOL&OFFICE') | Q(user_cate='OFFICE')).exclude(user_level='HOD')
			elif ((basic_det.offcat_id==4)|(basic_det.offcat_id==9)|(basic_det.offcat_id==10)|(basic_det.offcat_id==11)|(basic_det.offcat_id==11)):
				desig_det= User_desig.objects.filter(Q(user_cate='SCHOOL&OFFICE') | Q(user_cate='OFFICE'))
			else:
				desig_det=''
			sch_key = basic_det.id
			return render (request,'post_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	
	def post(self,request,**kwargs):
		if request.user.is_authenticated():
			tid=self.kwargs.get('pk')
			basic_det=Basicinfo.objects.get(udise_code=request.user.account.id)
			form = staff_form(request.POST,request.FILES)
			instance=Staff.objects.get(id=tid)
			newnonteachpost = Staff.objects.get(id=tid)		

			if form.is_valid():
				newnonteachpost.post_name = form.cleaned_data['post_name']			
				newnonteachpost.post_sanc = form.cleaned_data['post_sanc']
				newnonteachpost.post_mode = form.cleaned_data['post_mode']
				newnonteachpost.post_GO = form.cleaned_data['post_GO']
				newnonteachpost.post_GO_dt = form.cleaned_data['post_GO_dt']
				newnonteachpost.post_GO_pd = form.cleaned_data['post_GO_pd']
				newnonteachpost.post_sub = form.cleaned_data['post_sub']
				newnonteachpost.staff_cat = 2
				newnonteachpost.post_vac = (form.cleaned_data['post_sanc']-newnonteachpost.post_filled)
				if newnonteachpost.post_mode=='Permanent':
					newnonteachpost.temgofm_dt = None
					newnonteachpost.temgoto_dt = None
				else:
					newnonteachpost.temgofm_dt = form.cleaned_data['temgofm_dt']
					newnonteachpost.temgoto_dt = form.cleaned_data['temgoto_dt']
				newnonteachpost.save()
				messages.success(request,'Non-Teaching Post Details Updated successfully')
				return HttpResponseRedirect('/schoolnew/offnonteaching_edit/')
			else:
				messages.warning(request,'Office Non-Teaching Staff details Not Updated')
				print form.errors
				return render (request,'off_staff_edit_upd.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	


class Offnonteaching_delete(View):
	
	def get(self, request,**kwargs):
		if request.user.is_authenticated():    	
			tid=self.kwargs.get('pk')
			data=Staff.objects.get(id=tid)
			data.delete()
			msg= data.post_name +" - Posts has been successfully removed "
			messages.success(request, msg ) 
			return HttpResponseRedirect('/schoolnew/offnonteaching_edit/')
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))			
	



class Sch_Blk_abs(View):
	
	def get(self,request,**kwargs):
		blk_id=self.kwargs['pk']
		deptlst=Manage_cate.objects.all().order_by('id')

		# blkid=Basicinfo.objects.get(udise_code=int(request.user.username))

		totsch=Basicinfo.objects.filter(block1=blk_id,chk_dept__in=[1,2,3],chk_manage__in=[1,2,3]).values('chk_manage','chk_dept').annotate(mang_schtot=Count('chk_dept')).order_by('chk_dept','chk_manage')

		totschst=Basicinfo.objects.filter(chk_dept__in=[1,2,3],chk_manage__in=[1,2,3],block1=blk_id).values('chk_dept').annotate(schmantot=Count('chk_dept'))
		totschgrtot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],chk_manage__in=[1,2,3],block1=blk_id).count()


		bitotsch=Basicinfo.objects.filter(chk_dept__in=[1,2,3],manage_cate_id__in=[1,2,3],block_id=blk_id).values('chk_manage','chk_dept').annotate(bi_schtot=Count('chk_dept')).order_by('chk_dept','chk_manage')
		bischst=Basicinfo.objects.filter(chk_dept__in=[1,2,3],manage_cate_id__in=[1,2,3],block_id=blk_id).values('chk_dept').annotate(bimantot=Count('chk_dept'))
		bigrtot=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3],block_id=blk_id).count()
		aitotsch=Basicinfo.objects.filter(chk_dept__in=[1,2,3],manage_cate_id__in=[1,2,3],block_id=blk_id).values('chk_manage','chk_dept').annotate(bi_schtot=Count('chk_dept'),acad_schcoun=Count('academicinfo')).order_by('chk_dept','chk_manage')
		aistot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],block_id=blk_id).values('chk_dept').annotate(acad_schtot=Count('academicinfo')).order_by('chk_dept')
		aigrtot=Basicinfo.objects.filter(block_id=blk_id).values('academicinfo__school_key').count()

		iitotsch=Basicinfo.objects.filter(chk_dept__in=[1,2,3],manage_cate_id__in=[1,2,3],block_id=blk_id).values('chk_manage','chk_dept').annotate(bi_schtot=Count('chk_dept'),infra_schcoun=Count('infradet')).order_by('chk_dept','chk_manage')
		iistot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],block_id=blk_id).values('chk_dept').annotate(infra_schtot=Count('infradet')).order_by('chk_dept')
		iigrtot=Basicinfo.objects.filter(block_id=blk_id).values('infradet__school_key').count()

		cstotsch=Basicinfo.objects.filter(chk_dept__in=[1,2,3],manage_cate_id__in=[1,2,3],block_id=blk_id).values('chk_manage','chk_dept').annotate(cs_schtot=Count('chk_dept'),cs_schcoun=Count('class_section__school_key',distinct = True)).order_by('chk_dept','chk_manage')
		csstot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],block_id=blk_id).values('chk_dept').annotate(cs_subtot=Count('class_section__school_key',distinct = True)).order_by('chk_dept')
		csgrtot=Basicinfo.objects.filter(block_id=blk_id).values('class_section__school_key').distinct().count()

		tptotsch=Basicinfo.objects.filter(chk_dept__in=[1,2,3],manage_cate_id__in=[1,2,3],staff__staff_cat='1',block_id=blk_id).values('chk_manage','chk_dept').annotate(tp_schtot=Count('chk_dept'),tp_schcoun=Sum('staff__post_sanc')).order_by('chk_dept','chk_manage')
		tpstot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],staff__staff_cat='1',block_id=blk_id).values('chk_dept').annotate(tp_schtot=Sum('staff__post_sanc')).order_by('chk_dept')
		tpgrtot=Basicinfo.objects.filter(staff__staff_cat='1',block_id=blk_id).values('staff__post_sanc').aggregate(Sum('staff__post_sanc'))
		
		tpftotsch=Basicinfo.objects.filter(chk_dept__in=[1,2,3],manage_cate_id__in=[1,2,3],staff__staff_cat='1',staff__post_filled__gt='0',block_id=blk_id).values('chk_manage','chk_dept').annotate(tpf_schtot=Count('chk_dept'),tpf_schcoun=Sum('staff__post_filled')).order_by('chk_dept','chk_manage')
		tpfstot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],staff__staff_cat='1',staff__post_filled__gt='0',block_id=blk_id).values('chk_dept').annotate(tpf_schtot=Sum('staff__post_filled')).order_by('chk_dept')
		tpfgrtot=Basicinfo.objects.filter(block_id=blk_id,staff__staff_cat='1',staff__post_filled__gt='0').values('staff__post_filled').aggregate(Sum('staff__post_filled'))

		# ntptotsch=Basicinfo.objects.filter(chk_dept__in=[1,2,3,manage_cate_id__in=[1,2,3],staff__staff_cat='2').values('chk_manage','chk_dept').annotate(ntp_schtot=Count('chk_dept'),ntp_schcoun=Sum('staff__post_sanc')).order_by('chk_dept','chk_manage')
		ntptotsch=Basicinfo.objects.filter(staff__staff_cat='2',block_id=blk_id).values('chk_manage','chk_dept').annotate(ntp_schtot=Count('chk_dept'),ntp_schcoun=Sum('staff__post_sanc')).order_by('chk_dept','chk_manage')
		ntpstot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],staff__staff_cat='2',block_id=blk_id).values('chk_dept').annotate(ntp_schtot=Sum('staff__post_sanc')).order_by('chk_dept')
		# ntpgrtot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],staff__staff_cat='2').values('staff__post_sanc').annotate(Sum('staff__post_sanc'))	
		# ntpgrtot=Staff.objects.filter(staff_cat='2',block_id=blk_id).aggregate(Sum('post_sanc'))
		ntpgrtot=Basicinfo.objects.filter(block_id=blk_id,staff__staff_cat='2').aggregate(Sum('staff__post_sanc'))

		# ntpftotsch=Basicinfo.objects.filter(chk_dept__in=[1,2,3],manage_cate_id__in=[1,2,3],staff__staff_cat='2',staff__post_filled__gt='0').values('chk_manage','chk_dept').annotate(ntpf_schtot=Count('chk_dept'),ntpf_schcoun=Count('staff')).order_by('chk_dept','chk_manage')
		ntpftotsch=Basicinfo.objects.filter(staff__staff_cat='2',staff__post_filled__gt='0',block_id=blk_id).values('chk_manage','chk_dept').annotate(ntpf_schtot=Count('chk_dept'),ntpf_schcoun=Sum('staff__post_filled')).order_by('chk_dept','chk_manage')
		ntpfstot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],staff__staff_cat='2',staff__post_filled__gt='0',block_id=blk_id).values('chk_dept').annotate(ntpf_schtot=Sum('staff__post_filled')).order_by('chk_dept')
		# ntpfgrtot=Staff.objects.filter(staff_cat='2',post_filled__gt='0',block_id=blk_id).aggregate(Sum('post_filled'))
		ntpfgrtot=Basicinfo.objects.filter(block_id=blk_id,staff__staff_cat='2',staff__post_filled__gt='0').aggregate(Sum('staff__post_filled'))

		return render(request,'block_abs.html',locals())



class Sch_Dist_abs(View):
	
	def get(self,request,**kwargs):
		d_id=self.kwargs['pk']
		deptlst=Manage_cate.objects.all().order_by('id')

		blkid=Basicinfo.objects.get(udise_code=int(request.user.username))

		totsch=Basicinfo.objects.filter(district1=d_id,chk_dept__in=[1,2,3],chk_manage__in=[1,2,3]).values('chk_manage','chk_dept').annotate(mang_schtot=Count('chk_dept')).order_by('chk_dept','chk_manage')

		totschst=Basicinfo.objects.filter(chk_dept__in=[1,2,3],chk_manage__in=[1,2,3],district1=d_id).values('chk_dept').annotate(schmantot=Count('chk_dept'))
		totschgrtot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],chk_manage__in=[1,2,3],district1=d_id).count()


		bitotsch=Basicinfo.objects.filter(chk_dept__in=[1,2,3],manage_cate_id__in=[1,2,3],district_id=d_id).values('chk_manage','chk_dept').annotate(bi_schtot=Count('chk_dept')).order_by('chk_dept','chk_manage')
		bischst=Basicinfo.objects.filter(chk_dept__in=[1,2,3],manage_cate_id__in=[1,2,3],district_id=d_id).values('chk_dept').annotate(bimantot=Count('chk_dept'))
		bigrtot=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3],district_id=d_id).count()
		aitotsch=Basicinfo.objects.filter(chk_dept__in=[1,2,3],manage_cate_id__in=[1,2,3],district_id=d_id).values('chk_manage','chk_dept').annotate(bi_schtot=Count('chk_dept'),acad_schcoun=Count('academicinfo')).order_by('chk_dept','chk_manage')
		aistot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],district_id=d_id).values('chk_dept').annotate(acad_schtot=Count('academicinfo')).order_by('chk_dept')
		aigrtot=Basicinfo.objects.filter(district_id=d_id).values('academicinfo__school_key').count()

		iitotsch=Basicinfo.objects.filter(chk_dept__in=[1,2,3],manage_cate_id__in=[1,2,3],district_id=d_id).values('chk_manage','chk_dept').annotate(bi_schtot=Count('chk_dept'),infra_schcoun=Count('infradet')).order_by('chk_dept','chk_manage')
		iistot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],district_id=d_id).values('chk_dept').annotate(infra_schtot=Count('infradet')).order_by('chk_dept')
		iigrtot=Basicinfo.objects.filter(district_id=d_id).values('infradet__school_key').count()

		cstotsch=Basicinfo.objects.filter(chk_dept__in=[1,2,3],manage_cate_id__in=[1,2,3],district_id=d_id).values('chk_manage','chk_dept').annotate(cs_schtot=Count('chk_dept'),cs_schcoun=Count('class_section__school_key',distinct = True)).order_by('chk_dept','chk_manage')
		csstot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],district_id=d_id).values('chk_dept').annotate(cs_subtot=Count('class_section__school_key',distinct = True)).order_by('chk_dept')
		csgrtot=Basicinfo.objects.filter(district_id=d_id).values('class_section__school_key').distinct().count()

		tptotsch=Basicinfo.objects.filter(chk_dept__in=[1,2,3],manage_cate_id__in=[1,2,3],staff__staff_cat='1',district_id=d_id).values('chk_manage','chk_dept').annotate(tp_schtot=Count('chk_dept'),tp_schcoun=Sum('staff__post_sanc')).order_by('chk_dept','chk_manage')
		tpstot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],staff__staff_cat='1',district_id=d_id).values('chk_dept').annotate(tp_schtot=Sum('staff__post_sanc')).order_by('chk_dept')
		tpgrtot=Basicinfo.objects.filter(staff__staff_cat='1',district_id=d_id).values('staff__post_sanc').aggregate(Sum('staff__post_sanc'))
		
		tpftotsch=Basicinfo.objects.filter(chk_dept__in=[1,2,3],manage_cate_id__in=[1,2,3],staff__staff_cat='1',staff__post_filled__gt='0',district_id=d_id).values('chk_manage','chk_dept').annotate(tpf_schtot=Count('chk_dept'),tpf_schcoun=Sum('staff__post_filled')).order_by('chk_dept','chk_manage')
		tpfstot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],staff__staff_cat='1',staff__post_filled__gt='0',district_id=d_id).values('chk_dept').annotate(tpf_schtot=Sum('staff__post_filled')).order_by('chk_dept')
		tpfgrtot=Basicinfo.objects.filter(district_id=d_id,staff__staff_cat='1',staff__post_filled__gt='0').values('staff__post_filled').aggregate(Sum('staff__post_filled'))

		# ntptotsch=Basicinfo.objects.filter(chk_dept__in=[1,2,3,manage_cate_id__in=[1,2,3],staff__staff_cat='2').values('chk_manage','chk_dept').annotate(ntp_schtot=Count('chk_dept'),ntp_schcoun=Sum('staff__post_sanc')).order_by('chk_dept','chk_manage')
		ntptotsch=Basicinfo.objects.filter(staff__staff_cat='2',district_id=d_id).values('chk_manage','chk_dept').annotate(ntp_schtot=Count('chk_dept'),ntp_schcoun=Sum('staff__post_sanc')).order_by('chk_dept','chk_manage')
		ntpstot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],staff__staff_cat='2',district_id=d_id).values('chk_dept').annotate(ntp_schtot=Sum('staff__post_sanc')).order_by('chk_dept')
		# ntpgrtot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],staff__staff_cat='2').values('staff__post_sanc').annotate(Sum('staff__post_sanc'))	
		# ntpgrtot=Staff.objects.filter(staff_cat='2',district_id=d_id).aggregate(Sum('post_sanc'))
		ntpgrtot=Basicinfo.objects.filter(district_id=d_id,staff__staff_cat='2').aggregate(Sum('staff__post_sanc'))

		# ntpftotsch=Basicinfo.objects.filter(chk_dept__in=[1,2,3],manage_cate_id__in=[1,2,3],staff__staff_cat='2',staff__post_filled__gt='0').values('chk_manage','chk_dept').annotate(ntpf_schtot=Count('chk_dept'),ntpf_schcoun=Count('staff')).order_by('chk_dept','chk_manage')
		ntpftotsch=Basicinfo.objects.filter(staff__staff_cat='2',staff__post_filled__gt='0',district_id=d_id).values('chk_manage','chk_dept').annotate(ntpf_schtot=Count('chk_dept'),ntpf_schcoun=Sum('staff__post_filled')).order_by('chk_dept','chk_manage')
		ntpfstot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],staff__staff_cat='2',staff__post_filled__gt='0',district_id=d_id).values('chk_dept').annotate(ntpf_schtot=Sum('staff__post_filled')).order_by('chk_dept')
		# ntpfgrtot=Staff.objects.filter(staff_cat='2',post_filled__gt='0',district_id=d_id).aggregate(Sum('post_filled'))
		ntpfgrtot=Basicinfo.objects.filter(district_id=d_id,staff__staff_cat='2',staff__post_filled__gt='0').aggregate(Sum('staff__post_filled'))

		return render(request,'dist_abs.html',locals())




class Sch_State_abs(View):
	
	def get(self,request,**kwargs):
		deptlst=Manage_cate.objects.all().order_by('id')
		
		totsch=Basicinfo.objects.filter(chk_dept__in=[1,2,3],chk_manage__in=[1,2,3]).values('chk_manage','chk_dept').annotate(mang_schtot=Count('chk_dept')).order_by('chk_dept','chk_manage')
		totschst=Basicinfo.objects.filter(chk_dept__in=[1,2,3],chk_manage__in=[1,2,3]).values('chk_dept').annotate(schmantot=Count('chk_dept'))
		totschgrtot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],chk_manage__in=[1,2,3]).count()

		bitotsch=Basicinfo.objects.filter(chk_dept__in=[1,2,3],manage_cate_id__in=[1,2,3]).values('chk_manage','chk_dept').annotate(bi_schtot=Count('chk_dept')).order_by('chk_dept','chk_manage')
		bischst=Basicinfo.objects.filter(chk_dept__in=[1,2,3],manage_cate_id__in=[1,2,3]).values('chk_dept').annotate(bimantot=Count('chk_dept'))
		bigrtot=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3]).count()
		aitotsch=Basicinfo.objects.filter(chk_dept__in=[1,2,3],manage_cate_id__in=[1,2,3]).values('chk_manage','chk_dept').annotate(bi_schtot=Count('chk_dept'),acad_schcoun=Count('academicinfo')).order_by('chk_dept','chk_manage')
		aistot=Basicinfo.objects.filter(chk_dept__in=[1,2,3]).values('chk_dept').annotate(acad_schtot=Count('academicinfo')).order_by('chk_dept')
		aigrtot=Academicinfo.objects.all().count()
		iitotsch=Basicinfo.objects.filter(chk_dept__in=[1,2,3],manage_cate_id__in=[1,2,3]).values('chk_manage','chk_dept').annotate(bi_schtot=Count('chk_dept'),infra_schcoun=Count('infradet')).order_by('chk_dept','chk_manage')
		iistot=Basicinfo.objects.filter(chk_dept__in=[1,2,3]).values('chk_dept').annotate(infra_schtot=Count('infradet')).order_by('chk_dept')
		iigrtot=Infradet.objects.all().count()

		cstotsch=Basicinfo.objects.filter(chk_dept__in=[1,2,3],manage_cate_id__in=[1,2,3]).values('chk_manage','chk_dept').annotate(cs_schtot=Count('chk_dept'),cs_schcoun=Count('class_section__school_key',distinct = True)).order_by('chk_dept','chk_manage')
		csstot=Basicinfo.objects.filter(chk_dept__in=[1,2,3]).values('chk_dept').annotate(cs_subtot=Count('class_section__school_key',distinct = True)).order_by('chk_dept')
		csgrtot=Class_section.objects.all().values('school_key').distinct().count()

		tptotsch=Basicinfo.objects.filter(chk_dept__in=[1,2,3],manage_cate_id__in=[1,2,3],staff__staff_cat='1').values('chk_manage','chk_dept').annotate(tp_schtot=Count('chk_dept'),tp_schcoun=Sum('staff__post_sanc')).order_by('chk_dept','chk_manage')
		tpstot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],staff__staff_cat='1').values('chk_dept').annotate(tp_schtot=Sum('staff__post_sanc')).order_by('chk_dept')
		tpgrtot=Staff.objects.filter(staff_cat='1').aggregate(Sum('post_sanc'))
		
		tpftotsch=Basicinfo.objects.filter(chk_dept__in=[1,2,3],manage_cate_id__in=[1,2,3],staff__staff_cat='1',staff__post_filled__gt='0').values('chk_manage','chk_dept').annotate(tpf_schtot=Count('chk_dept'),tpf_schcoun=Sum('staff__post_filled')).order_by('chk_dept','chk_manage')
		tpfstot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],staff__staff_cat='1',staff__post_filled__gt='0').values('chk_dept').annotate(tpf_schtot=Sum('staff__post_filled')).order_by('chk_dept')
		tpfgrtot=Staff.objects.filter(staff_cat='1',post_filled__gt='0').aggregate(Sum('post_filled'))

		ntptotsch=Basicinfo.objects.filter(staff__staff_cat='2').values('chk_manage','chk_dept').annotate(ntp_schtot=Count('chk_dept'),ntp_schcoun=Sum('staff__post_sanc')).order_by('chk_dept','chk_manage')
		ntpstot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],staff__staff_cat='2').values('chk_dept').annotate(ntp_schtot=Sum('staff__post_sanc')).order_by('chk_dept')
		ntpgrtot=Staff.objects.filter(staff_cat='2').aggregate(Sum('post_sanc'))
		
		ntpftotsch=Basicinfo.objects.filter(staff__staff_cat='2',staff__post_filled__gt='0').values('chk_manage','chk_dept').annotate(ntpf_schtot=Count('chk_dept'),ntpf_schcoun=Sum('staff__post_filled')).order_by('chk_dept','chk_manage')
		ntpfstot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],staff__staff_cat='2',staff__post_filled__gt='0').values('chk_dept').annotate(ntpf_schtot=Sum('staff__post_filled')).order_by('chk_dept')
		ntpfgrtot=Staff.objects.filter(staff_cat='2',post_filled__gt='0').aggregate(Sum('post_filled'))

		return render(request,'state_abs.html',locals())

class Sch_sr_bi(View):
	
	def get(self,request,**kwargs):
		dl=District.objects.all().order_by('id')
		schlst=Basicinfo.objects.all().values('chk_dept','district').annotate(disttot=Count('district')).order_by('district')
		disttot=Basicinfo.objects.filter(chk_dept__in=[1,2,3]).values('district').annotate(schsubtot=Count('chk_dept'))
		schgrtot=Basicinfo.objects.filter(chk_dept__in=[1,2,3]).values('chk_dept').annotate(schgtot=Count('chk_dept'))
		schtotal=Basicinfo.objects.filter(chk_dept__in=[1,2,3]).count()

		mandet=Basicinfo.objects.filter(chk_dept__in=[1,2,3]).values('manage_cate_id','district').annotate(mdet=Count('district')).order_by('district')
		mansubtot=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3]).values('district').annotate(mantot=Count('district'))
		mangrtot=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3]).values('manage_cate').annotate(mangtot=Count('manage_cate'))
		mantotal=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3]).count()

		dsemandet=Basicinfo.objects.filter(chk_dept__in=[1]).values('manage_cate_id','district').annotate(dsemdet=Count('district')).order_by('district')
		dsemansubtot=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3]).values('district').annotate(dsemantot=Count('district'))
		dsemangrtot=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3]).values('manage_cate').annotate(dsemangtot=Count('manage_cate'))
		dsemantotal=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3]).count()

		deemandet=Basicinfo.objects.filter(chk_dept__in=[2]).values('manage_cate_id','district').annotate(deemdet=Count('district')).order_by('district')
		deemansubtot=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3]).values('district').annotate(deemantot=Count('district'))
		deemangrtot=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3]).values('manage_cate').annotate(deemangtot=Count('manage_cate'))
		deemantotal=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3]).count()

		dmsmandet=Basicinfo.objects.filter(chk_dept__in=[3]).values('manage_cate_id','district').annotate(dmsmdet=Count('district')).order_by('district')
		dmsmansubtot=Basicinfo.objects.filter(chk_dept__in=[3],manage_cate_id__in=[1,2,3]).values('district').annotate(dmsmantot=Count('district'))
		dmsmangrtot=Basicinfo.objects.filter(chk_dept__in=[3],manage_cate_id__in=[1,2,3]).values('manage_cate').annotate(dmsmangtot=Count('manage_cate'))
		dmsmantotal=Basicinfo.objects.filter(chk_dept__in=[3],manage_cate_id__in=[1,2,3]).count()


		return render(request,'drep_bi.html',locals())



class Sch_sr_ai(View):
	
	def get(self,request,**kwargs):
		dl=District.objects.all().order_by('id')
		schlst=Basicinfo.objects.all().values('chk_dept','district').annotate(disttot=Count('district')).order_by('district')
		disttot=Basicinfo.objects.filter(chk_dept__in=[1,2,3]).values('district').annotate(schsubtot=Count('chk_dept'))
		schgrtot=Basicinfo.objects.filter(chk_dept__in=[1,2,3]).values('chk_dept').annotate(schgtot=Count('chk_dept'))
		schtotal=Basicinfo.objects.filter(chk_dept__in=[1,2,3]).count()

		mandet=Basicinfo.objects.filter(chk_dept__in=[1,2,3]).values('manage_cate_id','district').annotate(mdet=Count('academicinfo__school_key')).order_by('district')
		mansubtot=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3]).values('district').annotate(mantot=Count('academicinfo__school_key'))
		mangrtot=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3]).values('manage_cate').annotate(mangtot=Count('academicinfo__school_key'))
		mantotal=Academicinfo.objects.all().count()

		dsemandet=Basicinfo.objects.filter(chk_dept__in=[1]).values('manage_cate_id','district').annotate(dsemdet=Count('academicinfo__school_key')).order_by('district')
		dsemansubtot=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3]).values('district').annotate(dsemantot=Count('academicinfo__school_key'))
		dsemangrtot=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3]).values('manage_cate').annotate(dsemangtot=Count('academicinfo__school_key'))
		dsemantotal=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3]).values('academicinfo__school_key').count()

		deemandet=Basicinfo.objects.filter(chk_dept__in=[2]).values('manage_cate_id','district').annotate(deemdet=Count('academicinfo__school_key')).order_by('district')
		deemansubtot=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3]).values('district').annotate(deemantot=Count('academicinfo__school_key'))
		deemangrtot=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3]).values('manage_cate').annotate(deemangtot=Count('academicinfo__school_key'))
		deemantotal=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3]).values('academicinfo__school_key').count()

		dmsmandet=Basicinfo.objects.filter(chk_dept__in=[3]).values('manage_cate_id','district').annotate(dmsmdet=Count('academicinfo__school_key')).order_by('district')
		dmsmansubtot=Basicinfo.objects.filter(chk_dept__in=[3],manage_cate_id__in=[1,2,3]).values('district').annotate(dmsmantot=Count('academicinfo__school_key'))
		dmsmangrtot=Basicinfo.objects.filter(chk_dept__in=[3],manage_cate_id__in=[1,2,3]).values('manage_cate').annotate(dmsmangtot=Count('academicinfo__school_key'))
		dmsmantotal=Basicinfo.objects.filter(chk_dept__in=[3],manage_cate_id__in=[1,2,3]).values('academicinfo__school_key').count()

		return render(request,'drep_ai.html',locals())


class Sch_sr_ii(View):
	
	def get(self,request,**kwargs):
		dl=District.objects.all().order_by('id')
		schlst=Basicinfo.objects.all().values('chk_dept','district').annotate(disttot=Count('district')).order_by('district')
		disttot=Basicinfo.objects.filter(chk_dept__in=[1,2,3]).values('district').annotate(schsubtot=Count('chk_dept'))
		schgrtot=Basicinfo.objects.filter(chk_dept__in=[1,2,3]).values('chk_dept').annotate(schgtot=Count('chk_dept'))
		schtotal=Basicinfo.objects.filter(chk_dept__in=[1,2,3]).count()

		mandet=Basicinfo.objects.filter(chk_dept__in=[1,2,3]).values('manage_cate_id','district').annotate(mdet=Count('infradet__school_key')).order_by('district')
		mansubtot=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3]).values('district').annotate(mantot=Count('infradet__school_key'))
		mangrtot=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3]).values('manage_cate').annotate(mangtot=Count('infradet__school_key'))
		mantotal=Infradet.objects.all().count()

		dsemandet=Basicinfo.objects.filter(chk_dept__in=[1]).values('manage_cate_id','district').annotate(dsemdet=Count('infradet__school_key')).order_by('district')
		dsemansubtot=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3]).values('district').annotate(dsemantot=Count('infradet__school_key'))
		dsemangrtot=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3]).values('manage_cate').annotate(dsemangtot=Count('infradet__school_key'))
		dsemantotal=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3]).values('infradet__school_key').count()

		deemandet=Basicinfo.objects.filter(chk_dept__in=[2]).values('manage_cate_id','district').annotate(deemdet=Count('infradet__school_key')).order_by('district')
		deemansubtot=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3]).values('district').annotate(deemantot=Count('infradet__school_key'))
		deemangrtot=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3]).values('manage_cate').annotate(deemangtot=Count('infradet__school_key'))
		deemantotal=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3]).values('infradet__school_key').count()

		dmsmandet=Basicinfo.objects.filter(chk_dept__in=[3]).values('manage_cate_id','district').annotate(dmsmdet=Count('infradet__school_key')).order_by('district')
		dmsmansubtot=Basicinfo.objects.filter(chk_dept__in=[3],manage_cate_id__in=[1,2,3]).values('district').annotate(dmsmantot=Count('infradet__school_key'))
		dmsmangrtot=Basicinfo.objects.filter(chk_dept__in=[3],manage_cate_id__in=[1,2,3]).values('manage_cate').annotate(dmsmangtot=Count('infradet__school_key'))
		dmsmantotal=Basicinfo.objects.filter(chk_dept__in=[3],manage_cate_id__in=[1,2,3]).values('infradet__school_key').count()

		return render(request,'drep_ii.html',locals())



class Sch_sr_cs(View):
	
	def get(self,request,**kwargs):
		dl=District.objects.all().order_by('id')
		schlst=Basicinfo.objects.all().values('chk_dept','district').annotate(disttot=Count('district')).order_by('district')
		disttot=Basicinfo.objects.filter(chk_dept__in=[1,2,3]).values('district').annotate(schsubtot=Count('chk_dept'))
		schgrtot=Basicinfo.objects.filter(chk_dept__in=[1,2,3]).values('chk_dept').annotate(schgtot=Count('chk_dept'))
		schtotal=Basicinfo.objects.filter(chk_dept__in=[1,2,3]).count()

		mandet=Basicinfo.objects.filter(chk_dept__in=[1,2,3]).values('manage_cate_id','district').annotate(mdet=Count('class_section__school_key',distinct = True)).order_by('district')
		mansubtot=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3]).values('district').annotate(mantot=Count('class_section__school_key',distinct = True))
		mangrtot=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3]).values('manage_cate').annotate(mangtot=Count('class_section__school_key',distinct = True))
		mantotal=Class_section.objects.all().values('school_key').distinct().count()

		dsemandet=Basicinfo.objects.filter(chk_dept__in=[1]).values('manage_cate_id','district').annotate(dsemdet=Count('class_section__school_key',distinct = True)).order_by('district')
		dsemansubtot=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3]).values('district').annotate(dsemantot=Count('class_section__school_key',distinct = True))
		dsemangrtot=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3]).values('manage_cate').annotate(dsemangtot=Count('class_section__school_key',distinct = True))
		dsemantotal=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3]).values('class_section__school_key').distinct().count()


		deemandet=Basicinfo.objects.filter(chk_dept__in=[2]).values('manage_cate_id','district').annotate(deemdet=Count('class_section__school_key',distinct = True)).order_by('district')
		deemansubtot=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3]).values('district').annotate(deemantot=Count('class_section__school_key',distinct = True))
		deemangrtot=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3]).values('manage_cate').annotate(deemangtot=Count('class_section__school_key',distinct = True))
		deemantotal=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3]).values('class_section__school_key').distinct().count()

		dmsmandet=Basicinfo.objects.filter(chk_dept__in=[3]).values('manage_cate_id','district').annotate(dmsmdet=Count('class_section__school_key',distinct = True)).order_by('district')
		dmsmansubtot=Basicinfo.objects.filter(chk_dept__in=[3],manage_cate_id__in=[1,2,3]).values('district').annotate(dmsmantot=Count('class_section__school_key',distinct = True))
		dmsmangrtot=Basicinfo.objects.filter(chk_dept__in=[3],manage_cate_id__in=[1,2,3]).values('manage_cate').annotate(dmsmangtot=Count('class_section__school_key',distinct = True))
		dmsmantotal=Basicinfo.objects.filter(chk_dept__in=[3],manage_cate_id__in=[1,2,3]).values('class_section__school_key').distinct().count()

		return render(request,'drep_cs.html',locals())



class Sch_sr_ti(View):
	
	def get(self,request,**kwargs):
		dl=District.objects.all().order_by('id')
		schlst=Basicinfo.objects.all().values('chk_dept','district').annotate(disttot=Count('district')).order_by('district')
		disttot=Basicinfo.objects.filter(chk_dept__in=[1,2,3]).values('district').annotate(schsubtot=Count('chk_dept'))
		schgrtot=Basicinfo.objects.filter(chk_dept__in=[1,2,3]).values('chk_dept').annotate(schgtot=Count('chk_dept'))
		schtotal=Basicinfo.objects.filter(chk_dept__in=[1,2,3]).count()

		mandet=Basicinfo.objects.filter(chk_dept__in=[1,2,3],staff__staff_cat='1').values('manage_cate_id','district').annotate(mdet=Sum('staff__post_sanc')).order_by('district')
		mansubtot=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3],staff__staff_cat='1').values('district').annotate(mantot=Sum('staff__post_sanc'))
		mangrtot=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3],staff__staff_cat='1').values('manage_cate').annotate(mangtot=Sum('staff__post_sanc'))
		mantotal=Staff.objects.filter(staff_cat='1').aggregate(Sum('post_sanc'))

		dsemandet=Basicinfo.objects.filter(chk_dept__in=[1],staff__staff_cat='1').values('manage_cate_id','district').annotate(dsemdet=Sum('staff__post_sanc')).order_by('district')
		dsemansubtot=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3],staff__staff_cat='1').values('district').annotate(dsemantot=Sum('staff__post_sanc'))
		dsemangrtot=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3],staff__staff_cat='1').values('manage_cate').annotate(dsemangtot=Sum('staff__post_sanc'))
		dsemantotal=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3],staff__staff_cat='1').aggregate(Sum('staff__post_sanc'))

		deemandet=Basicinfo.objects.filter(chk_dept__in=[2],staff__staff_cat='1').values('manage_cate_id','district').annotate(deemdet=Sum('staff__post_sanc')).order_by('district')
		deemansubtot=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3],staff__staff_cat='1').values('district').annotate(deemantot=Sum('staff__post_sanc'))
		deemangrtot=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3],staff__staff_cat='1').values('manage_cate').annotate(deemangtot=Sum('staff__post_sanc'))
		deemantotal=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3],staff__staff_cat='1').aggregate(Sum('staff__post_sanc'))

		manfdet=Basicinfo.objects.filter(chk_dept__in=[1,2,3],staff__staff_cat='1',staff__post_filled__gt='0').values('manage_cate_id','district').annotate(mfdet=Sum('staff__post_filled')).order_by('district')
		manfsubtot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],manage_cate_id__in=[1,2,3],staff__staff_cat='1',staff__post_filled__gt='0').values('district').annotate(manftot=Sum('staff__post_filled'))
		manfgrtot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],manage_cate_id__in=[1,2,3],staff__staff_cat='1',staff__post_filled__gt='0').values('manage_cate').annotate(manfgtot=Sum('staff__post_filled'))
		manftotal=Staff.objects.filter(staff_cat='1',post_filled__gt='0').aggregate(Sum('post_filled'))
		
		dsemanfdet=Basicinfo.objects.filter(chk_dept__in=[1],staff__staff_cat='1',staff__post_filled__gt='0').values('manage_cate_id','district').annotate(dsemfdet=Sum('staff__post_filled')).order_by('district')
		dsemanfsubtot=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3],staff__staff_cat='1',staff__post_filled__gt='0').values('district').annotate(dsemanftot=Sum('staff__post_filled'))
		dsemanfgrtot=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3],staff__staff_cat='1',staff__post_filled__gt='0').values('manage_cate').annotate(dsemanfgtot=Sum('staff__post_filled'))
		dsemanftotal=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3],staff__staff_cat='1',staff__post_filled__gt='0').aggregate(Sum('staff__post_filled'))

		deemanfdet=Basicinfo.objects.filter(chk_dept__in=[2],staff__staff_cat='1',staff__post_filled__gt='0').values('manage_cate_id','district').annotate(deemfdet=Count('staff__school_key')).order_by('district')
		deemanfsubtot=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3],staff__staff_cat='1',staff__post_filled__gt='0').values('district').annotate(deemanftot=Sum('staff__post_filled'))
		deemanfgrtot=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3],staff__staff_cat='1',staff__post_filled__gt='0').values('manage_cate').annotate(deemangftot=Sum('staff__post_filled'))
		deemanftotal=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3],staff__staff_cat='1',staff__post_filled__gt='0').aggregate(Sum('staff__post_filled'))

		return render(request,'drep_ti.html',locals())


class Sch_sr_nti(View):
	
	def get(self,request,**kwargs):
		dl=District.objects.all().order_by('id')
		schlst=Basicinfo.objects.all().values('chk_dept','district').annotate(disttot=Count('district')).order_by('district')
		disttot=Basicinfo.objects.filter(chk_dept__in=[1,2,3]).values('district').annotate(schsubtot=Count('chk_dept'))
		schgrtot=Basicinfo.objects.filter(chk_dept__in=[1,2,3]).values('chk_dept').annotate(schgtot=Count('chk_dept'))
		schtotal=Basicinfo.objects.filter(chk_dept__in=[1,2,3]).count()

		mandet=Basicinfo.objects.filter(staff__staff_cat='2').values('manage_cate_id','district').annotate(mdet=Sum('staff__post_sanc')).order_by('district')
		mansubtot=Basicinfo.objects.filter(staff__staff_cat='2').values('district').annotate(mantot=Sum('staff__post_sanc'))
		mangrtot=Basicinfo.objects.filter(staff__staff_cat='2').values('manage_cate').annotate(mangtot=Sum('staff__post_sanc'))
		mantotal=Staff.objects.filter(staff_cat='2').aggregate(Sum('post_sanc'))

		dsemandet=Basicinfo.objects.filter(chk_dept__in=[1],staff__staff_cat='2').values('manage_cate_id','district').annotate(dsemdet=Sum('staff__post_sanc')).order_by('district')
		dsemansubtot=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3],staff__staff_cat='2').values('district').annotate(dsemantot=Sum('staff__post_sanc'))
		dsemangrtot=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3],staff__staff_cat='2').values('manage_cate').annotate(dsemangtot=Sum('staff__post_sanc'))
		dsemantotal=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3],staff__staff_cat='2').aggregate(Sum('staff__post_sanc'))

		deemandet=Basicinfo.objects.filter(chk_dept__in=[2],staff__staff_cat='2').values('manage_cate_id','district').annotate(deemdet=Sum('staff__post_sanc')).order_by('district')
		deemansubtot=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3],staff__staff_cat='2').values('district').annotate(deemantot=Sum('staff__post_sanc'))
		deemangrtot=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3],staff__staff_cat='2').values('manage_cate').annotate(deemangtot=Sum('staff__post_sanc'))
		deemantotal=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3],staff__staff_cat='2').aggregate(Sum('staff__post_sanc'))

		manfdet=Basicinfo.objects.filter(staff__staff_cat='2',staff__post_filled__gt='0').values('manage_cate_id','district').annotate(mfdet=Sum('staff__post_filled')).order_by('district')
		manfsubtot=Basicinfo.objects.filter(staff__staff_cat='2',staff__post_filled__gt='0').values('district').annotate(manftot=Sum('staff__post_filled'))
		manfgrtot=Basicinfo.objects.filter(staff__staff_cat='2',staff__post_filled__gt='0').values('manage_cate').annotate(manfgtot=Sum('staff__post_filled'))
		manftotal=Staff.objects.filter(staff_cat='2',post_filled__gt='0').aggregate(Sum('post_filled'))
		
		dsemanfdet=Basicinfo.objects.filter(chk_dept__in=[1],staff__staff_cat='2',staff__post_filled__gt='0').values('manage_cate_id','district').annotate(dsemfdet=Sum('staff__post_filled')).order_by('district')
		dsemanfsubtot=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3],staff__staff_cat='2',staff__post_filled__gt='0').values('district').annotate(dsemanftot=Sum('staff__post_filled'))
		dsemanfgrtot=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3],staff__staff_cat='2',staff__post_filled__gt='0').values('manage_cate').annotate(dsemanfgtot=Sum('staff__post_filled'))
		dsemanftotal=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3],staff__staff_cat='2',staff__post_filled__gt='0').aggregate(Sum('staff__post_filled'))

		deemanfdet=Basicinfo.objects.filter(chk_dept__in=[2],staff__staff_cat='2',staff__post_filled__gt='0').values('manage_cate_id','district').annotate(deemfdet=Sum('staff__post_filled')).order_by('district')
		deemanfsubtot=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3],staff__staff_cat='2',staff__post_filled__gt='0').values('district').annotate(deemanftot=Sum('staff__post_filled'))
		deemanfgrtot=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3],staff__staff_cat='2',staff__post_filled__gt='0').values('manage_cate').annotate(deemangftot=Sum('staff__post_filled'))
		deemanftotal=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3],staff__staff_cat='2',staff__post_filled__gt='0').aggregate(Sum('staff__post_filled'))

		return render(request,'drep_nti.html',locals())


class Sch_blkr_bi(View):
	
	def get(self,request,**kwargs):
		d_id=self.kwargs['blk']
		if (self.kwargs.get('code')):
			dept_opt=int(self.kwargs.get('code'))	

		bl=Block.objects.filter(district=d_id).order_by('block_name')
		try:
			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
		except:
			pass
		else:
			basic_det=Basicinfo.objects.get(udise_code=request.user.username)
		finally:
			pass

		schlst=Basicinfo.objects.all().values('chk_dept','block').annotate(schblktot=Count('block')).order_by('block')
		blktot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],district=d_id).values('block').annotate(schsubtot=Count('chk_dept'))
		schgrtot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],district=d_id).values('chk_dept').annotate(schgtot=Count('chk_dept'))
		schtotal=Basicinfo.objects.filter(chk_dept__in=[1,2,3],district=d_id).count()

		mandet=Basicinfo.objects.filter(chk_dept__in=[1,2,3],district=d_id).values('manage_cate_id','block').annotate(mdet=Count('block')).order_by('block')
		mansubtot=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3],district=d_id).values('block').annotate(mantot=Count('block'))
		mangrtot=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3],district=d_id).values('manage_cate').annotate(mangtot=Count('manage_cate'))
		mantotal=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3],district=d_id).count()

		dsemandet=Basicinfo.objects.filter(chk_dept__in=[1],district=d_id).values('manage_cate_id','block').annotate(dsemdet=Count('block')).order_by('block')
		dsemansubtot=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3],district=d_id).values('block').annotate(dsemantot=Count('block'))
		dsemangrtot=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3],district=d_id).values('manage_cate').annotate(dsemangtot=Count('manage_cate'))
		dsemantotal=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3],district=d_id).count()

		deemandet=Basicinfo.objects.filter(chk_dept__in=[2],district=d_id).values('manage_cate_id','block').annotate(deemdet=Count('block')).order_by('block')
		deemansubtot=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3],district=d_id).values('block').annotate(deemantot=Count('block'))
		deemangrtot=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3],district=d_id).values('manage_cate').annotate(deemangtot=Count('manage_cate'))
		deemantotal=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3],district=d_id).count()

		dmsmandet=Basicinfo.objects.filter(chk_dept__in=[3],district=d_id).values('manage_cate_id','block').annotate(dmsmdet=Count('block')).order_by('block')
		dmsmansubtot=Basicinfo.objects.filter(chk_dept__in=[3],manage_cate_id__in=[1,2,3],district=d_id).values('block').annotate(dmsmantot=Count('block'))
		dmsmangrtot=Basicinfo.objects.filter(chk_dept__in=[3],manage_cate_id__in=[1,2,3],district=d_id).values('manage_cate').annotate(dmsmangtot=Count('manage_cate'))
		dmsmantotal=Basicinfo.objects.filter(chk_dept__in=[3],manage_cate_id__in=[1,2,3],district=d_id).count()
		return render(request,'blkrep_bi.html',locals())


class Sch_blkr_ai(View):
	
	def get(self,request,**kwargs):
		d_id=self.kwargs['blk']
		if (self.kwargs.get('code')):
			dept_opt=int(self.kwargs.get('code'))	
		bl=Block.objects.filter(district=d_id).order_by('block_name')
		basic_det=Basicinfo.objects.get(udise_code=request.user.username)

		schlst=Basicinfo.objects.all().values('chk_dept','block').annotate(schblktot=Count('block')).order_by('block')
		blktot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],district=d_id).values('block').annotate(schsubtot=Count('chk_dept'))
		schgrtot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],district=d_id).values('chk_dept').annotate(schgtot=Count('chk_dept'))
		schtotal=Basicinfo.objects.filter(chk_dept__in=[1,2,3],district=d_id).count()

		mandet=Basicinfo.objects.filter(chk_dept__in=[1,2,3],district=d_id).values('manage_cate_id','block').annotate(mdet=Count('academicinfo__school_key')).order_by('block')
		mansubtot=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3],district=d_id).values('block').annotate(mantot=Count('academicinfo__school_key'))
		mangrtot=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3],district=d_id).values('manage_cate').annotate(mangtot=Count('academicinfo__school_key'))
		mantotal=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3],district=d_id).values('academicinfo__school_key').count()

		dsemandet=Basicinfo.objects.filter(chk_dept__in=[1],district=d_id).values('manage_cate_id','block').annotate(dsemdet=Count('academicinfo__school_key')).order_by('block')
		dsemansubtot=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3],district=d_id).values('block').annotate(dsemantot=Count('academicinfo__school_key'))
		dsemangrtot=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3],district=d_id).values('manage_cate').annotate(dsemangtot=Count('academicinfo__school_key'))
		dsemantotal=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3],district=d_id).values('academicinfo__school_key').count()

		deemandet=Basicinfo.objects.filter(chk_dept__in=[2],district=d_id).values('manage_cate_id','block').annotate(deemdet=Count('academicinfo__school_key')).order_by('block')
		deemansubtot=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3],district=d_id).values('block').annotate(deemantot=Count('academicinfo__school_key'))
		deemangrtot=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3],district=d_id).values('manage_cate').annotate(deemangtot=Count('academicinfo__school_key'))
		deemantotal=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3],district=d_id).values('academicinfo__school_key').count()

		dmsmandet=Basicinfo.objects.filter(chk_dept__in=[3],district=d_id).values('manage_cate_id','block').annotate(dmsmdet=Count('academicinfo__school_key')).order_by('block')
		dmsmansubtot=Basicinfo.objects.filter(chk_dept__in=[3],manage_cate_id__in=[1,2,3],district=d_id).values('block').annotate(dmsmantot=Count('academicinfo__school_key'))
		dmsmangrtot=Basicinfo.objects.filter(chk_dept__in=[3],manage_cate_id__in=[1,2,3],district=d_id).values('manage_cate').annotate(dmsmangtot=Count('academicinfo__school_key'))
		dmsmantotal=Basicinfo.objects.filter(chk_dept__in=[3],manage_cate_id__in=[1,2,3],district=d_id).values('academicinfo__school_key').count()
		return render(request,'blkrep_ai.html',locals())

class Sch_blkr_ii(View):
	
	def get(self,request,**kwargs):
		d_id=self.kwargs['blk']
		if (self.kwargs.get('code')):
			dept_opt=int(self.kwargs.get('code'))	
		bl=Block.objects.filter(district=d_id).order_by('block_name')
		basic_det=Basicinfo.objects.get(udise_code=request.user.username)

		schlst=Basicinfo.objects.all().values('chk_dept','block').annotate(schblktot=Count('block')).order_by('block')
		blktot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],district=d_id).values('block').annotate(schsubtot=Count('chk_dept'))
		schgrtot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],district=d_id).values('chk_dept').annotate(schgtot=Count('chk_dept'))
		schtotal=Basicinfo.objects.filter(chk_dept__in=[1,2,3],district=d_id).count()

		mandet=Basicinfo.objects.filter(chk_dept__in=[1,2,3],district=d_id).values('manage_cate_id','block').annotate(mdet=Count('infradet__school_key')).order_by('block')
		mansubtot=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3],district=d_id).values('block').annotate(mantot=Count('infradet__school_key'))
		mangrtot=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3],district=d_id).values('manage_cate').annotate(mangtot=Count('infradet__school_key'))
		mantotal=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3],district=d_id).values('infradet__school_key').count()

		dsemandet=Basicinfo.objects.filter(chk_dept__in=[1],district=d_id).values('manage_cate_id','block').annotate(dsemdet=Count('infradet__school_key')).order_by('block')
		dsemansubtot=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3],district=d_id).values('block').annotate(dsemantot=Count('infradet__school_key'))
		dsemangrtot=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3],district=d_id).values('manage_cate').annotate(dsemangtot=Count('infradet__school_key'))
		dsemantotal=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3],district=d_id).values('infradet__school_key').count()

		deemandet=Basicinfo.objects.filter(chk_dept__in=[2],district=d_id).values('manage_cate_id','block').annotate(deemdet=Count('infradet__school_key')).order_by('block')
		deemansubtot=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3],district=d_id).values('block').annotate(deemantot=Count('infradet__school_key'))
		deemangrtot=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3],district=d_id).values('manage_cate').annotate(deemangtot=Count('infradet__school_key'))
		deemantotal=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3],district=d_id).values('infradet__school_key').count()

		dmsmandet=Basicinfo.objects.filter(chk_dept__in=[3],district=d_id).values('manage_cate_id','block').annotate(dmsmdet=Count('infradet__school_key')).order_by('block')
		dmsmansubtot=Basicinfo.objects.filter(chk_dept__in=[3],manage_cate_id__in=[1,2,3],district=d_id).values('block').annotate(dmsmantot=Count('infradet__school_key'))
		dmsmangrtot=Basicinfo.objects.filter(chk_dept__in=[3],manage_cate_id__in=[1,2,3],district=d_id).values('manage_cate').annotate(dmsmangtot=Count('infradet__school_key'))
		dmsmantotal=Basicinfo.objects.filter(chk_dept__in=[3],manage_cate_id__in=[1,2,3],district=d_id).values('infradet__school_key').count()
		return render(request,'blkrep_ii.html',locals())

class Sch_blkr_cs(View):
	
	def get(self,request,**kwargs):
		d_id=self.kwargs['blk']
		if (self.kwargs.get('code')):
			dept_opt=int(self.kwargs.get('code'))	
		bl=Block.objects.filter(district=d_id).order_by('block_name')
		basic_det=Basicinfo.objects.get(udise_code=request.user.username)

		schlst=Basicinfo.objects.all().values('chk_dept','block').annotate(schblktot=Count('block')).order_by('block')
		blktot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],district=d_id).values('block').annotate(schsubtot=Count('chk_dept'))
		schgrtot=Basicinfo.objects.filter(chk_dept__in=[1,2,3],district=d_id).values('chk_dept').annotate(schgtot=Count('chk_dept'))
		schtotal=Basicinfo.objects.filter(chk_dept__in=[1,2,3],district=d_id).count()

		mandet=Basicinfo.objects.filter(chk_dept__in=[1,2,3],district=d_id).values('manage_cate_id','block').annotate(mdet=Count('class_section__school_key',distinct = True)).order_by('block')
		mansubtot=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3],district=d_id).values('block').annotate(mantot=Count('class_section__school_key',distinct = True))
		mangrtot=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3],district=d_id).values('manage_cate').annotate(mangtot=Count('class_section__school_key',distinct = True))
		mantotal=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3],district=d_id).values('class_section__school_key').distinct().count()

		dsemandet=Basicinfo.objects.filter(chk_dept__in=[1],district=d_id).values('manage_cate_id','block').annotate(dsemdet=Count('class_section__school_key',distinct = True)).order_by('block')
		dsemansubtot=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3],district=d_id).values('block').annotate(dsemantot=Count('class_section__school_key',distinct = True))
		dsemangrtot=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3],district=d_id).values('manage_cate').annotate(dsemangtot=Count('class_section__school_key',distinct = True))
		dsemantotal=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2,3],district=d_id).values('class_section__school_key').distinct().count()

		deemandet=Basicinfo.objects.filter(chk_dept__in=[2],district=d_id).values('manage_cate_id','block').annotate(deemdet=Count('class_section__school_key',distinct = True)).order_by('block')
		deemansubtot=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3],district=d_id).values('block').annotate(deemantot=Count('class_section__school_key',distinct = True))
		deemangrtot=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3],district=d_id).values('manage_cate').annotate(deemangtot=Count('class_section__school_key',distinct = True))
		deemantotal=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2,3],district=d_id).values('class_section__school_key').distinct().count()

		dmsmandet=Basicinfo.objects.filter(chk_dept__in=[3],district=d_id).values('manage_cate_id','block').annotate(dmsmdet=Count('class_section__school_key',distinct = True)).order_by('block')
		dmsmansubtot=Basicinfo.objects.filter(chk_dept__in=[3],manage_cate_id__in=[1,2,3],district=d_id).values('block').annotate(dmsmantot=Count('class_section__school_key',distinct = True))
		dmsmangrtot=Basicinfo.objects.filter(chk_dept__in=[3],manage_cate_id__in=[1,2,3],district=d_id).values('manage_cate').annotate(dmsmangtot=Count('class_section__school_key',distinct = True))
		dmsmantotal=Basicinfo.objects.filter(chk_dept__in=[3],manage_cate_id__in=[1,2,3],district=d_id).values('class_section__school_key').distinct().count()
		return render(request,'blkrep_cs.html',locals())


class Sch_blkr_ti(View):
	
	def get(self,request,**kwargs):
		d_id=self.kwargs['blk']
		if (self.kwargs.get('code')):
			dept_opt=int(self.kwargs.get('code'))	
		bl=Block.objects.filter(district=d_id).order_by('block_name')
		basic_det=Basicinfo.objects.get(udise_code=request.user.username)

		schlst=Basicinfo.objects.filter(chk_dept__in=[1,2],district=d_id).values('chk_dept','block').annotate(schblktot=Count('block')).order_by('block')
		blktot=Basicinfo.objects.filter(chk_dept__in=[1,2],district=d_id).values('block').annotate(schsubtot=Count('chk_dept'))
		schgrtot=Basicinfo.objects.filter(chk_dept__in=[1,2],district=d_id).values('chk_dept').annotate(schgtot=Count('chk_dept'))
		schtotal=Basicinfo.objects.filter(chk_dept__in=[1,2],district=d_id).count()

		mandet=Basicinfo.objects.filter(chk_dept__in=[1,2],staff__staff_cat='1',district=d_id).values('manage_cate_id','block').annotate(mdet=Sum('staff__post_sanc')).order_by('block')
		mansubtot=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3],staff__staff_cat='1',district=d_id).values('block').annotate(mantot=Sum('staff__post_sanc'))
		mangrtot=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3],staff__staff_cat='1',district=d_id).values('manage_cate').annotate(mangtot=Sum('staff__post_sanc'))
		mantotal=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3],staff__staff_cat='1',district=d_id).aggregate(manatot=Sum('staff__post_sanc'))


		dsemandet=Basicinfo.objects.filter(chk_dept__in=[1],staff__staff_cat='1',district=d_id).values('manage_cate_id','block').annotate(dsemdet=Sum('staff__post_sanc')).order_by('block')
		dsemansubtot=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2],district=d_id,staff__staff_cat='1').values('block').annotate(dsemantot=Sum('staff__post_sanc'))
		dsemangrtot=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2],district=d_id,staff__staff_cat='1').values('manage_cate').annotate(dsemangtot=Sum('staff__post_sanc'))
		dsemantotal=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2],district=d_id,staff__staff_cat='1').aggregate(Sum('staff__post_sanc'))

		deemandet=Basicinfo.objects.filter(chk_dept__in=[2],staff__staff_cat='1').values('manage_cate_id','block').annotate(deemdet=Sum('staff__post_sanc')).order_by('block')
		deemansubtot=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2],district=d_id,staff__staff_cat='1').values('block').annotate(deemantot=Sum('staff__post_sanc'))
		deemangrtot=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2],district=d_id,staff__staff_cat='1').values('manage_cate').annotate(deemangtot=Sum('staff__post_sanc'))
		deemantotal=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2],district=d_id,staff__staff_cat='1').aggregate(Sum('staff__post_sanc'))

		manfdet=Basicinfo.objects.filter(chk_dept__in=[1,2],staff__staff_cat='1',staff__post_filled__gt='0',district=d_id).values('manage_cate_id','block').annotate(mfdet=Sum('staff__post_filled')).order_by('block')
		manfsubtot=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3],staff__staff_cat='1',staff__post_filled__gt='0',district=d_id).values('block').annotate(manftot=Sum('staff__post_filled'))
		manfgrtot=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3],staff__staff_cat='1',staff__post_filled__gt='0',district=d_id).values('manage_cate').annotate(manfgtot=Sum('staff__post_filled'))
		manftotal=Basicinfo.objects.filter(district=d_id,manage_cate_id__in=[1,2,3],staff__staff_cat='1',staff__post_filled__gt='0').aggregate(Sum('staff__post_filled'))
		manftotal=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3],staff__staff_cat='1',district=d_id).aggregate(manftot=Sum('staff__post_filled'))

		dsemanfdet=Basicinfo.objects.filter(chk_dept__in=[1],district=d_id,staff__staff_cat='1',staff__post_filled__gt='0').values('manage_cate_id','block').annotate(dsemfdet=Sum('staff__post_filled')).order_by('block')
		dsemanfsubtot=Basicinfo.objects.filter(chk_dept__in=[1],district=d_id,manage_cate_id__in=[1,2,3],staff__staff_cat='1',staff__post_filled__gt='0').values('block').annotate(dsemanftot=Sum('staff__post_filled'))
		dsemanfgrtot=Basicinfo.objects.filter(chk_dept__in=[1],district=d_id,manage_cate_id__in=[1,2,3],staff__staff_cat='1',staff__post_filled__gt='0').values('manage_cate').annotate(dsemanfgtot=Sum('staff__post_filled'))
		dsemanftotal=Basicinfo.objects.filter(chk_dept__in=[1],district=d_id,manage_cate_id__in=[1,2,3],staff__staff_cat='1',staff__post_filled__gt='0').aggregate(Sum('staff__post_filled'))

		deemanfdet=Basicinfo.objects.filter(chk_dept__in=[2],district=d_id,staff__staff_cat='1',staff__post_filled__gt='0').values('manage_cate_id','block').annotate(deemfdet=Sum('staff__post_filled')).order_by('block')
		deemanfsubtot=Basicinfo.objects.filter(chk_dept__in=[2],district=d_id,manage_cate_id__in=[1,2,3],staff__staff_cat='1',staff__post_filled__gt='0').values('block').annotate(deemanftot=Sum('staff__post_filled'))
		deemanfgrtot=Basicinfo.objects.filter(chk_dept__in=[2],district=d_id,manage_cate_id__in=[1,2,3],staff__staff_cat='1',staff__post_filled__gt='0').values('manage_cate').annotate(deemangftot=Sum('staff__post_filled'))
		deemanftotal=Basicinfo.objects.filter(chk_dept__in=[2],district=d_id,manage_cate_id__in=[1,2,3],staff__staff_cat='1',staff__post_filled__gt='0').aggregate(Sum('staff__post_filled'))

		return render(request,'blkrep_ti.html',locals())


class Sch_blkr_nti(View):
	
	def get(self,request,**kwargs):
		d_id=self.kwargs['blk']
		if (self.kwargs.get('code')):
			dept_opt=int(self.kwargs.get('code'))	
		bl=Block.objects.filter(district=d_id).order_by('block_name')
		basic_det=Basicinfo.objects.get(udise_code=request.user.username)

		schlst=Basicinfo.objects.filter(chk_dept__in=[1,2],district=d_id).values('chk_dept','block').annotate(schblktot=Count('block')).order_by('block')
		blktot=Basicinfo.objects.filter(chk_dept__in=[1,2],district=d_id).values('block').annotate(schsubtot=Count('chk_dept'))
		schgrtot=Basicinfo.objects.filter(chk_dept__in=[1,2],district=d_id).values('chk_dept').annotate(schgtot=Count('chk_dept'))
		schtotal=Basicinfo.objects.filter(chk_dept__in=[1,2],district=d_id).count()

		mandet=Basicinfo.objects.filter(staff__staff_cat='2',district=d_id).values('manage_cate_id','block').annotate(mdet=Sum('staff__post_sanc')).order_by('block')
		mansubtot=Basicinfo.objects.filter(staff__staff_cat='2',district=d_id).values('block').annotate(mantot=Sum('staff__post_sanc'))
		mangrtot=Basicinfo.objects.filter(staff__staff_cat='2',district=d_id).values('manage_cate').annotate(mangtot=Sum('staff__post_sanc'))
		mantotal=Basicinfo.objects.filter(staff__staff_cat='2',district=d_id).aggregate(manatot=Sum('staff__post_sanc'))


		dsemandet=Basicinfo.objects.filter(chk_dept__in=[1],staff__staff_cat='2',district=d_id).values('manage_cate_id','block').annotate(dsemdet=Sum('staff__post_sanc')).order_by('block')
		dsemansubtot=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2],district=d_id,staff__staff_cat='2').values('block').annotate(dsemantot=Sum('staff__post_sanc'))
		dsemangrtot=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2],district=d_id,staff__staff_cat='2').values('manage_cate').annotate(dsemangtot=Sum('staff__post_sanc'))
		dsemantotal=Basicinfo.objects.filter(chk_dept__in=[1],manage_cate_id__in=[1,2],district=d_id,staff__staff_cat='2').aggregate(Sum('staff__post_sanc'))

		deemandet=Basicinfo.objects.filter(chk_dept__in=[2],staff__staff_cat='2').values('manage_cate_id','block').annotate(deemdet=Sum('staff__post_sanc')).order_by('block')
		deemansubtot=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2],district=d_id,staff__staff_cat='2').values('block').annotate(deemantot=Sum('staff__post_sanc'))
		deemangrtot=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2],district=d_id,staff__staff_cat='2').values('manage_cate').annotate(deemangtot=Sum('staff__post_sanc'))
		deemantotal=Basicinfo.objects.filter(chk_dept__in=[2],manage_cate_id__in=[1,2],district=d_id,staff__staff_cat='2').aggregate(Sum('staff__post_sanc'))

		manfdet=Basicinfo.objects.filter(chk_dept__in=[1,2],staff__staff_cat='2',staff__post_filled__gt='0',district=d_id).values('manage_cate_id','block').annotate(mfdet=Sum('staff__post_filled')).order_by('block')
		manfsubtot=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3],staff__staff_cat='2',staff__post_filled__gt='0',district=d_id).values('block').annotate(manftot=Sum('staff__post_filled'))
		manfgrtot=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3],staff__staff_cat='2',staff__post_filled__gt='0',district=d_id).values('manage_cate').annotate(manfgtot=Sum('staff__post_filled'))
		manftotal=Basicinfo.objects.filter(district=d_id,manage_cate_id__in=[1,2,3],staff__staff_cat='2',staff__post_filled__gt='0').aggregate(Sum('staff__post_filled'))
		manftotal=Basicinfo.objects.filter(manage_cate_id__in=[1,2,3],staff__staff_cat='2',district=d_id).aggregate(manftot=Sum('staff__post_filled'))

		dsemanfdet=Basicinfo.objects.filter(chk_dept__in=[1],district=d_id,staff__staff_cat='2',staff__post_filled__gt='0').values('manage_cate_id','block').annotate(dsemfdet=Sum('staff__post_filled')).order_by('block')
		dsemanfsubtot=Basicinfo.objects.filter(chk_dept__in=[1],district=d_id,manage_cate_id__in=[1,2,3],staff__staff_cat='2',staff__post_filled__gt='0').values('block').annotate(dsemanftot=Sum('staff__post_filled'))
		dsemanfgrtot=Basicinfo.objects.filter(chk_dept__in=[1],district=d_id,manage_cate_id__in=[1,2,3],staff__staff_cat='2',staff__post_filled__gt='0').values('manage_cate').annotate(dsemanfgtot=Sum('staff__post_filled'))
		dsemanftotal=Basicinfo.objects.filter(chk_dept__in=[1],district=d_id,manage_cate_id__in=[1,2,3],staff__staff_cat='2',staff__post_filled__gt='0').aggregate(Sum('staff__post_filled'))

		deemanfdet=Basicinfo.objects.filter(chk_dept__in=[2],district=d_id,staff__staff_cat='2',staff__post_filled__gt='0').values('manage_cate_id','block').annotate(deemfdet=Sum('staff__post_filled')).order_by('block')
		deemanfsubtot=Basicinfo.objects.filter(chk_dept__in=[2],district=d_id,manage_cate_id__in=[1,2,3],staff__staff_cat='2',staff__post_filled__gt='0').values('block').annotate(deemanftot=Sum('staff__post_filled'))
		deemanfgrtot=Basicinfo.objects.filter(chk_dept__in=[2],district=d_id,manage_cate_id__in=[1,2,3],staff__staff_cat='2',staff__post_filled__gt='0').values('manage_cate').annotate(deemangftot=Sum('staff__post_filled'))
		deemanftotal=Basicinfo.objects.filter(chk_dept__in=[2],district=d_id,manage_cate_id__in=[1,2,3],staff__staff_cat='2',staff__post_filled__gt='0').aggregate(Sum('staff__post_filled'))

		return render(request,'blkrep_nti.html',locals())


class Sch_srep(View):
	
	def get(self,request,**kwargs):
		b_id=self.kwargs['blk']
		try:
			dept_opt=int(self.kwargs.get('code'))
		except Exception:
			pass

		allsl=Basicinfo.objects.filter(block=b_id).order_by('school_name')
		blkid=Basicinfo.objects.get(udise_code=int(request.user.username))
		basic_det=Basicinfo.objects.get(udise_code=request.user.username)
		dsesl=Basicinfo.objects.filter(chk_dept__in=[1],block=b_id).order_by('school_name')
		deesl=Basicinfo.objects.filter(chk_dept__in=[2],block=b_id).order_by('school_name')
		dmssl=Basicinfo.objects.filter(chk_dept__in=[3],block=b_id).order_by('school_name')
		schbi=Basicinfo.objects.filter(block=b_id,manage_cate_id__gt=0).order_by('school_name')
		schai=Academicinfo.objects.filter(school_key_id=allsl)
		schii=Infradet.objects.filter(school_key_id=allsl)
		schsi=Staff.objects.filter(school_key_id=allsl)			
		schtsis=Basicinfo.objects.filter(staff__school_key_id=allsl,staff__staff_cat='1').values('staff__school_key_id').annotate(tptstot=Sum('staff__post_sanc'))
		schtsif=Basicinfo.objects.filter(staff__school_key_id=allsl,staff__staff_cat='1').values('staff__school_key_id').annotate(tptftot=Sum('staff__post_filled'))
		schntsis=Basicinfo.objects.filter(staff__school_key_id=allsl,staff__staff_cat='2').values('staff__school_key_id').annotate(tpntstot=Sum('staff__post_sanc'))
		schntsif=Basicinfo.objects.filter(staff__school_key_id=allsl,staff__staff_cat='2').values('staff__school_key_id').annotate(tpntftot=Sum('staff__post_filled'))
		return render(request,'schrep.html',locals())