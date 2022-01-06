import datetime
from os.path import dirname, join

import pandas as pd
from scipy.signal import savgol_filter

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, DataRange1d, Select, Slider,HoverTool, Panel
from bokeh.palettes import Blues4
from bokeh.plotting import figure

# STATISTICS = ['record_min_temp', 'actual_min_temp', 'average_min_temp', 'average_max_temp', 'actual_max_temp', 'record_max_temp']

def line_tab(covid_data):
    def get_dataset(src, name, min_year, max_year):
        df = src[src.Province == name].copy()
        df = df.set_index(['Date'])
        df.sort_index(inplace=True)

        if (min_year <= max_year):
            df = df[df.Year >= min_year]
            df = df[df.Year <= max_year]

        return ColumnDataSource(data=df)

    def make_plot(source, title):
        
        plot = figure(x_axis_type="datetime", width=1000)
        plot.add_tools(HoverTool(
            tooltips=[
                ("Province", "@Province"),
                ("Date", "@Date{%F}"),
                ("Total", "@Total_Active_Cases")
            ],
            formatters={
                '@Date': 'datetime'
            },
            mode = 'vline')
        )
        plot.title.text = title

        plot.line(x='Date', y='Total_Active_Cases', source=source, color='red')

        # fixed attributes
        plot.xaxis.axis_label = None
        plot.yaxis.axis_label = "Cases"
        plot.axis.axis_label_text_font_style = "bold"
        plot.x_range = DataRange1d(range_padding=0.0)
        plot.grid.grid_line_alpha = 0.3

        return plot

    def update_plot(attrname, old, new):
        province = province_select.value
        plot.title.text = "Total Active Cases for " + province
        min_year = min_year_slider.value
        max_year = max_year_slider.value

        src = get_dataset(df, province, min_year, max_year)
        source.data.update(src.data)

    province = 'DKI Jakarta'
    min_year = 2020
    max_year = 2021

    provinces = ['DKI Jakarta', 'Banten', 'Daerah Istimewa Yogyakarta', 'Jawa Barat', 'Jawa Tengah', 'Jawa Timur']
    years = [2020, 2021]

    province_select = Select(value=province, title='Province', options=provinces)
    min_year_slider = Slider(title="Start Year", start=2020, end=2021, value=2020, step=1)
    max_year_slider = Slider(title="End Year", start=2020, end=2021, value=2021, step=1)
    #ini ganti ke slider tahun
    # year_select = Select(value=year, title='Year', options=years)

    # distribution_select = Select(value=distribution, title='Distribution', options=['Discrete', 'Smoothed'])

    df = covid_data.copy()
    df['Date'] = pd.to_datetime(df.Date)
    source = get_dataset(df, province, min_year, max_year)
    plot = make_plot(source, "Total Active Cases for " + province)

    province_select.on_change('value', update_plot)
    min_year_slider.on_change('value', update_plot)
    max_year_slider.on_change('value', update_plot)
    # year_select.on_change('value', update_plot)

    # controls = column(province_select, year_select)
    controls = column(province_select, min_year_slider, max_year_slider)

    layout = row(controls, plot)
	
	# Make a tab with the layout 
    tab = Panel(child=layout, title = 'Active Cases')
    
    return tab