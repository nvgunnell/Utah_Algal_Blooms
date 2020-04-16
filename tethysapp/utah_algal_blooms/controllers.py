from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import MapView, Button, TextInput, DatePicker, SelectInput, DataTableView, MVDraw, MVView
from tethys_sdk.workspaces import app_workspace
from .model import add_new_bloom, get_all_blooms

@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    new_bloom_button = Button(
        display_text='New Bloom',
        name='new_bloom-button',
        icon='glyphicon glyphicon-plus',
        style='success',
        href=reverse('utah_algal_blooms:new_bloom')
    )

    context = {
        'new_bloom_button': new_bloom_button
    }

    return render(request, 'utah_algal_blooms/home.html', context)


@app_workspace
@login_required()
def new_bloom(request, app_workspace):
    """
    Controller for the background page.
    """
    #Default Values
    location = ''
    type = 'Lake'
    severity = ''
    date = ''
    mapdraw = ''

    #Errors
    location_error = ''
    type_error = ''
    severity_error = ''
    date_error = ''
    mapdraw_error = ''

    #Handle form submission
    if request.POST and 'add-button' in request.POST:
        #Get values
        has_errors = False
        location = request.POST.get('location', None)
        type = request.POST.get('type', None)
        severity = request.POST.get('severity', None)
        date = request.POST.get('date', None)
        mapdraw = request.POST.get('geometry', None)

        #validate
        if not location:
            has_errors = True
            location_error = 'Location is required.'

        if not type:
            has_errors = True
            type_error = 'Type is required.'

        if not severity:
            has_errors = True
            severity_error = 'Severity is required.'

        if not date:
            has_errors = True
            date_error = 'Date is required.'

        if not mapdraw:
            has_errors = True
            mapdraw_error = 'Must draw location on map.'

        if not has_errors:
            add_new_bloom(db_directory=app_workspace.path, mapdraw=mapdraw, location=location, type=type, severity=severity, date=date)
            return redirect(reverse('utah_algal_blooms:home'))

        messages.error(request, "Please fix errors.")


    # Define form gizmos
    location_input = TextInput(
        display_text='Location',
        name='location',
        placeholder='e.g.: Utah Lake',
        initial=location,
        error=location_error
    )

    type_input = SelectInput(
        display_text='Water Body Type',
        name='type',
        multiple=False,
        options=[('Lake', 'Lake'), ('Reservoir', 'Reservoir'), ('Other', 'Other')],
        initial=type,
        error=type_error
    )

    severity_input = SelectInput(
        display_text='Severity',
        name='severity',
        multiple=False,
        options=[('Low','Low'),('Moderate','Moderate'),('High','High'),('Extreme','Extreme')],
        initial=severity,
        error=severity_error
    )

    date = DatePicker(
        name='date',
        display_text='Date of Appearance',
        autoclose=True,
        format='MM d, yyyy',
        start_view='decade',
        today_button=True,
        initial=date,
        error=date_error
    )

    initial_view = MVView(
        projection='EPSG:4326',
        center=[-98.6, 39.8],
        zoom=3.5
    )

    drawing_options = MVDraw(
        controls=['Modify', 'Delete', 'Move', 'Point'],
        initial='Point',
        output_format='GeoJSON',
        point_color='#FF0000'
    )

    mapdraw_input = MapView(
        height='300px',
        width='100%',
        basemap='OpenStreetMap',
        draw=drawing_options,
        view=initial_view
    )


    add_button = Button(
        display_text='Add',
        name='add-button',
        icon='glyphicon glyphicon-plus',
        style='success',
        attributes={'form': 'add-bloom-form'},
        submit=True
    )
    cancel_button = Button(
        display_text='Cancel',
        name='cancel-button',
        href=reverse('utah_algal_blooms:home')
    )
    context = {
        'location_input': location_input,
        'type_input': type_input,
        'severity_input': severity_input,
        'date_input': date,
        'mapdraw_input': mapdraw_input,
        'mapdraw_error': mapdraw_error,
        'add_button': add_button,
        'cancel_button': cancel_button,
    }

    return render(request,'utah_algal_blooms/new_bloom.html',context)


@app_workspace
@login_required()
def list_blooms(request, app_workspace):
    """
    Show all blooms in a table view.
    """
    blooms = get_all_blooms(app_workspace.path)
    table_rows = []

    for blooms in blooms:
        table_rows.append(
            (
                blooms['location'], blooms['type'],
                blooms['severity'], blooms['date']
            )
        )

    blooms_table = DataTableView(
        column_names=('Location', 'Type', 'Severity', 'Date of Appearance'),
        rows=table_rows,
        searching=False,
        orderClasses=False,
        lengthMenu=[ [10, 25, 50, -1], [10, 25, 50, "All"] ],
    )

    context = {
        'blooms_table': blooms_table
    }

    return render(request, 'utah_algal_blooms/list_blooms.html', context)


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