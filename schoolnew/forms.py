from django import forms

from schoolnew.models import *

class BasicForm(forms.ModelForm):
	class Meta:
		model = Basicinfo

class academicinfo_form(forms.ModelForm):
	class Meta:
		model = Academicinfo
		
class class_section_form(forms.ModelForm):
	class Meta:
		model =Class_section

class staff_form(forms.ModelForm):
	class Meta:
		model = Staff

class parttimestaff_form(forms.ModelForm):
	class Meta:
		model = Parttimestaff
class infradet_form(forms.ModelForm):
	class Meta:
		model = Infradet
class land_form(forms.ModelForm):
	class Meta:
		model = Land

class building_form(forms.ModelForm):
	class Meta:
		model = Building
class building_abs_form(forms.ModelForm):
	class Meta:
		model = Building_abs
class sports_form(forms.ModelForm):
	class Meta:
		model = Sports
class ictentry_form(forms.ModelForm):
	class Meta:
		model = Ictentry
class sch_groups_form(forms.ModelForm):
	class Meta:
		model = Sch_groups
class pass_form(forms.ModelForm):
	class Meta:
		model = Passpercent
			

