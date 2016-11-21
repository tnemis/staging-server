from django.db import models
from django.db.models.fields import *
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
import caching.base
from baseapp.models import *
from schoolnew.models import *
from django.core.validators import MaxValueValidator, MinValueValidator



"""
Model for Religion (Teachers)
"""

class T_Religion(models.Model):
   religion_name = models.CharField(max_length=100)

   def __unicode__(self):
       return u'%s' % (self.religion_name)




"""
Model for Community (Teachers)
"""


class T_Community(models.Model):
   community_code = models.CharField(max_length=100)
   community_name = models.CharField(max_length=100)
   religion = models.ForeignKey('T_Religion')
   def __unicode__(self):
       return u'%s' % (self.community_name)

"""
Model for Sub Castes (Teachers)
"""


class T_Sub_Castes(models.Model):
   caste_code = models.CharField(max_length=10)
   caste_name = models.CharField(max_length=1000)
   community = models.ForeignKey('T_Community')

   def __unicode__(self):
       return u'%s %s %s' % (self.caste_name,self.caste_code, self.community.community_name)

"""
Models for Teacher Posting Type
"""
class Posting_type(models.Model):
    posting_name= models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s' % (self.posting_name)


class Teacher_pay_officer(models.Model):
    designation_code = models.CharField(max_length=10)
    designation_name = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % (self.designation_name)


class Count_id(models.Model):
    count_stand=models.PositiveIntegerField()

    def __unicode__(self):
        return u'%d' %(self.count_stand)

class count_DSE_Teaching(models.Model):
    count_DSE_Teaching=models.PositiveIntegerField()

    def __unicode__(self):
        return u'%d' %(self.count_DSE_Teaching)


class count_DSE_Non_Teaching(models.Model):
    count_DSE_Non_Teaching=models.PositiveIntegerField()

    def __unicode__(self):
        return u'%d' %(self.count_DSE_Non_Teaching)


class count_DEE_Teaching(models.Model):
    count_DEE_Teaching=models.PositiveIntegerField()

    def __unicode__(self):
        return u'%d' %(self.count_DEE_Teaching)



class staff_count(models.Model):
    dse_teaching=models.PositiveIntegerField()
    dse_non_teaching=models.PositiveIntegerField()
    dee_teaching=models.PositiveIntegerField()
    dee_non_teaching=models.PositiveIntegerField()


class Present_District(caching.base.CachingMixin, models.Model):
    district_code = models.PositiveIntegerField(
        unique=True, validators=[MinValueValidator(3300), MaxValueValidator(3399)])
    district_name = models.CharField(max_length=100)
    objects = caching.base.CachingManager()
    
    def __unicode__(self):
        return u'%s' % (self.district_name)

class Permanent_District(caching.base.CachingMixin, models.Model):
    district_code = models.PositiveIntegerField(
        unique=True, validators=[MinValueValidator(3300), MaxValueValidator(3399)])
    district_name = models.CharField(max_length=100)
    objects = caching.base.CachingManager()
    
    def __unicode__(self):
        return u'%s' % (self.district_name)


