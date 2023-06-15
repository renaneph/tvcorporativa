from django.urls import path
from . import views

urlpatterns = [
    path('visual-content/register/', views.register_content, name='register-content'),
    path('visual-content/list-contents/', views.table_contents, name='table-contents'),
    path('visual-content/delete/<int:id>', views.deletecontent, name='delete-content'),
    path('visual-content/edit/<int:id>', views.editcontent, name='edit-content'),
    path('list-campaigns/', views.table_campaigns, name='table-campaigns'),
    path('register/', views.register_campaign, name='register-campaign'),
    path('delete/<int:id>', views.deletecampaign, name='delete-campaign'),
    path('edit/<int:id>', views.editcampaign, name='edit-campaign'),
    path('list-content-campaign/<int:id>', views.contentcampaign, name='contents-campaign'),
    path('approval-campaigns/', views.table_approval_campaigns, name='approval-campaigns'),
    path('approval-campaigns/approved/<int:id>', views.approved_campaign, name='approved-campaign'),
    path('approval-campaigns/disapproved/<int:id>', views.disapproved_campaign, name='disapproved-campaign'),
]
