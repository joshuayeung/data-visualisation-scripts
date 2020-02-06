
# coding: utf-8

# In[32]:


import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math 

import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[33]:


# Import xlsx file and store each sheet in to a df list
xl_file = pd.ExcelFile('./data.xlsx',)

dfs = {sheet_name: xl_file.parse(sheet_name) 
          for sheet_name in xl_file.sheet_names}


# In[34]:


# Data from each sheet can be accessed via key
keyList = list(dfs.keys())


# In[35]:


# Data cleansing
for key, df in dfs.items():
    dfs[key].loc[:,'Confirmed'].fillna(value=0, inplace=True)
    dfs[key].loc[:,'Deaths'].fillna(value=0, inplace=True)
    dfs[key].loc[:,'Recovered'].fillna(value=0, inplace=True)
    dfs[key]=dfs[key].astype({'Confirmed':'int64', 'Deaths':'int64', 'Recovered':'int64'})
    # Change as China for coordinate search
    dfs[key]=dfs[key].replace({'Country/Region':'Mainland China'}, 'China')
    dfs[key]=dfs[key].replace({'Province/State':'Queensland'}, 'Brisbane')
    dfs[key]=dfs[key].replace({'Province/State':'New South Wales'}, 'Sydney')
    dfs[key]=dfs[key].replace({'Province/State':'Victoria'}, 'Melbourne')
    # Add a zero to the date so can be convert by datetime.strptime as 0-padded date
    dfs[key]['Last Update'] = '0' + dfs[key]['Last Update']
    # Convert time as Hong Kong time
    dfs[key]['Date_last_updated_AEDT'] = [datetime.strptime(d, '%m/%d/%Y %H:%M') for d in dfs[key]['Last Update']]
    dfs[key]['Date_last_updated_AEDT'] = dfs[key]['Date_last_updated_AEDT'] + timedelta(hours=13)


# In[36]:


# Check 
dfs[keyList[1]].head()


# In[37]:


# Import data with coordinates (coordinates were called seperately in "Updated_coordinates")
dfs[keyList[0]]=pd.read_csv('{}_data.csv'.format(keyList[0]))


# In[38]:


dfs[keyList[0]][dfs[keyList[0]]['Province/State']=='Hong Kong']


# In[39]:


# Save numbers into variables to use in the app
confirmedCases=dfs[keyList[0]][dfs[keyList[0]]['Province/State']=='Hong Kong']['Confirmed'].sum()
deathsCases=dfs[keyList[0]][dfs[keyList[0]]['Province/State']=='Hong Kong']['Deaths'].sum()
recoveredCases=dfs[keyList[0]][dfs[keyList[0]]['Province/State']=='Hong Kong']['Recovered'].sum()


# In[40]:


confirmedCases


# In[59]:


# Construct new dataframe for line plot
DateList = []
ChinaList =[]
HKList = []
OtherList = []

for key, df in dfs.items():
    dfTpm = df.groupby(['Country/Region'])['Confirmed'].agg(np.sum)
    dfTpm = pd.DataFrame({'Code':dfTpm.index, 'Confirmed':dfTpm.values})
    dfTpm = dfTpm.sort_values(by='Confirmed', ascending=False).reset_index(drop=True)
    DateList.append(df['Date_last_updated_AEDT'][0])
    ChinaList.append(dfTpm['Confirmed'][0])
    HKList.append(dfTpm[dfTpm['Code']=='Hong Kong']['Confirmed'].sum())
    OtherList.append(dfTpm['Confirmed'][1:].sum()-dfTpm[dfTpm['Code']=='Hong Kong']['Confirmed'].sum())
    
df_confirmed = pd.DataFrame({'Date':DateList,
                             'Mainland China':ChinaList,
                             'Hong Kong':HKList,
                             'Other locations':OtherList})    


# In[61]:


