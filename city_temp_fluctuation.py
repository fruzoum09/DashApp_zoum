#import the necessary libraries
import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table

# Read the data and filter if necessary
df_cities = pd.read_csv('mart_conditions_week.csv')
avg_temp_cities = df_cities.groupby(['country', 'year', 'city']).agg({'avg_temp_c': 'mean'}).reset_index()

# Prepare the data for visualization
df_yaounde1_dict = df_cities.to_dict('records')

# Create a Dash app with the DARKLY theme
app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])

# Define custom styles for the header and cells
header_style = {'backgroundColor': 'rgb(30, 30, 30)', 'fontWeight': 'bold', 'color': 'white'}
cell_style = {'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white'}

# Create a Dash DataTable component with custom styles
d_table = dash_table.DataTable(
    data=df_yaounde1_dict,
    columns=[{'name': i, 'id': i} for i in df_cities.columns],
    style_header=header_style,
    style_cell=cell_style
)

df_rain = df_cities.groupby(['country', 'year']).agg({'will_it_rain_days': 'mean'}).reset_index()
df_rain

df_snow = df_cities.groupby(['country', 'year']).agg({'will_it_snow_days': 'mean'}).reset_index()
df_snow

# Define custom colors for each city
color_map = {'Berlin': 'blue', 'Yaounde': 'green', 'Dublin': 'orange', 'Madrid': 'red'}

# Create figures
fig1 = px.bar(df_rain, 
              x='country', 
              y='will_it_rain_days',  
              color='year',
              barmode='group',
              color_discrete_map=color_map,  # Assign custom colors
              height=300, title="Yaounde vs Dublin, Berlin & Madrid")

fig1 = fig1.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )
fig2 = px.bar(df_snow, 
              x='country', 
              y='will_it_snow_days', 
              color='year',
              labels={'will_it_snow_days': 'Number of Snowy Days', 'city': 'City'},
              title='Number of Snowy Days by City',
              color_continuous_scale='blues')

# Update layout
fig2.update_layout(xaxis_title='City', yaxis_title='Number of Snowy Days')


# Defining colors for each city
color_map = {'Berlin': 'blue', 'Yaounde': 'green', 'Dublin': 'orange', 'Madrid': 'red'}

# Creating choropleth map
fig5 = px.choropleth(df_rain, 
                    locations='country', 
                    color='year',
                    locationmode='country names',  # Corrected locationmode
                    color_discrete_map=color_map,
                    labels={'city': 'City'},
                    title='City Choropleth Map')


fcolor_map = {'Berlin': 'blue', 'Yaounde': 'green', 'Dublin': 'orange', 'Madrid': 'red'}

# Creating choropleth map
fig6 = px.choropleth(df_rain, 
                     locations='country', 
                     color='year',
                     locationmode='country names',
                     color_discrete_map=color_map,
                     labels={'city': 'City'},
                     title='Country Will It Rain Map',
                     color_continuous_scale=px.colors.sequential.ice,  # Set color scale
                     animation_frame='will_it_rain_days') 

# Updated layout
fig6 = fig6.update_layout(
    plot_bgcolor="#222222",  
    paper_bgcolor="#222222",
    font_color="white", 
    geo_bgcolor="#222222", 
    legend_title='City', 
    height=400, 
    width=800 
)

fig6 = px.choropleth(df_cities.groupby(['country', 'year']).agg({'avg_temp_c': 'mean'}).reset_index(),
                     locations='country',
                     color='avg_temp_c',
                     locationmode='country names',
                     color_continuous_scale='Viridis',
                     title='Average Temperature by Country',
                     animation_frame='year',
                     scope='world',
                     projection='natural earth',
                     width=1000,
                     height=400)

df_agg = df_cities.groupby(['country', 'year']).agg({'avg_temp_c': 'mean'}).reset_index()

# choropleth map 
fig7 = px.choropleth(df_agg, 
                    locations='country', 
                    color='avg_temp_c',
                    locationmode='country names',
                    color_continuous_scale='Viridis',
                    title='Average Temperature by Country with Animation',
                    animation_frame='year',
                    scope='world', 
                    projection='natural earth',
                    width=1000, 
                    height=400)  

# Customize layout
fig7.update_layout(
    geo=dict(bgcolor="#222222"),
    plot_bgcolor="#222222",
    paper_bgcolor="#222222",
    font_color="white"
)

# slider animation
fig7.update_layout(
    sliders=[{
        "active": 0,
        "steps": [{
            "label": year,
            "method": "animate",
            "args": [[year], {"frame": {"duration": 1000, "redraw": True}, "mode": "immediate", "transition": {"duration": 0}}]
        } for year in df_agg['year'].unique()]
    }]
)


# Set app layout
app =dash.Dash(external_stylesheets=[dbc.themes.DARKLY])
server=app.server
app.layout = html.Div([
    html.H1('Number Of Rainy Days For Each City', style={'textAlign': 'center', 'color': 'coral'}),
    html.H2('Rainy Days', style={'paddingLeft': '30px'}),
    html.H3('Graphs Below'),
    html.Div(d_table),
    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig5),
    dcc.Graph(figure=fig6),
    dcc.Graph(figure=fig7),
   
])


# Run the app
if __name__ == '__main__':
    app.run_server(port=8092)


