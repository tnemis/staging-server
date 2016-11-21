from django.conf.urls import patterns, url,include
from django.contrib.auth.decorators import login_required
from teachers.views.teacher_main_views import *

urlpatterns = patterns('', 

    url(
        regex=r'^teachers_school_level_name_list/(?P<pk>\d+?)/$',
        view=Teachers_school_level_name_list.as_view(),
        name='teachers_school_level_name_list'
    ),
    url(
       regex=r'^teacher_promotion/(?P<pk>\d+?)/$',
       view=teacher_promotion.as_view(),
       name='teacher_promotion'
   ),
    
    url(
        regex=r'^teachers_unique_id_generation/$',
        view=Teachers_unique_id_generation.as_view(),
        name='Teachers_unique_id_generation'
    ),

    url(
        regex=r'^teachers_block_level_reports/$',
        view=Teachers_block_level_reports.as_view(),
        name='teachers_block_level_reports'
    ),

    url(
       regex=r'^download_staff_list/$',
       view=download_staff_list.as_view(),
       name='download_staff_list'
   ),

   
    url(
        regex=r'^teacher_new_entry/(?P<code>\d+?)/(?P<office_code>\d+?)/$',
        view=Teacher_new_entry.as_view(),
        name='teacher_new_entry'
    ),
    url(
        regex=r'^teacher_registration/$',
        view=Teacher_registration.as_view(),
        name='teacher_registration'
    ),

    url(
        regex=r'^teacher_personnel_entry/$',
        view=Teacher_personnel_entry.as_view(),
        name='teacher_personnel_entry'
    ),

    
    url(
        regex=r'^teacher_entry_details/(?P<pk>\d+?)/$',
        view=Teacher_entry_details.as_view(),
        name='teacher_entry_details'
    ),


    url(
       regex=r'^teacher_personnel_entry_after/(?P<pk>\d+?)/$',
       view=Teacher_personnel_entry_after.as_view(),
       name='teacher_personnel_entry_after'
   ),


    

    url(
        regex=r'^teacher_update/(?P<pk>\d+?)/$',
        view=Teacher_update.as_view(),
        name='teacher_update'
    ),
    

    url(
        regex=r'^teacher_delete/(?P<pk>\d+?)/$',
        view=Teacher_delete.as_view(),
        name='teacher_delete'
    ),

        
  
    url(
            regex=r'^avail_teac_namelist/(?P<pk>\d+?)/$',
            view=avail_teac_namelist.as_view(),
            name='avail_teac_namelist'
        ),
    url(
            regex=r'^avail_teac_namelist/(?P<pk>\d+?)/(?P<school_code>\d+?)/$',
            view=avail_teac_namelist.as_view(),
            name='avail_teac_namelist'
        ),

   
    url(
        regex=r'^Teacher_transfer/(?P<pk>\d+?)/school_search10/$',
        view=school_search10.as_view(),
        name='school_search10'
    ),

    url(
        regex=r'^Teacher_transfer/(?P<pk>\d+?)/$',
        view=Teacher_transfer.as_view(),
        name='Teacher_transfer'
    ),

    url(
        regex=r'^Teacher_transfer_parent/(?P<pk>\d+?)/$',
        view=Teacher_transfer_parent.as_view(),
        name='Teacher_transfer_parent'
    ),

    url(
        regex=r'^teacher_transfer_name_list/$',
        view=Teacher_transfer_name_list.as_view(),
        name='teacher_transfer_name_list'
    ),


    url(
        regex=r'^teacher_full_detail_more/(?P<pk>\d+?)/$',
        view=Teacher_full_detail_more.as_view(),
        name='teacher_full_detail_more'
    ),
    url(
        regex=r'^teacher_full_detail_more1/(?P<pk>\d+?)/$',
        view=Teacher_full_detail_more1.as_view(),
        name='teacher_full_detail_more'
    ),

    url(
        regex=r'^teacher_full_detail/(?P<pk>\d+?)/$',
        view=Teacher_full_detail.as_view(),
        name='teacher_full_detail'
    ),

    url(
        regex=r'^teacher_outofservice/(?P<pk>\d+?)/$',
        view=Teacher_outofservice_create.as_view(),
        name='teacher_outofservice'
    ),
url(
        regex=r'^printpdf/(?P<pk>\d+?)/$',
        view=myview.as_view(),
        name='printpdf'
    ),

    )

