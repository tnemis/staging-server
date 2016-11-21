from django.db import models
from datetime import datetime
from django.core.validators import MaxLengthValidator
from django.db.models.fields import *
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
import caching.base 
from django.core.validators import MaxValueValidator, MinValueValidator
from smart_selects.db_fields import ChainedForeignKey
from baseapp.models import *


# """
# Model for School Master tables 
# """

# """
# Model for District
# """



class district(caching.base.CachingMixin, models.Model):
    district_code = models.PositiveIntegerField(
        unique=True, validators=[MinValueValidator(3300), MaxValueValidator(3399)])
    district_name = models.CharField(max_length=100)
    objects = caching.base.CachingManager()
    def __unicode__(self):
        return u'%s' % (self.district_name)

# """
# Model for Block
# """

class Block(caching.base.CachingMixin, models.Model):
    block_code = models.PositiveIntegerField(unique=True)
    block_name = models.CharField(max_length=100)
    block_type = models.CharField(max_length=50)
    district = models.ForeignKey('District')
    objects = caching.base.CachingManager()   
    def __unicode__(self):
        return u'%s' % (self.block_name)


# """
# Model for Edn. District Linked with Blocks
# """

class Edn_dist_block(caching.base.CachingMixin, models.Model):
    edn_dist_name = models.CharField(max_length=100)
    edn_dist_id = models.PositiveIntegerField()
    block = models.ForeignKey('Block')
    objects = caching.base.CachingManager()   
    def __unicode__(self):
        return u'%s' % (self.edn_dist_name)


# """
# Model for Edn. District Master
# """

class Edn_dist_mas(caching.base.CachingMixin, models.Model):
    edn_dist_name = models.CharField(max_length=100)
    district = models.ForeignKey('District')
    objects = caching.base.CachingManager()   
    def __unicode__(self):
        return u'%s' % (self.edn_dist_name)


# """
# Model for Local_body
# """
class Local_body(caching.base.CachingMixin, models.Model):
    localbody_name = models.CharField(max_length=25)
    district = models.ForeignKey('District')
    objects = caching.base.CachingManager()
    def __unicode__(self):
        return u'%s' % (self.localbody_name)

class Manage_cate(caching.base.CachingMixin, models.Model):
    manage_name = models.CharField(max_length=100)
    objects = caching.base.CachingManager()
    def __unicode__(self):
        return u'%s' % (self.manage_name)

class Management(caching.base.CachingMixin, models.Model):
	management_code = models.CharField(max_length=100)
	management = models.CharField(max_length=100)
	mana_cate = models.ForeignKey(Manage_cate)
	objects = caching.base.CachingManager()

	def __unicode__(self):
		return u'%s' % (self.management)

class School_department(caching.base.CachingMixin, models.Model):
	department_code = models.CharField(max_length=10)
	department = models.CharField(max_length=100)
	school_mana= models.ForeignKey(Management)
	objects = caching.base.CachingManager()
	def __unicode__(self):
		return u'%s' % (self.department)

class School_category(caching.base.CachingMixin, models.Model):
	category_code = models.CharField(max_length=100)
	category = models.CharField(max_length=100)
	school_dept= models.ForeignKey(School_department)
	objects = caching.base.CachingManager()
	def __unicode__(self):
		return u'%s' % (self.category)

class Part_time_Subjects(models.Model):
	subject_code = models.CharField(max_length=100)
	subject = models.CharField(max_length=100)
	def __unicode__(self):
		return u'%s' % (self.subject)    

class Ict_list(models.Model):
	ict_type = models.CharField(max_length=50)
	def __unicode__(self):
		return u'%s' % (self.ict_type)

class Supplier(models.Model):
	name = models.CharField(max_length=100)
	def __unicode__(self):
		return u'%s ' % (self.name)

class Panchayat(models.Model):
	panchayat = models.CharField(max_length=30)
	def __unicode__(self):
		return u'%s' % (self.panchayat)


class Zone_type(models.Model):
    zone_type = models.CharField(max_length=25)
    def __unicode__(self):
        return u'%s' % (self.zone_type)

class Village_panchayat(caching.base.CachingMixin, models.Model):
    zone_type = models.ForeignKey(Zone_type)
    code = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100)
    block = models.ForeignKey('Block')
    objects = caching.base.CachingManager()
    def __unicode__(self):
        return u'%s' % (self.name)


class Townpanchayat(caching.base.CachingMixin, models.Model):
	zone_type = models.ForeignKey(Zone_type)
	townpanchayat = models.CharField(max_length=100)
	district = models.ForeignKey('District')
	objects = caching.base.CachingManager()
	def __unicode__(self):
		return u'%s' % (self.townpanchayat)

class Municipality(caching.base.CachingMixin, models.Model):
	zone_type = models.ForeignKey(Zone_type)
	municipality = models.CharField(max_length=100)
	district = models.ForeignKey('District')
	objects = caching.base.CachingManager()
	def __unicode__(self):
		return u'%s' % (self.municipality)

class Contonment(caching.base.CachingMixin, models.Model):
	zone_type = models.ForeignKey(Zone_type)
	contonment = models.CharField(max_length=100)
	district = models.ForeignKey('District')
	objects = caching.base.CachingManager()
	def __unicode__(self):
		return u'%s' % (self.contonment)

class Township(caching.base.CachingMixin, models.Model):
	zone_type = models.ForeignKey(Zone_type)
	township = models.CharField(max_length=100)
	district = models.ForeignKey('District')
	objects = caching.base.CachingManager()
	def __unicode__(self):
		return u'%s' % (self.township)

class Corporation(caching.base.CachingMixin, models.Model):
	zone_type = models.ForeignKey(Zone_type)
	corporation = models.CharField(max_length=100)
	district = models.ForeignKey('District')
	objects = caching.base.CachingManager()
	def __unicode__(self):
		return u'%s' % (self.corporation)

class Corporation_zone(caching.base.CachingMixin, models.Model):
	corpn_zone = models.CharField(max_length=100)
	corporation = models.ForeignKey('Corporation')
	objects = caching.base.CachingManager()

	def __unicode__(self):
		return u'%s' % (self.corpn_zone)

class Village_habitation(caching.base.CachingMixin, models.Model):
    name = models.CharField(max_length=100)
    village_panchayat = models.ForeignKey('Village_panchayat')
    objects = caching.base.CachingManager()
    def __unicode__(self):
        return u'%s' % (self.name)

class Town_panchayat_habitation(caching.base.CachingMixin, models.Model):
    name = models.CharField(max_length=100)
    town_panchayat = models.ForeignKey('Townpanchayat')
    objects = caching.base.CachingManager()
    def __unicode__(self):
        return u'%s' % (self.name)

