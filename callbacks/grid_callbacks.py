import time

import pandas as pd
from dash import Input, Output, State, ctx, no_update
from dash.exceptions import PreventUpdate

import source.example_grids as example_grids
import source.objects as objects
import source.stylesheets as stylesheets
from source.layout import menu_objects
from source.modules import (calculate_power_flow, connection_allowed,
                            generate_grid_object, get_connected_edges,
                            get_last_id)


def grid_callbacks(app):
    @app.callback(Output('store_flow_data', 'data'),
                  Output('graph_image', 'style'),
                  Output('graph_image', 'src'),
                  Output('alert_externalgrid', 'children'),
                  Output('alert_externalgrid', 'hide'),
                  Output('tabs_menu', 'value'),
                  Output('cyto1', 'stylesheet'),
                  Output('timestep_slider', 'max'),
                  Output('store_edge_labels', 'data'),
                  Output('store_notification2', 'data'),
                  Input('button_calculate', 'n_clicks'),
                  Input('timestep_slider', 'value'),
                  State('store_flow_data', 'data'),
                  State('cyto1', 'elements'),
                  State('store_grid_object_dict', 'data'),
                  State('tabs_main', 'value'),
                  prevent_initial_call=True)
    def start_calculation_grid(btn, slider, flow, elements, gridObject_dict, tabs_main):
        try:
            if tabs_main == 'grid':
                triggered_id = ctx.triggered_id
                if triggered_id == 'button_calculate':
                    df_flow, labels, format_img_src = calculate_power_flow(elements, gridObject_dict)
                    df_flow_json = df_flow.to_json(orient='index')
                    img_src = 'data:image/png;base64,{}'.format(format_img_src)
                    return df_flow_json, {'display': 'block'}, img_src, no_update, no_update, 'results', \
                           stylesheets.cyto_stylesheet_calculated, len(df_flow.index), labels, no_update
                elif triggered_id == 'timestep_slider':
                    df_flow = pd.read_json(flow, orient='index')
                    labels = df_flow.loc[slider - 1].to_dict()
                    if df_flow.loc[slider - 1, 'external_grid'].item() > 0:
                        text_alert = "Es werden " + str(
                            abs(df_flow.loc[slider - 1, 'external_grid'].item())) + " kW an das Netz abgegeben."
                    else:
                        text_alert = "Es werden " + str(
                            abs(df_flow.loc[slider - 1, 'external_grid'].item())) + " kW aus dem Netz bezogen."
                    return no_update, no_update, no_update, text_alert, False, no_update, no_update, no_update, labels, no_update
                else:
                    raise PreventUpdate
            else:
                raise PreventUpdate
        except PreventUpdate:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, \
                   no_update
        except Exception as err:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, \
                   err.args[0]

    @app.callback(Output('cyto1', 'elements'),  # Callback to change elements of cyto
                  Output('store_grid_object_dict', 'data'),
                  Output('start_of_line', 'data'),
                  Output('store_element_deleted', 'data'),
                  Output('store_notification1', 'data'),
                  Output('store_get_voltage', 'data'),
                  Output('modal_voltage', 'opened'),
                  Input('store_add_node', 'data'),
                  Input('cyto1', 'selectedNodeData'),
                  Input('edit_delete_button', 'n_clicks'),
                  Input('button_line', 'n_clicks'),
                  Input('example_button', 'n_clicks'),
                  Input('store_edge_labels', 'data'),
                  Input('button_voltage_hv', 'n_clicks'),
                  Input('button_voltage_lv', 'n_clicks'),
                  State('cyto1', 'elements'),
                  State('store_grid_object_dict', 'data'),
                  State('store_line_edit_active', 'data'),
                  State('start_of_line', 'data'),
                  State('store_selected_element_grid', 'data'),
                  State('store_get_voltage', 'data'),
                  State('tabs_main', 'value'),
                  prevent_initial_call=True)
    def edit_grid(btn_add, node, btn_delete, btn_line, btn_example, labels, button_hv, button_lv, elements,
                  gridObject_dict, btn_line_active, start_of_line, selected_element, node_ids, tabs_main):
        triggered_id = ctx.triggered_id
        if triggered_id == 'button_line':  # Start line edit mode, set 'start_of_line' as None
            return no_update, no_update, None, no_update, no_update, no_update, no_update
        elif triggered_id == 'store_add_node':
            last_id = get_last_id(elements)
            new_gridobject = generate_grid_object(btn_add, 'node' + str(last_id[0] + 1), 'node' + str(last_id[0] + 1))
            image_src = app.get_asset_url('Icons/' + new_gridobject['icon'])
            gridObject_dict[new_gridobject['id']] = new_gridobject
            new_element = {'data': {'id': 'node' + str(last_id[0] + 1)},
                           'position': {'x': 50, 'y': 50}, 'classes': 'node_style',
                           'style': {'background-image': image_src, 'background-color': new_gridobject['ui_color']}}
            elements.append(new_element)
            return elements, gridObject_dict, no_update, no_update, no_update, no_update, no_update
        elif triggered_id == 'cyto1':  # # Node was clicked
            if not node == []:
                if btn_line_active:  # Add-line-mode is on
                    if start_of_line is not None:
                        if connection_allowed(start_of_line[0]['id'], node[0]['id'], gridObject_dict):
                            last_id = get_last_id(elements)
                            return_temp = no_update
                            modal_boolean = False
                            start_object = gridObject_dict[start_of_line[0]['id']]
                            end_object = gridObject_dict[node[0]['id']]
                            if start_object['voltage'] is None and end_object[
                                'voltage'] is None:  # Check if voltage level of connection is defined through one of the components
                                return_temp = [start_object['id'], end_object['id']]
                                modal_boolean = True
                            new_edge = {'data': {'source': start_of_line[0]['id'], 'target': node[0]['id'],
                                                 'id': 'edge' + str(last_id[1] + 1), 'label': 'x'},
                                        'classes': 'line_style'}
                            gridObject_dict[new_edge['data']['id']] = objects.create_LineObject(new_edge['data']['id'],
                                                                                                new_edge['data']['id'])
                            elements.append(new_edge)
                            return elements, gridObject_dict, None, no_update, no_update, return_temp, modal_boolean
                        else:
                            return elements, no_update, None, no_update, "notification_false_connection", no_update, no_update
                    else:
                        return elements, no_update, node, no_update, no_update, no_update, no_update
                else:  # Node is clicked in normal mode
                    raise PreventUpdate
            else:
                raise PreventUpdate
        elif triggered_id == 'edit_delete_button':  # Delete Object
            if tabs_main == 'grid':  # Check if it was clicked in grid mode
                if btn_delete is not None:
                    index = 0
                    for ele in elements:
                        if ele['data']['id'] == selected_element:
                            break
                        index += 1
                    if 'position' in elements[index]:  # Check if it is node
                        connected_edges = get_connected_edges(elements, elements[index])
                        for edge in connected_edges:
                            elements.pop(elements.index(edge))
                    elements.pop(index)
                    del gridObject_dict[selected_element]  # Remove element from grid object dict
                    return elements, gridObject_dict, no_update, selected_element, no_update, no_update, no_update
                else:
                    raise PreventUpdate
            else:
                raise PreventUpdate  # Button was clicked in other mode than grid
        elif triggered_id == 'example_button':
            ele, gridObject_dict = example_grids.simple_grid_timeseries_day(app, 24 * 60)
            return ele, gridObject_dict, no_update, no_update, no_update, no_update, no_update
        elif triggered_id == 'store_edge_labels':  # Set labels of edges with power values
            for edge, label in labels.items():
                for ele in elements:
                    if edge == ele['data']['id']:
                        ele['data']['label'] = str(label)
                        break
            return elements, no_update, no_update, no_update, no_update, no_update, no_update
        elif triggered_id == 'button_voltage_hv':
            for node_id in node_ids:
                obj = gridObject_dict[node_id]
                if obj['object_type'] != "transformer":
                    obj['voltage'] = 20000
            return no_update, gridObject_dict, no_update, no_update, no_update, no_update, False
        elif triggered_id == 'button_voltage_lv':
            for node_id in node_ids:
                obj = gridObject_dict[node_id]
                if obj['object_type'] != "transformer":
                    obj['voltage'] = 400
            return no_update, gridObject_dict, no_update, no_update, no_update, no_update, False
        else:
            raise PreventUpdate

    @app.callback(Output('store_menu_change_tab_grid', 'data'),
                  Output('cyto1', 'tapNodeData'),
                  Output('cyto1', 'tapEdgeData'),
                  Output('store_selected_element_grid', 'data'),
                  Output('store_notification3', 'data'),
                  Input('cyto1', 'tapNodeData'),
                  Input('cyto1', 'tapEdgeData'),
                  Input('edit_save_button', 'n_clicks'),
                  Input('store_element_deleted', 'data'),
                  State('store_grid_object_dict', 'data'),
                  State('store_line_edit_active', 'data'),
                  State('tabs_main', 'value'))
    def edit_grid_objects(node, edge, btn_save, element_deleted, gridObject_dict, btn_line_active, tabs_main):
        try:
            triggered_id = ctx.triggered_id
            triggered = ctx.triggered
            if triggered_id == 'cyto1':
                if triggered[0]['prop_id'] == 'cyto1.tapNodeData':  # Node was clicked
                    if not btn_line_active:
                        return gridObject_dict[node['id']]['object_type'], None, None, node[
                            'id'], no_update  # Reset tapNodeData and tapEdgeData and return type of node for tab in menu
                    else:
                        raise PreventUpdate
                elif triggered[0]['prop_id'] == 'cyto1.tapEdgeData':  # Edge was clicked
                    return gridObject_dict[edge['id']]['object_type'], None, None, edge[
                        'id'], no_update  # Reset tapNodeData and tapEdgeData and return type of edge for tab in menu
                else:
                    raise Exception("Weder Node noch Edge wurde geklickt.")
            elif triggered_id == 'edit_save_button':  # Save button was clicked in the menu
                if tabs_main != 'grid' or btn_save is None:  # If it was clicked in house mode or is None do nothing
                    raise PreventUpdate
                raise PreventUpdate
            elif triggered_id == 'store_element_deleted':
                if element_deleted is not None:
                    return 'empty', None, None, no_update, no_update
                else:
                    return PreventUpdate
            else:
                raise PreventUpdate
        except PreventUpdate:
            return no_update, no_update, no_update, no_update, no_update
        except Exception as err:
            return no_update, no_update, no_update, no_update, err.args[0]

    @app.callback(Output('cyto1', 'autoungrabify'),  # Callback to make Node ungrabbable when adding lines
                  Output('store_line_edit_active', 'data'),
                  Output('button_line', 'variant'),
                  Input('button_line', 'n_clicks'),
                  Input('key_event_listener', 'n_events'),
                  State('key_event_listener', 'event'),
                  State('store_line_edit_active', 'data'),
                  prevent_initial_call=True)
    def edit_mode(btn_line, n_events, event, btn_active):
        triggered_id = ctx.triggered_id
        if triggered_id == 'button_line':
            if not btn_active:
                return True, True, 'light'
            else:
                return False, False, 'filled'
        elif triggered_id == 'key_event_listener':
            if event['key'] == 'Escape' and btn_active:
                return False, False, 'filled'
            else:
                raise PreventUpdate

    @app.callback(Output('store_add_node', 'data'),
                  [Input(object_id[0], 'n_clicks') for object_id in menu_objects],
                  prevent_initial_call=True)
    def button_add_pressed(*args):
        triggered_id = ctx.triggered_id
        if triggered_id == 'button_line':
            raise PreventUpdate
        else:
            return triggered_id#

    @app.callback(Output('cyto1', 'layout'),
                  Output('example_button', 'disabled'),
                  Input('example_button', 'n_clicks'),
                  prevent_initial_call=True)
    def activate_example(btn):
        time.sleep(0.25)
        return {'name': 'cose'}, True