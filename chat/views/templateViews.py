# imports
from django.shortcuts import render
# rest framework imports


# Create your views here.
# testing urls


def index(request):
    return render(request, 'index.html', {})


def personal(request, msg_from, msg_to):
    return render(request, 'personal.html', {
        'msg_from': msg_from,
        'msg_to': msg_to,
    })


def group(request, msg_from, grp):
    return render(request, 'group.html', {
        'msg_from': msg_from,
        'grp': grp,
    })


def room(request, msg_from, msg_to):
    return render(request, 'room.html', {
        'msg_from': msg_from,
        'msg_to': msg_to,
    })


def special(request, msg_from, msg_to):
    return render(request, 'special.html', {
        'msg_from': msg_from,
        'msg_to': msg_to,
    })


def info(request, msg_from, msg_to):
    return render(request, 'info.html', {
        'msg_from': msg_from,
        'msg_to': msg_to,
    })
