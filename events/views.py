from django.shortcuts import render,redirect
from events.models import Event,Category
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count,Q
from events.forms import EventModelForm,CategoryForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test,permission_required
from users.views import is_admin
from django.utils.decorators import method_decorator
from django.views.generic.edit import DeleteView,CreateView
from django.views.generic import ListView
from django.urls import reverse_lazy

User = get_user_model()


# Create your views here.
@login_required
def show_opt(req):
    return render(req,'opt_create_del.html')

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_participant(user):
    print(user.groups)
    return user.groups.filter(name='Participant').exists()

def no_permission(request):
    return render(request, 'no_permission.html')

def home(req):
    # all_events = Event.objects.select_related('category').prefetch_related('participants').all()

    query = req.GET.get('q','')
    cat = req.GET.get('c','')
    start = req.GET.get('s','')
    end = req.GET.get('e','')
    # date range filter in django

    if query:
        # print(query)
        all_events= Event.objects.select_related('category').prefetch_related('participants').filter(name__icontains=query)
    elif cat:
        all_events =  Event.objects.select_related('category').prefetch_related('participants').filter(category__name__icontains=cat)
    elif start and end:
        all_events = Event.objects.select_related('category').prefetch_related('participants').filter(date__range=[start,end])
    else:
        all_events = Event.objects.select_related('category').prefetch_related('participants').all()

    context={
        'all_events': all_events
    }
    return render(req,'home.html',context)


def organizer_dashboard(request):
    all_events = Event.objects.select_related('category').prefetch_related('participants').all()
    curr_date = timezone.now()
    total_people = User.objects.count()
    user=request.user

    type = request.GET.get('type','today')

    base_query = Event.objects.select_related('category').prefetch_related('participants')

    if type == 'previous':
        all_events = base_query.filter(date__lt=curr_date)
    elif type == 'upcoming':
        all_events = base_query.filter(date__gt=curr_date)
    elif type == 'today':
        all_events = base_query.filter(date=curr_date)
    elif type == 'rsvp':
        all_events = base_query.filter(participants=user)
    elif type=='all':
        all_events = base_query.all()

    counts = Event.objects.aggregate(
        upcoming = Count('id',filter=Q(date__gt=curr_date)),
        previous = Count('id',filter=Q(date__lt=curr_date)),
        total = Count('id')
    )
    
    rsvp = Event.objects.filter(participants=user).count()

    context={
        'all_events': all_events,
        'counts':counts,
        'total_people':total_people,
        'rsvp_count':rsvp
    }
    return render(request,'manager_dashboard.html',context)

def part_dashboard(request):
    all_events = Event.objects.select_related('category').prefetch_related('participants').all()
    curr_date = timezone.now()
    user=request.user

    type = request.GET.get('type','today')

    base_query = Event.objects.select_related('category').prefetch_related('participants')

    if type == 'previous':
        all_events = base_query.filter(date__lt=curr_date)
    elif type == 'upcoming':
        all_events = base_query.filter(date__gt=curr_date)
    elif type == 'today':
        all_events = base_query.filter(date=curr_date)
    elif type == 'rsvp':
        all_events = base_query.filter(participants=user)
    elif type=='all':
        all_events = base_query.all()

    counts = Event.objects.aggregate(
        upcoming = Count('id',filter=Q(date__gt=curr_date)),
        previous = Count('id',filter=Q(date__lt=curr_date)),
        total = Count('id')
    )
    
    rsvp = Event.objects.filter(participants=user).count()

    context={
        'all_events': all_events,
        'counts':counts,
        'rsvp_count':rsvp
    }
    return render(request,'part_dashboard_detail.html',context)

@user_passes_test(is_admin,login_url='no-permission')
def all_part(req):
    all_part = User.objects.all()
    context={
        'all_part':all_part
    }
    return render(req,'participants.html',context)

view_participant_decorators = [login_required, permission_required(
    "events.view_participant", login_url='no-permission')]

@method_decorator(view_participant_decorators,name='dispatch')
class ParticipantListView(ListView):
    model = User
    template_name = 'participants.html'
    context_object_name = 'all_part'

view_category_decorators = [login_required, permission_required(
    "events.view_category", login_url='no-permission')]

