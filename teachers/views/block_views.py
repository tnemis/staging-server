from django.views.generic import View
from django.contrib import messages
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from students.models import Child_detail, School_child_count
from teachers.models import Teacher_detail, block_wise_abstract, district_wise_abstract
from schoolnew.models import Basicinfo, Staff
from baseapp.models import District, Block, School, Habitation, Zone
from django.core.paginator import Paginator, PageNotAnInteger
from django.db.models import Count, Sum
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache


class block_level_list(View):
	#@never_cache
	def get(self,request,**kwargs):
		if request.user.is_authenticated():
			distid=int(self.kwargs.get('blockid'))
			associateid=int(self.kwargs.get('associateid'))
			request.user.account.user_category_id=associateid
			if (block_wise_abstract.objects.filter(district_code_id=distid)>0):
				block_wise_abstract.objects.filter(district_code_id=distid).delete()

			basic_det=Basicinfo.objects.filter(district_id=distid)
			Number_of_schools_in_block=basic_det.count()
			
			
			try:

				for basic_table_record in basic_det:
					tsanc_count=0
					nsanc_count=0
					tvaccant_count=0
					nvaccant_count=0
					tfilled_count=0
					nfilled_count=0
					tfilled_count = Teacher_detail.objects.filter(school_id=basic_table_record.school_id,stafs='Teaching')
					nfilled_count = Teacher_detail.objects.filter(school_id=basic_table_record.school_id,stafs='Non Teaching')
					
					if (Teachingstaff.objects.filter(school_key=basic_table_record.id).count())>0:
						teach_det = Teachingstaff.objects.filter(school_key=basic_table_record.id).values('tpost_name').annotate(tcount=Sum('tpost_sanc'))
						for t_count in teach_det:

							tsanc_count=tsanc_count+ t_count.get('tcount')

						
					if (NonTeachingstaff.objects.filter(school_key=basic_table_record.id).count())>0:
						nteach_det = NonTeachingstaff.objects.filter(school_key=basic_table_record.id).values('ntpost_name').annotate(ntcount=Sum('ntpost_sanc'))
						for nt_count in nteach_det:

							nsanc_count=nsanc_count+ nt_count.get('ntcount')
						
				
					tvaccant_count=int(tsanc_count)-int(tfilled_count.count())
					nvaccant_count=int(nsanc_count)-int(nfilled_count.count())
					if nvaccant_count<0:
						nvaccant_count=0
					if tvaccant_count<0:
						tvaccant_count=0
					N = Block.objects.get(id=basic_table_record.block_id)
					
					block_wise_count=block_wise_abstract(school_key=basic_table_record.id,
							district_code_id=basic_table_record.district_id,
							block_code_id=basic_table_record.block_id,
							block_name=N.block_name,
							school_code=basic_table_record.school_id,
							school_name=basic_table_record.school_name,
							tsanctioned_post=tsanc_count,
							tfilled_post=tfilled_count.count(),
							tvaccant_post=tvaccant_count,
							ntsanctioned_post=nsanc_count,
							ntfilled_post=nfilled_count.count(),
							ntvaccant_post=nvaccant_count,
							udise_code=basic_table_record.udise_code,
							flag='Yes',)
					
					block_wise_count.save()
					print block_wise_count
			
				

				c=block_wise_abstract.objects.filter(district_code_id=distid).values('block_name','block_code').annotate(tount=Count('block_code')).annotate(tcount=Sum('tsanctioned_post')).annotate(tcount1=Sum('tfilled_post')).annotate(tcount2=Sum('tvaccant_post'))
				

			 	block_wise_records=block_wise_abstract.objects.filter(district_code_id=distid)
			 	tsanctioned_post_total=0
				tfilled_post_total=0
				tvaccant_post_total=0
				nsanctioned_post_total=0
				nfilled_post_total=0
				nvaccant_post_total=0
				
				for counting in block_wise_records:

					tsanctioned_post_total=tsanctioned_post_total+counting.tsanctioned_post
					tfilled_post_total=tfilled_post_total+counting.tfilled_post
					tvaccant_post_total=tvaccant_post_total+counting.tvaccant_post
					nsanctioned_post_total=nsanctioned_post_total+counting.ntsanctioned_post
					nfilled_post_total=nfilled_post_total+counting.ntfilled_post
					nvaccant_post_total=nvaccant_post_total+counting.ntvaccant_post
				
				return render(request,'teachers/block/dist_detail.html',locals())
			except:
				return HttpResponseRedirect('/')
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	
		

