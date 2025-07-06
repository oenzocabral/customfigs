from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import EventForm
from figures.models import Album

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            return redirect('event_detail', event.id)
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})

def event_list(request):
    events = Event.objects.filter(is_active=True).order_by('-start_date')
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    has_ticket = False
    if request.user.is_authenticated:
        has_ticket = Album.objects.filter(event=event, owner=request.user).exists()
    return render(request, 'events/event_detail.html', {
        'event': event,
        'has_ticket': has_ticket,
    })

@login_required
def buy_ticket(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Check if user already has an album for this event
    if Album.objects.filter(event=event, owner=request.user).exists():
        return redirect('event_detail', event.id)
    
    # In a real app, process payment here
    # For now, just create the album
    Album.objects.create(event=event, owner=request.user)
    return redirect('event_detail', event.id)

