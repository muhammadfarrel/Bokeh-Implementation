# Pandas for data management
import pandas as pd

# os methods for manipulating paths
from os.path import dirname, join

# Bokeh basics 
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs


# Each tab is drawn by one script
from scripts.line_chart import line_tab
from scripts.bar_chart import bar_tab

# Using included state data from Bokeh for map
# from bokeh.sampledata.us_states import data as states

# Read data into dataframes
df = pd.read_csv(join(dirname(__file__), 'data/covid.csv'))

# Formatted Flight Delay Data for map

# Create each of the tabs
# tab1 = histogram_tab(flights)
# tab2 = density_tab(flights)
tab1 = line_tab(df)
tab2 = bar_tab(df)

# Put all the tabs into one application
tabs = Tabs(tabs = [tab1, tab2])

# Put the tabs in the current document for display
curdoc().add_root(tabs)


