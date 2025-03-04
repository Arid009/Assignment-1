from django.urls import path
from events.views import view_sin_event,home,dashboard,create_event,create_category,update_event,delete_event,all_part,delete_part,all_cat,update_cat,delete_cat,show_opt,no_permission,rsvp_event,organizer_dashboard

urlpatterns = [
    path('home/',home,name='home'),
    path('dashboard/',dashboard,name="dashboard"),
    path('manager-dashboard/',organizer_dashboard,name="manager-dashboard"),
    path('create-event/',create_event,name='create-event'),
    path('create-category/',create_category,name='create-category'),
    path('update-event/<int:id>/',update_event,name="update-event"),
    path('update-cat/<int:id>/',update_cat,name="update-cat"),
    path('delete-event/<int:id>/',delete_event,name="delete-event"),
    path('delete-part/<int:id>/',delete_part,name="delete-part"),
    path('delete-cat/<int:id>/',delete_cat,name="delete-cat"),
    path('event-detail/<int:id>/',view_sin_event,name="event-detail"),
    path('all-participants/',all_part,name="all-part"),
    path('all-categories/',all_cat,name="all-cat"),
    path('create-see/',show_opt,name="show-opt"),
    path('not-found/',no_permission,name="no-permission"),
    path('events/<int:id>/rsvp/',rsvp_event , name='rsvp_event')
]