class Municipal_habitation(caching.base.CachingMixin, models.Model):
    name = models.CharField(max_length=100)
    municipal = models.ForeignKey('Municipality')
    objects = caching.base.CachingManager()
    def __unicode__(self):
        return u'%s' % (self.name)

class Contonment_habitation(caching.base.CachingMixin, models.Model):
    name = models.CharField(max_length=100)
    contonment = models.ForeignKey('Contonment')
    objects = caching.base.CachingManager()
    def __unicode__(self):
        return u'%s' % (self.name)

class Township_habitation(caching.base.CachingMixin, models.Model):
    name = models.CharField(max_length=100)
    township = models.ForeignKey('Township')
    objects = caching.base.CachingManager()
    def __unicode__(self):
        return u'%s' % (self.name)

class Corpn_habitation(caching.base.CachingMixin, models.Model):
    name = models.CharField(max_length=100)
    corpn_zone = models.ForeignKey('Corporation_zone')
    objects = caching.base.CachingManager()
    def __unicode__(self):
        return u'%s' % (self.name)        

# """
# Model for Bank Dist. Master
# """


class Bank_district(models.Model):
    district_code = models.PositiveIntegerField(
        unique=True, validators=[MinValueValidator(3300), MaxValueValidator(3399)])
    bank_dist = models.CharField(max_length=100)
    def __unicode__(self):
        return u'%s' % (self.bank_dist)

# """
# Model for Bank Master
# """
class Bank(caching.base.CachingMixin, models.Model):
    bank_dist=models.ForeignKey('Bank_district')
    bankcode = models.CharField(max_length=4)
    bank = models.CharField(max_length=200)
    objects = caching.base.CachingManager()
    def __unicode__(self):
        return u'%s' % (self.bank)

# """
# Model for Bank Branch Master
# """

class Branch(caching.base.CachingMixin, models.Model):
    bank = models.ForeignKey('Bank')
    bank_name= models.CharField(max_length=200)
    branch = models.CharField(max_length=200)
    branch_add=models.CharField(max_length=300)
    contact_no=models.CharField(max_length=20,blank=True,null=True)
    city=models.CharField(max_length=50,blank=True,null=True)
    ifsc_code= models.CharField(max_length=30)
    micr_code=models.CharField(max_length=30)
    objects = caching.base.CachingManager()
    def __unicode__(self):
        return u'%s%s%s' % (self.branch,", IFSC:",self.ifsc_code)   


# """
# Model for Parliamentary Master
# """
class Parliament(caching.base.CachingMixin, models.Model):
	assembly = models.ForeignKey('Assembly')
	parli_name = models.CharField(max_length=200)
	objects = caching.base.CachingManager()
	def __unicode__(self):
		return u'%s' % (self.parli_name)

# """
# Model for Assembly Master
# """

class Assembly(caching.base.CachingMixin, models.Model):
	district = models.ForeignKey('District')
	assembly_name = models.CharField(max_length=200)
	objects = caching.base.CachingManager()
	def __unicode__(self):
		return u'%s' % (self.assembly_name)

# """
# Model for Ward Master
# """

class Ward(models.Model):
	ward = models.CharField(max_length=30)
	def __unicode__(self):
		return u'%s' % (self.ward)

# """
# Model for Groups code for hsc Master
# """

class Groups(caching.base.CachingMixin, models.Model):
    group_code=models.PositiveIntegerField(unique=True)
    group_name = models.CharField(max_length=100)
    subject3 = models.ForeignKey('Subjects', related_name='subject3')
    subject4 = models.ForeignKey('Subjects', related_name='subject4')
    subject5 = models.ForeignKey('Subjects', related_name='subject5')
    subject6 = models.ForeignKey('Subjects', related_name='subject6')
    objects = caching.base.CachingManager()
    def __unicode__(self):
        return u'%s' % (self.group_name)

# """
# Model for Group Subjects Master
# """

class Subjects(models.Model):
	sub_code=models.PositiveIntegerField(unique=True)
	sub_name=models.CharField(max_length=100)

	def __unicode__(self):
		return u'%s %s' % (self.sub_code, self.sub_name)

# """
# Model for Block Level Gis-Lat-Long info Master
# """

class Gis_block_code(models.Model):	
	emis_block_code = models.PositiveIntegerField(unique=True, validators=[MinValueValidator(330000), MaxValueValidator(339999)])
	udise_block_code = models.PositiveIntegerField(unique=True)
	gis_lat = models.DecimalField(blank=True,null=True,max_digits=20, decimal_places=15)
	gis_long = models.DecimalField(blank=True,null=True,max_digits=20, decimal_places=15)
	def __unicode__(self):
		return u'%d %d' % (self.gis_lat,self.gis_long )


# """
# Model for Room Category Master
# """

class Room_cate(models.Model):
	room_cat=models.CharField(max_length=100)
	def __unicode__(self):
		return u'%s' % (self.room_cat,)

# """
# Model for Sports List Master
# """

class Sport_list(models.Model):
	sport_name=models.CharField(max_length=100)
	def __unicode__(self):
		return u'%s' % (self.sport_name,)

# """
# Model for Ict_suppliers List Master
# """

class Ict_suppliers(models.Model):
	supplier_name=models.CharField(max_length=100)
	def __unicode__(self):
		return u'%s' % (self.supplier_name,)

# """
# Model for designations Master
# """		
class User_desig(caching.base.CachingMixin,models.Model):
	user_cate = models.CharField(max_length=20,blank=True,null=True)
	user_desig = models.CharField(max_length=60,blank=True,null=True)
	user_level= models.CharField(max_length=10,blank=True,null=True)
	ser_type = models.CharField(max_length=1,null=True,blank=True)
	objects = caching.base.CachingManager()
	def __unicode__(self):
		return u'%s' % (self.user_desig)


# """
# Model for Designation Subjects Master
# """

class Desig_subjects(caching.base.CachingMixin,models.Model):
	desig_sub_name=models.CharField(max_length=100)
	desig = models.ForeignKey(User_desig)
	objects = caching.base.CachingManager()
	def __unicode__(self):
		return u'%s' % (self.desig_sub_name)



class Cluster_mas(caching.base.CachingMixin, models.Model):

	clus_code = models.BigIntegerField(primary_key=True)
	blk_code = models.ForeignKey('Block')
	clus_name = models.CharField(max_length=100)
	objects = caching.base.CachingManager()
	def __unicode__(self):
		return u'%s' % (self.clus_name,)

# """
# Model for std code for automate entry by  getting udise master file
# """