df_confirmed['date_day']=[d.date() for d in df_confirmed['Date']]
df_confirmed=df_confirmed.groupby(by=df_confirmed['date_day'], sort=False).transform(max).drop_duplicates(['Date'])
df_confirmed['Total']=df_confirmed['Mainland China']+df_confirmed['Hong Kong']+df_confirmed['Other locations']
df_confirmed=df_confirmed.reset_index(drop=True)
df_confirmed


# In[64]:


# Construct new dataframe for line plot
DateList = []
ChinaList =[]
HKList = []
OtherList = []

for key, df in dfs.items():
    dfTpm = df.groupby(['Country/Region'])['Recovered'].agg(np.sum)
    dfTpm = pd.DataFrame({'Code':dfTpm.index, 'Recovered':dfTpm.values})
    dfTpm = dfTpm.sort_values(by='Recovered', ascending=False).reset_index(drop=True)
    DateList.append(df['Date_last_updated_AEDT'][0])
    ChinaList.append(dfTpm['Recovered'][0])
    HKList.append(dfTpm[dfTpm['Code']=='Hong Kong']['Recovered'].sum())
    OtherList.append(dfTpm['Recovered'][1:].sum()-dfTpm[dfTpm['Code']=='Hong Kong']['Recovered'].sum())
    
df_recovered = pd.DataFrame({'Date':DateList,
                             'Mainland China':ChinaList,
                             'Hong Kong': HKList,
                             'Other locations':OtherList})  


# In[65]:


df_recovered['date_day']=[d.date() for d in df_recovered['Date']]
df_recovered=df_recovered.groupby(by=df_recovered['date_day'], sort=False).transform(max).drop_duplicates(['Date'])

df_recovered


# In[67]:


# Construct new dataframe for line plot
DateList = []
ChinaList =[]
HKList = []
OtherList = []

for key, df in dfs.items():
    dfTpm = df.groupby(['Country/Region'])['Deaths'].agg(np.sum)
    dfTpm = pd.DataFrame({'Code':dfTpm.index, 'Deaths':dfTpm.values})
    dfTpm = dfTpm.sort_values(by='Deaths', ascending=False).reset_index(drop=True)
    DateList.append(df['Date_last_updated_AEDT'][0])
    ChinaList.append(dfTpm['Deaths'][0])
    HKList.append(dfTpm[dfTpm['Code']=='Hong Kong']['Deaths'].sum())
    OtherList.append(dfTpm['Deaths'][1:].sum()-dfTpm[dfTpm['Code']=='Hong Kong']['Deaths'].sum())
    
df_deaths = pd.DataFrame({'Date':DateList,
                          'Mainland China':ChinaList,
                          'Hong Kong':HKList,
                          'Other locations':OtherList})  


# In[68]:


df_deaths['date_day']=[d.date() for d in df_deaths['Date']]
df_deaths=df_deaths.groupby(by='date_day', sort=False).transform(max).drop_duplicates(['Date'])

df_deaths


# In[69]:


# Save numbers into variables to use in the app
latestDate=datetime.strftime(df_confirmed['Date'][0], '%b %d %Y %H:%M AEDT')
daysOutbreak=(df_confirmed['Date'][0] - datetime.strptime('12/31/2019', '%m/%d/%Y')).days


# In[70]:


latestDate


# In[71]:


# Line plot for confirmed cases
# Set up tick scale based on confirmed case number
tickList = list(np.arange(0, df_confirmed['Hong Kong'].max()+10, 20))

