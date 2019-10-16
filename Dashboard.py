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
from bokeh.models import GeoJSONDataSource, CategoricalColorMapper, Legend, LegendItem, OpenURL, TapTool
from bokeh.palettes import brewer

from bokeh.io.doc import curdoc
from bokeh.models import Slider, HoverTool, Select
from bokeh.layouts import widgetbox, row, column, gridplot
from bokeh.transform import cumsum

from bokeh.core.properties import value

from bokeh.events import Tap

from bokeh.embed import json_item, components
from bokeh.resources import CDN

from flask import Flask, render_template, request, redirect
#from jinja2 import Template

# compresses static css and js
from flask_static_compress import FlaskStaticCompress

# import country plots module
from country_plots import make_country_plot

## Create the JSON Data for the GeoJSONDataSource

COUNTRIES_SELECT = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola',
       'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia',
       'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh',
       'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan',
       'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil',
       'Brunei', 'Bulgaria', 'Burkina Faso', 'Burma (Myanmar)', 'Burundi',
       'Cambodia', 'Cameroon', 'Canada', 'Cape Verde',
       'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia',
       'Comoros', 'Congo (Brazzaville)', 'Congo (Kinshasa)', 'Costa Rica',
       'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark',
       'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt',
       'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia',
       'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia',
       'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala',
       'Guinea', 'Guinea Bissau', 'Guyana', 'Haiti', 'Honduras',
       'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran',
       'Iraq', 'Ireland', 'Israel', 'Italy', 'Ivory Coast', 'Jamaica',
       'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kosovo',
       'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho',
       'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg',
       'Macedonia (F.Y.R.O.M.)', 'Madagascar', 'Malawi', 'Malaysia',
       'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania',
       'Mauritius', 'Mexico', 'Micronesia', 'Moldova', 'Monaco',
       'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Namibia',
       'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua',
       'Niger', 'Nigeria', 'North Korea', 'Norway', 'Oman', 'Pakistan',
       'Palau', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru',
       'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia',
       'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia',
       'Saint Thomas and Principe', 'Saint Vincent and Grenadines',
       'Samoa', 'San Marino', 'Saudi Arabia', 'Senegal', 'Serbia',
       'Serbia and Montenegro', 'Seychelles', 'Sierra Leone', 'Singapore',
       'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'Somaliland',
       'South Africa', 'South Korea', 'South Sudan', 'Spain', 'Sri Lanka',
       'Sudan', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Syria',
       'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor Leste',
       'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey',
       'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine',
       'United Arab Emirates', 'United Kingdom', 'United States',
       'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Vietnam',
       'West Bank and Gaza', 'Yemen', 'Zambia', 'Zimbabwe']


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

    from math import pi

    
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

    # Add pie chart
    x1 = {'Subscription.': 103, 'Free-to-view.': 10, 'Free-to-air.':16, 'Pay-per-view.':1,
       'Rights are held by middle-man.':1}

    x2 = {'Privately owned.':125, 'Government ownership.':6}

    data1 = pd.Series(x1).reset_index(name='value').rename(columns={'index':'business_model'})

    data2 = pd.Series(x2).reset_index(name='value').rename(columns={'index':'ownership'})

    data1['angle'] = data1['value']/data1['value'].sum() * 2*pi

    data2['angle'] = data2['value']/data2['value'].sum() * 2*pi

    pie_data = {'business_model': data1, 'ownership': data2}

    pie = figure(plot_height=200, title="", toolbar_location=None,
           tools="hover", tooltips="@{}: @value".format(field_name), x_range=(-0.5, 1.0), output_backend="webgl", sizing_mode='scale_both')



    pie.wedge(x=0, y=1, radius=0.2,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color={'field' : field_name, 'transform' : color_mapper}, 
        source=pie_data[field_name] , legend=field_name)

    pie.legend.location = "bottom_right"

    pie.axis.axis_label=None
    pie.axis.visible=False
    pie.grid.grid_line_color = None

    
    # legend workaround from https://github.com/bokeh/bokeh/issues/5904
    for factor, color in zip(color_mapper.factors, color_mapper.palette):
        p.circle(x=[], y=[], fill_color=color, legend=factor)
        p.legend.location = "bottom_left"


    # Add patch renderer to figure. 
    data_patches = p.patches('xs','ys', source = geosource, fill_color = {'field' : field_name, 'transform' : color_mapper},
              line_color = 'black', line_width = 0.25, fill_alpha = 1, selection_fill_color = {'field' : field_name, 'transform' : color_mapper},
              nonselection_fill_color = {'field' : field_name, 'transform' : color_mapper}, selection_fill_alpha = 1, nonselection_fill_alpha = 1, 
              selection_line_color = 'black',nonselection_line_color = 'black')
    
    null_patches = p.patches('xs','ys', source = geosource_nulls, fill_color = '#d9d9d9',
              line_color = 'grey', line_width = 0.25, fill_alpha = 1, selection_fill_color = '#d9d9d9',
              nonselection_fill_color = '#d9d9d9', selection_fill_alpha = 1, nonselection_fill_alpha = 1,
              selection_line_color = 'grey', nonselection_line_color = 'grey')

    # # try legend

    # legend = Legend(items=[LegendItem(label = color_mapper.factors[i], renderers=[data_patches], 
    # index = i, name = color_mapper.factors[i]) for i in range(len(color_mapper.factors))])

    # enable tooltip only for countries that have official broadcasters
    hover_data.renderers = [data_patches]

    # tooltip for countries without official broadcasters
    hover_null.renderers = [null_patches]

    # Add the hover tools to the graph as well as the taptool
    p.add_tools(hover_data, hover_null, taptool)

    return column(p, pie)


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