from teachers.views.teacher_education_views import *
urlpatterns += patterns('',
 
     url(
        regex=r'^teacher_education_create/(?P<pk>\d+?)/$',
        view=Teacher_education_create.as_view(),
        name='teacher_education_create'
    ),
url( 
        regex=r'^teacher_edu_update/(?P<pk>\d+?)/(?P<pk1>\d+?)/$', 
        view=teacher_edu_update.as_view(), 
        name='teacher_edu_update' 
    ), 

    
    
    url(r'^/teachers/views/fetch_id/$','teachers/fetch_id',name='fetch_id'),
)



from teachers.views.teacher_family_detail_views import *
urlpatterns += patterns('',
   
    url( 
        regex=r'^teacher_family_delete/(?P<pk>\d+?)/(?P<pk1>\d+?)/$', 
        view=teacher_family_delete.as_view(), 
        name='teacher_family_delete' 
    ),

   

    url(
        regex=r'^teacher_family_create/(?P<pk>\d+?)/$',
        view=Teacher_family_create.as_view(),
        name='teacher_family_create'
    ),
 url( 
        regex=r'^teacher_family_update/(?P<pk>\d+?)/(?P<pk1>\d+?)/$', 
        view=teacher_family_update.as_view(), 
        name='teacher_family_update' 
    ), 
)


from teachers.views.teacher_nomini_views import *
urlpatterns += patterns('',
url( 
        regex=r'^teacher_nomini_create/(?P<pk>\d+?)/$', 
        view=Teacher_nomini_create.as_view(), 
        name='teacher_nomini_create' 
    ), 
 url( 
        regex=r'^teacher_nomini_update/(?P<pk>\d+?)/(?P<pk1>\d+?)/$', 
        view=teacher_nomini_update.as_view(), 
        name='teacher_nomini_update' 
    ), 

   
    
    

   

)
from teachers.views.teacher_posting_views import *
urlpatterns += patterns('',

    url(
        regex=r'^teacher_posting_create/(?P<pk>\d+?)/school_search2/$',
        view=school_search2.as_view(),
        name='school_search2'
    ),

     url(
        regex=r'^teacher_posting_update/(?P<pk>\d+?)/(?P<pk1>\d+?)/school_search2/$',
        view=school_search2.as_view(),
        name='school_search2'
    ),
    url(
        regex=r'^teacher_posting_create/(?P<pk>\d+?)/$',
        view=Teacher_posting_create.as_view(),
        name='teacher_posting_create'
    ),
   
    url( 
        regex=r'^teacher_posting_update/(?P<pk>\d+?)/(?P<pk1>\d+?)/$', 
        view=teacher_posting_update.as_view(), 
        name='teacher_posting_update' 
    ), 


)

from teachers.views.teacher_probation_views import *
urlpatterns += patterns('',
    

    url(
        regex=r'^teacher_probation_create/(?P<pk>\d+?)/$',
        view=Teacher_probation_create.as_view(),
        name='teacher_probation_create'
    ),
    url( 
        regex=r'^teacher_probation_update/(?P<pk>\d+?)/(?P<pk1>\d+?)/$', 
        view=teacher_probation_update.as_view(), 
        name='teacher_probation_update' 
    ), 

    

)

from teachers.views.teacher_regularisation_views import *
urlpatterns += patterns('',
    url(
        regex=r'^teacher_regularisation_create/(?P<pk>\d+?)/$',
        view=Teacher_regularisation_create.as_view(),
        name='teacher_regularisation_create'
    ),
    url( 
        regex=r'^teacher_regularisation_update/(?P<pk>\d+?)/(?P<pk1>\d+?)/$', 
        view=teacher_regularisation_update.as_view(), 
        name='teacher_regularisation_update' 
    ), 


    
   


)

