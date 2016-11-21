from django.db import models
from django.db.models.fields import *
from baseapp.models import School
from students.models import Child_detail


class Student_schemes(models.Model):
    school = models.ForeignKey(School,null=True,blank=True)
    academic_year = models.CharField(max_length=20,null=True,blank=True)
    student = models.ForeignKey(Child_detail,null=True,blank=True)
    cls=models.IntegerField(null=True,blank=True)  
    uniform_1 =models.CharField(max_length=5,null=True,blank=True)
    uniform_2 =models.CharField(max_length=5,null=True,blank=True)
    uniform_3 =models.CharField(max_length=5,null=True,blank=True)
    uniform_4 =models.CharField(max_length=5,null=True,blank=True)
    textbook =models.CharField(max_length=5,null=True,blank=True)
    textbook_1 =models.CharField(max_length=5,null=True,blank=True)
    textbook_2 =models.CharField(max_length=5,null=True,blank=True)
    textbook_3 =models.CharField(max_length=5,null=True,blank=True)
    notebook =models.CharField(max_length=5,null=True,blank=True)
    notebook_1 =models.CharField(max_length=5,null=True,blank=True)
    notebook_2 =models.CharField(max_length=5,null=True,blank=True)
    notebook_3 =models.CharField(max_length=5,null=True,blank=True)
    bag =models.CharField(max_length=5,null=True,blank=True)
    footware =models.CharField(max_length=5,null=True,blank=True)
    sweater =models.CharField(max_length=5,null=True,blank=True)
    crayon =models.CharField(max_length=5,null=True,blank=True)
    colorpencil =models.CharField(max_length=5,null=True,blank=True)
    geometrybox =models.CharField(max_length=5,null=True,blank=True)
    atlas =models.CharField(max_length=5,null=True,blank=True)
    cycle =models.CharField(max_length=5,null=True,blank=True)
    laptop =models.CharField(max_length=5,null=True,blank=True)
    bw =models.CharField(max_length=5,null=True,blank=True)
    sci =models.CharField(max_length=5,null=True,blank=True)
    laptop_no=models.CharField(max_length=25,null=True,blank=True)
    laptop_date=models.CharField(max_length=20,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)