class Teacher_detail(caching.base.CachingMixin, models.Model):
    count=models.BigIntegerField()
    school_id=models.BigIntegerField()
    staff_id=models.CharField(max_length=50,blank=True, null=True)
    name=models.CharField(default='', max_length=20, blank=True, null=True )
    name_tamil=models.CharField(default='', max_length=20,blank=True, null=True)
    dob=  models.DateField(blank=True,null=True)
    gender= models.CharField(max_length=50,blank=True, null=True)
    management=models.CharField(max_length=100,blank=True,null=True) 
    stafs=models.CharField(max_length=1,blank=True,null=True) 
    designation=models.ForeignKey(User_desig)
    subject=models.ForeignKey(Desig_subjects)
    post_go_id=models.PositiveIntegerField(max_length=4)
    teacher_differently_abled = models.CharField(max_length=5,blank=True,null=True)
    differently_abled_type = models.CharField(max_length=40,blank=True, null=True)
    mother_name= models.CharField(max_length=50,blank=True, null=True)
    father_name= models.CharField(max_length=50,blank=True, null=True)  
    marital= models.CharField(max_length=50,blank=True, null=True) 
    spouse_name= models.CharField(max_length=50,blank=True, null=True)
    religion=models.ForeignKey(T_Religion,blank=True,null=True)
    community = ChainedForeignKey(
        T_Community, chained_field='religion', chained_model_field='religion', auto_choose=True,blank=True,null=True)
    sub_caste = ChainedForeignKey(
        T_Sub_Castes, chained_field='community', chained_model_field='community', auto_choose=True,blank=True,null=True)
    mothertongue=models.ForeignKey(Language,blank=True,null=True)
    native_district=models.ForeignKey(District,blank=True,null=True)
    imark1= models.CharField(max_length=50,blank=True, null=True)
    imark2= models.CharField(max_length=50,blank=True, null=True)
    blood_group = models.CharField(max_length=10, blank=True, null=True)
    height= models.BigIntegerField(blank=True, null=True,default=0)
    weight= models.BigIntegerField(blank=True, null=True,default=0)
    email= models.CharField(max_length=50,blank=True, null=True)
    phone_number= models.CharField(max_length=20,blank=True, null=True)
    landline=models.BigIntegerField(blank=True,null=True,default=0)
    pan_number= models.CharField(max_length=10,blank=True, null=True)     
    aadhaar_number= models.BigIntegerField(blank=True, null=True,default=0) 
    health_number=  models.CharField(max_length=50,blank=True, null=True)
    bank_dist=models.ForeignKey(Bank_district,blank=True,null=True)
    bank = ChainedForeignKey(
        Bank, chained_field='bank_dist', chained_model_field='bank_dist', auto_choose=True,blank=True,null=True)
    branch = ChainedForeignKey(
        Branch, chained_field='bank', chained_model_field='bank', auto_choose=True,blank=True,null=True)
    bank_account_no= models.BigIntegerField(blank=True, null=True) 
    passport=  models.CharField(max_length=50,blank=True, null=True)  
    passport_no= models.CharField(max_length=30,blank=True, null=True)
    passport_date_from= models.DateField(blank=True,null=True)  
    passport_date_to= models.DateField(blank=True,null=True)
    pres_add_flatno=models.CharField(max_length=50,blank=True, null=True)
    pres_add_street=models.CharField(max_length=50,blank=True, null=True)
    pres_add_area=models.CharField(max_length=50,blank=True, null=True)
    pres_add_city=models.CharField(max_length=50,blank=True, null=True)
    present_pincode= models.CharField(max_length=6,blank=True, null=True)
    present_district=models.ForeignKey(Present_District,blank=True,null=True)
    perm_add_flatno=models.CharField(max_length=50,blank=True, null=True)
    perm_add_street=models.CharField(max_length=50,blank=True, null=True)
    perm_add_area=models.CharField(max_length=50,blank=True, null=True)
    perm_add_city=models.CharField(max_length=50,blank=True, null=True)
    permanent_pincode= models.CharField(max_length=6,blank=True, null=True)
    permanent_district=models.ForeignKey(Permanent_District,blank=True,null=True)
    pension_name=  models.CharField(max_length=50,blank=True, null=True)
    pension_number=  models.CharField(max_length=50,null=True,default=0)
    dofags=models.DateField(blank=True,null=True)
    designation_fags=models.CharField(max_length=50, blank=True, null=True)
    dofsed= models.DateField(blank=True,null=True) 
    designation_fased=models.PositiveIntegerField(max_length=10, blank=True, null=True)

    dojocs=models.DateField()
    dojocs_session=models.CharField(max_length=2,blank=True,null=True)
    topocs= models.ForeignKey(Posting_type)
    doregu=models.DateField(blank=True,null=True) 
    doregu_session=models.CharField(max_length=2,blank=True,null=True)
    uta= models.CharField(max_length=50,blank=True, null=True,default=None)
    uta_date=models.DateField(blank=True,null=True)
    uta_order_no=models.CharField(max_length=50,blank=True, null=True)   
    doprob=models.DateField(blank=True,null=True)  
    doprob_session=models.CharField(max_length=2,blank=True,null=True)
    # designation_relinq=models.CharField(max_length=100,blank=True, null=True)
    typewite_skill_level=models.CharField(max_length=10,blank=True, null=True)   
    tamil_jr = models.BooleanField(default=False,blank=True)
    eng_jr = models.BooleanField(default=False,blank=True)
    tamil_sr = models.BooleanField(default=False,blank=True)
    eng_sr = models.BooleanField(default=False,blank=True)
    # typewite_skill_language=models.CharField(max_length=50,blank=True, null=True)  
    employment_status=models.CharField(max_length=50,blank=True, null=True) 
    appointed_aided= models.CharField(max_length=50,blank=True, null=True)  
    appointed_aided_date= models.DateField(blank=True,null=True)  
    approval_aided_date= models.DateField(blank=True,null=True)   
    aided_order_no= models.CharField(max_length=50,blank=True, null=True) 
    pay_drawing_officer=models.ForeignKey(Teacher_pay_officer,blank=True,null=True)
    increment_month=  models.CharField(max_length=50,blank=True, null=True) 
    language_test= models.CharField(max_length=50,blank=True, null=True)  
    evaluation=  models.CharField(max_length=50,blank=True, null=True)  
    evaluation_date= models.DateField(blank=True,null=True)
    eval_order_no= models.CharField(max_length=50,blank=True, null=True)
    evaluation_auth=models.CharField(max_length=40,blank=True,null=True)
    
    uploadfile=models.FileField(upload_to='teachers_pics',blank=True, null=True)   
    dor= models.DateField(blank=True,null=True) 
    ofs_flag=models.BooleanField(default=False)
    school_office=BigIntegerField(default=0)
    ofs_reason=models.CharField(max_length=25,default="None",blank=True,null=True)
    ofs_date=models.DateField(blank=True,null=True)
    super_annum_flag=models.BooleanField(default=False)

    transfer_flag=models.CharField(max_length=3,default='No')
    timestamp = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    
    def __unicode__(self):
    	return '%s%d%s' %(self.name,self.count,self.dofsed)




        

