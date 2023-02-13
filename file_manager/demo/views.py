from django.shortcuts import render

# Create your views here.


def index(request):
    template_to_load = 'demo/index.html'
    return render(request, template_to_load, {})


def show_registration(request):
    template_to_load = "demo/documentation.html"
    return render(request, template_to_load, {})


def show_authentication(request):
    template_to_load = "demo/authentication.html"
    return render(request, template_to_load, {})


def show_meeting(request):
    template_to_load = "demo/meeting.html"
    return render(request, template_to_load, {})


def show_contract(request):
    template_to_load = "demo/contractmanagement.html"
    return render(request, template_to_load, {})

def show_voting(request):
    template_to_load = "demo/voting.html"
    return render(request, template_to_load, {})
