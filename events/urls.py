from django.urls import path
from events.views import view_sin_event,home,manager_dashboard,create_event,create_category,create_participants,update_event,delete_event,all_part,update_part,delete_part,all_cat,update_cat,delete_cat

urlpatterns = [
    path('home/',home,name='home'),
    path('manager-dashboard',manager_dashboard,name="manager-dashboard"),
    path('create-event/',create_event,name='create-event'),
    path('create-category/',create_category,name='create-category'),
    path('create-participants/',create_participants,name='create-participants'),
    path('update-event/<int:id>/',update_event,name="update-event"),
    path('update-part/<int:id>/',update_part,name="update-part"),
    path('update-cat/<int:id>/',update_cat,name="update-cat"),
    path('delete-event/<int:id>/',delete_event,name="delete-event"),
    path('delete-part/<int:id>/',delete_part,name="delete-part"),
    path('delete-cat/<int:id>/',delete_cat,name="delete-cat"),
    path('event-detail/<int:id>/',view_sin_event,name="event-detail"),
    path('all-participants/',all_part,name="all-part"),
    path('all-categories/',all_cat,name="all-cat")
]
