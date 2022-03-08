from django.urls import path

from .views import allEventsView, eventView, accountView, searchView, purchaseView

urlpatterns = [
    path('', allEventsView, name='events'),
    path('events/<int:event_id>/', eventView, name='event'),
    path('account/', accountView, name='account'),
    path('search/', searchView, name='search'),
    path('purchase/', purchaseView, name='purchase')
]