class Stdcode_mas(models.Model):

	std_code = models.CharField(max_length=10,blank=True,null=True)
	area_name = models.CharField(max_length=50,blank=True,null=True)	
	dist_id = models.BigIntegerField(blank=True)
	def __unicode__(self):
		return u'%s' % (self.std_code,)

# """
# Model for academic year master
# """

class Acadyr_mas(models.Model):

	acad_yr = models.CharField(max_length=10,blank=True,null=True)
	def __unicode__(self):
		return u'%s' % (self.acad_yr,)


# """
# Model for School Profile (child tables)
# """

class Basicinfo(caching.base.CachingMixin, models.Model):
	school_id= models.BigIntegerField(blank=True)
	school_name = models.CharField(max_length=200)
	school_name_tamil = models.CharField(max_length=200,blank=True,null=True,default='')
	udise_code = models.BigIntegerField(blank=True,null=True)
	office_code = models.CharField(max_length=30,blank=True,null=True)
	offcat_id=models.BigIntegerField(blank=True,null=True)
	district = models.ForeignKey(District)
	block = ChainedForeignKey(
		Block, chained_field='district', chained_model_field='district', auto_choose=True)
	local_body_type= ChainedForeignKey(
		Local_body, chained_field='district', chained_model_field='district', auto_choose=True,blank=True,null=True)
	village_panchayat =ChainedForeignKey(
		Village_panchayat, chained_field='block', chained_model_field='block', auto_choose=True,blank=True,null=True)
	vill_habitation = ChainedForeignKey(
		Village_habitation, chained_field='village_panchayat', chained_model_field='village_panchayat', auto_choose=True,blank=True,null=True)
	town_panchayat = ChainedForeignKey(
		Townpanchayat, chained_field='district', chained_model_field='district', auto_choose=True,blank=True,null=True)
	town_panchayat_ward = ChainedForeignKey(
		Town_panchayat_habitation, chained_field='town_panchayat', chained_model_field='town_panchayat',auto_choose=True,blank=True,null=True)
	municipality = ChainedForeignKey(
		Municipality, chained_field='district', chained_model_field='district', auto_choose=True,blank=True,null=True )
	municipal_ward = ChainedForeignKey(
		Municipal_habitation, chained_field='municipality', chained_model_field='municipal', auto_choose=True,blank=True,null=True )
	cantonment = ChainedForeignKey(
		Contonment, chained_field='district', chained_model_field='district', auto_choose=True,blank=True,null=True )
	cantonment_ward = ChainedForeignKey(
		Contonment_habitation, chained_field='contonment', chained_model_field='contonment', auto_choose=True,blank=True,null=True)
	township = ChainedForeignKey(
		Township, chained_field='district', chained_model_field='district', auto_choose=True,blank=True,null=True)
	township_ward = ChainedForeignKey(
	 	Township_habitation, chained_field='township', chained_model_field='township', auto_choose=True,blank=True,null=True)
	corporation = ChainedForeignKey(
		Corporation, chained_field='district', chained_model_field='district', auto_choose=True,blank=True,null=True)	
	corpn_zone = ChainedForeignKey(
		Corporation_zone, chained_field='corporation', chained_model_field='corporation', auto_choose=True,blank=True,null=True)
	corpn_ward = ChainedForeignKey(
		Corpn_habitation, chained_field='corpn_zone', chained_model_field='corpn_zone', auto_choose=True,blank=True,null=True)
	edu_district = ChainedForeignKey(
		Edn_dist_block, chained_field='block', chained_model_field='block', auto_choose=True,blank=True,null=True)

	address  = models.CharField(max_length=200,blank=True,null=True)
	pincode = models.PositiveIntegerField(blank=True,null=True)
	stdcode = models.CharField(max_length=10,blank=True,null=True)
	stdcode= ChainedForeignKey(
		Stdcode_mas, chained_field='district', chained_model_field='dist_id', auto_choose=True,blank=True,null=True)

	landline = models.CharField(max_length=10,blank=True,null=True)
	landline2 = models.CharField(max_length=10,blank=True,null=True)
	mobile = models.CharField(max_length=14,blank=True,null=True)
	sch_email = models.EmailField(blank=True,null=True)
	office_email1 = models.EmailField(blank=True,null=True)
	office_email2 = models.EmailField(blank=True,null=True)	
	website = models.URLField(max_length=200,blank=True,null=True)
	new_build=models.CharField(max_length=30,blank=True,null=True)
	build_status=models.CharField(max_length=30,blank=True,null=True)

	bank_dist=models.ForeignKey(Bank_district,blank=True,null=True)
	bank = ChainedForeignKey(
		Bank, chained_field='bank_dist', chained_model_field='bank_dist', auto_choose=True,blank=True,null=True)
	branch = ChainedForeignKey(
		Branch, chained_field='bank', chained_model_field='bank', auto_choose=True,blank=True,null=True)
	bankaccno=models.CharField(max_length=30,blank=True,null=True)
	parliament = models.ForeignKey(Parliament,blank=True,null=True)
	assembly = ChainedForeignKey(
		Assembly, chained_field='district', chained_model_field='district', auto_choose=True,blank=True,null=True )
	parliament = ChainedForeignKey(
		Parliament, chained_field='assembly', chained_model_field='assembly', auto_choose=True,blank=True,null=True)	
	latitude = models.DecimalField(blank=True,null=True,max_digits=20, decimal_places=15)
	longitude = models.DecimalField(blank=True,null=True,max_digits=20, decimal_places=15)

	manage_cate = models.ForeignKey(Manage_cate,blank=True,null=True)
	sch_management=ChainedForeignKey(
		Management, chained_field='manage_cate', chained_model_field='mana_cate', auto_choose=True,blank=True,null=True)

	sch_directorate=ChainedForeignKey(
		School_department, chained_field='sch_management', chained_model_field='school_mana', auto_choose=True,blank=True,null=True)

	sch_cate=ChainedForeignKey(
		School_category, chained_field='sch_directorate', chained_model_field='school_dept', auto_choose=True,blank=True,null=True)
	draw_off_code= models.CharField(max_length=10,blank=True,null=True)

	pta_esta = models.CharField(max_length=3,blank=True,null=True)
	pta_no= models.CharField(max_length=25,blank=True,null=True)
	pta_sub_yr= models.CharField(max_length=25,blank=True,null=True)
	prekg=models.CharField(max_length=3,blank=True,null=True)
	kgsec=models.CharField(max_length=3,blank=True,null=True)
	cluster =ChainedForeignKey(
		Cluster_mas, chained_field='block', chained_model_field='blk_code', auto_choose=True,blank=True,null=True)
	mgt_opn_year= models.CharField(max_length=25,blank=True,null=True)
	mgt_type=models.CharField(max_length=50,blank=True,null=True)
	mgt_name=models.CharField(max_length=50,blank=True,null=True)
	mgt_address=models.CharField(max_length=250,blank=True,null=True)
	mgt_regis_no= models.CharField(max_length=20,blank=True,null=True)
	mgt_regis_dt= models.DateField(blank=True,null=True)
	regis_by_office= models.CharField(max_length=50,blank=True,null=True)
	district1 = models.BigIntegerField(blank=True,null=True)
	block1 = models.BigIntegerField(blank=True,null=True)
	school_code = models.BigIntegerField(blank=True,null=True)
	habitation_id = models.BigIntegerField(blank=True,null=True)
	management_id = models.BigIntegerField(blank=True,null=True)
	category_id = models.BigIntegerField(blank=True,null=True)
	student_id_count = models.PositiveIntegerField(blank=True,null=True)
	authenticate_1 = models.CharField(max_length=30,blank=True,null=True)
	authenticate_2 = models.CharField(max_length=30,blank=True,null=True)
	authenticate_3 = models.CharField(max_length=30,blank=True,null=True)
	chk_dept = models.IntegerField(blank=True,null=True)
	chk_manage = models.IntegerField(blank=True,null=True)
	curr_stat = models.IntegerField(blank=True,null=True)
	created_date = models.DateTimeField(auto_now_add=True, editable=False)
	modified_date = models.DateTimeField(auto_now=True)
	objects = caching.base.CachingManager()
	def __unicode__(self):
		return u'%s %d %s %s %s %s' % (self.school_name, self.udise_code, self.district, self.edu_district, self.block,self.manage_cate,)




