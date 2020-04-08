from django.shortcuts import render
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import Button

@login_required()
def home(request):
    """
    Controller for the app home page.
    """

    context = {

    }

    return render(request, 'utah_algal_blooms/home.html', context)


@login_required()
def info(request):
    """
    Controller for the background page.
    """
    context = {}

    return render(request,'utah_algal_blooms/info.html',context)


@login_required()
def help(request):
    """
    Controller for the background page.
    """
    context = {}

    return render(request,'utah_algal_blooms/help.html',context)