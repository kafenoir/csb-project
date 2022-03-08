from django.http import Http404, HttpResponse
from .models import Event, Account, Ticket
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
import logging

logger = logging.getLogger('django')


@login_required
def allEventsView(request):
    events = Event.objects.order_by('-date')
    return render(request, 'index.html', {'events': events})


@login_required
def eventView(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    ntickets = Ticket.objects.filter(
        event_id=event.id).filter(booker_id=1).count()
    logger.info(ntickets)
    return render(request, 'event.html', {'event': event, 'tickets': ntickets})


@login_required
def accountView(request):
    account = Account.objects.get(user=request.user)
    tickets = Ticket.objects.filter(booker=account)
    return render(request, 'account.html', {'tickets': tickets, 'balance': account.funds})


def searchView(request):
    sterm = request.GET.get('search_term')
    #events = Event.objects.filter(name__contains=sterm)
    query = "SELECT * FROM ticketbooker_event WHERE name LIKE '%%%s%%'" % sterm
    events = Event.objects.raw(query)
    return render(request, 'index.html', {'events': events})

@login_required
def purchaseView(request):

    ev = Event.objects.get(id=request.POST.get('event'))
    n = int(request.POST.get('ntickets'))
    logger.info(ev)

    tickets = Ticket.objects.filter(event_id=ev.id).filter(booker_id=1)
    account = Account.objects.get(user_id=request.user.id)

    tleft = tickets.count()

    if tleft < n:
        messages.error(request, 'Not enough tickets.')
        return render(request, 'event.html', {'event': ev, 'tickets': tleft, 'balance': account.funds})

    purchase(account, ev.price, tickets, n)
    messages.success(request, 'Purchase successfull!')
    return render(request, 'event.html', {'event': ev, 'tickets': tleft-n, 'balance': account.funds})


def purchase(account, price, tickets, n):

    account.funds -= price * n

    i = 0
    for t in tickets:
        if i == n:
            break
        t.booker_id = account.id
        t.save()
        i += 1