class Academicinfo(caching.base.CachingMixin, models.Model):
	school_key = models.ForeignKey(Basicinfo)
	schooltype = models.CharField(max_length=10,blank=True,null=True)
	board = models.CharField(max_length= 30,blank=True,null=True)
	tamil_med = models.BooleanField(default=False,blank=True)
	eng_med = models.BooleanField(default=False,blank=True)
	tel_med = models.BooleanField(default=False,blank=True)
	mal_med = models.BooleanField(default=False,blank=True)
	kan_med = models.BooleanField(default=False,blank=True)
	urdu_med = models.BooleanField(default=False,blank=True)
	oth_med = models.BooleanField(default=False,blank=True)
	other_med = models.CharField(max_length= 50,blank=True,null=True)
	noof_med= models.BigIntegerField(default=0,blank=True,null=True)
	minority = models.BooleanField(default=False,blank=True)
	rel_minority = models.BooleanField(default=False,blank=True)
	ling_minority = models.BooleanField(default=False,blank=True)
	min_ord_no = models.CharField(max_length=50,blank=True,null=True)
	min_dt_iss = models.DateField(blank=True,null=True)
	iss_auth = models.CharField(max_length=50,blank=True,null=True)
	start_order = models.CharField(max_length= 200,blank=True,null=True)
	start_yr = models.CharField(max_length= 10,blank=True,null=True)
	recog_typ = models.CharField(max_length= 12,blank=True,null=True)
	recog_ord = models.CharField(max_length= 200,blank=True,null=True)
	recog_dt_fm = models.DateField(blank=True,null=True)
	recog_dt_to = models.DateField(blank=True,null=True)
	hssstart_order = models.CharField(max_length= 200,blank=True,null=True)
	hssstart_yr = models.CharField(max_length= 10,blank=True,null=True)
	hssrecog_typ = models.CharField(max_length= 12,blank=True,null=True)
	hssrecog_ord = models.CharField(max_length= 200,blank=True,null=True)
	hssrecog_dt_fm = models.DateField(blank=True,null=True)
	hssrecog_dt_to = models.DateField(blank=True,null=True)	
	upgr_det = models.CharField(max_length= 200,blank=True,null=True)
	other_board_aff=models.CharField(max_length= 200,blank=True,null=True)
	hssboard=models.CharField(max_length= 30,blank=True,null=True)
	spl_school = models.BooleanField(default=False,blank=True)
	spl_type = models.CharField(max_length= 50,blank=True,null=True)
	boarding = models.BooleanField(default = False,blank=True)
	hostel_floor = models.BigIntegerField(default=0,null=True,blank=True)
	hostel_rooms = models.BigIntegerField(default=0,null=True,blank=True)
	hostel_boys = models.BigIntegerField(default=0,null=True,blank=True)
	hostel_girls = models.BigIntegerField(default=0,null=True,blank=True)
	hostel_staff = models.BigIntegerField(default=0,null=True,blank=True)
	low_class = models.CharField(max_length=10)
	high_class =  models.CharField(max_length=10)
	nrstc=models.BooleanField(default=False,blank=True)	
	extra_scout=models.CharField(max_length=35,null=True,blank=True)
	extra_jrc=models.CharField(max_length=15,null=True,blank=True)
	extra_nss=models.CharField(max_length=15,null=True,blank=True)
	extra_ncc=models.CharField(max_length=15,null=True,blank=True)
	extra_rrc=models.CharField(max_length=15,null=True,blank=True)
	extra_ec=models.CharField(max_length=15,null=True,blank=True)
	extra_cub=models.CharField(max_length=15,null=True,blank=True)
	smc_smdc = models.CharField(max_length=3,blank=True,null=True)
	dge_no_ten= models.CharField(max_length=15,blank=True,null=True)
	dge_no_twelve= models.CharField(max_length=15,blank=True,null=True)
	created_date = models.DateTimeField(auto_now_add=True, editable=False)
	modified_date = models.DateTimeField(auto_now=True)
	
	objects = caching.base.CachingManager()
	def __unicode__(self):
		return u'%s %s %s %s %s %s %s' % (self.school_key, self.board, self.schooltype,self.modified_date,self.recog_dt_fm,self.recog_dt_to,self.min_dt_iss)

class User_map(models.Model):
	school_code = models.BigIntegerField(blank=True,null=True)
	user_name = models.CharField(max_length=30)


class Man_chk(models.Model):
	school_code = models.BigIntegerField(blank=True,null=True)
	manage_cat = models.IntegerField(blank=True,null=True)

class dept_tem(models.Model):
	school_code = models.BigIntegerField(blank=True,null=True)
	dept = models.IntegerField(blank=True,null=True)
	manage = models.IntegerField(blank=True,null=True)

