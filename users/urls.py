from django.urls import path, reverse_lazy
from users.views import sign_up,sign_in,delete_group,sign_out,group_list,activate_user,create_group,assign_role,ProfileView,EditProfileView,ChangePassword,CustomPasswordResetConfirmView,CustomPasswordResetView
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView

urlpatterns = [
    path('sign-up/', sign_up, name='sign-up'),
    path('sign-in/', sign_in, name='sign-in'),
    path('log-out/', LogoutView.as_view(next_page = reverse_lazy('home')), name='logout'),
    path('activate/<int:user_id>/<str:token>/', activate_user),
    # path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/create-group/', create_group, name='create-group'),
    path('delete-group/<int:id>/',delete_group,name="delete-group"),
    path('admin/<int:user_id>/assign-role/', assign_role, name='assign-role'),
    path('admin/group-list/', group_list, name='group-list'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile'),
    path('password-change/', ChangePassword.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'), name='password_change_done'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/',
         CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]