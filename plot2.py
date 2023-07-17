#Get current Premier League Standings in a list
import pandas as pd
from html.parser import HTMLParser
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
from dash import Dash, html, dcc, dash_table
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from plotly.subplots import make_subplots
url = "https://www.espn.com/soccer/table/_/league/eng.1"
page = requests.get(url)
soup = bs(page.content, "html.parser")
results = soup.find_all("a", class_= 'AnchorLink')
results2 = soup.find_all("abbr", style= 'text-decoration:none')
results3 = soup.find_all("span", "team-position ml2 pr3")
results4 = soup.find(class_="Table__Scroller")
results5 = results4.select("td:nth-child("+str(8)+")")
results6 = results4.select("td:nth-child("+str(5)+")")
results7 = results4.select("td:nth-child("+str(6)+")")
results8 = results4.select("td:nth-child("+str(7)+")")
stand = []
for r, i, g, h, j, k in zip(results2, results3, results5, results6, results7, results8):
    stand.append(i.text + ","+ r.text + "," + g.text + "," + h.text + "," + j.text + "," + k.text)
df = pd.DataFrame([sub.split(",") for sub in stand])
df = df.reset_index(drop = True)

cols = ['Standing', 'Team', 'points', 'Scored For', 'Scored Against', 'Differential']
df.columns = cols
df[['Standing', 'points', 'Scored For', 'Scored Against', 'Differential']] = df[['Standing',  'points', 'Scored For', 'Scored Against', 'Differential']].apply(pd.to_numeric)
df


fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.05,
    specs=[[{"type": "Bar"}],
           [{"type": "Table"}]]
)

fig.add_trace(
    go.Bar(
        x=df["Team"],
        y=df["Scored For"],
        name="Scored For"
    ),
    row=1, col=1
)
fig.add_trace(
    go.Bar(
        x=df["Team"],
        y=df["Scored Against"],
        name="Scored Against",
    ),
    row=1, col=1
)

fig.add_trace(go.Table(
    header=dict(values=list(df.columns),
                align='left', fill_color ='rgba(0,0,0,0)',font=dict(color='white', size=12)),
    cells=dict(values=[df.Standing, df.Team, df.points, df['Scored For'], df['Scored Against'], df.Differential],
               align='left', fill_color ='rgba(0,0,0,0)', font=dict(color='white', size=12))),
    row = 2, col = 1)

fig.update_layout(
    height=1200,
    showlegend=True,
    title_text="The 2023-2024 Premier League Table",
title_y = 0.985, title_x = 0,
title_font_color="white",
legend_font_color = "white"
)
fig.layout.xaxis.color = 'white'
fig.layout.yaxis.color = 'white'
fig.update_yaxes(showgrid = False)
#fig.show()
fig.update_layout(legend = dict(bgcolor = 'rgba(0,0,0,0)'))
fig.update_layout(paper_bgcolor="rgb(0,0,0,0)",  plot_bgcolor='rgba(0,0,0,0)')
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
load_figure_template("darkly")
app = Dash(__name__,external_stylesheets=[dbc.themes.QUARTZ, dbc_css])
server = app.server 



app.layout = html.Div(children=[
    html.H1(children='  Prem Dash'),

    html.Div(children='''
        A Pemier League Team Statistic Dashboard with an Accompanying Visualization:
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )

])

if __name__ == '__main__':
    app.run_server(debug=True)
