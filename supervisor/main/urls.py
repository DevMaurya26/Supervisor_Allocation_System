from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('allocation/', views.generated, name='list'),
    path('file/<str:file_name>', views.download, name='file_res'),
    path('change_request/<str:data>',views.change_req, name='change_req'),
    path('your_change_req',views.user_change_req,name='your_change_req'),
    path('admin_decision/<int:decision>/<req_id>',views.admin_aprove_reject,name='admin_decision'),
    path('staff_list/<str:institute>',views.staff,name='staff_list'),
    path('staff_remove/<user_id>',views.remove_staff,name='staff_remove')
]