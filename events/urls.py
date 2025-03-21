from django.urls import path
from events.views import DeleteEvent,part_dashboard,view_sin_event,home,dashboard,update_event,delete_part,update_cat,delete_cat,show_opt,no_permission,rsvp_event,organizer_dashboard,CreateEventView,CreateCategoryView,CategoryListView,ParticipantListView

urlpatterns = [
    path('home/',home,name='home'),
    path('dashboard/',dashboard,name="dashboard"),
    path('manager-dashboard/',organizer_dashboard,name="manager-dashboard"),
    path('part-dashboard/',part_dashboard,name="part-dashboard"),
    path('create-event/',CreateEventView.as_view(),name='create-event'),
    path('create-category/',CreateCategoryView.as_view(),name='create-category'),
    path('update-event/<int:id>/',update_event,name="update-event"),
    path('update-cat/<int:id>/',update_cat,name="update-cat"),
    path('delete-event/<int:pk>/',DeleteEvent.as_view(),name="delete-event"),
    path('delete-part/<int:id>/',delete_part,name="delete-part"),
    path('delete-cat/<int:id>/',delete_cat,name="delete-cat"),
    path('event-detail/<int:id>/',view_sin_event,name="event-detail"),
    path('all-participants/',ParticipantListView.as_view(),name="all-part"),
    path('all-categories/',CategoryListView.as_view(),name="all-cat"),
    path('create-see/',show_opt,name="show-opt"),
    path('not-found/',no_permission,name="no-permission"),
    path('events/<int:id>/rsvp/',rsvp_event , name='rsvp_event')
]
