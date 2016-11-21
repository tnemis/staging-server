from django.views.generic import ListView, DetailView, CreateView, \
                                 DeleteView, UpdateView, \
                                 ArchiveIndexView, DateDetailView, \
                                 DayArchiveView, MonthArchiveView, \
                                 TodayArchiveView, WeekArchiveView, \
                                 YearArchiveView, View


# from p8app.models import *
# from p8app.forms import *
from schoolnew.models import *
from schoolnew.forms import *
# from baseapp.models import School, Block
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

def home(request):
	v = Basicinfo.objects.all()
	return render(request,'school/schoolnew/home.html',locals())
	
class myentry(CreateView):
	template_name = 'school/schoolnew/basic.html'
	success_url = '/'
	model = Basicinfo

class delete(View):
	def get(self,request,**kwargs):
		pk = self.kwargs.get('id') 
		data = Basicinfo.objects.get(id=pk)
		return render(request,'school/schoolnew/home.html',locals())

	def post(self,request,**kwargs):
		pk = self.kwargs.get('id') 
		data = Basicinfo.objects.get(id=pk)
		data.delete()
		return render(request,'school/schoolnew/home.html',locals())

class update(UpdateView):
	form_class = BasicForm
	model = Basicinfo
	template_name = 'school/schoolnew/basic.html'
	success_url = '/'

	def get(self, request, **kwargs):
		self.object = Basicinfo.objects.get(id=self.kwargs.get('id'))
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		context = self.get_context_data(object=self.object, form=form)
		return self.render_to_response(context)

	def get_object(self, queryset=None):
		obj = Basicinfo.objects.get(id=self.kwargs.get('id'))
		return obj

