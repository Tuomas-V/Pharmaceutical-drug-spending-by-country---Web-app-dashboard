import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px



# data from CSV
df = pd.read_csv(f'./flat-ui__data Fri Nov 21 2025.csv')
country_list = df['LOCATION'].unique()

# preparing dataframes for pie and bar charts
median_per_capita = df.groupby('LOCATION')['USD_CAP'].median().reset_index(name='Median')
median_per_capita['Median'] = round(median_per_capita['Median'], 1)
mean_health_spending = df.groupby('LOCATION')['PC_HEALTHXP'].mean().reset_index(name='HealthSpending')
mean_health_spending['HealthSpending'] = round(mean_health_spending['HealthSpending'], 2)



# Visualization
#===============

background_color = "#262B2E"
plot_color = "#232628"
grid_color = "#254260"
text_color = "#E1E1E1"

app = Dash(__name__)

# html layout
app.layout = html.Div(children=[
    html.H2('Pharmaceutical drug spending by country'),
    html.Br(),
    html.Div(className="line-graph-div", children=[
        dcc.Dropdown(
            id="country_dropdown",
            value=country_list[:5],
            options=country_list,
            multi=True,
            style={'color': text_color, 'background-color':background_color},
            className="country-dropdown",
        ),
        dcc.Graph(id="country_graph"),
    ]),
    html.Div(className="wrapper", children=[
        html.Div(className="pie-chart-div", children=[
            dcc.Graph(id="pie_chart_graph"),
        ]),
        html.Div(className="bar-chart-div", children=[
            dcc.Graph(id="health_spending_graph"),
        ]),
    ]),
])

# on graph update
@app.callback(
    Output("country_graph", "figure"),
    Output("pie_chart_graph", "figure"),
    Output("health_spending_graph", "figure"),
    Input("country_dropdown", "value"),
)
def update_graph(country):
    selected_df = df[df['LOCATION'].isin(country)]
    selected_median = median_per_capita[median_per_capita['LOCATION'].isin(country)]
    selected_mean = mean_health_spending[mean_health_spending['LOCATION'].isin(country)]

    # line graph
    fig1 = px.line(selected_df, x='TIME', y='PC_GDP',
        color="LOCATION",
        color_discrete_sequence=px.colors.qualitative.Set1,
        line_group="LOCATION")
    fig1.update_xaxes(title=None, gridcolor=grid_color)
    fig1.update_yaxes(title=None, ticksuffix="%", gridcolor=grid_color)
    fig1.update_layout(title='Percentage of GDP spent on pharmaceutical drugs by country', showlegend=False, hovermode="x unified", title_x=0.5,
                       paper_bgcolor=background_color, font_color=text_color, plot_bgcolor=plot_color)
    fig1.update_traces(hovertemplate=None)

    # pie chart
    fig2 = px.pie(selected_median,
        values='Median',
        color='LOCATION',
        color_discrete_sequence=px.colors.qualitative.Set1,
        names='LOCATION',)
    fig2.update_layout(title="Median yearly spending per capita (USD)", showlegend=False, title_x=0.5,
                       paper_bgcolor=background_color, font_color=text_color, plot_bgcolor=plot_color)
    fig2.update_traces(hovertemplate="%{label}<br>$%{value} USD", texttemplate="$%{value}", textfont_size=14)

    # bar chart
    fig3 = px.bar(selected_mean, x='LOCATION', y='HealthSpending',
        color='LOCATION',
        color_discrete_sequence=px.colors.qualitative.Set1)
    fig3.update_xaxes(title=None, gridcolor=grid_color)
    fig3.update_yaxes(title=None, ticksuffix="%", gridcolor=grid_color, zerolinecolor=background_color)
    fig3.update_layout(title="Average yearly percentage of health spending", showlegend=False, title_x=0.5,
                       paper_bgcolor=background_color, font_color=text_color, plot_bgcolor=plot_color)
    fig3.update_traces(hovertemplate="%{label}<br>Health spending: %{value}<extra></extra>", texttemplate="%{value}" ,textfont_size=14, marker_line_width=0)

    return fig1, fig2, fig3

if __name__ == "__main__":
    app.run()
