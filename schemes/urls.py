from django.conf.urls import patterns, url
from schemes.views import *


urlpatterns = patterns('',

    
    url(
        regex=r'^student_schemes/$',
        view=Schemes_class_wise_count.as_view(),
        name='student_schemes'
    ),



    url(
        regex=r'^schemes/(?P<cl_id>\d+?)/$',
        view=Student_schemesView.as_view(),
        name='student_schemes_class'
    ),


)