class BlockView_teachers(View):
	#@never_cache
	def get(self,request,**kwargs):
		if request.user.is_authenticated():
		
			# try:
			if request.user.account.user_category_id == 6 or request.user.account.user_category_id == 7 or request.user.account.user_category_id == 8 or request.user.account.user_category_id == 9 or request.user.account.user_category_id == 10 or request.user.account.user_category_id == 11 or request.user.account.user_category_id == 12 or request.user.account.user_category_id == 13 or request.user.account.user_category_id == 14 or request.user.account.user_category_id == 15 or request.user.account.user_category_id == 16 or request.user.account.user_category_id == 17 or request.user.account.user_category_id == 4 or request.user.account.user_category_id == 3:
				
				if request.user.account.user_category_id == 3:
					if(block_wise_abstract.objects.filter(district_code_id=request.user.account.associated_with)>0):
						block_wise_abstract.objects.filter(district_code_id=request.user.account.associated_with).delete()
					if (district_wise_abstract.objects.filter(district_code_id=request.user.account.associated_with)>0):
						district_wise_abstract.objects.filter(district_code_id=request.user.account.associated_with).delete()
					basic_det=Basicinfo.objects.filter(district_id=request.user.account.associated_with)

					
					Number_of_schools_in_block=basic_det.count()
					try:

						for basic_table_record in basic_det:
							tsanc_count=0
							nsanc_count=0
							tvaccant_count=0
							nvaccant_count=0
							tfilled_count=0
							nfilled_count=0
							tfilled_count = Teacher_detail.objects.filter(school_id=basic_table_record.school_id,stafs='Teaching')
							nfilled_count = Teacher_detail.objects.filter(school_id=basic_table_record.school_id,stafs='Non Teaching')
							
							if (Staff.objects.filter(school_key=basic_table_record.id).count())>0:

								teach_det = Staff.objects.filter(school_key=basic_table_record.id,staff_cat=1).values('post_name').annotate(tcount=Sum('post_sanc'))
								for t_count in teach_det:

									tsanc_count=tsanc_count+ t_count.get('tcount')


								nteach_det = Staff.objects.filter(school_key=basic_table_record.id,staff_cat=2).values('post_name').annotate(tcount=Sum('post_sanc'))

								for nt_count in nteach_det:

									nsanc_count=nsanc_count+ nt_count.get('ntcount')
														
							tvaccant_count=int(tsanc_count)-int(tfilled_count.count())
							nvaccant_count=int(nsanc_count)-int(nfilled_count.count())
							
							if tvaccant_count<0:
								tvaccant_count=0
							if nvaccant_count<0:
								nvaccant_count=0
							block_wise_count=block_wise_abstract(school_key=basic_table_record.id,
									district_code_id=basic_table_record.district_id,
									block_code_id=basic_table_record.block_id,
									school_code=basic_table_record.school_id,
									school_name=basic_table_record.school_name,
									tsanctioned_post=tsanc_count,
									tfilled_post=tfilled_count.count(),
									tvaccant_post=tvaccant_count,
									ntsanctioned_post=nsanc_count,
									ntfilled_post=nfilled_count.count(),
									ntvaccant_post=nvaccant_count,
									udise_code=basic_table_record.udise_code,
									flag='Yes',)
							
							block_wise_count.save()

						# block_wise_records=block_wise_abstract.objects.all().order_by('block_code') 	
					

						block_wise_records=block_wise_abstract.objects.filter(district_code_id=request.user.account.associated_with).order_by('block_code')
						
					 	tsanctioned_post_total=0
						tfilled_post_total=0
						tvaccant_post_total=0
						nsanctioned_post_total=0
						nfilled_post_total=0
						nvaccant_post_total=0
						
						for counting in block_wise_records:

							tsanctioned_post_total=tsanctioned_post_total+counting.tsanctioned_post
							tfilled_post_total=tfilled_post_total+counting.tfilled_post
							tvaccant_post_total=tvaccant_post_total+counting.tvaccant_post
							nsanctioned_post_total=nsanctioned_post_total+counting.ntsanctioned_post
							nfilled_post_total=nfilled_post_total+counting.ntfilled_post
							nvaccant_post_total=nvaccant_post_total+counting.ntvaccant_post
							block_name_print=counting.block_code.block_name
						block_wise_count=district_wise_abstract(school_key=basic_table_record.id,
								block_code_id=basic_table_record.block_id,
								district_code_id=basic_table_record.district_id,
								
								tsanctioned_post=tsanctioned_post_total,
								tfilled_post=tfilled_post_total,
								tvaccant_post=tvaccant_post_total,
								ntsanctioned_post=nsanctioned_post_total,
								ntfilled_post=nfilled_post_total,
								ntvaccant_post=nvaccant_post_total,

								flag='Yes',)
						
						block_wise_count.save()
						
						block_wise_records = district_wise_abstract.objects.filter(district_code_id=request.user.account.associated_with).order_by('block_code')

						
						return render(request,'teachers/block/district_detail.html',locals())
					except:
						return HttpResponseRedirect('/')
				
			else:
				if request.user.account.user_category_id == 18:
					
					abstract_page=1
					block_wise_abstract.objects.filter(authenticate_1=request.user).delete()
					
					# Number_of_schools_in_block1 = School.objects.filter(block_id=request.user.account.associated_with)
					# Number_of_schools_in_block=Basicinfo.objects.filter(authenticate_1=request.user).count()
					basic_det=Basicinfo.objects.filter(authenticate_1=request.user)
					Number_of_schools_in_block=basic_det.count()
					for i in basic_det:
						a=i.authenticate_1
						
					

					# try:

					for basic_table_record in basic_det:
						tsanc_count=0
						nsanc_count=0
						tvaccant_count=0
						nvaccant_count=0
						tfilled_count=0
						nfilled_count=0
						tfilled_count = Teacher_detail.objects.filter(school_id=basic_table_record.school_id,stafs=1)
						nfilled_count = Teacher_detail.objects.filter(school_id=basic_table_record.school_id,stafs=2)
						
						if (Staff.objects.filter(school_key=basic_table_record.id).count())>0:

							teach_det = Staff.objects.filter(school_key=basic_table_record.id).filter(staff_cat=1).values('post_name').annotate(tcount=Sum('post_sanc'))
							for t_count in teach_det:

								tsanc_count=tsanc_count+ t_count.get('tcount')
								

							nteach_det = Staff.objects.filter(school_key=basic_table_record.id,staff_cat=2).values('post_name').annotate(ntcount=Sum('post_sanc'))

							for nt_count in nteach_det:

								nsanc_count=nsanc_count+ nt_count.get('ntcount')
													
						tvaccant_count=int(tsanc_count)-int(tfilled_count.count())
						nvaccant_count=int(nsanc_count)-int(nfilled_count.count())
						
						if tvaccant_count<0:
							tvaccant_count=0
						if nvaccant_count<0:
							nvaccant_count=0
						block_wise_count=block_wise_abstract(school_key=basic_table_record.id,
								district_code_id=basic_table_record.district_id,
								block_code_id=basic_table_record.block_id,
								school_code=basic_table_record.school_id,
								school_name=basic_table_record.school_name,
								tsanctioned_post=tsanc_count,
								tfilled_post=tfilled_count.count(),
								tvaccant_post=tvaccant_count,
								ntsanctioned_post=nsanc_count,
								ntfilled_post=nfilled_count.count(),
								ntvaccant_post=nvaccant_count,
								authenticate_1=request.user,
								udise_code=basic_table_record.udise_code,
								flag='Yes',)
						
						block_wise_count.save()

				 	block_wise_records=block_wise_abstract.objects.filter(authenticate_1=request.user)
				 	tsanctioned_post_total=0
					tfilled_post_total=0
					tvaccant_post_total=0
					nsanctioned_post_total=0
					nfilled_post_total=0
					nvaccant_post_total=0
					
					for counting in block_wise_records:

						tsanctioned_post_total=tsanctioned_post_total+counting.tsanctioned_post
						tfilled_post_total=tfilled_post_total+counting.tfilled_post
						tvaccant_post_total=tvaccant_post_total+counting.tvaccant_post
						nsanctioned_post_total=nsanctioned_post_total+counting.ntsanctioned_post
						nfilled_post_total=nfilled_post_total+counting.ntfilled_post
						nvaccant_post_total=nvaccant_post_total+counting.ntvaccant_post
						block_name_print=counting.block_code.block_name
					
				# return HttpResponseRedirect('/')
					return render(request,'teachers/block/block_detail.html',locals())
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
			
		
class district_block_level_list(View):
	#@never_cache
	def get(self,request,**kwargs):
		if request.user.is_authenticated():
			blockid=int(self.kwargs.get('blockid'))
			associateid=int(self.kwargs.get('associateid'))
			block_wise_abstract.objects.filter(block_code=blockid).delete()
				
			
			basic_det=Basicinfo.objects.filter(block_id=blockid)
			Number_of_schools_in_block=basic_det.count()
			try:

				for basic_table_record in basic_det:
					tsanc_count=0
					nsanc_count=0
					tvaccant_count=0
					nvaccant_count=0
					tfilled_count=0
					nfilled_count=0
					tfilled_count = Teacher_detail.objects.filter(school_id=basic_table_record.school_id,stafs='Teaching')
					nfilled_count = Teacher_detail.objects.filter(school_id=basic_table_record.school_id,stafs='Non Teaching')
					
					if (Teachingstaff.objects.filter(school_key=basic_table_record.id).count())>0:
						teach_det = Teachingstaff.objects.filter(school_key=basic_table_record.id).values('tpost_name').annotate(tcount=Sum('tpost_sanc'))
						for t_count in teach_det:

							tsanc_count=tsanc_count+ t_count.get('tcount')

						
					if (NonTeachingstaff.objects.filter(school_key=basic_table_record.id).count())>0:
						nteach_det = NonTeachingstaff.objects.filter(school_key=basic_table_record.id).values('ntpost_name').annotate(ntcount=Sum('ntpost_sanc'))
						for nt_count in nteach_det:

							nsanc_count=nsanc_count+ nt_count.get('ntcount')
						
						
				
						
					
					
					
					tvaccant_count=int(tsanc_count)-int(tfilled_count.count())
					nvaccant_count=int(nsanc_count)-int(nfilled_count.count())
					if nvaccant_count<0:
						nvaccant_count=0
					if tvaccant_count<0:
						tvaccant_count=0
					block_wise_count=block_wise_abstract(school_key=basic_table_record.id,
							district_code_id=basic_table_record.district_id,
							block_code_id=basic_table_record.block_id,
							school_code=basic_table_record.school_id,
							school_name=basic_table_record.school_name,
							tsanctioned_post=tsanc_count,
							tfilled_post=tfilled_count.count(),
							tvaccant_post=tvaccant_count,
							ntsanctioned_post=nsanc_count,
							ntfilled_post=nfilled_count.count(),
							ntvaccant_post=nvaccant_count,
							udise_code=basic_table_record.udise_code,
							flag='Yes',)
					
					block_wise_count.save()
				a=block_wise_abstract.objects.all()
				
			 	block_wise_records=block_wise_abstract.objects.filter(block_code=blockid)
			 	tsanctioned_post_total=0
				tfilled_post_total=0
				tvaccant_post_total=0
				nsanctioned_post_total=0
				nfilled_post_total=0
				nvaccant_post_total=0
				
				for counting in block_wise_records:

					tsanctioned_post_total=tsanctioned_post_total+counting.tsanctioned_post
					tfilled_post_total=tfilled_post_total+counting.tfilled_post
					tvaccant_post_total=tvaccant_post_total+counting.tvaccant_post
					nsanctioned_post_total=nsanctioned_post_total+counting.ntsanctioned_post
					nfilled_post_total=nfilled_post_total+counting.ntfilled_post
					nvaccant_post_total=nvaccant_post_total+counting.ntvaccant_post
				

				return render(request,'teachers/block/block_detail.html',locals())
			except:
				return HttpResponseRedirect('/')
		else:
			return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

		