# class Bapptem(models.Model):
# 	school_code = models.BigIntegerField(blank=True,null=True)
# 	school_name = models.CharField(max_length=100)
# 	district = models.BigIntegerField(blank=True,null=True)
# 	block = models.BigIntegerField(blank=True,null=True)
# 	#block = models.ForeignKey('Block')
# 	habitation = models.BigIntegerField(blank=True,null=True)
# 	management = models.BigIntegerField(blank=True,null=True)
# 	category = models.BigIntegerField(blank=True,null=True)
# 	student_id_count = models.PositiveIntegerField(blank=True,null=True)
# 	created_date = models.DateTimeField(auto_now_add=True, editable=False)
# 	modified_date = models.DateTimeField(auto_now=True)

# Models for Class Section details - Student strength

class Class_section(caching.base.CachingMixin, models.Model):
	school_key = models.ForeignKey(Basicinfo)
	class_id = models.CharField(max_length=10,blank=True,null=True)
	sections = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)])
	no_sec_aided=models.PositiveIntegerField(default=0,blank=True,null=True)
	tam_stud=models.PositiveIntegerField(default=0,blank=True,null=True)
	eng_stud=models.PositiveIntegerField(default=0,blank=True,null=True)
	oth_stud=models.PositiveIntegerField(default=0,blank=True,null=True)
	no_stud=models.PositiveIntegerField(default=0,blank=True,null=True)
	cwsn_stud_no=models.PositiveIntegerField(default=0,blank=True,null=True)
	modified_date = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return u'%s %s %s %s %s %s' % (self.id,self.school_key, self.class_id,self.sections,self.no_sec_aided,self.no_stud)


class Staff(caching.base.CachingMixin, models.Model):
	school_key = models.ForeignKey(Basicinfo)
	post_name = models.ForeignKey(User_desig)
	post_sub = ChainedForeignKey(
		Desig_subjects, chained_field='post_name', chained_model_field='desig', auto_choose=True)
	post_sanc = models.BigIntegerField(blank=True,null=True)
	post_mode = models.CharField(max_length=9,blank=True,null=True)
	post_GO = models.CharField(max_length= 30,blank=True,null=True)
	post_GO_dt = models.DateField(blank=True,null=True)
	temgofm_dt = models.DateField(blank=True,null=True)
	temgoto_dt = models.DateField(blank=True,null=True)	
	post_GO_pd = models.CharField(max_length=200,null=True,blank=True)
	post_filled = models.BigIntegerField(blank=True,null=True)
	post_vac = models.BigIntegerField(blank=True,null=True)
	staff_cat = models.PositiveIntegerField(blank=True,null=True)
	modified_date = models.DateTimeField(auto_now=True)		
	objects = caching.base.CachingManager()
	def __unicode__(self):
		return u'%s %s %s' % (self.school_key, self.post_name,self.post_GO_dt)


class Parttimestaff(caching.base.CachingMixin, models.Model):
	school_key = models.ForeignKey(Basicinfo)
	part_instr = models.CharField(max_length=70,blank=True,null=True)
	part_instr_sub = models.CharField(max_length=50,blank=True,null=True)
	doa=models.DateField(blank=True,null=True)
	objects = caching.base.CachingManager()
	modified_date = models.DateTimeField(auto_now=True)		
	def __unicode__(self):
		return u'%s %s' % (self.school_key,self.part_instr)





