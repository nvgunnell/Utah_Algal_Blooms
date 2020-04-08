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