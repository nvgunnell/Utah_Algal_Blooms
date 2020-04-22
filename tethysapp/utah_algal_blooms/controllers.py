from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import MapView, Button, TextInput, DatePicker, SelectInput, DataTableView, MVDraw, MVView, MVLayer
from tethys_sdk.workspaces import app_workspace
from .model import add_new_bloom, get_all_blooms

@app_workspace
@login_required()
def home(request, app_workspace):
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
        center=[-110, 39.8],
        zoom=5
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
def map_blooms(request, app_workspace):
    """
    Controller for the background page.
    """

    # Get list of blooms and create blooms MVLayer:
    blooms = get_all_blooms(app_workspace.path)
    features = []
    lat_list = []
    lng_list = []


    # Define GeoJSON Features
    for bloom in blooms:
        bloom_mapdraw = bloom.pop('mapdraw')
        lat_list.append(bloom_mapdraw['coordinates'][1])
        lng_list.append(bloom_mapdraw['coordinates'][0])

        bloom_feature = {
            'type': 'Feature',
            'geometry': {
                'type': bloom_mapdraw['type'],
                'coordinates': bloom_mapdraw['coordinates'],
            }
        }

        features.append(bloom_feature)

    # Define GeoJSON FeatureCollection
    blooms_feature_collection = {
        'type': 'FeatureCollection',
        'crs': {
            'type': 'name',
            'properties': {
                'name': 'EPSG:4326'
            }
        },
        'features': features
    }

    style = {'ol.style.Style': {
        'image': {'ol.style.Circle': {
            'radius': 10,
            'fill': {'ol.style.Fill': {
                'color':  '#d84e1f'
            }},
            'stroke': {'ol.style.Stroke': {
                'color': '#ffffff',
                'width': 1
            }}
        }}
    }}


    # Create a Map View Layer
    blooms_layer = MVLayer(
        source='GeoJSON',
        options=blooms_feature_collection,
        legend_title='Blooms',
        layer_options={'style': style}
    )

    # Define view centered on dam locations
    try:
        view_center = [sum(lng_list) / float(len(lng_list)), sum(lat_list) / float(len(lat_list))]
    except ZeroDivisionError:
        view_center = [-98.6, 39.8]

    view_options = MVView(
        projection='EPSG:4326',
        center=view_center,
        zoom=7,
        maxZoom=18,
        minZoom=2
    )

    algal_bloom_map = MapView(
        height='100%',
        width='100%',
        layers=[blooms_layer],
        basemap='OpenStreetMap',
        view=view_options,
    )

    new_bloom_button = Button(
        display_text='New Bloom',
        name='new_bloom-button',
        icon='glyphicon glyphicon-plus',
        style='success',
        href=reverse('utah_algal_blooms:new_bloom')
    )

    context = {
        'algal_bloom_map': algal_bloom_map,
        'new_bloom_button': new_bloom_button
    }

    return render(request,'utah_algal_blooms/map_blooms.html',context)


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