class Infradet(caching.base.CachingMixin, models.Model):
	school_key = models.ForeignKey(Basicinfo)
	electricity = models.CharField(max_length=10,null=True,blank=True)
	tot_area= models.BigIntegerField(blank=True, null=True,default=0)
	tot_type=models.CharField(max_length=15,null=True,blank=True)
	tot_ft = models.BigIntegerField(blank=True, null=True,default=0)
	tot_mt = models.BigIntegerField(blank=True, null=True,default=0)
	cov= models.BigIntegerField(blank=True, null=True,default=0)
	cov_type=models.CharField(max_length=15,null=True,blank=True)
	covered_ft = models.BigIntegerField(blank=True, null=True,default=0)
	covered_mt = models.BigIntegerField(blank=True, null=True,default=0)
	opn= models.BigIntegerField(blank=True, null=True,default=0)
	opn_type=models.CharField(max_length=15,null=True,blank=True)
	open_ft = models.BigIntegerField(blank=True, null=True,default=0)
	open_mt = models.BigIntegerField(blank=True, null=True,default=0)
	play= models.BigIntegerField(blank=True, null=True,default=0)
	play_type=models.CharField(max_length=15,null=True,blank=True)
	play_ft = models.BigIntegerField(blank=True, null=True,default=0)
	play_mt = models.BigIntegerField(blank=True, null=True,default=0)	
	cwall = models.BooleanField(default=False,blank=True)
	cwall_concre = models.BooleanField(default=False,blank=True)
	cwall_fence = models.BooleanField(default=False,blank=True)
	cwall_existbu = models.BooleanField(default=False,blank=True)
	cwall_nbarr = models.BooleanField(default=False,blank=True)
	cwall_concre_len = models.BigIntegerField(null=True,blank=True,default=0)
	cwall_fence_len = models.BigIntegerField(null=True,blank=True,default=0)
	cwall_existbu_len = models.BigIntegerField(null=True,blank=True,default=0)
	cwall_nbarr_len = models.BigIntegerField(null=True,blank=True,default=0)
	cwall_notcon_len = models.BigIntegerField(null=True,blank=True,default=0)
	fireext= models.BooleanField(default=False,blank=True)
	fireext_no = models.PositiveIntegerField(null=True,blank=True)
	fireext_w = models.PositiveIntegerField(null=True,blank=True)
	firstaid_box= models.CharField(max_length=10,null=True,blank=True)
	rainwater = models.CharField(max_length=10,null=True,blank=True)
	kitchenshed= models.CharField(max_length=10,null=True,blank=True)
	furn_desk_no = models.PositiveIntegerField(null=True,blank=True,default=0)
	furn_desk_use = models.PositiveIntegerField(null=True,blank=True,default=0)
	furn_bench_no = models.PositiveIntegerField(null=True,blank=True,default=0)
	furn_bench_use = models.PositiveIntegerField(null=True,blank=True,default=0)
	fans = models.BigIntegerField(null=True,blank=True)
	fans_work = models.BigIntegerField(null=True,blank=True)
	tubelights = models.BigIntegerField(null=True,blank=True)
	tlights_work = models.BigIntegerField(null=True,blank=True)
	bu_no = models.BigIntegerField(null=True,blank=True,default=0)
	bu_usable = models.BigIntegerField(null=True,blank=True,default=0)
	bu_minrep = models.BigIntegerField(null=True,blank=True,default=0)
	bu_majrep = models.BigIntegerField(null=True,blank=True,default=0)
	gu_no = models.BigIntegerField(null=True,blank=True,default=0)
	gu_usable = models.BigIntegerField(null=True,blank=True,default=0)
	gu_minrep = models.BigIntegerField(null=True,blank=True,default=0)
	gu_majrep = models.BigIntegerField(null=True,blank=True,default=0)
	bl_no = models.BigIntegerField(null=True,blank=True,default=0)
	bl_usable = models.BigIntegerField(null=True,blank=True,default=0)
	bl_minrep = models.BigIntegerField(null=True,blank=True,default=0)
	bl_majrep = models.BigIntegerField(null=True,blank=True,default=0)
	gl_no = models.BigIntegerField(null=True,blank=True,default=0)
	gl_usable = models.BigIntegerField(null=True,blank=True,default=0)
	gl_minrep = models.BigIntegerField(null=True,blank=True,default=0)
	gl_majrep = models.BigIntegerField(null=True,blank=True,default=0)
	gentsu_no = models.BigIntegerField(null=True,blank=True,default=0)
	gentsu_usable = models.BigIntegerField(null=True,blank=True,default=0)
	gentsu_minrep = models.BigIntegerField(null=True,blank=True,default=0)
	gentsu_majrep = models.BigIntegerField(null=True,blank=True,default=0)
	ladiesu_no = models.BigIntegerField(null=True,blank=True,default=0)
	ladiesu_usable = models.BigIntegerField(null=True,blank=True,default=0)
	ladiesu_minrep = models.BigIntegerField(null=True,blank=True,default=0)
	ladiesu_majrep = models.BigIntegerField(null=True,blank=True,default=0)
	gentsl_no = models.BigIntegerField(null=True,blank=True,default=0)
	gentsl_usable = models.BigIntegerField(null=True,blank=True,default=0)
	gentsl_minrep = models.BigIntegerField(null=True,blank=True,default=0)
	gentsl_majrep = models.BigIntegerField(null=True,blank=True,default=0)
	ladiesl_no = models.BigIntegerField(null=True,blank=True,default=0)
	ladiesl_usable = models.BigIntegerField(null=True,blank=True,default=0)
	ladiesl_minrep = models.BigIntegerField(null=True,blank=True,default=0)
	ladiesl_majrep = models.BigIntegerField(null=True,blank=True,default=0)
	incinirator=models.CharField(max_length=10,null=True,blank=True)
	water_toilet = models.BooleanField(default=False,blank=True)
	cwsn_toilet = models.BooleanField(default=False,blank=True)
	cwsn_toilet_no = models.BigIntegerField(null=True,blank=True,default=0)
	water_facility=models.CharField(max_length=10,null=True,blank=True)
	water_source=models.CharField(max_length=50,null=True,blank=True)
	well_dia=models.BigIntegerField(null=True,blank=True,default=0)
	well_close=models.CharField(max_length=15,null=True,blank=True)
	water_puri=models.CharField(max_length=15,null=True,blank=True)
	water_access  = models.CharField(max_length=35,null=True,blank=True)
	internet_yes = models.BooleanField(default=False,blank=True)
	lightning_arest = models.CharField(max_length=10,null=True,blank=True)
	lib_tamil = models.BigIntegerField(null=True,blank=True)
	lib_eng = models.BigIntegerField(null=True,blank=True)
	lib_others = models.BigIntegerField(null=True,blank=True)
	lib_tamil_news = models.BigIntegerField(null=True,blank=True)
	lib_eng_news = models.BigIntegerField(null=True,blank=True)
	lib_periodic = models.BigIntegerField(null=True,blank=True)
	trans_faci=models.BooleanField(default=False,blank=True)
	trans_bus=models.BigIntegerField(null=True,blank=True)
	trans_van=models.BigIntegerField(null=True,blank=True)
	trans_stud=models.BigIntegerField(null=True,blank=True)
	trans_rules=models.BooleanField(default=False,blank=True)
	award_recd=models.BooleanField(default=False,blank=True)
	award_info = models.CharField(max_length=100,null=True,blank=True)
	phy_lab=models.BigIntegerField(null=True,blank=True)
	che_lab=models.BigIntegerField(null=True,blank=True)
	bot_lab=models.BigIntegerField(null=True,blank=True)
	zoo_lab=models.BigIntegerField(null=True,blank=True)
	gas_cylin=models.BooleanField(default=False,blank=True)
	suffi_equip=models.BooleanField(default=False,blank=True)
	eb_ht_line=models.BooleanField(default=False,blank=True)
	created_date = models.DateTimeField(auto_now_add=True, editable=False)
	modified_date = models.DateTimeField(auto_now=True)	
	objects = caching.base.CachingManager()

	def __unicode__(self):
		return u'%s %s' % (self.school_key,self.cwall_type)

class Land(caching.base.CachingMixin, models.Model):
	school_key = models.ForeignKey(Basicinfo)
	name = models.CharField(max_length=100,blank=True,null=True)
	own_type= models.CharField(max_length=25,blank=True,null=True)
	lease_yrs=models.BigIntegerField(blank=True, null=True,default=0)
	lease_name=models.CharField(max_length=15,blank=True,null=True)
	tot_area=models.BigIntegerField(blank=True, null=True,default=0)
	area_mes_type = models.CharField(max_length=8,blank=True,null=True)
	area_ground = models.BigIntegerField(blank=True, null=True,default=0)
	area_cent = models.BigIntegerField(blank=True, null=True,default=0)
	patta_no = models.CharField(max_length=50,blank=True,null=True)
	survey_no = models.CharField(max_length=50,null=True,blank=True)
	subdiv_no = models.CharField(max_length=50,null=True,blank=True)
	land_type=	models.CharField(max_length=50,null=True,blank=True)
	doc_no=models.CharField(max_length=50,null=True,blank=True)
	doc_regn_dt=models.DateField(blank=True,null=True)
	place_regn=models.CharField(max_length=50,null=True,blank=True)
	ec_cer_no=models.CharField(max_length=20,blank=True,null=True)
	ec_cer_dt=models.DateField(blank=True,null=True)
	ec_cer_fm=models.DateField(blank=True,null=True)
	ec_cer_to=models.DateField(blank=True,null=True)
	ec_period=models.BigIntegerField(blank=True, null=True,default=0)
	modified_date = models.DateTimeField(auto_now=True)		
	objects = caching.base.CachingManager()
	def __unicode__(self):
		return u'%s %s' % (self.school_key, self.name)



class Building(caching.base.CachingMixin, models.Model):
	school_key = models.ForeignKey(Basicinfo)
	room_cat = models.CharField(max_length=50,null=True,blank=True)
	room_count = models.BigIntegerField(null=True,blank=True,default=0)
	roof_type = models.CharField(max_length=50,null=True,blank=True)
	builtup_area = models.BigIntegerField(blank=True, null=True,default=0)
	modified_date = models.DateTimeField(auto_now=True)		
	objects = caching.base.CachingManager()

	def __unicode__(self):
		return u'%s %s' % (self.school_key, self.status)

