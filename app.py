import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
user_data_df = pd.read_csv("User_data.csv")
user_data_df['Date'] = pd.to_datetime(user_data_df['Date'])
user_data_df = user_data_df.sort_values(by='Date')
user_data_grouped_weekly_df = user_data_df.groupby(pd.Grouper(freq='W-FRI', key='Date'))[
    'pageviews', 'time_on_page_sec'].sum()
user_data_grouped_weekly_df = user_data_grouped_weekly_df.reset_index()
user_data_grouped_weekly_df['Date'] = user_data_grouped_weekly_df['Date'].dt.date
fig = make_subplots(
    rows=2, cols=2,
    shared_xaxes=True,
    vertical_spacing=0.15,
    specs=[[{"type": "bar"},
            {"type": "domain"}],
           [{"type": "bar"},
            {"type": "table"}]]
)
fig.add_trace(
    go.Bar(x=user_data_grouped_weekly_df['Date'],
           y=user_data_grouped_weekly_df['time_on_page_sec'],
           xaxis='x2', yaxis='y2',
           marker=dict(color='#FF6600'),
           name='Time On Page (Bar Chart 1)'
           ),
    row=1, col=1
)
fig.add_trace(
    go.Bar(x=user_data_grouped_weekly_df['Date'],
           y=user_data_grouped_weekly_df['pageviews'],
           xaxis='x2', yaxis='y2',
           marker=dict(color='#0099ff'),
           name='Page Views (Bar Chart 2)'),
    row=2, col=1
)
fig.add_trace(
    go.Table(
        header=dict(
            values=["Date", "Page Views", "Seconds on Page"],
            font=dict(size=10),
            align="left"
        ),
        cells=dict(
            values=[user_data_grouped_weekly_df[k].tolist() for k in user_data_grouped_weekly_df.columns[0:]],
            align="left")
    ),
    row=2, col=2
)
user_data_grouped_country_df = user_data_df.groupby(pd.Grouper(key='country'))[
    'pageviews', 'time_on_page_sec'].sum()
user_data_grouped_country_df = user_data_grouped_country_df.reset_index()
user_data_grouped_country_df = user_data_grouped_country_df.head(10)
fig.add_trace(
    go.Pie(labels=user_data_grouped_country_df["country"],
           values=user_data_grouped_country_df["pageviews"],
           name='Countries',
           ),
    row=1, col=2
)
fig.update_layout(
    template="plotly_dark",
    margin=dict(r=10, t=25, b=40, l=60),
    annotations=[dict(text="", showarrow=False, xref="paper", yref="paper", x=0, y=0)]
)
app.layout = html.Div(children=[
    html.H1(children='Hadi Data Analyst Test Q1 and Q2 Demo'),
    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server()