from teachers.views.teacher_post_relinquish_views  import *
urlpatterns += patterns('',
   


      url(
        regex=r'^teacher_relinquis_create/(?P<pk>\d+?)/$',
        view=Teacher_relinquis_create.as_view(),
        name='teacher_relinquis_create'
    ),
    url( 
        regex=r'^teacher_relinquis_update/(?P<pk>\d+?)/(?P<pk1>\d+?)/$', 
        view=teacher_relinqui_update.as_view(), 
        name='teacher_relinqui_update' 
    ), 
)






from teachers.views.teacher_action_views import * 
urlpatterns += patterns('', 
    url( 
        regex=r'^teacher_action_create/(?P<pk>\d+?)/$', 
        view=Teacher_action_create.as_view(), 
        name='teacher_action_create' 
    ), 
   
    url( 
        regex=r'^teacher_action_update/(?P<pk>\d+?)/(?P<pk1>\d+?)/$', 
        view=teacher_action_update.as_view(), 
        name='teacher_action_update' 
    ), 

    url( 
        regex=r'^teacher_action_history/(?P<pk>\d+?)/$', 
        view=teacher_action_history.as_view(), 
        name='teacher_action_history' 
    ), 

) 


from teachers.views.teacher_tpf_loan_views import *
urlpatterns += patterns('',
    
    url(
        regex=r'^teacher_tpf_loan_create/(?P<pk>\d+?)/$',
        view=Teacher_tpf_loan_create.as_view(),
        name='teacher_tpf_loan_create'
    ),
    url( 
        regex=r'^teacher_tpf_loan_update/(?P<pk>\d+?)/(?P<pk1>\d+?)/$', 
        view=teacher_tpf_loan_update.as_view(), 
        name='teacher_tpf_loan_update' 
    ), 


 
    

)




from teachers.views.teacher_loan_views import *
urlpatterns += patterns('',
    
    url(
        regex=r'^teacher_loan_create/(?P<pk>\d+?)/$',
        view=Teacher_loan_create.as_view(),
        name='teacher_loan_create'
    ),
    url( 
        regex=r'^teacher_loan_update/(?P<pk>\d+?)/(?P<pk1>\d+?)/$', 
        view=teacher_loan_update.as_view(), 
        name='teacher_loan_update' 
    ), 



 

)


from teachers.views.teacher_ltc_views import *
urlpatterns += patterns('',
    url( 
        regex=r'^teacher_ltc_create/(?P<pk>\d+?)/$', 
        view=Teacher_ltc_create.as_view(), 
        name='teacher_ltc_create' 
    ), 
    url( 
        regex=r'^teacher_ltc_update/(?P<pk>\d+?)/(?P<pk1>\d+?)/$', 
        view=teacher_ltc_update.as_view(), 
        name='teacher_ltc_update' 
    ), 

  
    


)


from teachers.views.teacher_movable_property_views import *
urlpatterns += patterns('',
    url(
        regex=r'^teacher_movable_property_create/(?P<pk>\d+?)/$',
        view=Teacher_movable_property_create.as_view(),
        name='teacher_movable_property_create'
    ),
 url( 
        regex=r'^teacher_movable_update/(?P<pk>\d+?)/(?P<pk1>\d+?)/$', 
        view=teacher_movable_update.as_view(), 
        name='teacher_movable_update' 
    ), 

   
 
    
    url(
        regex=r'^teacher_movable_update/(?P<pk>\d+?)/$',
        view=teacher_movable_update.as_view(),
        name='teacher_movable_update'
    ),


)



from teachers.views.teacher_immovable_property_views import *
urlpatterns += patterns('',

    url(
        regex=r'^teacher_immovable_property_create/(?P<pk>\d+?)/$',
        view=Teacher_immovable_property_create.as_view(),
        name='teacher_immovable_property_create'
    ),
 url( 
        regex=r'^teacher_immovable_update/(?P<pk>\d+?)/(?P<pk1>\d+?)/$', 
        view=teacher_immovable_update.as_view(), 
        name='teacher_immovable_update' 
    ), 
    
  
    

)



