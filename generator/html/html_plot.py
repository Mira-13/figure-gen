import json

template = """
<script>
var ctx = document.getElementById('__canvas_id__').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        datasets:[ __data_sets__ ],
    },
    options: {
        responsive: true,
        scales: {
            xAxes: [{
			    display: true,
                type: '__x_scale__',
			}],
			yAxes: [{
				display: true,
				type: '__y_scale__',
			}]
        }
    }
});
</script>
"""

template = """
<script>
var ctx = document.getElementById('__canvas_id__').getContext('2d');
var color = Chart.helpers.color;
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        datasets: [__data_sets__],
    },
    options: {
        legend: {
            display: false,
        },
        responsive: true,
        scales: {
            x: {
                scaleLabel: {
                    labelString: "__x_label__",
                    display: __has_x_label__,
                    align: "center",
                    fontSize: __fontsize__,
                    padding: 0
                },
                gridLines: {
                    color: 'rgba(0, 0, 0, 0.1)', 
                    display: true, 
                    borderColor: "black",
                    tickMarkLength: 4,
                    borderWidth: 1,
                    lineWidth: 0.5
                },
			    display: true,
                type: '__x_scale__',
                min: __x_min_value__,
                max: __x_max_value__,
                ticks: {
                    source: 'data',
                    fontSize: __fontsize__,
                    maxRotation: 0,
                    callback: function(value, index, values) {
                        if (__x_visible_ticks_condition__)
                            return value.toString();
                        else
                            return ""
                    }
                }
			},
			y: {
                scaleLabel: {
                    labelString: "__y_label__",
                    display: __has_y_label__,
                    align: "center",
                    fontSize: __fontsize__,
                    padding: 0
                },
                gridLines: {
                    color: 'rgba(0, 0, 0, 0.1)', 
                    display: true, 
                    borderColor: "black",
                    offsetGridLines: false,
                    tickMarkLength: 4,
                    borderWidth: 1,
                    lineWidth: 0.5
                },
                min: __y_min_value__,
                max: __y_max_value__,
				display: true,
				type: '__y_scale__',
                ticks: {
                    fontSize: __fontsize__,
                    callback: function(value, index, values) {
                        if (__y_visible_ticks_condition__)
                            return value.toString();
                        else
                            return ""
                    }
                }
			}
        }
    }
});
</script>
"""

def rgb_to_rgba(color):
    return 'rgba('+str(color[0])+', '+str(color[1])+', '+str(color[2])+', 1.0)'

def tick_condition(module_data, axis):
    condition = ''
    valid_values = module_data['axis_properties'][axis]['ticks'] 
    for value in valid_values:
        condition += 'value=='+str(value)+'||'
    condition += 'false'
    return condition

def create_data_string(module_data):
    datastr = ''
    data_idx = 0
    for data in module_data["data"]:
        datastr += '{'

        datastr += 'pointRadius:0, '
        datastr += 'borderWidth:1, '
        #datastr += 'label: "test label", '
        datastr += 'backgroundColor: "rgba(0,0,0,0)", '
        datastr += 'borderColor: "'+ rgb_to_rgba(module_data['plot_color'][data_idx]) +'", '

        datastr += 'data: ['
        for i in range(len(data[0])):
            x = data[0][i]
            y = data[1][i]
            datastr += '{'
            datastr += f'x:{x},'
            datastr += f'y:{y}'
            datastr += '},'
        datastr += ']},'
        data_idx += 1
    return datastr

def get_label(module_data, axis):
    try:
        label = module_data['axis_labels'][axis]['text']
    except:
        return ''
    return label.replace('\n', ' ')

def check_for_axis_label(module_data, axis):
    label = get_label(module_data, axis)
    if label == '':
        return 'false'
    return 'true'

def get_axis_range(module_data, axis):
    return module_data['axis_properties'][axis]['range']

def axis_type(module_data, axis):
    if module_data['axis_properties'][axis]['use_log_scale']:
        return 'logarithmic'
    return 'linear'

def create_replacement_table(module_data, module_idx):
    return {
        "__canvas_id__": "canvas-"+str(module_idx),
        "__data_sets__": create_data_string(module_data),
        "__x_scale__": axis_type(module_data, 'x'),
        "__y_scale__": axis_type(module_data, 'y'),
        "__x_label__": get_label(module_data, 'x'),
        "__has_x_label__": check_for_axis_label(module_data, 'x'),
        "__y_label__": get_label(module_data, 'y'),
        "__has_y_label__": check_for_axis_label(module_data, 'y'),
        "__fontsize__": str(module_data['plot_config']['font']['fontsize_pt']),
        "__x_min_value__": str(get_axis_range(module_data, 'x')[0]),
        "__x_max_value__": str(get_axis_range(module_data, 'x')[1]),
        "__y_min_value__": str(get_axis_range(module_data, 'y')[0]),
        "__y_max_value__": str(get_axis_range(module_data, 'y')[1]),
        "__x_visible_ticks_condition__": tick_condition(module_data, 'x'),
        "__y_visible_ticks_condition__": tick_condition(module_data, 'y'),
    }

def create_canvas(module_data, module_idx):
    c = '<canvas id="canvas-'+str(module_idx)+'"'
    width = module_data['total_width']
    height = module_data['total_height']
    w_a_h = ' style="width:'+str(width)+'mm; height:'+str(height)+'mm;"'
    return c + w_a_h + '></canvas>\n'

def create_script(module_data, module_idx):
    table = create_replacement_table(module_data, module_idx)

    result = template
    for (placeholder, value) in table.items():
        result = result.replace(placeholder, value)

    return result