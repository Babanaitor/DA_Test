######################################################### 1 is weekly improving?


import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash

app = dash.Dash(__name__)
server = app.server

# open data file
user_data_df = pd.read_csv("User_data.csv")

# check data and its type
print((user_data_df.at[0, 'Date']))
print(type(user_data_df.at[0, 'Date']))

# covert str to datetime
user_data_df['Date'] = pd.to_datetime(user_data_df['Date'])

# check data type again
print((user_data_df.at[0, 'Date']))
print(type(user_data_df.at[0, 'Date']))

# sort by date
user_data_df = user_data_df.sort_values(by='Date')
print(user_data_df)

# group data weekly
user_data_grouped_weekly_df = user_data_df.groupby(pd.Grouper(freq='W-FRI', key='Date'))[
    'pageviews', 'time_on_page_sec'].sum()
print(user_data_grouped_weekly_df)

# graph
user_data_grouped_weekly_df = user_data_grouped_weekly_df.reset_index()
print(user_data_grouped_weekly_df)

# convert datetime to date
user_data_grouped_weekly_df['Date'] = user_data_grouped_weekly_df['Date'].dt.date
print(user_data_grouped_weekly_df)

# create subplots area
fig = make_subplots(
    rows=2, cols=2,
    shared_xaxes=True,
    vertical_spacing=0.15,
    specs=[[{"type": "bar"},
            {"type": "domain"}],
           [{"type": "bar"},
            {"type": "table"}]]
)

# add time on page
fig.add_trace(
    go.Bar(x=user_data_grouped_weekly_df['Date'],
           y=user_data_grouped_weekly_df['time_on_page_sec'],
           xaxis='x2', yaxis='y2',
           marker=dict(color='#FF6600'),
           name='Time On Page (Bar Chart 1)'
           ),
    row=1, col=1
)

# add pageviews bar chart
fig.add_trace(
    go.Bar(x=user_data_grouped_weekly_df['Date'],
           y=user_data_grouped_weekly_df['pageviews'],
           xaxis='x2', yaxis='y2',
           marker=dict(color='#0099ff'),
           name='Page Views (Bar Chart 2)'),
    row=2, col=1
)

# add table
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

######################################################### 2. (Pi chart) which countries contributing most? (JORDAN)


# group data weekly starting saturday
user_data_grouped_country_df = user_data_df.groupby(pd.Grouper(key='country'))[
    'pageviews', 'time_on_page_sec'].sum()
user_data_grouped_country_df = user_data_grouped_country_df.reset_index()
print(user_data_grouped_country_df)
user_data_grouped_country_df = user_data_grouped_country_df.head(10)

# add Pie trace
fig.add_trace(
    go.Pie(labels=user_data_grouped_country_df["country"],
           values=user_data_grouped_country_df["pageviews"],
           name='Countries',
           ),
    row=1, col=2
)

# Set theme, margin, and annotation in layout
fig.update_layout(
    template="plotly_dark",
    margin=dict(r=10, t=25, b=40, l=60),
    annotations=[dict(text="", showarrow=False, xref="paper", yref="paper", x=0, y=0)]
)

fig.show()

if __name__ == '__main__':
    app.run_server()