class Teacher_transfer_history1(models.Model):
    teacher=models.BigIntegerField(blank=True, null=True,default=0)
    old_school_id=models.BigIntegerField(blank=True, null=True,default=0)

    reason=models.CharField(max_length=50,blank=True, null=True)
    Designation_after_transfer=models.PositiveIntegerField(blank=True, null=True)
   
    subject_after_promotion=models.PositiveIntegerField(blank=True, null=True)

    previous_designation=models.ForeignKey(User_desig,blank=True, null=True)
    
    prev_subject = ChainedForeignKey(
        Desig_subjects, chained_field='previous_designation', chained_model_field='desig', auto_choose=True)
    
    releiving_order_no=models.CharField(max_length=50,blank=True, null=True)
    releiving_order_date=models.DateField(blank=True, null=True)
    new_school_id=models.BigIntegerField(blank=True, null=True,default=0)

    
    Designation_after_transfer=models.PositiveIntegerField(blank=True, null=True)
   
    subject_after_promotion=models.PositiveIntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    
    joining_order_no=models.CharField(max_length=50,blank=True, null=True)
    joining_order_date=models.DateField(blank=True, null=True)


class Teacher_transfer_history(models.Model):
    teacher=models.BigIntegerField(blank=True, null=True,default=0)
    old_school_id=models.BigIntegerField(blank=True, null=True,default=0)
    reason=models.CharField(max_length=50,blank=True, null=True)
    previous_designation=models.ForeignKey(User_desig,blank=True, null=True)
    prev_subject=models.ForeignKey(Desig_subjects,blank=True, null=True)

    releiving_order_no=models.CharField(max_length=50,blank=True, null=True)
    releiving_order_date=models.DateField(blank=True, null=True)
    new_school_id=models.BigIntegerField(blank=True, null=True,default=0)

    
    Designation_after_transfer=models.PositiveIntegerField(blank=True, null=True)
   
    subject_after_promotion=models.PositiveIntegerField(blank=True, null=True)
    # timestamp = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    
    joining_order_no=models.CharField(max_length=50,blank=True, null=True)
    joining_order_date=models.DateField(blank=True, null=True)


    




"""
Model for teacher family details
"""

class family_relationship(models.Model):
    relationship_name = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % (self.relationship_name)


"""
Model for teacher family details
"""
class Teacher_family_detail(models.Model):
    teacherid = models.ForeignKey(Teacher_detail)
    name = models.CharField(max_length=50)
    aadhaar_number= models.BigIntegerField(blank=True, null=True,default=0) 
    dob = models.DateField()
    age = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    relation = models.ForeignKey(family_relationship)
    district=models.ForeignKey(District,blank=True,null=True)
    block= ChainedForeignKey(Block, chained_field='district',
        chained_model_field='district',
        auto_choose=True,
        blank=True,
        null=True)
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
    contonment = ChainedForeignKey(
        Contonment, chained_field='district', chained_model_field='district', auto_choose=True,blank=True,null=True )
    contonment_ward = ChainedForeignKey(
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

    complete_flag = models.CharField(max_length=1,default="0")
    # modification_flag = models.CharField(max_length=1)
    # verification_flag = models.CharField(max_length=1)
    staff_id = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    spou_gov=models.CharField(max_length=3,default='No')
    def __unicode__(self):
        return u'%s %s %d' % (self.name,self.relation.relationship_name,self.age)


class fund_category(models.Model):   
    fund_name = models.CharField(max_length=500)
    def __unicode__(self):
        return u'%s' % (self.fund_name)
    
"""
Models for Teacher nomini details
"""
class Teacher_nomini(models.Model):
    teacherid = models.ForeignKey(Teacher_detail)
    fund_name = models.ForeignKey(fund_category)
    nominee_name = models.ForeignKey(Teacher_family_detail,blank=True,null=True)  
    other_nominee=models.CharField(max_length=100,blank=True,null=True) 
    percentage = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    nom_dt  = models.DateField()
    complete_flag = models.CharField(max_length=1,default="0")

    # modification_flag = models.CharField(max_length=1)
    # verification_flag = models.CharField(max_length=1)
    staff_id = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % (self.teacherid_id)                




"""
Model for Teacher immovalble property details
"""
class Teacher_immovalble_property(models.Model):
    teacherid = models.ForeignKey(Teacher_detail)
    prop_description = models.CharField(max_length=100)
    purchase_value =models.PositiveIntegerField(validators=[MinValueValidator(1)])
    present_value = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    place = models.CharField(max_length=100)
    doc_date = models.DateField()    
    acquired_source = models.CharField(max_length=100,blank=True,null=True)
    doc_number = models.CharField(max_length=50,blank=True,null=True)
    order_no = models.CharField(max_length=50,blank=True,null=True)
    order_date = models.DateField(blank=True,null=True)
    # complete_flag = models.CharField(max_length=1,default="0")
    # modification_flag = models.CharField(max_length=1)
    # verification_flag = models.CharField(max_length=1)
    staff_id = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self): 
        return u'%s' % (self.teacherid)


"""
Model for Teacher movable property details
"""
class Teacher_movable_property(caching.base.CachingMixin, models.Model):
    teacherid = models.ForeignKey(Teacher_detail)
    prop_description = models.CharField(max_length=100)
    purchase_value = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    present_value = models.PositiveIntegerField(validators=[MinValueValidator(1)])    
    purchase_doc_date = models.DateField()
    
    order_date = models.DateField(blank=True,null=True,default='None')
    source = models.CharField(max_length=100,blank=True,null=True,default='None')
    # complete_flag = models.CharField(max_length=1,default="0")
    # modification_flag = models.CharField(max_length=1)
    # verification_flag = models.CharField(max_length=1)
    staff_id = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self): 
        return u'%s' % (self.teacherid)