# Create empty figure canvas
fig_confirmed = go.Figure()
# Add trace to the figure
# fig_confirmed.add_trace(go.Scatter(x=df_confirmed['Date'], y=df_confirmed['Mainland China'],
#                                    mode='lines+markers',
#                                    name='Mainland China',
#                                    line=dict(color='#921113', width=3),
#                                    marker=dict(size=8, color='#f4f4f2',
#                                                line=dict(width=1,color='#921113')),
#                                    text=[datetime.strftime(d, '%b %d %Y AEDT') for d in df_confirmed['Date']],
#                                    hovertext=['Mainland China confirmed<br>{:,d} cases<br>'.format(i) for i in df_confirmed['Mainland China']],
#                                    hovertemplate='<b>%{text}</b><br></br>'+
#                                                  '%{hovertext}'+
#                                                  '<extra></extra>'))
fig_confirmed.add_trace(go.Scatter(x=df_confirmed['Date'], y=df_confirmed['Hong Kong'],
                                   mode='lines+markers',
                                   name='Hong Kong',
                                   line=dict(color='#921113', width=3),
                                   marker=dict(size=8, color='#f4f4f2',
                                               line=dict(width=1,color='#921113')),
                                   text=[datetime.strftime(d, '%b %d %Y AEDT') for d in df_confirmed['Date']],
                                   hovertext=['Hong Kong confirmed<br>{:,d} cases<br>'.format(i) for i in df_confirmed['Hong Kong']],
                                   hovertemplate='<b>%{text}</b><br></br>'+
                                                 '%{hovertext}'+
                                                 '<extra></extra>'))
# fig_confirmed.add_trace(go.Scatter(x=df_confirmed['Date'], y=df_confirmed['Other locations'],
#                                    mode='lines+markers',
#                                    name='Other Region',
#                                    line=dict(color='#eb5254', width=3),
#                                    marker=dict(size=8, color='#f4f4f2',
#                                                line=dict(width=1,color='#eb5254')),
#                                    text=[datetime.strftime(d, '%b %d %Y AEDT') for d in df_confirmed['Date']],
#                                    hovertext=['Other locations confirmed<br>{:,d} cases<br>'.format(i) for i in df_confirmed['Other locations']],
#                                    hovertemplate='<b>%{text}</b><br></br>'+
#                                                  '%{hovertext}'+
#                                                  '<extra></extra>'))
# Customise layout
fig_confirmed.update_layout(
    #title=dict(
    #    text="<b>Confirmed Cases Timeline<b>",
    #    y=0.96, x=0.5, xanchor='center', yanchor='top',
    #    font=dict(size=20, color="#292929", family="Playfair Display")
    #),
    margin=go.layout.Margin(
        l=10,
        r=10,
        b=10,
        t=5,
        pad=0
    ),
    yaxis=dict(
        showline=True, linecolor='#272e3e',
        zeroline=False,
        gridcolor='#cbd2d3',
        gridwidth = .1,
        tickmode='array',
        # Set tick range based on the maximum number
        tickvals=tickList,
        # Set tick label accordingly
        ticktext=["{:.0f}k".format(i/1000) for i in tickList]
    ),
#    yaxis_title="Total Confirmed Case Number",
    xaxis=dict(
        showline=True, linecolor='#272e3e',
        gridcolor='#cbd2d3',
        gridwidth = .1,
        zeroline=False
    ),
    xaxis_tickformat='%b %d',
    hovermode = 'x',
    legend_orientation="h",
#    legend=dict(x=.35, y=-.05),
    plot_bgcolor='#f4f4f2',
    paper_bgcolor='#cbd2d3',
    font=dict(color='#292929')
)

fig_confirmed.show()


# In[75]:


# Line plot for recovered cases
# Set up tick scale based on confirmed case number
tickList = list(np.arange(0, df_recovered['Hong Kong'].max()+10, 100))

