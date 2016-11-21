from django import forms
from teachers.models import *
# from baseapp.models import *

class Teacher_detailform(forms.ModelForm):
    class Meta:
        model = Teacher_detail
        exclude = ('count','transfer_flag','ofs_flag','ofs_reason','ofs_date','super_annum_flag')

class Teacher_outofserviceform(forms.ModelForm):
        model=Teacher_detail


class Teacher_detailform1(forms.ModelForm):
    class Meta:
        model = Teacher_detail
        exclude = ('transfer_flag',)
class Teacher_leave_masterform(forms.ModelForm):
    class Meta:
        model = Teacher_leave_master
        exclude = ('teacherid',)

class Teacher_posting_entryform(forms.ModelForm):
    class Meta:
        model = Teacher_posting_entry
        exclude = ('complete_flag','teacherid','staff_id','school')

class educationform(forms.ModelForm):
    class Meta:
        model = Teacher_edu
        exclude = ('complete_flag','teacherid','staff_id')

class Teacher_regularisation_entryform(forms.ModelForm):
    class Meta:
        model = Teacher_regularisation_entry
        exclude = ('complete_flag','teacherid','staff_id')

class Teacher_probation_entryform(forms.ModelForm):
    class Meta:
        model = Teacher_probation_entry
        exclude = ('complete_flag','teacherid','staff_id')
        
class  Teacher_relinquisform(forms.ModelForm):
   class Meta:
       model =  Teacher_relinquish_entry
       exclude = ('complete_flag','teacherid','staff_id')

class  Teacher_trainingform(forms.ModelForm):
    class Meta:
        model =  Teacher_training
        exclude = ('complete_flag','teacherid','staff_id')

class  Teacher_testform(forms.ModelForm):
    class Meta:
        model =  Teacher_test
        exclude = ('complete_flag','teacherid','staff_id')
  
class  Teacher_leaveform(forms.ModelForm):
    class Meta:
        model =  Teacher_leave
        exclude = ('complete_flag','teacherid','staff_id')



class  Teacher_ltcform(forms.ModelForm):
    class Meta:
        model =  Teacher_ltc
        exclude = ('complete_flag','teacherid','staff_id')

class  Teacher_GPF_loanform(forms.ModelForm):
    class Meta:
        model =  Teacher_GPF_loan
        exclude = ('complete_flag','teacherid','staff_id')

class  Teacher_loanform(forms.ModelForm):
    class Meta:
        model =  Teacher_loan
        exclude = ('complete_flag','teacherid','staff_id')






class Teacher_family_detailform(forms.ModelForm):
    class Meta:
        model = Teacher_family_detail
        exclude = ('complete_flag','teacherid','staff_id')



class Teacher_movable_propertyform(forms.ModelForm):
    class Meta:
        model = Teacher_movable_property
        exclude = ('complete_flag','teacherid','staff_id')



class Teacher_immovalble_propertyform(forms.ModelForm):
    class Meta:
        model = Teacher_immovalble_property
        exclude = ('complete_flag','teacherid','staff_id')


class Teacher_nominiform(forms.ModelForm):
    class Meta:
        model = Teacher_nomini
        exclude = ('complete_flag','teacherid','staff_id')

class Teacher_actionform(forms.ModelForm):
    class Meta:
        model = Teacher_action
        exclude = ('cleared_flag','teacherid','staff_id')
         


class Teacher_transfer_history_form(forms.ModelForm):
	class Meta:
		model=Teacher_transfer_history


class Teacher_leave_creditform(forms.ModelForm): 
    class Meta: 
        model = Teacher_leave_credit 
        exclude = ('complete_flag','teacherid')

class Teacher_leave_surrenderform(forms.ModelForm): 
    class Meta: 
        model = Teacher_leave_surrender 
        exclude = ('complete_flag','teacherid','staff_id')


class private_teachers_detailform(forms.ModelForm):
   class Meta:
       model=private_teachers_detail
       exclude = ('pri_tea_id','school_name')


class private_educationform(forms.ModelForm):
   class Meta:
       model=Teacher_edu_private
       exclude = ('private_tea_id','unique_id')       


class Teacher_result_exam_form(forms.ModelForm):
    class Meta:
        model = Teacher_result_exam
        exclude = ('teacherid',)
class Teacher_award_form(forms.ModelForm):
    class Meta:
        model = Teacher_award
        exclude = ('teacherid',)
class Teacher_award_form(forms.ModelForm):
    class Meta:
        model = Teacher_award
        exclude = ('teacherid',)

class Teacher_transfer_purpose_form(forms.ModelForm):
    class Meta:
        model=Teacher_transfer_purpose


        