class completed_table(models.Model):
    teacherid = models.ForeignKey(Teacher_detail)
    school_id=models.BigIntegerField()
    Teacher_posting=models.CharField(max_length=2,default=0)
    Teacher_regularisation=models.CharField(max_length=2,default=0)
    Teacher_probation=models.CharField(max_length=2,default=0)
    Teacher_post_relinquish=models.CharField(max_length=2,default=0)
    Teacher_edu=models.CharField(max_length=2,default=0)
    Teacher_trainin=models.CharField(max_length=2,default=0)
    Teacher_testpass=models.CharField(max_length=2,default=0)
    Teacher_gpf=models.CharField(max_length=2,default=0)
    Teacher_leav=models.CharField(max_length=2,default=0)
    Teacher_leavcredit=models.CharField(max_length=2,default=0)
    Teacher_leavsurr=models.CharField(max_length=2,default=0)
    Teacher_lon=models.CharField(max_length=2,default=0)
    Teacher_familyrel=models.CharField(max_length=2,default=0)
    Teacher_financ=models.CharField(max_length=2,default=0)
    Teacher_movabl=models.CharField(max_length=2,default=0)
    Teacher_immovabl=models.CharField(max_length=2,default=0)
    Teacher_ltcc=models.CharField(max_length=2,default=0)
    Teacher_disaction=models.CharField(max_length=2,default=0)
    Teacher_result=models.CharField(max_length=2,default=0)
    Teacher_award=models.CharField(max_length=2,default=0)
    ofs_flag=models.BooleanField(default=False) 
    
    def __unicode__(self):
        return u'%d%d%s%s%s' % (self.id,self.teacherid_id,self.Teacher_edu,self.Teacher_regularisation,self.Teacher_posting)
    
"""
Model for Qualification for Education 
"""
class Qualification(caching.base.CachingMixin,models.Model):   
    qualification = models.CharField(max_length=100)

    def __unicode__(self):
        return u'%s' % (self.qualification)

"""
Model for Subject for Education
"""
class Edu_subjects(caching.base.CachingMixin,models.Model):
    subject = models.CharField(max_length=100)
    qualification_sub = models.ForeignKey('Qualification')

    def __unicode__(self):
        return u'%s' % (self.subject)

"""
Model for Teaching Medium
"""
class Medium(models.Model):
    medium_name = models.CharField(max_length=15)

    def __unicode__(self):
        return u'%s' % (self.medium_name)


"""
Model for Months of a Year
"""
class Months(models.Model):
    months_name = models.CharField(max_length=15)

    def __unicode__(self):
        return u'%s' % (self.months_name)

"""
Model for Distinction of university
"""
class Distinction(models.Model):
    class_name = models.CharField(max_length=15)

    def __unicode__(self):
        return u'%s' % (self.class_name)

"""
Model for Teacher education details

"""
class Teacher_edu(caching.base.CachingMixin,models.Model):
    teacherid = models.ForeignKey(Teacher_detail)
    qualification=models.ForeignKey(Qualification)
    subject = ChainedForeignKey(Edu_subjects, 
        chained_field='qualification',
        chained_model_field='qualification_sub',
        show_all=False,
        auto_choose=True,
        )
    medium_of_instruction= models.ForeignKey(Medium)
    month = models.ForeignKey(Months)
    year = models.CharField(max_length=4)
    university = models.CharField(max_length=50)
    remarks=models.ForeignKey(Distinction)
    complete_flag = models.CharField(max_length=1,default="5")
    # modification_flag = models.CharField(max_length=1)
    # verification_flag = models.CharField(max_length=1)
    staff_id = models.CharField(max_length=10,blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % (self.teacherid)

"""
Model for Teacher tests details
"""
class test_master(models.Model):
    test_code = models.CharField(max_length=30)
    test_name = models.CharField(max_length=300)

    def __unicode__(self):
        return u'%s' % (self.test_name)




"""
Model for Teacher passed tests details
"""
class Teacher_test(models.Model):
    teacherid = models.ForeignKey(Teacher_detail)
    tests_passed = models.ForeignKey(test_master)
    month = models.ForeignKey(Months)
    year = models.PositiveIntegerField(validators=[MinValueValidator(1965),MaxValueValidator(2100)])
    reg_no = models.CharField(max_length=15)
    gaz_no = models.CharField(max_length=30)
    gaz_date = models.DateField()
    page_no = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(2000)])
    complete_flag = models.CharField(max_length=1,default="0")
    # modification_flag = models.CharField(max_length=1)
    # verification_flag = models.CharField(max_length=1)
    staff_id = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % (self.teacherid_id)


"""
Model for teacher's training details
"""
class Teacher_training(models.Model):
    teacherid = models.ForeignKey(Teacher_detail)
    course = models.CharField(max_length=50,blank=True,null=True)
    institution = models.CharField(max_length=30,blank=True,null=True)
    city = models.CharField(max_length=30,blank=True,null=True)
    country = models.CharField(max_length=30,blank=True,null=True)
    duration_from = models.DateField()
    duration_to = models.DateField()
    complete_flag = models.CharField(max_length=1,default="0")
    # modification_flag = models.CharField(max_length=1)
    # verification_flag = models.CharField(max_length=1)
    staff_id = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self): 
        return u'%s' % (self.teacherid_id)

