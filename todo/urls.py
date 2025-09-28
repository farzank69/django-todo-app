from django.urls import path 
from . import views 


urlpatterns = [ 
    path('signup/', views.signup, name='signup'), 
    path('login/', views.custom_login, name='login'), 
    path('complete/<int:task_id>', views.mark_complete, name='mark_complete'), 
    path('delete/<int:task_id>', views.delete_task, name='delete_task'), 
    path('task/<int:task_id>', views.task_detail, name='task_detail'), 
    path('task/<int:task_id>/update/', views.update_task, name='update_task'), 
    path('send-email/', views.send_email, name='send_email'),
]