from teachers.views.teacher_leave_views import *
urlpatterns += patterns('',



    url(
        regex=r'^teacher_leave_entry_create/(?P<pk>\d+?)/$',
        view=teacher_leave_entry_create.as_view(),
        name='teacher_leave_entry_create'
    ),
  

    url( 
        regex=r'^teacher_leave_update/(?P<pk>\d+?)/(?P<pk1>\d+?)/$', 
        view=teacher_leave_update.as_view(), 
        name='teacher_leave_update' 
    ),
)





from teachers.views.teacher_test_views import *
urlpatterns += patterns('',
    

    url(
        regex=r'^teacher_test_create/(?P<pk>\d+?)/$',
        view=Teacher_test_create.as_view(),
        name='teacher_test_create'
    ),
    url( 
        regex=r'^teacher_test_update/(?P<pk>\d+?)/(?P<pk1>\d+?)/$', 
        view=teacher_test_update.as_view(), 
        name='teacher_test_update' 
    ), 
   
)

from teachers.views.teacher_training_views import *
urlpatterns += patterns('',
    

    url(
        regex=r'^teacher_training_create/(?P<pk>\d+?)/$',
        view=Teacher_training_create.as_view(),
        name='teacher_training_create'
    ),
    url( 
        regex=r'^teacher_training_update/(?P<pk>\d+?)/(?P<pk1>\d+?)/$', 
        view=teacher_training_update.as_view(), 
        name='teacher_training_update' 
    ), 

   

    
)

from teachers.views.teacher_detail_categorywise_views import *
urlpatterns += patterns('',
   url(
       regex=r'^teacher_detailListView/$',
       view=teacher_detailListView.as_view(),
       name='teacher_detailListView'
   ),
   url(
       regex=r'^teacher_detailListView/(?P<cat_id>\d+?)/$',
       view=teacher_detailListView.as_view(),
       name='teacher_detailListView'
   ),
   url(
       regex=r'^staff_detailListView/$',
       view=staff_detailListView.as_view(),
       name='staff_detailListView'
   ), 
url(
       regex=r'^Teacher_detailList/(?P<cat_id>\d+?)/$',
       view=Teacher_detailList.as_view(),
       name='Teacher_detailList'
   ),
url(
       regex=r'^teacher_detailListView1/(?P<cat_id>\d+?)/$',
       view=teacher_detailListView1.as_view(),
       name='teacher_detailListView1'
   ), 
)



from teachers.views.teacher_leave_credit_views import * 
urlpatterns += patterns('', 

    url(
        regex=r'^leave_master_view/(?P<pk>\d+?)/$',
        view=leave_master_view.as_view(),
        name='leave_master_view'
    ),

     url( 
        regex=r'^teacher_leave_credit_create1/(?P<pk>\d+?)/$', 
        view=Teacher_leave_credit_create1.as_view(), 
        name='teacher_leave_credit_create1' 
    ), 
   
    
    url(
        regex=r'^master_db_update/(?P<pk>\d+?)/$',
        view=master_db_update.as_view(),
        name='master_db_update'
    ),
    url( 
        regex=r'^teacher_leave_credit_create/(?P<pk>\d+?)/$', 
        view=Teacher_leave_credit_create.as_view(), 
        name='teacher_leave_credit_create' 
    ), 
    url( 
        regex=r'^teacher_leave_credit_delete/(?P<pk>\d+?)/$', 
        view=Teacher_leave_credit_delete.as_view(), 
        name='teacher_leave_credit_delete' 
    ), 
    url( 
        regex=r'^teacher_leave_credit_update/(?P<pk>\d+?)/(?P<pk1>\d+?)/$', 
        view=teacher_leave_credit_update.as_view(), 
        name='teacher_leave_credit_update' 
    ), 

)