"""        
Leave types
"""
class Teacher_leave_type(models.Model):
    leave_name = models.CharField(max_length=100)

    def __unicode__(self):
        return u'%s' % (self.leave_name)

"""
Leave master entry table
"""
class Teacher_leave_master(models.Model):
    teacherid = models.ForeignKey(Teacher_detail)
    el_ob=models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(240)],default=0)
    el_taken=models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(240)],default=0)
    el_bal=models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(240)],default=0)
    uel_mc_ob=models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(540)],default=0)
    uel_mc_taken=models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(540)],default=0)
    uel_mc_bal=models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(540)],default=0)
    llp_mc_ob=models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(540)],default=0)
    llp_mc_taken=models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(540)],default=0)
    llp_mc_bal=models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(540)],default=0)
    uel_pa_ob=models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(180)],default=0)
    uel_pa_taken=models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(180)],default=0)
    uel_pa_bal=models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(180)],default=0)
    llp_womc_ob=models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(940)],default=0)
    llp_womc_taken=models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(540)],default=0)
    llp_womc_bal=models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(540)],default=0)
    spl_leave_ob=models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(42)],default=0)
    spl_leave_taken=models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(42)],default=0)
    spl_leave_bal=models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(42)],default=0)
    maternity_leave_ob=models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(180)],default=0)
    maternity_leave_taken=models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(180)],default=0)
    maternity_leave_bal=models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(180)],default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
def __unicode__(self):
        return u'%d' % (self.teacherid)
def attrs(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value


class Teacher_leave_code(models.Model):
    leave_name = models.CharField(max_length=100)

    def __unicode__(self):
        return u'%s' % (self.leave_name)





""" 
Model for teacher leave surrender details 
""" 
class Teacher_leave_surrender(models.Model): 
    teacherid = models.ForeignKey(Teacher_detail) 
    surrender_date = models.DateField(blank=True,null=True) 
    current_balance_days = models.PositiveIntegerField() 
    no_of_days = models.PositiveIntegerField() 
    order_no = models.CharField(max_length=30,blank=True,null=True) 
    order_date = models.DateField() 
    complete_flag = models.CharField(max_length=1,default="0") 
    # modification_flag = models.CharField(max_length=1) 
    # verification_flag = models.CharField(max_length=1) 
    staff_id = models.CharField(max_length=10) 
    timestamp = models.DateTimeField(auto_now_add=True) 

    def __unicode__(self): 
        return u'%s' % (self.teacherid_id)

class ltc_leave_type(models.Model):
    leave_name = models.CharField(max_length=100)

    def __unicode__(self):
        return u'%s' % (self.leave_name)

class ltc_destination(models.Model):
    leave_name = models.CharField(max_length=100)

    def __unicode__(self):
        return u'%s' % (self.leave_name)

"""
Model for teacher leave details
"""
class Teacher_leave(models.Model):
    teacherid = models.ForeignKey(Teacher_detail)
    leave_type = models.ForeignKey(Teacher_leave_type)
    leave_from = models.DateField(blank=True,null=True)
    leave_to = models.DateField(blank=True,null=True)
    order_no = models.CharField(max_length=50,blank=True,null=True)
    order_date = models.DateField(blank=True,null=True)
    complete_flag = models.CharField(max_length=1,default="0")
    ob=models.PositiveIntegerField(blank=True, null=True)
    taken=models.PositiveIntegerField(blank=True, null=True)
    bal=models.PositiveIntegerField(blank=True, null=True)
   
    # modification_flag = models.CharField(max_length=1)
    # verification_flag = models.CharField(max_length=1)
    
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % (self.teacherid_id)


class ltc_leave_type(models.Model):
    leave_name = models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s' % (self.leave_name)

class ltc_destination(models.Model):
    leave_name = models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s' % (self.leave_name)


class ltc_base(models.Model):
    year=models.CharField(max_length=4)
    block_year=models.CharField(max_length=9)

    def __unicode__(self): 
        return u'%s' % (self.block_year)




"""
Model for teacher previous LTC
"""
class Teacher_ltc(models.Model):
    teacherid = models.ForeignKey(Teacher_detail)
    from_year =models.CharField(max_length=4)
    block_yeear =models.CharField(max_length=9,blank=True,null=True)
    leave_from=models.DateField()
    leave_to = models.DateField()
    destination_type = models.ForeignKey(ltc_destination)
    leave_type = models.ForeignKey(ltc_leave_type)
    sanction_amt = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    no_of_days_sanctioned = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    sanction_order = models.CharField(max_length=50)
    sanction_date = models.DateField()
    # complete_flag = models.CharField(max_length=1,default="0")
    # modification_flag = models.CharField(max_length=1)
    # verification_flag = models.CharField(max_length=1)
    staff_id = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self): 
        return u'%s' % (self.teacherid_id)