@method_decorator(view_category_decorators,name='dispatch')
class CategoryListView(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'all_cat'

@login_required
@permission_required("events.view_category", login_url='no-permission')
def all_cat(req):
    all_cat = Category.objects.all()
    context={
        'all_cat':all_cat
    }
    return render(req,'categories.html',context)

@login_required
@permission_required("events.change_event", login_url='no-permission')
def update_event(request,id):
    event = Event.objects.get(id=id)
    event_form = EventModelForm(instance=event)

    if request.method == "POST":
        event_form = EventModelForm(request.POST, instance=event)
        

        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event Updated Successfully")
            return redirect('manager-dashboard')

    context = {"event_form": event_form}
    return render(request, "event_update_form.html", context)

@login_required
@permission_required("events.change_category", login_url='no-permission')
def update_cat(request,id):
    cat = Category.objects.get(id=id)
    cat_form = CategoryForm(instance=cat)
    print(cat)

    if request.method == "POST":
        cat_form = CategoryForm(request.POST, instance=cat)
        if cat_form.is_valid():
            cat_form.save()
            messages.success(request, "Category Updated Successfully")
            return redirect('all-cat')

    context = {"category_form": cat_form}
    return render(request, "category_form.html", context)

@user_passes_test(is_admin,login_url='no-permission')
def delete_part(request, id):
    if request.method == 'POST':
        part = User.objects.get(id=id)
        part.delete()
        messages.success(request, 'Part Deleted Successfully')
        return redirect('all-part')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('all-part')

@login_required
@permission_required("events.delete_category", login_url='no-permission')
def delete_cat(request, id):
    if request.method == 'POST':
        cat = Category.objects.get(id=id)
        cat.delete()
        messages.success(request, 'Cart Deleted Successfully')
        return redirect('all-cat')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('all-cat')

@login_required
@permission_required("events.delete_event", login_url='no-permission')
def delete_event(request, id):
    if request.method == 'POST':
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request, 'Event Deleted Successfully')
        return redirect('manager-dashboard')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('manager-dashboard')

delete_event_decorators = [login_required, permission_required(
    "events.delete_event", login_url='no-permission')]

@method_decorator(delete_event_decorators,name='dispatch')
class DeleteEvent(DeleteView):
    model = Event
    success_url = reverse_lazy("dashboard")

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Event Deleted Successfully')
        return super().delete(request, *args, **kwargs)


def view_sin_event(req,id):    
    event = Event.objects.prefetch_related('participants').get(id=id)

    participants = event.participants.all()
    # print(participants)
    context = {
        'event':event,
        'participants':participants

    }
    return render(req,'event_detail.html',context)

@login_required
@permission_required("events.add_event", login_url='no-permission')
def create_event(request):
    if request.method == "POST":
        event_form = EventModelForm(request.POST,request.FILES)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event Created Successfully")
            return redirect('home')
    else:
        event_form = EventModelForm()

    context = {"event_form": event_form}
    return render(request, "event_form.html", context)

create_event_decorators = [login_required, permission_required(
    "events.add_event", login_url='no-permission')]

@method_decorator(create_event_decorators,name='dispatch')
class CreateEventView(CreateView):
    model = Event
    form_class = EventModelForm
    template_name = 'event_form.html'
    success_url = reverse_lazy("dashboard")
    context_object_name = 'form'

    def form_valid(self, form):
        messages.success(self.request, "Event Created Successfully")
        return super().form_valid(form)

create_category_decorators = [login_required, permission_required(
    "events.add_category", login_url='no-permission')]

@method_decorator(create_category_decorators,name='dispatch')
class CreateCategoryView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_form.html'
    success_url = reverse_lazy("dashboard")
    context_object_name = 'form'

    def form_valid(self, form):
        messages.success(self.request, "Category Created Successfully")
        return super().form_valid(form)


@login_required
@permission_required("events.add_category", login_url='no-permission')
def create_category(request):
    if request.method == "POST":
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            messages.success(request, "Category Created Successfully")
            return redirect('home')
    else:
        category_form = CategoryForm()

    context = {"category_form": category_form}
    return render(request, "category_form.html", context)

@login_required
def rsvp_event(request, id):
    event = Event.objects.get(id=id)
    user = request.user
    rsvped=False
    
    # Check if user is already a participant
    if user in event.participants.all():
        messages.error(request, "You have RSVP Once")
        return redirect('home') 

    event.participants.add(user)

    messages.success(request, "You have RSVP")
    
    return redirect('home') 

@login_required
def dashboard(request):
    if is_organizer(request.user):
        return redirect('manager-dashboard')
    elif is_admin(request.user):
        return redirect('manager-dashboard')
    elif is_participant(request.user):
        return redirect('part-dashboard')
    return redirect('no-permission')