from teachers.views.teacher_leave_surrender_views import * 
urlpatterns += patterns('', 
    url( 
        regex=r'^teacher_leave_surrender_create/(?P<pk>\d+?)/$', 
        view=Teacher_leave_surrender_create.as_view(), 
        name='teacher_leave_surrender_create' 
    ), 

    url( 
        regex=r'^teacher_leave_surrender_update/(?P<pk>\d+?)/(?P<pk1>\d+?)/$', 
        view=teacher_leave_surrender_update.as_view(), 
        name='teacher_leave_surrender_update' 
    ), 

    url( 
        regex=r'^teacher_leave_surrender_delete/(?P<pk>\d+?)/$', 
        view=Teacher_leave_surrender_delete.as_view(), 
        name='teacher_leave_surrender_delete' 
    ), 

)

from teachers.views.teacher_private_teacing_views import *
urlpatterns +=patterns('',
    url(
        regex=r'^private_teachers_create/', 
        view=private_teachers_create.as_view(), 
        name='private_teachers_create'

    ),
    
   
    url(
        regex=r'^pdfprint/(?P<pk>\d+?)/$',
        view=private_teacher_view.as_view(),
        name='pdfprint'
    ),

    url(
        regex=r'^private_teacher_update/(?P<pk>\d+?)/$', 
        view=private_teacher_update.as_view(), 
        name='private_teacher_update'

    ),

    url(
        regex=r'^private_teacher_delete/(?P<pk>\d+?)/$',
        view=private_teacher_delete.as_view(),
        name='private_teacher_delete'
    ),

      url(
        regex=r'^private_teachers_school_level_name_list/', 
        view=private_teachers_school_level_name_list.as_view(), 
        name='private_teachers_school_level_name_list'

    ),
      
     url(
        regex=r'^edu_qualifaction_create/(?P<pk>\d+?)/$', 
        view=edu_qualifaction_create.as_view(), 
        name='edu_qualifaction_create'
    ),

     url( 
        regex=r'^edu_qualifaction_update/(?P<pk>\d+?)/(?P<pk1>\d+?)/$', 
        view=edu_qualifaction_update.as_view(), 
        name='edu_qualifaction_update' 
    ), 

     
     url(
        regex=r'^teacher_full_detail_private/(?P<pk>\d+?)/$',
        view=teacher_full_detail_private.as_view(),
        name='teacher_full_detail_private'
    ),


    ) 

from teachers.views.block_views import *
urlpatterns += patterns('',
    url(
        regex=r'^block_teacher/$',
        view=BlockView_teachers.as_view(),
        name='BlockView_teachers'
    ),

    
    url(
        regex=r'^block_level_list/(?P<blockid>\d+?)/(?P<associateid>\d+?)/$',
        view=block_level_list.as_view(),
        name='block_level_list'
    ),
    
    url(
        regex=r'^district_block_level_list/(?P<blockid>\d+?)/(?P<associateid>\d+?)/$',
        view=district_block_level_list.as_view(),
        name='district_block_level_list'
    ),
)

from teachers.views.exam_camp_duty import *
urlpatterns += patterns('',
    

    url(
        regex=r'^exam_camp_duty_create/(?P<pk>\d+?)/$',
        view=exam_camp_duty_create.as_view(),
        name='exam_camp_duty_create'
    ),
    url( 
        regex=r'^exam_camp_duty_update/(?P<pk>\d+?)/(?P<pk1>\d+?)/$', 
        view=exam_camp_duty_update.as_view(), 
        name='exam_camp_duty_update' 
    ), 

   


    


)

from teachers.views.award_details import *
urlpatterns += patterns('',
    

    url(
        regex=r'^award_create/(?P<pk>\d+?)/$',
        view=award_create.as_view(),
        name='award_create'
    ),
    url( 
        regex=r'^award_update/(?P<pk>\d+?)/(?P<pk1>\d+?)/$', 
        view=award_update.as_view(), 
        name='award_update' 
    ), 




)