# Create empty figure canvas
fig_recovered = go.Figure()
# Add trace to the figure
# fig_recovered.add_trace(go.Scatter(x=df_recovered['Date'], y=df_recovered['Mainland China'],
#                                    mode='lines+markers',
#                                    name='Mainland China',
#                                    line=dict(color='#168038', width=3),
#                                    marker=dict(size=8, color='#f4f4f2',
#                                                line=dict(width=1,color='#168038')),
#                                    text=[datetime.strftime(d, '%b %d %Y AEDT') for d in df_recovered['Date']],
#                                    hovertext=['Mainland China recovered<br>{:,d} cases<br>'.format(i) for i in df_recovered['Mainland China']],
#                                    hovertemplate='<b>%{text}</b><br></br>'+
#                                                  '%{hovertext}'+
#                                                  '<extra></extra>'))
fig_recovered.add_trace(go.Scatter(x=df_recovered['Date'], y=df_recovered['Hong Kong'],
                                   mode='lines+markers',
                                   name='Hong Kong',
                                   line=dict(color='#168038', width=3),
                                   marker=dict(size=8, color='#f4f4f2',
                                               line=dict(width=1,color='#168038')),
                                   text=[datetime.strftime(d, '%b %d %Y AEDT') for d in df_recovered['Date']],
                                   hovertext=['Hong Kong recovered<br>{:,d} cases<br>'.format(i) for i in df_recovered['Hong Kong']],
                                   hovertemplate='<b>%{text}</b><br></br>'+
                                                 '%{hovertext}'+
                                                 '<extra></extra>'))
# fig_recovered.add_trace(go.Scatter(x=df_recovered['Date'], y=df_recovered['Other locations'],
#                                    mode='lines+markers',
#                                    name='Other Region',
#                                    line=dict(color='#25d75d', width=3),
#                                    marker=dict(size=8, color='#f4f4f2',
#                                                line=dict(width=1,color='#25d75d')),
#                                    text=[datetime.strftime(d, '%b %d %Y AEDT') for d in df_recovered['Date']],
#                                    hovertext=['Other locations recovered<br>{:,d} cases<br>'.format(i) for i in df_recovered['Other locations']],
#                                    hovertemplate='<b>%{text}</b><br></br>'+
#                                                  '%{hovertext}'+
#                                                  '<extra></extra>'))
# Customise layout
fig_recovered.update_layout(
    #title=dict(
    #    text="<b>Recovered Cases Timeline<b>",
    #    y=0.96, x=0.5, xanchor='center', yanchor='top',
    #    font=dict(size=20, color="#292929", family="Playfair Display")
    #),
    margin=go.layout.Margin(
        l=10,
        r=10,
        b=10,
        t=5,
        pad=0
    ),
    yaxis=dict(
        showline=True, linecolor='#272e3e',
        zeroline=False,
        gridcolor='#cbd2d3',
        gridwidth = .1,
        tickmode='array',
        # Set tick range based on the maximum number
        tickvals=tickList,
        # Set tick label accordingly
        ticktext=['{:.0f}'.format(i) for i in tickList]
    ),
#    yaxis_title="Total Recovered Case Number",
    xaxis=dict(
        showline=True, linecolor='#272e3e',
        gridcolor='#cbd2d3',
        gridwidth = .1,
        zeroline=False
    ),
    xaxis_tickformat='%b %d',
    hovermode = 'x',
    legend_orientation="h",
#    legend=dict(x=.35, y=-.05),
    plot_bgcolor='#f4f4f2',
    paper_bgcolor='#cbd2d3',
    font=dict(color='#292929')
)

fig_recovered.show()


# In[76]:


# Line plot for deaths cases
# Set up tick scale based on confirmed case number
tickList = list(np.arange(0, df_deaths['Hong Kong'].max()+100, 100))

# Create empty figure canvas
fig_deaths = go.Figure()
# Add trace to the figure
fig_deaths.add_trace(go.Scatter(x=df_deaths['Date'], y=df_deaths['Hong Kong'],
                                mode='lines+markers',
                                name='Hong Kong',
                                line=dict(color='#626262', width=3),
                                marker=dict(size=8, color='#f4f4f2',
                                            line=dict(width=1,color='#626262')),
                                text=[datetime.strftime(d, '%b %d %Y AEDT') for d in df_deaths['Date']],
                                hovertext=['Hong Kong death<br>{:,d} cases<br>'.format(i) for i in df_deaths['Hong Kong']],
                                hovertemplate='<b>%{text}</b><br></br>'+
                                              '%{hovertext}'+
                                              '<extra></extra>'))
