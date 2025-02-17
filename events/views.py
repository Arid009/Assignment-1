from django.shortcuts import render,redirect
from events.models import Event,Participant,Category
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count,Q
from events.forms import EventModelForm,CategoryForm,ParticipantForm


# Create your views here.

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

def manager_dashboard(request):
    all_events = Event.objects.select_related('category').prefetch_related('participants').all()
    curr_date = timezone.now()
    total_people = Participant.objects.count()

    type = request.GET.get('type','today')

    base_query = Event.objects.select_related('category').prefetch_related('participants')

    if type == 'previous':
        all_events = base_query.filter(date__lt=curr_date)
    elif type == 'upcoming':
        all_events = base_query.filter(date__gt=curr_date)
    elif type == 'today':
        all_events = base_query.filter(date=curr_date)
    elif type=='all':
        all_events = base_query.all()

    counts = Event.objects.aggregate(
        upcoming = Count('id',filter=Q(date__gt=curr_date)),
        previous = Count('id',filter=Q(date__lt=curr_date)),
        total = Count('id')
    )

    context={
        'all_events': all_events,
        'counts':counts,
        'total_people':total_people
    }
    return render(request,'manager_dashboard.html',context)

def all_part(req):
    all_part = Participant.objects.all()
    context={
        'all_part':all_part
    }
    return render(req,'participants.html',context)

def all_cat(req):
    all_cat = Category.objects.all()
    context={
        'all_cat':all_cat
    }
    return render(req,'categories.html',context)

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

def update_part(request,id):
    part = Participant.objects.get(id=id)
    part_form = ParticipantForm(instance=part)
    print(part)

    if request.method == "POST":
        part_form = ParticipantForm(request.POST, instance=part)
        if part_form.is_valid():
            part_form.save()
            messages.success(request, "Part Updated Successfully")
            return redirect('all-part')

    context = {"participants_form": part_form}
    return render(request, "part_form.html", context)

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

def delete_part(request, id):
    if request.method == 'POST':
        part = Participant.objects.get(id=id)
        part.delete()
        messages.success(request, 'Part Deleted Successfully')
        return redirect('all-part')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('all-part')

def delete_cat(request, id):
    if request.method == 'POST':
        cat = Category.objects.get(id=id)
        cat.delete()
        messages.success(request, 'Cart Deleted Successfully')
        return redirect('all-cat')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('all-cat')

def delete_event(request, id):
    if request.method == 'POST':
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request, 'Event Deleted Successfully')
        return redirect('manager-dashboard')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('manager-dashboard')

def view_sin_event(req,id):    
    event = Event.objects.prefetch_related('participants').get(id=id)

    participants = event.participants.all()
    # print(participants)
    context = {
        'event':event,
        'participants':participants

    }
    return render(req,'event_detail.html',context)

def create_event(request):
    if request.method == "POST":
        event_form = EventModelForm(request.POST)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event Created Successfully")
            return redirect('create-event')
    else:
        event_form = EventModelForm()

    context = {"event_form": event_form}
    return render(request, "event_form.html", context)

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

def create_participants(request):
    if request.method == "POST":
        participants_form = ParticipantForm(request.POST)
        if participants_form.is_valid():
            participants_form.save()
            messages.success(request, "Participants Created Successfully")
            return redirect('create-participants')
    else:
        participants_form = ParticipantForm()

    context = {"participants_form": participants_form}
    return render(request, "part_form.html", context)