class Building_abs(caching.base.CachingMixin, models.Model):
	school_key = models.ForeignKey(Basicinfo)
	building_name = models.CharField(max_length=50,null=True,blank=True)
	build_cons_yr = models.CharField(max_length=10,null=True,blank=True)
	no_of_floors= models.BigIntegerField(null=True,blank=True,default=0)
	stair_case_no= models.BigIntegerField(null=True,blank=True,default=0)
	stair_case_width= models.BigIntegerField(null=True,blank=True)
	building_funded = models.CharField(max_length=50,null=True)
	donor_name=models.CharField(max_length=100,null=True,blank=True)
	nabard_phase=models.CharField(max_length=10,null=True,blank=True)
	plan_approval=models.CharField(max_length=10,null=True,blank=True)
	stab_cer_no = models.CharField(max_length=20,null=True,blank=True)
	stab_cer_dt = models.DateField(blank=True,null=True)
	stab_fm_dt=models.DateField(blank=True,null=True)
	stab_to_dt=models.DateField(blank=True,null=True)
	stab_iss_auth=models.CharField(max_length=100,null=True,blank=True)
	no_stud=models.BigIntegerField(null=True,blank=True)
	lic_cer_no=models.CharField(max_length=20,null=True,blank=True)	
	lic_cer_dt=models.DateField(blank=True,null=True)
	lic_iss_auth=models.CharField(max_length=100,null=True,blank=True)
	san_cer_no=models.CharField(max_length=20,null=True,blank=True)	
	san_cer_dt=models.DateField(blank=True,null=True)
	san_iss_auth=models.CharField(max_length=100,null=True,blank=True)
	fire_cer_no=models.CharField(max_length=20,null=True,blank=True)
	fire_cer_dt=models.DateField(blank=True,null=True)
	fire_iss_auth=models.CharField(max_length=100,null=True,blank=True)	
	build_pres_cond = models.CharField(max_length=40,null=True,blank=True)
	modified_date = models.DateTimeField(auto_now=True)		
	objects = caching.base.CachingManager()

	def __unicode__(self):
		return u'%s %s %s' % (self.school_key, self.building_sno, self.building_name)
	
class Sports(caching.base.CachingMixin, models.Model):
	school_key = models.ForeignKey(Basicinfo)
	sports_name = models.CharField(max_length=100,null=True,blank=True)
	play_ground = models.CharField(max_length=50,null=True,blank=True)
	sports_equip= models.CharField(max_length=50,null=True,blank=True)
	sports_no_sets = models.CharField(max_length=100,null=True,blank=True)
	modified_date = models.DateTimeField(auto_now=True)		
	objects = caching.base.CachingManager()
	def __unicode__(self):
		return u'%s %s' % (self.school_key,self.sports_name)

class Ictentry(caching.base.CachingMixin, models.Model):
	school_key = models.ForeignKey(Basicinfo)
	ict_type = models.CharField(max_length=100,null=True,blank=True)
	working_no = models.BigIntegerField(null= True,blank=True)
	not_working_no = models.BigIntegerField(null=True,blank=True,default=0)
	supplied_by = models.CharField(max_length=100,null=True,blank=True)
	donor_ict = models.CharField(max_length=100,null=True,blank=True)
	modified_date = models.DateTimeField(auto_now=True)		
	objects = caching.base.CachingManager()

	def __unicode__(self):
		return u'%s %s' % (self.school_key,self.item_type)

class Sch_groups (caching.base.CachingMixin, models.Model):
	school_key = models.ForeignKey(Basicinfo)
	group_name = models.CharField(max_length=100)
	sec_in_group = models.PositiveIntegerField()
	sec_in_group_aid=models.PositiveIntegerField(blank=True,null=True)
	permis_ordno = models.CharField(max_length=50)
	permis_orddt = models.DateField(blank=True,null=True)
	modified_date = models.DateTimeField(auto_now=True)		
	objects = caching.base.CachingManager()

	def __unicode__(self):
		return u'%s' % (self.group_name )



# """
# Model for pass percent
# """

class Passpercent(models.Model):
	school_key = models.ForeignKey(Basicinfo)
	acad_yr = models.CharField(max_length=10,blank=True,null=True)
	ten_b_app =  models.PositiveIntegerField(default=0,null= True,blank=True)
	ten_b_pass =  models.PositiveIntegerField(default=0,null= True,blank=True)
	ten_g_app =  models.PositiveIntegerField(default=0,null= True,blank=True)
	ten_g_pass =  models.PositiveIntegerField(default=0,null= True,blank=True)
	ten_app =  models.PositiveIntegerField(default=0,null= True,blank=True)
	ten_pass =  models.PositiveIntegerField(default=0,null= True,blank=True)
	twelve_b_app =  models.PositiveIntegerField(default=0,null= True,blank=True)
	twelve_b_pass =  models.PositiveIntegerField(default=0,null= True,blank=True)	
	twelve_g_app =  models.PositiveIntegerField(default=0,null= True,blank=True)
	twelve_g_pass =  models.PositiveIntegerField(default=0,null= True,blank=True)
	twelve_app =  models.PositiveIntegerField(default=0,null= True,blank=True)
	twelve_pass =  models.PositiveIntegerField(default=0,null= True,blank=True)
	ten_b_per=models.DecimalField(default=0,max_digits=6,decimal_places=2,blank=True,null=True)
	ten_g_per=models.DecimalField(default=0,max_digits=6,decimal_places=2,blank=True,null=True)
	ten_a_per=models.DecimalField(default=0,max_digits=6,decimal_places=2,blank=True,null=True)
	twelve_b_per=models.DecimalField(default=0,max_digits=6,decimal_places=2,blank=True,null=True)
	twelve_g_per=models.DecimalField(default=0,max_digits=6,decimal_places=2,blank=True,null=True)
	twelve_a_per=models.DecimalField(default=0,max_digits=6,decimal_places=2,blank=True,null=True)
	def __unicode__(self):
		return u'%s%s%s' % (self.acad_yr,self.ten_a_per,self.twelve_a_per)



# """
# Model for School Profile (child tables)
# """

