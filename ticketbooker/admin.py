from django.contrib import admin

from .models import Account, Event, Ticket

admin.site.register(Account)
admin.site.register(Event)
admin.site.register(Ticket)
