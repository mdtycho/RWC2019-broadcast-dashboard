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

ds = gpd.read_file('new_ds.shp')


ds.crs = {'init': 'epsg:4326'}


#Drop row corresponding to 'Antarctica'
ds = ds.drop(ds.index[246])



ds['business_model'] = ds['Model (0=t'].apply(lambda x: get_model(x))

ds['ownership'] = ds['Privately'].apply(lambda x: get_ownership(x))


ds_nulls = ds[ds.isnull().any(axis=1)]

ds = ds.dropna()

ds_nulls.crs = ds.crs


# Create a plotting function
def make_plot(field_name, palette):
    
    to_verbage = {'business_model': 'Business Model', 'ownership' : 'Ownership'}
    
    categories = ds[field_name].unique()
    print('categories')
    print(categories)
    
    color_mapper = CategoricalColorMapper(palette = palette, factors = categories, nan_color = '#d9d9d9')

    # Create figure object.
    verbage = to_verbage[field_name]

    p = figure(title = verbage, 
                 plot_height = 700, plot_width = 1200,
                 toolbar_location = None)
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.axis.visible = False
    
    # legend workaround from https://github.com/bokeh/bokeh/issues/5904
    for factor, color in zip(color_mapper.factors, color_mapper.palette):
        p.circle(x=[], y=[], fill_color=color, legend=factor)

    # Add patch renderer to figure. 
    p.patches('xs','ys', source = geosource, fill_color = {'field' : field_name, 'transform' : color_mapper},
              line_color = 'black', line_width = 0.25, fill_alpha = 1)
    
    p.patches('xs','ys', source = geosource_nulls, fill_color = '#d9d9d9',
              line_color = 'black', line_width = 0.25, fill_alpha = 1)

    # Add the hover tool to the graph
    p.add_tools(hover)
    return p


# Define the callback function: update_plot
def update_plot(attr, old, new):
    to_input_field = {'Business Model' : 'business_model', 'Ownership': 'ownership'}
    new_data = json_data(ds)
    
    # The input cr is the criteria selected from the select box
    cr = select.value
    input_field = to_input_field[cr]
    
    num_categories = int(ds[input_field].nunique())
    
    if num_categories == 2:
        palette = ['#3385ff', '#ff1a1a']
    else:
        palette = brewer['Dark2'][num_categories]
    
    # Update the plot based on the changed inputs
    p = make_plot(input_field, palette)
    
    # Update the layout, clear the old document and display the new document
    layout = column(p, widgetbox(select))
    curdoc().clear()
    curdoc().add_root(layout)
    
    # Update the data
    geosource.geojson = new_data


# Input geojson source that contains features for plotting for:
# initial year 2018 and initial criteria sale_price_median
geosource = GeoJSONDataSource(geojson = json_data(ds))

geosource_nulls = GeoJSONDataSource(geojson = json_data(ds_nulls))

input_field = 'business_model'

# Define a categorical color hue for 5 possible values (including nans which are false in the data)
palette = brewer['Dark2'][5]

# Reverse color order so that dark blue is highest obesity.
# palette = palette[::-1]

# Add hover tool
hover = HoverTool(tooltips = [ ('Country','@NAME'),
                               ('Continent', '@Continent'),
                               ('Broadcaster', '@Company')])

# Call the plotting function
p = make_plot(input_field, palette)

# Make a slider object: slider 
# slider = Slider(title = 'Year',start = 2009, end = 2018, step = 1, value = 2018)
# slider.on_change('value', update_plot)

# Make a selection object: select
select = Select(title='Select Criteria:', value='Business Model', options=['Business Model', 'Ownership'])
select.on_change('value', update_plot)

# Make a column layout of widgetbox(slider) and plot, and add it to the current document
# Display the current document
layout = column(p, widgetbox(select))
curdoc().add_root(layout)

# Use the following code to test in a notebook
# Interactive features will no show in notebook
# output_notebook()
# show(p)


# ## * * End of main code

# ## Bokeh server