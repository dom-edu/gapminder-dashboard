# Exercise: Addd another callback function update_pie , that updates the pie graph in the same manner as the histogram
from dash import Dash, html

# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px 

# DEBUG TOGGLE 
DEBUG = True

# load data into dataframe 
gapminder_df = px.data.gapminder() 

# instantiate dash app 
app = Dash(__name__)

# figures 

## scatterplot 
def create_scatter_plot(df):

    """ 
    Create Scatter Plot figure 
    """

    scatter_ = px.scatter(df, x="gdpPercap", y="lifeExp",
                size="pop", color="continent",
                    hover_name="country", log_x=True, size_max=60)
    return scatter_
# bubble map 
def create_bubble_map(df):

    """ 
    Create Bubble Map figure 
    """

    return px.scatter_geo(
        df,
        locations="iso_alpha",
        color="continent",
        hover_name="country",
        size="pop",
        animation_frame="year",
        projection="natural earth")

# instantiate bubble map
bubble_map_ = create_bubble_map(gapminder_df.query("year==2007"))

# instantiate scatter plot 
scatter_plot_ = create_scatter_plot(gapminder_df.query("year==2007"))



# Controls 
cl_ops = gapminder_df['continent'].unique() # get unique continents as options 
cl_ops_sel = cl_ops[:2] # select the first two 
cl1_style = {
  'margin-top': '4%',
  'margin-left': '6%'
}

# checklist 
checklist1 = dcc.Checklist(cl_ops, cl_ops_sel, inline=True, style=cl1_style, id="checklist") 

# dropdown 
years_ = gapminder_df['year'].unique()
dd1 = dcc.Dropdown(
    years_,
    years_[:2], 
    placeholder="Select Year(s)",
    id='dd1',
    multi=True)

# rangeslider 
# reading the data we see there is a step of 5 years 
min_year_ = gapminder_df['year'].min()
max_year_ = gapminder_df['year'].max()
step_ = 5 # Data is gathered every five years
if DEBUG:
    print(min_year_)
    print(max_year_)
    print(step_)

rs1 = dcc.RangeSlider(
    min_year_,
    max_year_,
    step_, 
    value=[min_year_,min_year_ + 10], 
    # marks = {i}
    # included=True,
    marks={n:str(n) for n in gapminder_df['year'].tolist()},
    id="range-slider-1" ) 

# define app layout 
app.layout = [
    html.H1("Gapminder with controls", style={'textAlign':'center'}),
    checklist1, 
    dd1,
    html.H3("Life Expectancy for the year(s):", style={'textAlign':'center'}, id="life-exp-header"),
    dcc.Graph(figure = scatter_plot_ ,id="scatter-gap"),
    dcc.Graph(figure = bubble_map_, id ="bubble-map" ),
    rs1

]

# filter helper function 
def filter_gp_data(cl_sel, dd_sel, rs_sel):
    """
    filters Gapminder data by year and continent 
    """
    # | -> or gives us the intersection of the multi dropdown and rangeslider
    filter1_ = gapminder_df['year'].isin(dd_sel) | gapminder_df['year'].isin(rs_sel)

    # show only select continents 
    filter2_ = gapminder_df['continent'].isin(cl_sel)

    return gapminder_df[filter1_ & filter2_]


# h3 title callback 
@callback(
    Output('life-exp-header', 'children'),
    Input('dd1', 'value')
)
def update_header(years_):
    # make a string out of the years_ 

    # DEBUG
    if DEBUG:
        print("years_", years_)

    years_s = list(map(str, years_))
    years_str = ", ".join(years_s)
    complete_title = f"Life Expectancy for the year(s):{years_str}"
    return complete_title

# scatter plot callback 
@callback(
    Output('scatter-gap', 'figure'),
    Input('checklist','value'),
    Input('dd1','value'),
    Input('range-slider-1', 'value')
)
def update_scatter(cl_sel, dd_sel, rs_sel):

    # DEBUG
    if DEBUG:
        print("checklist selected:",cl_sel, type(cl_sel)) # value is a list in this case 
        print("dropdown selected",dd_sel, type(dd_sel))
        print("range slider selected: ",rs_sel, type(rs_sel))
    
    g_mind_filtered_df =  filter_gp_data(cl_sel, dd_sel, rs_sel)

    ## scatterplot 
    return create_scatter_plot(g_mind_filtered_df)

@callback(
    Output('bubble-map', 'figure'),
    Input('checklist','value'),
    Input('dd1','value'),
    Input('range-slider-1', 'value')
)
def update_bubble_map(cl_sel, dd_sel, rs_sel):

    # DEBUG
    if DEBUG:
        print("checklist selected:",cl_sel, type(cl_sel)) # value is a list in this case 
        print("dropdown selected",dd_sel, type(dd_sel))
        print("range slider selected: ",rs_sel, type(rs_sel))
    
   g_mind_filtered_df = filter_gp_data(cl_sel, dd_sel, rs_sel)

    # rerender the bubble_map 
    bubble_map_ = create_bubble_map(g_mind_filtered_df)
    
    return bubble_map_

if __name__ == '__main__':
    app.run(port=5006, debug = True) 
