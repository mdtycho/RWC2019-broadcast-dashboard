#!/usr/bin/env python
# coding: utf-8


# Import libraries
import pandas as pd
import numpy as np
import math

import geopandas as gpd
import json

from bokeh.io import output_notebook, output_file, show
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, NumeralTickFormatter, CategoricalColorMapper
from bokeh.palettes import brewer

from bokeh.io.doc import curdoc
from bokeh.models import Slider, HoverTool, Select
from bokeh.layouts import widgetbox, row, column

from bokeh.core.properties import value

from bokeh.embed import json_item, components
from bokeh.resources import CDN

from flask import Flask, render_template, request
#from jinja2 import Template

# compresses static css and js
from flask_static_compress import FlaskStaticCompress

## Create the JSON Data for the GeoJSONDataSource


def json_data(df):
    
    merged = df
    
    # Fill the null values
    #merged.fillna('', inplace = True)
    
    # Bokeh uses geojson formatting, representing geographical features, with json
    # Convert to json
    merged_json = json.loads(merged.to_json())
    
    # Convert to json preferred string-like object 
    json_data = json.dumps(merged_json)
    return json_data


# function to extract numbers from the Model column and convert them to string in second column

def get_model(val):
    
    if val == -1:
        return 'Rights are held by middle-man.'
    elif val == 1:
        return 'Free-to-air.'
    elif val == 2:
        return 'Pay-per-view.'
    elif val == 3:
        return 'Subscription.'
    else:
        return 'Free-to-view.'
    
# function to extract numbers from 'Privately Owned' column and convert to string

def get_ownership(val):
    
    if val == 1:
        return 'Privately owned.'
    else:
        return 'Government ownership.'


# import dataset
def import_ds():


    ds = gpd.read_file('new_ds.shp')


    ds.crs = {'init': 'epsg:4326'}


    #Drop row corresponding to 'Antarctica'
    ds = ds.drop(ds.index[246])



    ds['business_model'] = ds['Model (0=t'].apply(lambda x: get_model(x))

    ds['ownership'] = ds['Privately'].apply(lambda x: get_ownership(x))


    ds_nulls = ds[ds.isnull().any(axis=1)]

    ds = ds.dropna()

    ds_nulls.crs = ds.crs

    return (ds, ds_nulls)


# Create a plotting function
def make_plot(field_name, palette):

    
    to_verbage = {'business_model': 'Business Model', 'ownership' : 'Ownership'}
    
    categories = ds[field_name].unique()
    
    color_mapper = CategoricalColorMapper(palette = palette, factors = categories, nan_color = '#d9d9d9')

    # Create figure object.
    verbage = to_verbage[field_name]

    p = figure(title = verbage, 
                 plot_height = 700, plot_width = 1200,
                 toolbar_location = "left", toolbar_sticky = False,output_backend="webgl", sizing_mode='scale_both')
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.axis.visible = False
    
    # legend workaround from https://github.com/bokeh/bokeh/issues/5904
    for factor, color in zip(color_mapper.factors, color_mapper.palette):
        p.circle(x=[], y=[], fill_color=color, legend=factor)

    # Add patch renderer to figure. 
    data_patches = p.patches('xs','ys', source = geosource, fill_color = {'field' : field_name, 'transform' : color_mapper},
              line_color = 'black', line_width = 0.25, fill_alpha = 1)
    
    null_patches = p.patches('xs','ys', source = geosource_nulls, fill_color = '#d9d9d9',
              line_color = 'grey', line_width = 0.25, fill_alpha = 1)

    # enable tooltip only for countries that have official broadcasters
    hover_data.renderers = [data_patches]

    # tooltip for countries without official broadcasters
    hover_null.renderers = [null_patches]

    # Add the hover tool to the graph
    p.add_tools(hover_data, hover_null)
    return p


## Use flask

app = Flask(__name__, static_folder="static", template_folder="templates")

# initialise static file compressor
compress = FlaskStaticCompress(app)


ds, ds_nulls = import_ds()
# Input geojson source that contains features for plotting for:
# initial year 2018 and initial criteria sale_price_median
geosource = GeoJSONDataSource(geojson = json_data(ds))

geosource_nulls = GeoJSONDataSource(geojson = json_data(ds_nulls))

input_field = 'business_model'

# Define a categorical color hue for 5 possible values (including nans which are false in the data)
# palette = brewer['Dark2'][5]

# Reverse color order so that dark blue is highest obesity.
# palette = palette[::-1]

# Add hover tool
hover_data = HoverTool(tooltips = [ ('Country','@NAME'),
                                ('Broadcaster', '@Company'),
                                ('Ownership', '@ownership'),
                                ('Business Model', '@business_model')])

hover_null = HoverTool(tooltips = [ ('Country','@NAME')])

# Call the plotting function
# p = make_plot(input_field, palette)

# Make a slider object: slider 
# slider = Slider(title = 'Year',start = 2009, end = 2018, step = 1, value = 2018)
# slider.on_change('value', update_plot)

# Make a selection object: select
# select = Select(title='Select Criteria:', value='Business Model', options=['Business Model', 'Ownership'])
# select.on_change('value', update_plot)

# # Make a column layout of widgetbox(slider) and plot, and add it to the current document
# # Display the current document
# layout = column(p, widgetbox(select))
# curdoc().add_root(layout)

# # Use the following code to test in a notebook
# # Interactive features will no show in notebook
# # output_notebook()
# #show(p)

# current_field = input_field


# ## * * End of main code

# ## Bokeh server

# page = Template("""
# <!DOCTYPE html>
# <html lang="en">
# <head>
#   {{ resources }}
#   <script src="http://cdn.pydata.org/bokeh/release/bokeh-widgets-1.3.4.min.js"></script>
# </head>
# <body>
#   <div id="myplot"></div>
#   <script>
#   fetch('/plot')
#     .then(function(response) { return response.json(); })
#     .then(function(item) { Bokeh.embed.embed_item(item); })
#   </script>
# </body>
# """)

def get_palette(field):
    if field == 'business_model':
        return brewer['Dark2'][5]
    else:
        return ['#3385ff', '#ff1a1a']

@app.route('/')
def index():
    to_verbage = {'business_model': 'Business Model', 'ownership' : 'Ownership'}
    # determine selected field
    current_field = request.args.get("input_field")
    if current_field == None:
        current_field = 'business_model'
    # create plot
    p = make_plot(current_field, get_palette(current_field))
    # Make a column layout of widgetbox(slider) and plot, and add it to the current document
    # Display the current document
    layout = column(p, sizing_mode='scale_both')
    curdoc().add_root(layout)

    # Use the following code to test in a notebook
    # Interactive features will no show in notebook
    # output_notebook()
    #show(p)

    #current_field = input_field

    # Embed plot into HTML via Flask Render
    script, div = components(p)
    return render_template("page.html",script = script, div = div, template = Flask, 
    current_field = current_field, fields = ['ownership', 'business_model'], to_verbage = to_verbage)

# With debug=True, Flask server will auto-reload 
# when there are code changes
if __name__ == '__main__':
    print('test')
    app.run(port=5001, debug=True)