class School_CreateView(View):
	def get(self,request,**kwargs):
		form=BasicForm()
		district_list = District.objects.all().exclude(district_name='None').order_by('district_name')
		language_list = Language.objects.all().exclude(language_name='Undefined').order_by('language_name')
		education_medium_list = Education_medium.objects.all().exclude(education_medium='Undefined').order_by('education_medium')
		bank_list = Bank.objects.all()
		return render (request,'school/schoolnew/basic.html',{'form':form,'district_list':district_list,'language_list':language_list,'bank_list':bank_list,'education_medium_list':education_medium_list})

	def post(self,request,**kwargs):
		form = BasicForm(request.POST,request.FILES)
		if form.is_valid():
			basicinfo = Basicinfo(
			school_name = form.cleaned_data['school_name'],
			school_name_tamil = form.cleaned_data['school_name_tamil'],
			udise_code = form.cleaned_data['udise_code'],
			district = form.cleaned_data['district'],
			edu_district = form.cleaned_data['edu_district'],
			block = form.cleaned_data['block'],
			rural = form.cleaned_data['rural'],
			village_panchayat = form.cleaned_data['village_panchayat'],
			habitation = form.cleaned_data['habitation'],
			urban = form.cleaned_data['urban'],
			Town_panchayat = form.cleaned_data['Town_panchayat'],
			Ward_no = form.cleaned_data['Ward_no'],
			address = form.cleaned_data['address'],
			pincode = form.cleaned_data['pincode'],
			stdcode = form.cleaned_data['stdcode'],
			Landline = form.cleaned_data['Landline'],
			Mobile = form.cleaned_data['Mobile'],
			email = form.cleaned_data['email'],
			website  = form.cleaned_data['website'],
			Bank_name = form.cleaned_data['Bank_name'],
			branch_name = form.cleaned_data['branch_name'],
			ifsc_code = form.cleaned_data['ifsc_code'],
			smc_code = form.cleaned_data['smc_code'],
			assembly = form.cleaned_data['assembly'],
			parliament = form.cleaned_data['parliament'],
			latitude = form.cleaned_data['latitude'],
			longitude = form.cleaned_data['longitude'],
			)
			basicinfo.save()

			school_id = Basicinfo.objects.get(udise_code=basicinfo.udise_code)

			academicinfo = Academicinfo(
		    school_key = school_id,
			school_management = form.cleaned_data['school_management'],
			school_category = form.cleaned_data['school_category'],
			department = form.cleaned_data['department'],
			schooltype = form.cleaned_data['schooltype'],
			low_class = form.cleaned_data['low_class'],
			high_class = form.cleaned_data['high_class'],
			board = form.cleaned_data['board'],
			tamil_med = form.cleaned_data['tamil_med'],
			eng_med = form.cleaned_data['eng_med'],
			tel_med = form.cleaned_data['tel_med'],
			mal_med = form.cleaned_data['mal_med'],
			kan_med = form.cleaned_data['kan_med'],
			urdu_med = form.cleaned_data['urdu_med'],
			other_med = form.cleaned_data['other_med'],
			minority = form.cleaned_data['minority'],
			rel_minority = form.cleaned_data['rel_minority'],
			ling_minority = form.cleaned_data['ling_minority'],
			Ord_No = form.cleaned_data['Ord_No'],
			dt_iss = form.cleaned_data['dt_iss'],
			iss_auth = form.cleaned_data['iss_auth'],
			year_est = form.cleaned_data['year_est'],
			year_appr = form.cleaned_data['year_appr'],
			year_upgr = form.cleaned_data['year_upgr'],
			spl_school = form.cleaned_data['spl_school'],
			spl_type = form.cleaned_data['spl_type'],
			boarding = form.cleaned_data['boarding'],
			)
			academicinfo.save()

			infradet = Infradet(
			school_key = school_id,
			school_code = form.cleaned_data['school_code'],
			elec_yes = form.cleaned_data['elec_yes'],
			elec_no = form.cleaned_data['elec_no'],
			elec_w = form.cleaned_data['elec_w'],
			elec_nw = form.cleaned_data['elec_nw'],
			tot_ft = form.cleaned_data['tot_ft'],
			tot_mt = form.cleaned_data['tot_mt'],
			covered_ft = form.cleaned_data['covered_ft'],
			covered_mt = form.cleaned_data['covered_mt'],
			open_ft = form.cleaned_data['open_ft'],
			open_mt = form.cleaned_data['open_mt'],
			play_ft = form.cleaned_data['play_ft'],
			play_mt = form.cleaned_data['play_mt'],
			cwall_yes = form.cleaned_data['cwall_yes'],
			cwall_no  = form.cleaned_data['cwall_no'],
			cwall_type = form.cleaned_data['cwall_type'],
			no_sides = form.cleaned_data['no_sides'],
			fireext_yes = form.cleaned_data['fireext_yes'],
			fireext_no = form.cleaned_data['fireext_no'],
			fireext_w = form.cleaned_data['fireext_w'],
			fireext_nw = form.cleaned_data['fireext_nw'],
			rainwater_yes = form.cleaned_data['rainwater_yes'],
			kitchenshed_yes = form.cleaned_data['kitchenshed_yes'],
			bu_no = form.cleaned_data['bu_no'],
			bu_usable = form.cleaned_data['bu_usable'],
			bu_minrep = form.cleaned_data['bu_minrep'],
			bu_majrep = form.cleaned_data['bu_majrep'],
			gu_no = form.cleaned_data['gu_no'],
			gu_usable = form.cleaned_data['gu_usable'],
			gu_minrep = form.cleaned_data['gu_minrep'],
			gu_majrep = form.cleaned_data['gu_majrep'],
			bl_no = form.cleaned_data['bl_no'],
			bl_usable = form.cleaned_data['bl_usable'],
			bl_minrep = form.cleaned_data['bl_minrep'],
			bl_majrep = form.cleaned_data['bl_majrep'],
			gl_no = form.cleaned_data['gl_no'],
			gl_usable = form.cleaned_data['gl_usable'],
			gl_minrep = form.cleaned_data['gl_minrep'],
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
			available_yes = form.cleaned_data['available_yes'],
			available_no = form.cleaned_data['available_no'],
			source_pc = form.cleaned_data['source_pc'],
			source_bw = form.cleaned_data['source_bw'],
			source_pump = form.cleaned_data['source_pump'],
			Purification_wf = form.cleaned_data['Purification_wf'],
			Purification_ro = form.cleaned_data['Purification_ro'],
			Purification_na = form.cleaned_data['Purification_na'],
			access_pitcher  = form.cleaned_data['access_pitcher'],
			access_steeldrum  = form.cleaned_data['access_steeldrum'],
			access_cementtank  = form.cleaned_data['access_cementtank'],
			access_syntaxtank  = form.cleaned_data['access_syntaxtank'],
			avail_yes = form.cleaned_data['avail_yes'],
			avail_no = form.cleaned_data['avail_no'],
			no_seats = form.cleaned_data['no_seats'],
			fans = form.cleaned_data['fans'],
			tubelights = form.cleaned_data['tubelights'],
			available = form.cleaned_data['available'],
			not_available = form.cleaned_data['not_available'], 
			internet_yes = form.cleaned_data['internet_yes'], #to be added to model.py
			avai_yes = form.cleaned_data['avai_yes'], #to be added to model.py
			floors_no = form.cleaned_data['floors_no'],
			rooms_no = form.cleaned_data['rooms_no'],
			)
			infradet.save()

			try:
				teaching_no = request.POST.getlist('teaching_no')
				T_post_name = request.POST.getlist('T_post_name')
				T_post_sanc = request.POST.getlist('T_post_sanc')
				T_post_mode = request.POST.getlist('T_post_mode')
				T_post_GO = request.POST.getlist('T_post_GO')
				T_post_GO_dt = request.POST.getlist('T_post_GO_dt')
				T_post_GO_pd = request.POST.getlist('T_post_GO_pd')
				for entry in range(len(teaching_no)):
					teachingstaff = Teachingstaff(
					school_key = school_id,
					s_no = teaching_no[entry],
					T_post_name = T_post_name[entry],
					T_post_sanc  = T_post_sanc[entry],
					T_post_mode = T_post_mode[entry],
					T_post_GO = T_post_GO[entry],
					T_post_GO_dt = T_post_GO_dt[entry],
					T_post_GO_pd = T_post_GO_pd[entry],
					)
					teachingstaff.save()

				nonteaching_no = request.POST.getlist('nonteaching_no')
				NT_post_name = request.POST.getlist('NT_post_name')
				NT_post_sanc = request.POST.getlist('NT_post_sanc')
				NT_post_mode = request.POST.getlist('NT_post_mode')
				NT_post_GO = request.POST.getlist('NT_post_GO')
				NT_post_GO_dt = request.POST.getlist('NT_post_GO_dt')
				NT_post_GO_pd = request.POST.getlist('NT_post_GO_pd')
				for entry in range(len(nonteaching_no)):
					nonteachingstaff = NonTeachingstaff(
					school_key = school_id,
					s_no = nonteaching_no[entry],
					NT_post_name = NT_post_name[entry],
					NT_post_sanc  = NT_post_sanc[entry],
					NT_post_mode = NT_post_mode[entry],
					NT_post_GO = NT_post_GO[entry],
					NT_post_GO_dt = NT_post_GO_dt[entry],
					NT_post_GO_pd = NT_post_GO_pd[entry],
					)
					nonteachingstaff.save()

				parttime_no = request.POST.getlist('parttime_no')
				part_instr = request.POST.getlist('part_instr')
				part_instr_sub = request.POST.getlist('part_instr_sub')
				for entry in range(len(parttime_no)):
					parttimestaff = Parttimestaff(
					school_key = school_id,
					s_no = parttime_no[entry],
					parttime_no = parttime_no[entry],
					part_instr = part_instr[entry],
					part_instr_sub = part_instr_sub[entry],
					)
					parttimestaff.save()

				building_sno = request.POST.getlist('building_sno')
				room_type = request.POST.getlist('room_type')
				room_no = request.POST.getlist('room_no')
				buildup_area = request.POST.getlist('buildup_area')
				purpose = request.POST.getlist('purpose') #have to add in forms.py , models.py
				status = request.POST.getlist('status')
				for entry in range(len(building_sno)):
					building = Building(
					school_key = school_id,
					building_sno = building_sno[entry],
					room_type = room_type[entry],
					room_no = room_no[entry],
					buildup_area = buildup_area[entry],
					purpose = purpose[entry],
					status = status[entry],
					)
					building.save()

				land_sno = request.POST.getlist('land_sno')
				name = request.POST.getlist('name')
				area = request.POST.getlist('area')
				patta_no = request.POST.getlist('patta_no')
				survey_no = request.POST.getlist('survey_no')
				used_for = request.POST.getlist('used_for')
				for entry in range(len(land_sno)):
					land = Land(
					school_key = school_id,
					land_sno = land_sno[entry],
					name = name[entry],
					area = area[entry],
					patta_no = patta_no[entry],
					survey_no = survey_no[entry],
					used_for = used_for[entry],
					)
					land.save()

				sports_sno = request.POST.getlist('sports_sno')
				sports_name = request.POST.getlist('sports_name')
				wscp_yes = request.POST.getlist('wscp_yes')
				eavailability_y = request.POST.getlist('eavailability_y')
				no_sets = request.POST.getlist('no_sets')
				for entry in range(len(sports_sno)):
					sports = Sports(
					school_key = school_id,
					sports_sno = sports_sno[entry],
					sports_name = sports_name[entry],
					wscp_yes = wscp_yes[entry],
					eavailability_y = eavailability_y[entry],   
					no_sets = no_sets[entry],
					)
					sports.save()

				ict_sno = request.POST.getlist('ict_sno')
				item_type = request.POST.getlist('item_type')
				working = request.POST.getlist('working')
				not_working = request.POST.getlist('not_working')
				supplied_by = request.POST.getlist('supplied_by')
				for entry in range(len(ict_sno)):
					ictentry = Ictentry(
					school_key = school_id,
					ict_sno = ict_sno[entry],
					item_type = item_type[entry],
					working =  working[entry],
					not_working = not_working[entry],   
					supplied_by = supplied_by[entry],
					)
					ictentry.save()
			except Exception:
				pass
			msg = "School    " + str(school_id) + " details added successfully"
			messages.success(request, msg )
			return HttpResponseRedirect(reverse('schoolnewhome'))
		else:
			district_list = District.objects.all().exclude(district_name='None').order_by('district_name')
			return render (request,'school/schoolnew/basic.html',{'form':form,'district_list':district_list}) 