# class Office_info(caching.base.CachingMixin, models.Model):
# 	user_id=models.BigIntegerField()
# 	offcat_id=models.BigIntegerField()
# 	office_name = models.CharField(max_length=200)
# 	office_name_tamil = models.CharField(max_length=200,blank=True,null=True)
# 	district = models.ForeignKey(District)
# 	block = ChainedForeignKey(Block, chained_field='district', chained_model_field='district', auto_choose=True)
# 	local_body_type= ChainedForeignKey(Local_body, chained_field='district', chained_model_field='district', auto_choose=True,blank=True,null=True)
# 	village_panchayat =ChainedForeignKey(Village_panchayat, chained_field='block', chained_model_field='block', auto_choose=True,blank=True,null=True)
# 	vill_habitation = ChainedForeignKey(Village_habitation, chained_field='village_panchayat', chained_model_field='village_panchayat', auto_choose=True,blank=True,null=True)
# 	town_panchayat = ChainedForeignKey(Townpanchayat, chained_field='district', chained_model_field='district', auto_choose=True,blank=True,null=True)
# 	town_panchayat_ward = ChainedForeignKey(
# 		Town_panchayat_habitation, chained_field='town_panchayat', chained_model_field='town_panchayat',auto_choose=True,blank=True,null=True)
# 	municipality = ChainedForeignKey(
# 		Municipality, chained_field='district', chained_model_field='district', auto_choose=True,blank=True,null=True )
# 	municipal_ward = ChainedForeignKey(
# 		Municipal_habitation, chained_field='municipality', chained_model_field='municipal', auto_choose=True,blank=True,null=True )
# 	cantonment = ChainedForeignKey(
# 		Contonment, chained_field='district', chained_model_field='district', auto_choose=True,blank=True,null=True )
# 	cantonment_ward = ChainedForeignKey(
# 		Contonment_habitation, chained_field='contonment', chained_model_field='contonment', auto_choose=True,blank=True,null=True)
# 	township = ChainedForeignKey(
# 		Township, chained_field='district', chained_model_field='district', auto_choose=True,blank=True,null=True)
# 	township_ward = ChainedForeignKey(
# 	 	Township_habitation, chained_field='township', chained_model_field='township', auto_choose=True,blank=True,null=True)
# 	corporation = ChainedForeignKey(
# 		Corporation, chained_field='district', chained_model_field='district', auto_choose=True,blank=True,null=True)	
# 	corpn_zone = ChainedForeignKey(
# 		Corporation_zone, chained_field='corporation', chained_model_field='corporation', auto_choose=True,blank=True,null=True)
# 	corpn_ward = ChainedForeignKey(
# 		Corpn_habitation, chained_field='corpn_zone', chained_model_field='corpn_zone', auto_choose=True,blank=True,null=True)
# 	address  = models.CharField(max_length=200,blank=True,null=True)
# 	pincode = models.PositiveIntegerField(blank=True,null=True)
# 	stdcode = models.CharField(max_length=10,blank=True,null=True)
# 	landline = models.CharField(max_length=10,blank=True,null=True)
# 	landline2 = models.CharField(max_length=10,blank=True,null=True)
# 	mobile = models.CharField(max_length=13,blank=True,null=True)
# 	office_email1 = models.EmailField(blank=True,null=True)
# 	office_email2 = models.EmailField(blank=True,null=True)
# 	website = models.URLField(max_length=200,blank=True,null=True)
# 	new_build=models.CharField(max_length=30,blank=True,null=True)
# 	build_status=models.CharField(max_length=30,blank=True,null=True)
# 	bank_dist=models.ForeignKey(Bank_district,blank=True,null=True)
# 	bank = ChainedForeignKey(
# 		Bank, chained_field='bank_dist', chained_model_field='bank_dist', auto_choose=True,blank=True,null=True)
# 	branch = ChainedForeignKey(
# 		Branch, chained_field='bank', chained_model_field='bank', auto_choose=True,blank=True,null=True)
# 	bankaccno=models.CharField(max_length=30,blank=True,null=True)
# 	parliament = models.ForeignKey(Parliament,blank=True,null=True)
# 	assembly = ChainedForeignKey(
# 		Assembly, chained_field='district', chained_model_field='district', auto_choose=True,blank=True,null=True )
# 	parliament = ChainedForeignKey(
# 		Parliament, chained_field='assembly', chained_model_field='assembly', auto_choose=True,blank=True,null=True)	
# 	created_date = models.DateTimeField(auto_now_add=True, editable=False)
# 	modified_date = models.DateTimeField(auto_now=True)
# 	objects = caching.base.CachingManager()
# 	def __unicode__(self):
# 		return u'%s %s' % (self.office_name, self.district,)


# class Office_ict(caching.base.CachingMixin, models.Model):
# 	office_key = models.ForeignKey(Office_info)
# 	ict_type = models.CharField(max_length=100,null=True,blank=True)
# 	working_no = models.BigIntegerField(null= True,blank=True)
# 	not_working_no = models.BigIntegerField(null=True,blank=True,default=0)
# 	supplied_by = models.CharField(max_length=100,null=True,blank=True)
# 	modified_date = models.DateTimeField(auto_now=True)		
# 	objects = caching.base.CachingManager()

# 	def __unicode__(self):
# 		return u'%s %s' % (self.office_key,self.item_type)

# class Off_ntstaff(caching.base.CachingMixin, models.Model):
# 	office_key = models.ForeignKey(Office_info)
# 	NTpost_name = models.CharField(max_length= 60,null=True,blank=True)
# 	NTpost_sanc = models.BigIntegerField(null=True,blank=True)
# 	NTpost_mode = models.CharField(max_length=9,null=True,blank=True)
# 	NTpost_GO = models.CharField(max_length= 30,blank=True,null=True)
# 	NTpost_GO_dt = models.DateField(blank=True,null=True)
# 	NTtemgofm_dt = models.DateField(blank=True,null=True)
# 	NTtemgoto_dt = models.DateField(blank=True,null=True)
# 	NTpost_GO_pd = models.CharField(max_length=200,null=True,blank=True)
# 	modified_date = models.DateTimeField(auto_now=True)		
# 	objects = caching.base.CachingManager()
# 	def __unicode__(self):
# 		return u'%s %s' % (self.office_key,self.NTpost_name)


# """ Model for School Management Info """

# class school_management(models.Model):
#     schoolid= models.ForeignKey(UserProfile)
#     opening_year= models.PositiveIntegerField()
#     management_type=models.CharField(max_length=50)
#     management_name=models.CharField(max_length=50)
#     management_address=models.CharField(max_length=250)
#     management_regis_number= models.CharField(max_length=20)
#     management_regis_date= models.DateField()
#     registered_by_office= models.CharField(max_length=40)
#     management_regis_validity= models.DateField()
#     process_which = models.PositiveIntegerField()
#     created_date = models.DateTimeField(auto_now_add=True)
#     modified_date = models.DateTimeField(auto_now=True)

#     def __unicode__(self):
#         return u'%s %s' % (self.opening_date,self.management_name)		