""" 
Model for teacher leave credits 
""" 
class Teacher_leave_credit(models.Model): 
    teacherid = models.ForeignKey(Teacher_detail) 
    school_id=models.BigIntegerField()
    effective_date = models.DateField(blank=True,null=True) 
    no_of_days_credit = models.PositiveIntegerField(default="17") 
    stafs=models.CharField(max_length=30,blank=True,null=True) 
    designation=models.CharField(max_length=50,blank=True,null=True) 
    
    complete_flag = models.CharField(max_length=1,default="0") 
    
    timestamp = models.DateTimeField(auto_now_add=True) 

    def __unicode__(self): 
        return u'%s' % (self.teacherid_id)





"""
Models for Teacher GPF/TPF Loan details
"""

class Teacher_GPF_loan(models.Model):
    teacherid = models.ForeignKey(Teacher_detail)
    sanctioned_amt = models.BigIntegerField(validators=[MinValueValidator(1)])
    installments = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(1000)])
    monthly_installment = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(1000000)])
    first_insta_date = models.DateField()
    sanctioned_order = models.CharField(max_length=50)
    sanctioned_date = models.DateField()
    complete_flag = models.CharField(max_length=1,default="0")
    # modification_flag = models.CharField(max_length=1)
    # verification_flag = models.CharField(max_length=1)
    staff_id = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self): 
        return u'%s' % (self.teacherid_id)

class Teacher_loan_category(models.Model):
    loan_name = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % (self.loan_name)


"""
Models for Teacher loan details
"""
class Teacher_loan(models.Model):
    teacherid = models.ForeignKey(Teacher_detail)
    loan_category = models.ForeignKey(Teacher_loan_category)
    loan_purpose = models.CharField(max_length=50)
    sanctioned_amt = models.BigIntegerField(default=0)
    installments = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(1000)])
    monthly_installment = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(100000)])
    first_insta_date = models.DateField()
    sanctioned_order = models.CharField(max_length=50)
    sanctioned_date = models.DateField()
    complete_flag = models.CharField(max_length=1,default="0")
    # modification_flag = models.CharField(max_length=1)
    # verification_flag = models.CharField(max_length=1)
    staff_id = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self): 
        return u'%s' % (self.teacherid_id)


