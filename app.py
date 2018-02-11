from flask import Flask, render_template, jsonify, request
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.sources import AjaxDataSource

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/dashboard/')
def show_dashboard():
    plots = []
    plots.append(make_ajax_plot())
    plots.append(make_plot())

    return render_template('dashboard.html', plots=plots)

x = 0
@app.route('/data/', methods=['POST'])
def data():
    global x
    x += 1
    y = 2**x
    return jsonify(x=x, y=y)

def make_plot():
    plot = figure(plot_height=300, sizing_mode='scale_width')

    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    y = [2**v for v in x]

    plot.line(x, y, line_width=4)

    script, div = components(plot)
    return script, div

def make_ajax_plot():
    source = AjaxDataSource(data_url=request.url_root + 'data/',
                            polling_interval=2000, mode='append')

    source.data = dict(x=[], y=[])

    plot = figure(plot_height=300, sizing_mode='scale_width')
    plot.line('x', 'y', source=source, line_width=4)

    script, div = components(plot)
    return script, div
