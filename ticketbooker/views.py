from django.http import Http404, HttpResponse
from .models import Event, Account, Ticket
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.db import connection

@login_required
def allEventsView(request):
    events = Event.objects.order_by('-date')
    return render(request, 'index.html', {'events': events})

@login_required
def eventView(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    ntickets = Ticket.objects.filter(id=event_id).filter(booker=1).count()
    return render(request, 'event.html', {'event': event, 'tickets': ntickets})

@login_required
def accountView(request):
    account = Account.objects.get(user=request.user)
    tickets = Ticket.objects.filter(booker=account)
    return render(request, 'account.html', {'tickets': tickets})

def searchView(request):
    sterm=request.GET.get('search_term')
    #events = Event.objects.filter(name__contains=sterm)
    query = "SELECT * FROM ticketbooker_event WHERE name LIKE '%%%s%%'" % sterm
    events = Event.objects.raw(query)
    return render(request, 'index.html', {'events': events})
 


