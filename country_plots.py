import pandas as pd

from bokeh.plotting import figure

from bokeh.models import Slider, HoverTool, Select

from bokeh.layouts import gridplot

def make_country_plot(country, compare_to=False):
    df1 = pd.read_csv('country_data/press_freedom_clean.csv')
    df1.sort_values('Year', ascending=False, inplace=True)

    df2 = pd.read_csv('country_data/reg_credit_labour_business_clean.csv')
    df2.sort_values('Year', ascending=False, inplace=True)

    df3 = pd.read_csv('country_data/transparency_govt_policy_making_clean.csv')
    df3.sort_values('Year', ascending=False, inplace=True)

    df4 = pd.read_csv('country_data/efficiency_of_legal_framework_for_challenging_govt_regs_clean.csv')
    df4.sort_values('Year', ascending=False, inplace=True)

    x1, y1, t1 = df1[df1['Country'] == country]['Year'], df1[df1['Country'] == country]['Press Freedom Index'], df1.columns[2]

    x2, y2, t2 = df2[df2['Country'] == country]['Year'], df2[df2['Country'] == country]['Regulation of credit, labour and business.'], df2.columns[2]

    x3, y3, t3 = df3[df3['Country'] == country]['Year'], df3[df3['Country'] == country]['Transparency of government policy-making.'], df3.columns[2]

    x4, y4, t4 = df4[df4['Country'] == country]['Year'], df4[df4['Country'] == country]['Efficiency of legal framework in challenging government regulations.'], df4.columns[2]

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"

    # Add hover tool
    hover_line = HoverTool(tooltips = [ ('value','@y'),
                                ('year', '@x')])


    p1 = figure(plot_width=400, plot_height=400, title = t1,output_backend="webgl", 
    sizing_mode='scale_both', background_fill_color="#fafafa", tools=TOOLS)
    # add a line renderer
    p1.line(x1,y1, line_dash=(4, 4), line_width=2, color = '#85e0e0', legend = country)
    p1.circle(x1,y1)
    p1.xgrid.grid_line_color = None
    p1.ygrid.grid_line_color = None

    p1.add_tools(hover_line)

    p2 = figure(plot_width=400, plot_height=400, title = t2,output_backend="webgl", 
    sizing_mode='scale_both', background_fill_color="#fafafa", tools=TOOLS)
    # add a line renderer
    p2.line(x2,y2, line_dash=(4, 4), line_width=2, color = '#85e0e0', legend = country)
    p2.circle(x2,y2)
    p2.xgrid.grid_line_color = None
    p2.ygrid.grid_line_color = None

    p2.add_tools(hover_line)


    p3 = figure(plot_width=400, plot_height=400, title = t3,output_backend="webgl", 
    sizing_mode='scale_both', background_fill_color="#fafafa", tools=TOOLS)
    # add a line renderer
    p3.line(x3,y3, line_dash=(4, 4), line_width=2, color = '#85e0e0', legend = country)
    p3.circle(x3,y3)
    p3.xgrid.grid_line_color = None
    p3.ygrid.grid_line_color = None

    p3.add_tools(hover_line)


    p4 = figure(plot_width=400, plot_height=400, title = t4,output_backend="webgl", 
    sizing_mode='scale_both', background_fill_color="#fafafa", tools=TOOLS)
    # add a line renderer
    p4.line(x4,y4, line_dash=(4, 4), line_width=2, color = '#85e0e0', legend = country)
    p4.circle(x4,y4)
    p4.xgrid.grid_line_color = None
    p4.ygrid.grid_line_color = None

    p4.add_tools(hover_line)

    if (compare_to):
        x12, y12, t12 = df1[df1['Country'] == compare_to]['Year'], df1[df1['Country'] == compare_to]['Press Freedom Index'], df1.columns[2]

        x22, y22, t22 = df2[df2['Country'] == compare_to]['Year'], df2[df2['Country'] == compare_to]['Regulation of credit, labour and business.'], df2.columns[2]

        x32, y32, t32 = df3[df3['Country'] == compare_to]['Year'], df3[df3['Country'] == compare_to]['Transparency of government policy-making.'], df3.columns[2]

        x42, y42, t42 = df4[df4['Country'] == compare_to]['Year'], df4[df4['Country'] == compare_to]['Efficiency of legal framework in challenging government regulations.'], df4.columns[2]

        p1.line(x12,y12, line_dash=(4, 4), line_width=2, color = '#ff1aff', legend = compare_to)
        p1.circle(x12,y12, color = '#ff1aff')

        p2.line(x22,y22, line_dash=(4, 4), line_width=2, color = '#ff1aff', legend = compare_to)
        p2.circle(x22,y22, color = '#ff1aff')

        p3.line(x32,y32, line_dash=(4, 4), line_width=2, color = '#ff1aff', legend = compare_to)
        p3.circle(x32,y32, color = '#ff1aff')

        p4.line(x42,y42, line_dash=(4, 4), line_width=2, color = '#ff1aff', legend = compare_to)
        p4.circle(x42,y42, color = '#ff1aff')

    # make a grid
    grid = gridplot([[p1, p2], [p3, p4]], sizing_mode='scale_both', plot_width=1200, plot_height=850)

    return grid