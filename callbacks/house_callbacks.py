from dash import Input, Output, State, ctx, no_update
from dash.exceptions import PreventUpdate

import source.objects as objects


def house_callbacks(app):
    @app.callback(Output('cyto_bathroom', 'elements', allow_duplicate=True),
                  Output('cyto_livingroom', 'elements', allow_duplicate=True),
                  Output('cyto_kitchen', 'elements', allow_duplicate=True),
                  Output('cyto_office', 'elements', allow_duplicate=True),
                  Output('store_device_dict', 'data', allow_duplicate=True),
                  Input('interval_refresh', 'n_intervals'),
                  State('cyto_bathroom', 'elements'),
                  State('cyto_livingroom', 'elements'),
                  State('cyto_kitchen', 'elements'),
                  State('cyto_office', 'elements'),
                  State('store_device_dict', 'data'),
                  prevent_initial_call=True)
    def initial_room_configuration(interval, cyto_bathroom, cyto_livingroom, cyto_kitchen, cyto_office, device_dict):
        # Bathroom elements
        device_dict['house1']['lamp_bathroom'] = objects.create_LampObject(
            'lamp_office', "Bad")  # Add lamp to device dictionary
        device_dict['rooms']['bathroom'] = {}
        device_dict['rooms']['bathroom']['name'] = 'Bad'  # Create roomname
        device_dict['rooms']['bathroom']['devices'] = [
            'lamp_bathroom']  # Create list of devices in office in dictionary
        socket_node = {'data': {'id': 'socket1', 'parent': 'power_strip'}, 'position': {'x': 35, 'y': 175},
                       'classes': 'socket_node_style_on', 'linked_device': 'lamp_bathroom'}
        lamp_node = {'data': {'id': 'lamp_bathroom'}, 'position': {'x': 35, 'y': 25},
                     'classes': 'room_node_style',
                     'style': {'background-image': ['/assets/Icons/icon_bulb.png']}, 'linked_socket': 'socket1'}
        lamp_edge = {'data': {'source': 'socket1', 'target': 'lamp_bathroom'}}
        cyto_bathroom.append(socket_node)
        cyto_bathroom.append(lamp_node)
        cyto_bathroom.append(lamp_edge)

        # Livingroom elements
        device_dict['house1']['lamp_livingroom'] = objects.create_LampObject(
            'lamp_office', "Wohnzimmer")  # Add lamp to device dictionary
        device_dict['rooms']['livingroom'] = {}
        device_dict['rooms']['livingroom']['name'] = 'Wohnzimmer'  # Create roomname
        device_dict['rooms']['livingroom']['devices'] = [
            'lamp_livingroom']  # Create list of devices in office in dictionary
        socket_node = {'data': {'id': 'socket1', 'parent': 'power_strip'}, 'position': {'x': 35, 'y': 175},
                       'classes': 'socket_node_style_on', 'linked_device': 'lamp_livingroom'}
        lamp_node = {'data': {'id': 'lamp_livingroom'}, 'position': {'x': 35, 'y': 25},
                     'classes': 'room_node_style',
                     'style': {'background-image': ['/assets/Icons/icon_bulb.png']}, 'linked_socket': 'socket1'}
        lamp_edge = {'data': {'source': 'socket1', 'target': 'lamp_livingroom'}}
        cyto_livingroom.append(socket_node)
        cyto_livingroom.append(lamp_node)
        cyto_livingroom.append(lamp_edge)

        # Kitchen elements
        device_dict['house1']['lamp_kitchen'] = objects.create_LampObject(
            'lamp_office', "Küche")  # Add lamp to device dictionary
        device_dict['rooms']['kitchen'] = {}
        device_dict['rooms']['kitchen']['name'] = 'Küche'  # Create roomname
        device_dict['rooms']['kitchen']['devices'] = [
            'lamp_kitchen']  # Create list of devices in office in dictionary
        socket_node = {'data': {'id': 'socket1', 'parent': 'power_strip'}, 'position': {'x': 35, 'y': 175},
                       'classes': 'socket_node_style_on', 'linked_device': 'lamp_kitchen'}
        lamp_node = {'data': {'id': 'lamp_kitchen'}, 'position': {'x': 35, 'y': 25},
                     'classes': 'room_node_style',
                     'style': {'background-image': ['/assets/Icons/icon_bulb.png']}, 'linked_socket': 'socket1'}
        lamp_edge = {'data': {'source': 'socket1', 'target': 'lamp_kitchen'}}
        cyto_kitchen.append(socket_node)
        cyto_kitchen.append(lamp_node)
        cyto_kitchen.append(lamp_edge)

        # Office elements
        device_dict['house1']['lamp_office'] = objects.create_LampObject(
            'lamp_office', "Büro")  # Add lamp to device dictionary
        device_dict['rooms']['office'] = {}
        device_dict['rooms']['office']['name'] = 'Büro'  # Create roomname
        device_dict['rooms']['office']['devices'] = [
            'lamp_' + 'office']  # Create list of devices in office in dictionary
        socket_node = {'data': {'id': 'socket1', 'parent': 'power_strip'}, 'position': {'x': 35, 'y': 175},
                       'classes': 'socket_node_style_on', 'linked_device': 'lamp_office'}
        lamp_node = {'data': {'id': 'lamp_office'}, 'position': {'x': 35, 'y': 25},
                     'classes': 'room_node_style',
                     'style': {'background-image': ['/assets/Icons/icon_bulb.png']}, 'linked_socket': 'socket1'}
        lamp_edge = {'data': {'source': 'socket1', 'target': 'lamp_office'}}
        cyto_office.append(socket_node)
        cyto_office.append(lamp_node)
        cyto_office.append(lamp_edge)

        return cyto_bathroom, cyto_livingroom, cyto_kitchen, cyto_office, device_dict