# add taptool navigate to url
taptool = TapTool()
url = "/country?clicked_country=@NAME"
taptool.callback = OpenURL(url=url)

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

@app.route('/country')
def country_plots():
    

    country_map = {'Antigua and Barb.': 'Antigua and Barbuda','Bosnia and Herz.': 'Bosnia and Herzegovina',
    'Myanmar': 'Burma (Myanmar)','Cabo Verde': 'Cape Verde','Central African Rep.': 'Central African Republic',
    'Congo': 'Congo (Brazzaville)','Dem. Rep. Congo': 'Congo (Kinshasa)','Czechia': 'Czech Republic','Dominican Rep.': 'Dominican Republic',
    'Eq. Guinea': 'Equatorial Guinea','Guinea-Bissau': 'Guinea Bissau',"CÃ´te d'Ivoire": 'Ivory Coast',
    'Macedonia': 'Macedonia (F.Y.R.O.M.)','Marshall Is.': 'Marshall Islands','St. Kitts and Nevis': 'Saint Kitts and Nevis',
    'SÃ£o TomÃ© and Principe': 'Saint Thomas and Principe','St. Vin. and Gren.': 'Saint Vincent and Grenadines',
    'Serbia': 'Serbia and Montenegro','Solomon Is.': 'Solomon Islands','S. Sudan': 'South Sudan','eSwatini': 'Swaziland',
    'Timor-Leste': 'Timor Leste','United States of America': 'United States','Palestine': 'West Bank and Gaza'}
    clicked_country = request.args.get("clicked_country")

    compare_to = request.args.get("compare_to")
    if clicked_country == None:
        return redirect("/", code = 303)
    if compare_to == None:
        # create plot
        gp = make_country_plot(clicked_country if clicked_country not in country_map.keys() else country_map[clicked_country])
    else:
        gp = make_country_plot(clicked_country if clicked_country not in country_map.keys() else country_map[clicked_country], compare_to = compare_to)

    # Make a column layout of widgetbox(slider) and plot, and add it to the current document
    # Display the currentcurdoc document
    #curdoc().add_root(p)

    # Embed plot into HTML via Flask Render
    script, div = components(gp)
    return render_template("temp.html",script = script, div = div, template = Flask, 
    clicked_country = clicked_country, countries = COUNTRIES_SELECT, compare_to = compare_to)

# With debug=True, Flask server will auto-reload 
# when there are code changes
if __name__ == '__main__':
    print('test')
    app.run(port=5001, debug=True)