# fig_deaths.add_trace(go.Scatter(x=df_deaths['Date'], y=df_deaths['Other locations'],
#                                 mode='lines+markers',
#                                 name='Other Region',
#                                 line=dict(color='#a7a7a7', width=3),
#                                 marker=dict(size=8, color='#f4f4f2',
#                                             line=dict(width=1,color='#a7a7a7')),
#                                 text=[datetime.strftime(d, '%b %d %Y AEDT') for d in df_deaths['Date']],
#                                 hovertext=['Other locations death<br>{:,d} cases<br>'.format(i) for i in df_deaths['Other locations']],
#                                 hovertemplate='<b>%{text}</b><br></br>'+
#                                               '%{hovertext}'+
#                                               '<extra></extra>'))
# Customise layout
fig_deaths.update_layout(
#    title=dict(
#        text="<b>Death Cases Timeline<b>",
#        y=0.96, x=0.5, xanchor='center', yanchor='top',
#        font=dict(size=20, color="#292929", family="Playfair Display")
#    ),
    margin=go.layout.Margin(
        l=10,
        r=10,
        b=10,
        t=5,
        pad=0
    ),
    yaxis=dict(
        showline=True, linecolor='#272e3e',
        zeroline=False,
        gridcolor='#cbd2d3',
        gridwidth = .1,
        tickmode='array',
        # Set tick range based on the maximum number
        tickvals=tickList,
        # Set tick label accordingly
        ticktext=['{:.0f}'.format(i) for i in tickList]
    ),
#    yaxis_title="Total Death Case Number",
    xaxis=dict(
        showline=True, linecolor='#272e3e',
        gridcolor='#cbd2d3',
        gridwidth = .1,
        zeroline=False
    ),
    xaxis_tickformat='%b %d',
    hovermode = 'x',
    legend_orientation="h",
#    legend=dict(x=.35, y=-.05),
    plot_bgcolor='#f4f4f2',
    paper_bgcolor='#cbd2d3',
    font=dict(color='#292929')
)

fig_deaths.show()


# In[77]:


mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvNDMyaTAxYzkzeW5ubWdpZ2VjbmMifQ.TXcBE-xg9BFdV2ocecc_7g"

# Generate a list for hover text display
textList=[]
for area, region in zip(dfs[keyList[0]]['Province/State'], dfs[keyList[0]]['Country/Region']):
    
    if type(area) is str:
        if region == "Hong Kong" or region == "Macau" or region == "Taiwan":
            textList.append(area)
        else:
            textList.append(area+', '+region)
    else:
        textList.append(region)

fig2 = go.Figure(go.Scattermapbox(
        lat=dfs[keyList[0]]['lat'],
        lon=dfs[keyList[0]]['lon'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            color='#ca261d',
            size=dfs[keyList[0]]['Confirmed'].tolist(), 
            sizemin=2,
            sizemode='area',
            sizeref=2.*max(dfs[keyList[0]]['Confirmed'].tolist())/(80.**2),
        ),
        text=textList,
        hovertext=['Comfirmed: {}<br>Recovered: {}<br>Death: {}'.format(i, j, k) for i, j, k in zip(dfs[keyList[0]]['Confirmed'],
                                                                                                    dfs[keyList[0]]['Recovered'],
                                                                                                    dfs[keyList[0]]['Deaths'])],
    
        hovertemplate = "<b>%{text}</b><br><br>" +
                        "%{hovertext}<br>" +
                        "<extra></extra>")
    
        )

fig2.update_layout(
#    title=dict(
#        text="<b>Latest Coronavirus Outbreak Map<b>",
#        y=0.96, x=0.5, xanchor='center', yanchor='top',
#        font=dict(size=20, color="#292929", family="Playfair Display")
#    ),
    plot_bgcolor='#151920',
    paper_bgcolor='#cbd2d3',
    margin=go.layout.Margin(
        l=10,
        r=10,
        b=10,
        t=0,
        pad=40
    ),
    hovermode='closest',
    mapbox=go.layout.Mapbox(
        accesstoken=mapbox_access_token,
        style="light",
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=29.538860, 
            lon=173.304781
        ),
        pitch=0,
        zoom=2
    )
)