class School_UpdateView(View):

	def get(self, request,**kwargs):
		pk=self.kwargs.get('id')
		instance = Basicinfo.objects.get(udise_code=pk)

		try:
			
			teachingstaff = Teachingstaff.objects.filter(school_key=pk)
			nonteachingstaff = NonTeachingstaff.objects.filter(school_key=pk)
			parttimestaff = Parttimestaff.objects.filter(school_key=pk)
			building = Building.objects.filter(school_key=pk)
			land = Land.objects.filter(school_key=pk)
			sports = Sports.objects.filter(school_key=pk)
			ictentry = Ictentry.objects.filter(school_key=pk)

		except Exception:
			
			teachingstaff=None
			nonteachingstaff=None
			parttimestaff=None
			building=None
			land=None
			sports=None
			ictentry=None

		district_list = District.objects.all().exclude(district_name='None').order_by('district_name')
		form = BasicForm(instance=instance)
		tamilmed = instance.tamil_med
		engmed = instance.eng_med 
		telmed = instance.tel_med 
		malmed = instance.mal_med 
		kanmed = instance.kan_med 
		urdumed = instance.urdu_med 
		othermed = instance.other_med 
		minority = instance.minority 
		relminority = instance.rel_minority 
		lingminority = instance.ling_minority 
		splschool = instance.spl_school 
		boarding = instance.boarding 
		elecyes = instance.elec_yes 
		elecno = instance.elec_no 
		elec_w = instance.elec_w 
		elec_nw = instance.elec_nw 
		cwallyes = instance.cwall_yes 
		cwallno = instance.cwall_no 
		fireextyes = instance.fireext_yes 
		fireextno = instance.fireext_no 
		fireextw = instance.fireext_w 
		fireextnw = instance.fireext_nw 
		rainwateryes = instance.rainwater_yes 
		kitchenshedyes = instance.kitchenshed_yes 
		availableyes = instance.available_yes 
		availableno = instance.available_no 
		sourcepc = instance.source_pc 
		sourcebw = instance.source_bw 
		sourcepump = instance.source_pump 
		purificationwf = instance.Purification_wf 
		purificationro = instance.Purification_ro 
		purificationna = instance.Purification_na 
		accesspitcher = instance.access_pitcher  
		accesssteeldrum = instance.access_steeldrum  
		accesscementtank = instance.access_cementtank  
		accesssyntaxtank = instance.access_syntaxtank  
		availyes = instance.avail_yes 
		availno = instance.avail_no 
		available = instance.available 
		notavailable = instance.not_available 
		wscpyes = instance.wscp_yes 
		eavailabilityy = instance.eavailability_y 
		internetyes = instance.internet_yes 
		avaiyes = instance.avai_yes 
		
		# return render(request, 'students/child_detail/child_detail_form.html', {'form': form,'fmdetail':fmdetail,'district_list':district_list,'pk1':pk,'schemes':schemes,'differently_abled_list':differently_abled_list,'dis_advantaged_list':dis_advantaged_list,'ge':ge,'cls_section':cls_section,'cls_studying':cls_studying,'academic_yr':academic_yr,'mother_ocu':mother_ocu,'father_ocu':father_ocu,'bg':bg,'st_status':st_status,'differently_abled_list1':differently_abled_list1,'disadvantaged_group1':disadvantaged_group1,'schemes1':schemes1,'sport_participation':sport_participation,'sports_name':sports_name,'mthr_name':mthr_name,'nutritious_meal_programme':nutritious_meal_programme,'state_list':state_list,'parent_income_list':parent_income_list,'parent_income':parent_income,'class_studying_list':class_studying_list,'group_code_list':group_code_list,'bank_list':bank_list,'education_medium_list':education_medium_list,'nationality_list':nationality_list,'religion_list':religion_list,'community_list':community_list,'language_list':language_list,'mothrtongue':mothrtongue,'edu_medium':edu_medium,'nationality_value':nationality_value,'religion_value':religion_value,'parent_income':parent_income,'govt_aid_school_management_list':govt_aid_school_management_list,'aid_school_management_list':aid_school_management_list,'private_school_management_list':private_school_management_list,'onetoten':onetoten,'stud_admitted_section':stud_admitted_section,'address':address,'onetotwelve':onetotwelve,'onetoeight':onetoeight})
		return render(request, 'school/schoolnew/basic.html', locals())

	def post(self,request,**kwargs):
		pk=self.kwargs.get('id')
		instance = Basicinfo.objects.get(udise_code=pk)

		form = BasicForm(request.POST,request.FILES)
		if form.is_valid():
			basic_edit = Basicinfo.objects.get(udise_code=pk)

			basic_edit.school_name = form.cleaned_data['school_name']
			basic_edit.school_name_tamil = form.cleaned_data['school_name_tamil']
			basic_edit.udise_code = form.cleaned_data['udise_code']
			basic_edit.district = form.cleaned_data['district']
			basic_edit.edu_district = form.cleaned_data['edu_district']
			basic_edit.block = form.cleaned_data['block']
			basic_edit.rural = form.cleaned_data['rural']
			basic_edit.village_panchayat = form.cleaned_data['village_panchayat']
			basic_edit.habitation = form.cleaned_data['habitation']
			basic_edit.urban = form.cleaned_data['urban']
			basic_edit.Town_panchayat = form.cleaned_data['Town_panchayat']
			basic_edit.Ward_no = form.cleaned_data['Ward_no']
			basic_edit.address = form.cleaned_data['address']
			basic_edit.pincode = form.cleaned_data['pincode']
			basic_edit.stdcode = form.cleaned_data['stdcode']
			basic_edit.Landline = form.cleaned_data['Landline']
			basic_edit.Mobile = form.cleaned_data['Mobile']
			basic_edit.email = form.cleaned_data['email']
			basic_edit.website  = form.cleaned_data['website']
			basic_edit.Bank_name = form.cleaned_data['Bank_name']
			basic_edit.branch_name = form.cleaned_data['branch_name']
			basic_edit.ifsc_code = form.cleaned_data['ifsc_code']
			basic_edit.smc_code = form.cleaned_data['smc_code']
			basic_edit.assembly = form.cleaned_data['assembly']
			basic_edit.parliament = form.cleaned_data['parliament']
			basic_edit.latitude = form.cleaned_data['latitude']
			basic_edit.longitude = form.cleaned_data['longitude']

			basic_edit.save()

			academic_edit = Academicinfo.objects.get(school_key=pk)

			academic_edit.school_key = basic_edit
			academic_edit.school_management = form.cleaned_data['school_management']
			academic_edit.school_category = form.cleaned_data['school_category']
			academic_edit.department = form.cleaned_data['department']
			academic_edit.schooltype = form.cleaned_data['schooltype']
			academic_edit.low_class = form.cleaned_data['low_class']
			academic_edit.high_class = form.cleaned_data['high_class']
			academic_edit.board = form.cleaned_data['board']
			academic_edit.tamil_med = form.cleaned_data['tamil_med']
			academic_edit.eng_med = form.cleaned_data['eng_med']
			academic_edit.tel_med = form.cleaned_data['tel_med']
			academic_edit.mal_med = form.cleaned_data['mal_med']
			academic_edit.kan_med = form.cleaned_data['kan_med']
			academic_edit.urdu_med = form.cleaned_data['urdu_med']
			academic_edit.other_med = form.cleaned_data['other_med']
			academic_edit.minority = form.cleaned_data['minority']
			academic_edit.rel_minority = form.cleaned_data['rel_minority']
			academic_edit.ling_minority = form.cleaned_data['ling_minority']
			academic_edit.Ord_No = form.cleaned_data['Ord_No']
			academic_edit.dt_iss = form.cleaned_data['dt_iss']
			academic_edit.iss_auth = form.cleaned_data['iss_auth']
			academic_edit.year_est = form.cleaned_data['year_est']
			academic_edit.year_appr = form.cleaned_data['year_appr']
			academic_edit.year_upgr = form.cleaned_data['year_upgr']
			academic_edit.spl_school = form.cleaned_data['spl_school']
			academic_edit.spl_type = form.cleaned_data['spl_type']
			academic_edit.boarding = form.cleaned_data['boarding']
			
			academic_edit.save()

			infradet_edit = Infradet.objects.get(school_key=pk)

			infradet_edit.school_key = basic_edit
			infradet_edit.school_code = form.cleaned_data['school_code']
			infradet_edit.elec_yes = form.cleaned_data['elec_yes']
			infradet_edit.elec_no = form.cleaned_data['elec_no']
			infradet_edit.elec_w = form.cleaned_data['elec_w']
			infradet_edit.elec_nw = form.cleaned_data['elec_nw']
			infradet_edit.tot_ft = form.cleaned_data['tot_ft']
			infradet_edit.tot_mt = form.cleaned_data['tot_mt']
			infradet_edit.covered_ft = form.cleaned_data['covered_ft']
			infradet_edit.covered_mt = form.cleaned_data['covered_mt']
			infradet_edit.open_ft = form.cleaned_data['open_ft']
			infradet_edit.open_mt = form.cleaned_data['open_mt']
			infradet_edit.play_ft = form.cleaned_data['play_ft']
			infradet_edit.play_mt = form.cleaned_data['play_mt']
			infradet_edit.cwall_yes = form.cleaned_data['cwall_yes']
			infradet_edit.cwall_no  = form.cleaned_data['cwall_no']
			infradet_edit.cwall_type = form.cleaned_data['cwall_type']
			infradet_edit.no_sides = form.cleaned_data['no_sides']
			infradet_edit.fireext_yes = form.cleaned_data['fireext_yes']
			infradet_edit.fireext_no = form.cleaned_data['fireext_no']
			infradet_edit.fireext_w = form.cleaned_data['fireext_w']
			infradet_edit.fireext_nw = form.cleaned_data['fireext_nw']
			infradet_edit.rainwater_yes = form.cleaned_data['rainwater_yes']
			infradet_edit.kitchenshed_yes = form.cleaned_data['kitchenshed_yes']
			infradet_edit.bu_no = form.cleaned_data['bu_no']
			infradet_edit.bu_usable = form.cleaned_data['bu_usable']
			infradet_edit.bu_minrep = form.cleaned_data['bu_minrep']
			infradet_edit.bu_majrep = form.cleaned_data['bu_majrep']
			infradet_edit.gu_no = form.cleaned_data['gu_no']
			infradet_edit.gu_usable = form.cleaned_data['gu_usable']
			infradet_edit.gu_minrep = form.cleaned_data['gu_minrep']
			infradet_edit.gu_majrep = form.cleaned_data['gu_majrep']
			infradet_edit.bl_no = form.cleaned_data['bl_no']
			infradet_edit.bl_usable = form.cleaned_data['bl_usable']
			infradet_edit.bl_minrep = form.cleaned_data['bl_minrep']
			infradet_edit.bl_majrep = form.cleaned_data['bl_majrep']
			infradet_edit.gl_no = form.cleaned_data['gl_no']
			infradet_edit.gl_usable = form.cleaned_data['gl_usable']
			infradet_edit.gl_minrep = form.cleaned_data['gl_minrep']
			infradet_edit.gl_majrep = form.cleaned_data['gl_majrep']
			infradet_edit.gentsu_no = form.cleaned_data['gentsu_no']
			infradet_edit.gentsu_usable = form.cleaned_data['gentsu_usable']
			infradet_edit.gentsu_minrep = form.cleaned_data['gentsu_minrep']
			infradet_edit.gentsu_majrep = form.cleaned_data['gentsu_majrep']
			infradet_edit.ladiesu_no = form.cleaned_data['ladiesu_no']
			infradet_edit.ladiesu_usable = form.cleaned_data['ladiesu_usable']
			infradet_edit.ladiesu_minrep = form.cleaned_data['ladiesu_minrep']
			infradet_edit.ladiesu_majrep = form.cleaned_data['ladiesu_majrep']
			infradet_edit.gentsl_no = form.cleaned_data['gentsl_no']
			infradet_edit.gentsl_usable = form.cleaned_data['gentsl_usable']
			infradet_edit.gentsl_minrep = form.cleaned_data['gentsl_minrep']
			infradet_edit.gentsl_majrep = form.cleaned_data['gentsl_majrep']
			infradet_edit.ladiesl_no = form.cleaned_data['ladiesl_no']
			infradet_edit.ladiesl_usable = form.cleaned_data['ladiesl_usable']
			infradet_edit.ladiesl_minrep = form.cleaned_data['ladiesl_minrep']
			infradet_edit.ladiesl_majrep = form.cleaned_data['ladiesl_majrep']
			infradet_edit.available_yes = form.cleaned_data['available_yes']
			infradet_edit.available_no = form.cleaned_data['available_no']
			infradet_edit.source_pc = form.cleaned_data['source_pc']
			infradet_edit.source_bw = form.cleaned_data['source_bw']
			infradet_edit.source_pump = form.cleaned_data['source_pump']
			infradet_edit.Purification_wf = form.cleaned_data['Purification_wf']
			infradet_edit.Purification_ro = form.cleaned_data['Purification_ro']
			infradet_edit.Purification_na = form.cleaned_data['Purification_na']
			infradet_edit.access_pitcher  = form.cleaned_data['access_pitcher']
			infradet_edit.access_steeldrum  = form.cleaned_data['access_steeldrum']
			infradet_edit.access_cementtank  = form.cleaned_data['access_cementtank']
			infradet_edit.access_syntaxtank  = form.cleaned_data['access_syntaxtank']
			infradet_edit.avail_yes = form.cleaned_data['avail_yes']
			infradet_edit.avail_no = form.cleaned_data['avail_no']
			infradet_edit.no_seats = form.cleaned_data['no_seats']
			infradet_edit.fans = form.cleaned_data['fans']
			infradet_edit.tubelights = form.cleaned_data['tubelights']
			infradet_edit.available = form.cleaned_data['available']
			infradet_edit.not_available = form.cleaned_data['not_available'] 
			infradet_edit.internet_yes = form.cleaned_data['internet_yes'] 
			infradet_edit.avai_yes = form.cleaned_data['avai_yes'] 
			infradet_edit.floors_no = form.cleaned_data['floors_no']
			infradet_edit.rooms_no = form.cleaned_data['rooms_no']
			
			infradet_edit.save()

			try:
				teaching_no = request.POST.getlist('teaching_no')
				T_post_name = request.POST.getlist('T_post_name')
				T_post_sanc = request.POST.getlist('T_post_sanc')
				T_post_mode = request.POST.getlist('T_post_mode')
				T_post_GO = request.POST.getlist('T_post_GO')
				T_post_GO_dt = request.POST.getlist('T_post_GO_dt')
				T_post_GO_pd = request.POST.getlist('T_post_GO_pd')
				for entry in range(len(teaching_no)):
					teachingstaff_edit = Teachingstaff.objects.get(school_key=pk)
					teachingstaff_edit.school_key = basic_edit
					teachingstaff_edit.s_no = teaching_no[entry]
					teachingstaff_edit.T_post_name = T_post_name[entry]
					teachingstaff_edit.T_post_sanc  = T_post_sanc[entry]
					teachingstaff_edit.T_post_mode = T_post_mode[entry]
					teachingstaff_edit.T_post_GO = T_post_GO[entry]
					teachingstaff_edit.T_post_GO_dt = T_post_GO_dt[entry]
					teachingstaff_edit.T_post_GO_pd = T_post_GO_pd[entry]

					teachingstaff_edit.save()

				nonteaching_no = request.POST.getlist('nonteaching_no')
				NT_post_name = request.POST.getlist('NT_post_name')
				NT_post_sanc = request.POST.getlist('NT_post_sanc')
				NT_post_mode = request.POST.getlist('NT_post_mode')
				NT_post_GO = request.POST.getlist('NT_post_GO')
				NT_post_GO_dt = request.POST.getlist('NT_post_GO_dt')
				NT_post_GO_pd = request.POST.getlist('NT_post_GO_pd')
				for entry in range(len(nonteaching_no)):
					nonteachingstaff_edit = NonTeachingstaff.objects.get(school_key=pk)
					nonteachingstaff_edit.school_key = basic_edit
					nonteachingstaff_edit.s_no = nonteaching_no[entry]
					nonteachingstaff_edit.NT_post_name = NT_post_name[entry]
					nonteachingstaff_edit.NT_post_sanc  = NT_post_sanc[entry]
					nonteachingstaff_edit.NT_post_mode = NT_post_mode[entry]
					nonteachingstaff_edit.NT_post_GO = NT_post_GO[entry]
					nonteachingstaff_edit.NT_post_GO_dt = NT_post_GO_dt[entry]
					nonteachingstaff_edit.NT_post_GO_pd = NT_post_GO_pd[entry]
					
					nonteachingstaff_edit.save()

				parttime_no = request.POST.getlist('parttime_no')
				part_instr = request.POST.getlist('part_instr')
				part_instr_sub = request.POST.getlist('part_instr_sub')
				for entry in range(len(parttime_no)):
					parttimestaff_edit = Parttimestaff.objects.get(school_key=pk)
					parttimestaff_edit.school_key = basic_edit
					parttimestaff_edit.s_no = parttime_no[entry]
					parttimestaff_edit.parttime_no = parttime_no[entry]
					parttimestaff_edit.part_instr = part_instr[entry]
					parttimestaff_edit.part_instr_sub = part_instr_sub[entry]
					
					parttimestaff_edit.save()

				building_sno = request.POST.getlist('building_sno')
				room_type = request.POST.getlist('room_type')
				room_no = request.POST.getlist('room_no')
				buildup_area = request.POST.getlist('buildup_area')
				purpose = request.POST.getlist('purpose') 
				status = request.POST.getlist('status')
				for entry in range(len(building_sno)):
					building_edit = Building.objects.get(school_key=pk)
					building_edit.school_key = basic_edit
					building_edit.building_sno = building_sno[entry]
					building_edit.room_type = room_type[entry]
					building_edit.room_no = room_no[entry]
					building_edit.buildup_area = buildup_area[entry]
					building_edit.purpose = purpose[entry]
					building_edit.status = status[entry]
					
					building_edit.save()

				land_sno = request.POST.getlist('land_sno')
				name = request.POST.getlist('name')
				area = request.POST.getlist('area')
				patta_no = request.POST.getlist('patta_no')
				survey_no = request.POST.getlist('survey_no')
				used_for = request.POST.getlist('used_for')
				for entry in range(len(land_sno)):
					land_edit = Land.objects.get(school_key=pk)
					land_edit.school_key = basic_edit
					land_edit.land_sno = land_sno[entry]
					land_edit.name = name[entry]
					land_edit.area = area[entry]
					land_edit.patta_no = patta_no[entry]
					land_edit.survey_no = survey_no[entry]
					land_edit.used_for = used_for[entry]
					
					land_edit.save()

				sports_sno = request.POST.getlist('sports_sno')
				sports_name = request.POST.getlist('sports_name')
				wscp_yes = request.POST.getlist('wscp_yes')
				eavailability_y = request.POST.getlist('eavailability_y')
				no_sets = request.POST.getlist('no_sets')
				for entry in range(len(sports_sno)):
					sports_edit = Sports.objects.get(school_key=pk)
					sports_edit.school_key = basic_edit
					sports_edit.sports_sno = sports_sno[entry]
					sports_edit.sports_name = sports_name[entry]
					sports_edit.wscp_yes = wscp_yes[entry]
					sports_edit.eavailability_y = eavailability_y[entry]   
					sports_edit.no_sets = no_sets[entry]
					
					sports_edit.save()

				ict_sno = request.POST.getlist('ict_sno')
				item_type = request.POST.getlist('item_type')
				working = request.POST.getlist('working')
				not_working = request.POST.getlist('not_working')
				supplied_by = request.POST.getlist('supplied_by')
				for entry in range(len(ict_sno)):
					ictentry_edit = Ictentry.objects.get(school_key=pk)
					ictentry_edit.school_key = basic_edit
					ictentry_edit.ict_sno = ict_sno[entry]
					ictentry_edit.item_type = item_type[entry]
					ictentry_edit.working =  working[entry]
					ictentry_edit.not_working = not_working[entry]   
					ictentry_edit.supplied_by = supplied_by[entry]
					
					ictentry_edit.save()
			except Teachingstaff.DoesNotExist:
				pass
		else:
			# return render (request,'students/child_detail/child_detail_form.html',{'form':form,'pk1':pk,'cls_studying':cls_studying,'academic_yr':academic_yr})
			return render(request, 'school/schoolnew/basic.html', locals())
		msg = "School    " + form.cleaned_data['school_name'] + "  updated successfully"
		messages.success(request, msg )
		return HttpResponseRedirect(reverse('school_school_list'))