"""
Models for Teacher Posting Entry details
"""
class Teacher_posting_entry(models.Model):
    teacherid = models.ForeignKey(Teacher_detail)
    designation = models.ForeignKey(User_desig)
    district=models.ForeignKey(District)
    block= ChainedForeignKey(Block, chained_field='district',
        chained_model_field='district',
        auto_choose=True,
        blank=True,
        null=True)
    
    
    school_name1 = models.CharField(max_length=100,blank=True, null=True)
    type_of_posting = models.ForeignKey(Posting_type)
    period_from = models.DateField()
    period_to = models.DateField(blank=True, null=True)
    # modification_flag = models.CharField(max_length=1)
    # verification_flag = models.CharField(max_length=1)
    staff_id = models.CharField(max_length=10)
    complete_flag=models.CharField(max_length=1,default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s%s%s' % (self.designation.User_desig,self.district.district_name,self.school_name1)


class disp_rule(models.Model): 
    rule_name = models.CharField(max_length=10) 

    def __unicode__(self): 
        return u'%s' % (self.rule_name) 

class action(models.Model): 
    action_name = models.CharField(max_length=50) 

    def __unicode__(self): 
        return u'%s' % (self.action_name) 
""" 
Models for Teacher's Action 
""" 
class Teacher_action(models.Model): 
    teacherid = models.ForeignKey(Teacher_detail) 
    post_name_charge_committed=models.ForeignKey(Teacher_posting_entry) 
    gist = models.CharField(max_length=500) 
    
    charge_memo_number = models.CharField(max_length=50) 
    charge_memo_date =models.DateField() 
    charge_pending=models.CharField(max_length=300,blank=True,null=True)
    type_charge_memo=models.ForeignKey(disp_rule) 

    a_individual_exp_date = models.DateField(blank=True,null=True)
    a_final_order_no=models.CharField(max_length=50,blank=True,null=True) 
    a_final_order_date=models.DateField(blank=True,null=True) 
    a_final_status=models.CharField(max_length=50,blank=True,null=True) 
    a_increment_cut_years=models.CharField(max_length=10,blank=True,null=True) 

    e_whether_suspented=models.CharField(max_length=1,blank=True,null=True) 
    e_suspension_order_date=models.DateField(blank=True,null=True) 
    e_reinitiated_service=models.CharField(max_length=1,blank=True,null=True) 
    e_reinitiated_date=models.DateField(blank=True,null=True) 
    e_charge_memo = models.CharField(max_length=10,blank=True,null=True)  

    b_individula_exp_date=models.DateField(blank=True,null=True) 
    b_enquiry_officer_appointed=models.CharField(max_length=1,blank=True,null=True) 
    b_enquiry_officer_app_date=models.DateField(blank=True,null=True) 
    b_enquiry_officer_name=models.CharField(max_length=50,blank=True,null=True) 
    b_enquiry_officer_rpt_received=models.DateField(blank=True,null=True) 
    b_charges_proved=models.CharField(max_length=1,blank=True,null=True) 
    b_addl_exp_individual_date=models.DateField(blank=True,null=True) 
    b_final_order_date=models.DateField(blank=True,null=True) 
    b_punishment_type=models.ForeignKey(action,blank=True,null=True) 
    b_increment_cut_years=models.CharField(max_length=10,blank=True,null=True) 

    b_appeal_received=models.CharField(max_length=1,blank=True,null=True) 
    b_appeal_date=models.DateField(blank=True,null=True) 
    b_final_order_date_appeal=models.DateField(blank=True,null=True) 
    b_punishment_type_appeal=models.CharField(max_length=40,blank=True,null=True) 
    b_increment_cut_years_appeal=models.CharField(max_length=50,blank=True,null=True) 



    staff_id = models.CharField(max_length=10,blank=True,null=True) 
    cleared_flag= models.CharField(max_length=1,default="0")
    timestamp = models.DateTimeField(auto_now_add=True) 

    

    def __unicode__(self): 
        return u'%s' % (self.teacherid_id)
    def attrs(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value

    def sorted_attrs(self):
     
        return [(key, self.__dict__[key]) for key in sorted(self.__dict__)]







"""
Models for Teacher Probation Entry details
"""
class Teacher_probation_entry(models.Model):
    teacherid = models.ForeignKey(Teacher_detail)
    designation = models.ForeignKey(Teacher_posting_entry)
    order_no = models.CharField(max_length=50)
    order_date = models.DateField()
    date_of_clearance = models.DateField()
    doprob_session=models.CharField(max_length=2,blank=True,null=True)
    complete_flag = models.CharField(max_length=1,default="0")
    # modification_flag = models.CharField(max_length=1)
    # verification_flag = models.CharField(max_length=1)
    staff_id = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % (self.teacherid)




"""
Models for Teacher Regularisation Entry details
"""
class Teacher_regularisation_entry(models.Model):
    teacherid = models.ForeignKey(Teacher_detail)
    designation = models.ForeignKey(Teacher_posting_entry)
    order_no = models.CharField(max_length=50)
    order_date = models.DateField()
    date_of_regularisation = models.DateField()
    doregu_session=models.CharField(max_length=2,blank=True,null=True)
    complete_flag = models.CharField(max_length=1,default=2)
    # modification_flag = models.CharField(max_length=1)
    # verification_flag = models.CharField(max_length=1)
    staff_id = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % (self.teacherid)


""" 
Models for Relinquishment Entry details 
""" 
class Teacher_relinquish_entry(models.Model): 
    teacherid = models.ForeignKey(Teacher_detail)   
    current_designation= models.ForeignKey(Teacher_posting_entry)
    promoted_to = models.ForeignKey(User_desig)  
   
    date_of_relinqui = models.DateField() 
    order_no= models.CharField(max_length=50) 
    
    crucial_date_for_promotion = models.DateField() 
    promo_next_eligible_date= models.DateField() 
    complete_flag = models.CharField(max_length=1,default=2) 
    # modification_flag = models.CharField(max_length=1) 
    # verification_flag = models.CharField(max_length=1) 
    staff_id = models.CharField(max_length=10) 
    timestamp = models.DateTimeField(auto_now_add=True) 

    def __unicode__(self): 
        return u'%s' % (self.teacherid)



class Teacher_transfer_purpose(models.Model):

    district=models.ForeignKey(District)
    block= ChainedForeignKey(Block, chained_field='district',
        chained_model_field='district',
        auto_choose=True,
        blank=True,
        null=True)



""" Model for teacher leave credits  """ 
class scale_register_abstract(models.Model): 
    
    udise_code =models.BigIntegerField()
    management=models.CharField(max_length=100,blank=True,null=True) 
    stafs_category=models.CharField(max_length=30,blank=True,null=True) 
    designation=models.CharField(max_length=50,blank=True,null=True) 
    subject=models.CharField(max_length=30,blank=True,null=True) 
    sanctioned_post=models.PositiveIntegerField(default=0)
    filled_post=models.PositiveIntegerField(default=0)
    vaccant_post=models.PositiveIntegerField(default=0)    
    office_entry=models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True) 

    def __unicode__(self): 
        return u'%s%d' % (self.stafs_category,self.office_entry)

class count_private_Teaching(models.Model):
    count_private_Teaching=models.PositiveIntegerField()

    def __unicode__(self):
        return u'%d' %(self.count_private_Teaching)


class Count_private(models.Model):
    count_stand=models.PositiveIntegerField()

    def __unicode__(self):
        return u'%d' %(self.count_stand)


        


class staff_type(models.Model):
    staff_type=models.CharField(max_length=15)

    def __unicode__(self):
        return u'%s' %(self.staff_type)

class private_designation(models.Model):
    designation_typeno=models.ForeignKey(staff_type)
    designation=models.CharField(max_length=50)


    def __unicode__(self):
        return u'%s' %(self.designation)

class class_assigned_master(models.Model):
    class_ass=models.CharField(max_length=5)

    def __unicode__(self):
        return u'%s' %(self.class_ass)


class private_teachers_detail(models.Model):
    pri_tea_id=models.BigIntegerField()
    name=models.CharField(default='', max_length=40,blank=True,null=True)
    school_name=models.BigIntegerField()
    dob=models.DateField(blank=True,null=True)
    gender= models.CharField(max_length=50,blank=True, null=True)  
    father_name= models.CharField(max_length=50,blank=True, null=True)
    doa=models.DateField(blank=True, null=True)
    designation_typeno=models.ForeignKey(staff_type,blank=True, null=True)    
    designation = ChainedForeignKey(private_designation, 
        chained_field='designation_typeno',
        chained_model_field='designation_typeno',
        show_all=False,
        auto_choose=True,
        blank=True, 
        null=True
        )
    subject=models.CharField(max_length=50,blank=True,null=True) 
    class_assigned=models.ForeignKey(class_assigned_master,blank=True, null=True)
    teaching_experience=models.PositiveIntegerField(blank=True,null=True,max_length=2)
    train_untrain=models.CharField(max_length=3,blank=True,null=True)
    scaleofpay=models.PositiveIntegerField(blank=True,null=True,max_length=5)
    grossofpay=models.PositiveIntegerField(blank=True,null=True,max_length=5)
    whethertet= models.BooleanField(default=False)
    date_of_pass=models.DateField(blank=True,null=True)
    reg_no=models.CharField(max_length=15,blank=True,null=True)
    esino=models.CharField(max_length=20,blank=True,null=True)
    epfno=models.CharField(max_length=20,blank=True,null=True)


    def __unicode__(self):
        return u'%d' %(self.pri_tea_id)


class Teacher_edu_private(caching.base.CachingMixin,models.Model):
    private_tea_id = models.ForeignKey(private_teachers_detail)
    unique_id=models.BigIntegerField()
    qualification=models.ForeignKey(Qualification)
    subject = ChainedForeignKey(Edu_subjects, 
        chained_field='qualification',
        chained_model_field='qualification_sub',
        show_all=False,
        auto_choose=True,
        )
    medium_of_instruction= models.ForeignKey(Medium)
    month = models.ForeignKey(Months)
    year = models.CharField(max_length=4)
    university = models.CharField(max_length=50)
    remarks=models.ForeignKey(Distinction)
     
    staff_id = models.CharField(max_length=10,blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % (self.private_tea_id)


""" 
# Model for block wise report
# """ 
class block_wise_abstract(models.Model): 
    school_key = models.PositiveIntegerField()
    district_code = models.ForeignKey(District)
    block_code = models.ForeignKey(Block) 
    block_name = models.CharField(max_length=100)
    school_code = models.PositiveIntegerField()   
    school_name = models.CharField(max_length=100)
    udise_code=models.BigIntegerField()
    tsanctioned_post=models.PositiveIntegerField(default=0)
    tfilled_post=models.PositiveIntegerField(default=0)
    tvaccant_post=models.PositiveIntegerField(default=0)
    ntsanctioned_post=models.PositiveIntegerField(default=0)
    ntfilled_post=models.PositiveIntegerField(default=0)
    ntvaccant_post=models.PositiveIntegerField(default=0)
    flag=models.CharField(max_length=3,default='No') 
    authenticate_1=models.CharField(max_length=15,blank=True,null=True,default='others')
    timestamp = models.DateTimeField(auto_now_add=True) 

    def __unicode__(self): 
        return u'%s' % (self.school_key)

""" 
# Model for District wise report
# """ 
class district_wise_abstract(models.Model): 
    school_key = models.PositiveIntegerField()
    district_code=models.ForeignKey(District,blank=True,null=True) 
    block_code = models.ForeignKey(Block)   
    tsanctioned_post=models.PositiveIntegerField(default=0)
    tfilled_post=models.PositiveIntegerField(default=0)
    tvaccant_post=models.PositiveIntegerField(default=0)
    ntsanctioned_post=models.PositiveIntegerField(default=0)
    ntfilled_post=models.PositiveIntegerField(default=0)
    ntvaccant_post=models.PositiveIntegerField(default=0)
    flag=models.CharField(max_length=3,default='No') 
    timestamp = models.DateTimeField(auto_now_add=True) 

    def __unicode__(self): 
        return u'%s' % (self.school_key)



class Exam_duty(models.Model):
    exam_duty_post=models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return u'%s' %(self.exam_duty_post)


class Camp_duty(models.Model):
    camp_duty_post=models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return u'%s' %(self.camp_duty_post)


"""
# Model for Teacher exam and camp duty result
# """

class Teacher_result_exam(models.Model):
   teacherid = models.ForeignKey(Teacher_detail)
   month = models.ForeignKey(Months)
   year=models.CharField(max_length=20, blank=True, null=True )
  
   subject=models.CharField(max_length=30,blank=True,null=True) 
   appeared=models.PositiveIntegerField(default=0)
   passed=models.PositiveIntegerField(default=0)
   percentage=models.PositiveIntegerField(default=0)
   exam_duty=models.CharField(max_length=30,blank=True,null=True)
   val_camp=models.CharField(max_length=30,blank=True,null=True)

   def __unicode__(self):
       return u'%d' % (self.teacherid)


 

class Awards(models.Model):
    Awards_name=models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return u'%s' %(self.Awards_name)


class Award_Level(models.Model):
    Award_Level_position=models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return u'%s' %(self.Award_Level_position)



class Teacher_award(models.Model):
   teacherid = models.ForeignKey(Teacher_detail)
   award_name=models.ForeignKey(Awards)
   level=models.ForeignKey(Award_Level)
   year=models.PositiveIntegerField(default=0)
   remarks=models.CharField(max_length=50, blank=True,null=True)
   
   def __unicode__(self):
       return u'%d' % (self.teacherid)