fig2.show()


# In[79]:


import dash
import dash_core_components as dcc
import dash_html_components as html 
import dash_bootstrap_components as dbc


# In[80]:


app = dash.Dash(__name__, assets_folder='./assets/',
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, height=device-height, initial-scale=1.0"}
    ])


# In[81]:


app.layout = html.Div(style={'backgroundColor':'#f4f4f2'},
    children=[
        html.Div(
            id="header",
            children=[                          
                html.H4(children="Wuhan Coronavirus (2019-nCoV) Outbreak Monitor"),
                html.P(
                    id="description",
                    children="On Dec 31, 2019, the World Health Organization (WHO) was informed of \
                    an outbreak of “pneumonia of unknown cause” detected in Wuhan City, Hubei Province, China – the \
                    seventh-largest city in China with 11 million residents. As of {}, there are over {} cases \
                    of 2019-nCoV confirmed globally.\
                    This dash board is developed to visualise and track the recent reported \
                    cases on a daily timescale.".format(latestDate, confirmedCases),
                ),
                html.P(style={'fontWeight':'bold'},
                    children="Last updated on {}.".format(latestDate))
            ]        
        ),
        html.Div(
            id="number-plate",
            style={'marginLeft':'1.5%','marginRight':'1.5%','marginBottom':'.5%'},
                 children=[
                     html.Div(
                         style={'width':'24.4%','backgroundColor':'#cbd2d3','display':'inline-block',
                                'marginRight':'.8%','verticalAlign':'top'},
                              children=[
                                  html.H3(style={'textAlign':'center',
                                                       'fontWeight':'bold','color':'#ffffbf'},
                                               children='{}'.format(daysOutbreak)),
                                  html.P(style={'textAlign':'center',
                                                      'fontWeight':'bold','color':'#ffffbf','padding':'.1rem'},
                                               children="Days Since Outbreak")                                        
                                       ]),
                     html.Div(
                         style={'width':'24.4%','backgroundColor':'#cbd2d3','display':'inline-block',
                                'marginRight':'.8%','verticalAlign':'top'},
                              children=[
                                  html.H3(style={'textAlign':'center',
                                                       'fontWeight':'bold','color':'#d7191c'},
                                                children='{:,d}'.format(confirmedCases)),
                                  html.P(style={'textAlign':'center',
                                                      'fontWeight':'bold','color':'#d7191c','padding':'.1rem'},
                                               children="Confirmed Cases")                                        
                                       ]),
                     html.Div(
                         style={'width':'24.4%','backgroundColor':'#cbd2d3','display':'inline-block',
                                'marginRight':'.8%','verticalAlign':'top'},
                              children=[
                                  html.H3(style={'textAlign':'center',
                                                       'fontWeight':'bold','color':'#1a9622'},
                                               children='{:,d}'.format(recoveredCases)),
                                  html.P(style={'textAlign':'center',
                                                      'fontWeight':'bold','color':'#1a9622','padding':'.1rem'},
                                               children="Recovered Cases")                                        
                                       ]),
                     html.Div(
                         style={'width':'24.4%','backgroundColor':'#cbd2d3','display':'inline-block',
                                'verticalAlign':'top'},
                              children=[
                                  html.H3(style={'textAlign':'center',
                                                       'fontWeight':'bold','color':'#6c6c6c'},
                                                children='{:,d}'.format(deathsCases)),
                                  html.P(style={'textAlign':'center',
                                                      'fontWeight':'bold','color':'#6c6c6c','padding':'.1rem'},
                                               children="Death Cases")                                        
                                       ])
                          ]),
        html.Div(
            id='dcc-plot',
            style={'marginLeft':'1.5%','marginRight':'1.5%','marginBottom':'.35%','marginTop':'.5%'},
                 children=[
                     html.Div(
                         style={'width':'32.79%','display':'inline-block','marginRight':'.8%','verticalAlign':'top'},
                              children=[
                                  html.H5(style={'textAlign':'center','backgroundColor':'#cbd2d3',
                                                 'color':'#292929','padding':'1rem','marginBottom':'0'},
                                               children='Confirmed Case Timeline'),
                                  dcc.Graph(figure=fig_confirmed)]),
                     html.Div(
                         style={'width':'32.79%','display':'inline-block','marginRight':'.8%','verticalAlign':'top'},
                              children=[
                                  html.H5(style={'textAlign':'center','backgroundColor':'#cbd2d3',
                                                 'color':'#292929','padding':'1rem','marginBottom':'0'},
                                               children='Recovered Case Timeline'),
                                  dcc.Graph(figure=fig_recovered)]),
                     html.Div(
                         style={'width':'32.79%','display':'inline-block','verticalAlign':'top'},
                              children=[
                                  html.H5(style={'textAlign':'center','backgroundColor':'#cbd2d3',
                                                 'color':'#292929','padding':'1rem','marginBottom':'0'},
                                               children='Death Case Timeline'),
                                  dcc.Graph(figure=fig_deaths)])]),
        html.Div(
            id='dcc-map',
            style={'marginLeft':'1.5%','marginRight':'1.5%','marginBottom':'.5%'},
                 children=[
                     html.Div(style={'width':'100%','display':'inline-block','verticalAlign':'top'},
                              children=[
                                  html.H5(style={'textAlign':'center','backgroundColor':'#cbd2d3',
                                                 'color':'#292929','padding':'1rem','marginBottom':'0'},
                                               children='Latest Coronavirus Outbreak Map'),
                                  dcc.Graph(figure=fig2)]),]),
        html.Div(style={'marginLeft':'1.5%','marginRight':'1.5%'},
                 children=[
                     html.P(style={'textAlign':'center','margin':'auto'},
                            children=["Data source from ", 
                                      html.A('JHU CSSE,', href='https://docs.google.com/spreadsheets/d/1yZv9w9z\
                                      RKwrGTaR-YzmAqMefw4wMlaXocejdxZaTs6w/htmlview?usp=sharing&sle=true#'),
                                      html.A(' Dingxiangyuan', href='https://ncov.dxy.cn/ncovh5/view/pneumonia?sce\
                                      ne=2&clicktime=1579582238&enterid=1579582238&from=singlemessage&isappinstalled=0'),
                                      " | 🙏 Pray for China, Pray for the World 🙏 |",
                                      " Developed by ",html.A('Jun', href='https://junye0798.com/')," with ❤️"])])

            ])


