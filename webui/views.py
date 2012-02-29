from django.template import Context, loader
from django.http import HttpResponse
from webui.models import *

def welcome(request):
    latest_tickets = Ticket.objects.all().order_by('-date_reported')[:6]
    latest_packages = Package.objects.all().order_by('-date_uploaded')[:6]
    latest_events = Event.objects.all().order_by('-date_created')[:6]
    latest_promotions = User.objects.all().order_by('-date_promoted')[:6]

    return render_to_response('html/index.html', {'latest_poll_list': latest_poll_list})

def detail(request, poll_id):
    return HttpResponse("You're looking at poll %s." % poll_id)

def results(request, poll_id):
    return HttpResponse("You're looking at the results of poll %s." % poll_id)

def vote(request, poll_id):
    return HttpResponse("You're voting on poll %s." % poll_id)
