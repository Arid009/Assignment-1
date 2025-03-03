from django.urls import path
from users.views import sign_up,sign_in,delete_group,sign_out,group_list,activate_user,create_group

urlpatterns = [
    path('sign-up/', sign_up, name='sign-up'),
    path('sign-in/', sign_in, name='sign-in'),
    path('log-out/', sign_out, name='logout'),
    path('activate/<int:user_id>/<str:token>/', activate_user),
    # path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/create-group/', create_group, name='create-group'),
    path('delete-group/<int:id>/',delete_group,name="delete-group"),
    # path('admin/<int:user_id>/assign-role/', assign_role, name='assign-role'),
    path('admin/group-list/', group_list, name='group-list')
]