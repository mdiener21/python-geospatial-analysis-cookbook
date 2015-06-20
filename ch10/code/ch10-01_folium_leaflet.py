#!/usr/bin/env python
# -*- coding: utf-8 -*-
import folium
import pandas as pd

states_geojson = r'us-states.json'
state_unemployment = r'html/US_Unemployment_Oct2012.csv'
state_data = pd.read_csv(state_unemployment)

#Let Folium determine the scale
map = folium.Map(location=[48, -102], zoom_start=3, tiles="Stamen Toner")
map.geo_json(geo_path=states_geojson, data=state_data,
             columns=['State', 'Unemployment'],
             threshold_scale=[5, 6, 7, 8, 9, 10],
             key_on='feature.id',
             fill_color='YlGn', fill_opacity=0.7, line_opacity=0.2,
             legend_name='Unemployment Rate (%)')

map.create_map(path='html/us_states.html')