# In[82]:


if __name__ == '__main__':
    app.run_server(port=8882)


# In[83]:


app.layout = html.Div(style={'backgroundColor':'#f4f4f2'},
    children=[
        html.Div(
            id="header",
            children=[                          
                html.H4(children="Wuhan Coronavirus (2019-nCoV) Outbreak Monitor"),
                html.P(
                    id="description",
                    children="On Dec 31, 2019, the World Health Organization (WHO) was informed of \
                    an outbreak of “pneumonia of unknown cause” detected in Wuhan City, Hubei Province, China – the \
                    seventh-largest city in China with 11 million residents. As of {}, there are over {} cases \
                    of 2019-nCoV confirmed globally.\
                    This dash board is developed to visualise and track the recent reported \
                    cases on a daily timescale.".format(latestDate, confirmedCases),
                ),
                html.P(style={'fontWeight':'bold'},
                    children="Last updated on {}.".format(latestDate))
            ]        
        ),
        html.Div(
            style={'marginLeft':'1.5%','marginRight':'1.5%','display':'flex'},
            children=[
                html.Div(
                    style={'marginRight':'.8%','flex':'.2'},
                    children=[
                        html.Div(style={'width':'100%','marginBottom':'.8%','display':'inline-block'},
                                 children=[dcc.Graph(figure=fig_confirmed)]),
                        html.Div(style={'width':'100%','marginBottom':'.8%','display':'inline-block'},
                                 children=[dcc.Graph(figure=fig_recovered)]),
                        html.Div(style={'width':'100%','display':'inline-block'},
                                 children=[dcc.Graph(figure=fig_deaths)]),
                    ]
                ),
                html.Div(
                    style={'marginRight':'.8%',
                           'flex':'.65'},
                    children=[
                                html.Div(
                                    style={'width':'24.4%','height':'15%','backgroundColor':'#cbd2d3','display':'inline-block','marginRight':'.8%'},
                                    children=[
                                        html.H3(style={'textAlign':'center',
                                                       'fontWeight':'bold','color':'#ffffbf'},
                                                children='{}'.format(daysOutbreak)),
                                        html.P(style={'textAlign':'center',
                                                      'fontWeight':'bold','color':'#ffffbf','padding':'.1rem'},
                                               children="Days Since Outbreak")                                        
                                       ]),
                                html.Div(
                                    style={'width':'24.4%','height':'15%','backgroundColor':'#cbd2d3','display':'inline-block','marginRight':'.8%'},
                                    children=[
                                        html.H3(style={'textAlign':'center',
                                                       'fontWeight':'bold','color':'#d7191c'},
                                                children='{:,d}'.format(confirmedCases)),
                                        html.P(style={'textAlign':'center',
                                                      'fontWeight':'bold','color':'#d7191c','padding':'.1rem'},
                                               children="Confirmed Cases")                                        
                                       ]),
                                 html.Div(
                                     style={'width':'24.4%','height':'15%','backgroundColor':'#cbd2d3','display':'inline-block','marginRight':'.8%'},
                                     children=[
                                         html.H3(style={'textAlign':'center',
                                                        'fontWeight':'bold','color':'#1a9622'},
                                                 children='{:,d}'.format(recoveredCases)),
                                         html.P(style={'textAlign':'center',
                                                       'fontWeight':'bold','color':'#1a9622','padding':'.1rem'},
                                                 children="Recovered Cases")                                        
                                       ]),
                                 html.Div(
                                     style={'width':'24.4%','height':'15%','backgroundColor':'#cbd2d3','display':'inline-block'},
                                     children=[
                                         html.H3(style={'textAlign':'center',
                                                        'fontWeight':'bold','color':'#6c6c6c'},
                                                 children='{:,d}'.format(deathsCases)),
                                         html.P(style={'textAlign':'center',
                                                       'fontWeight':'bold','color':'#6c6c6c','padding':'.1rem'},
                                                 children="Death Cases")                                        
                                       ]),
                                 html.Div(
                                     style={'width':'100%','height':'85%','margniTop':'.8%','display':'inline-block'},
                                     children=[
                                         dcc.Graph(figure=fig2)                                 
                                        ])                               
                           ]),
                html.Div(
                    style={'flex':'.13'},
                    children=[
                        dcc.Graph(figure=fig2)                        
                    ]
                )
            ]
        
        ),
        html.Div(style={'marginLeft':'1.5%','marginRight':'1.5%','marginTop':'.8%'},
                 children=[
                     html.P(style={'textAlign':'center','margin':'auto'},
                            children=["Data source from ", 
                                      html.A('JHU CSSE,', href='https://docs.google.com/spreadsheets/d/1yZv9w9z\
                                      RKwrGTaR-YzmAqMefw4wMlaXocejdxZaTs6w/htmlview?usp=sharing&sle=true#'),
                                      html.A(' Dingxiangyuan', href='https://ncov.dxy.cn/ncovh5/view/pneumonia?sce\
                                      ne=2&clicktime=1579582238&enterid=1579582238&from=singlemessage&isappinstalled=0'),
                                      " | 🙏 Pray for China, Pray for the World 🙏 |",
                                      " Developed by ",html.A('Jun', href='https://junye0798.com/')," with ❤️"])])

])


# In[85]:


if __name__ == '__main__':
    app.run_server(port=8882)

