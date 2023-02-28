#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')
from jupyter_dash import JupyterDash
import dash_html_components as html 
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from plotly.subplots import make_subplots


# In[2]:


df_url = pd.read_csv('finalURL_version3.csv')


# In[3]:


emailSMSData = pd.read_csv('spam1.csv', encoding='latin-1')


# In[4]:


from dash import Dash, dcc, html, dash_table, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
import plotly.graph_objects as go


features = ['?','=','.','%','//']
names = {'?':'Question Mark (?)','=':'Equal sign(=)','.':'Dot (.)','%':'Precentage (%)','//':'Double Slash (//)'}
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = JupyterDash(external_stylesheets=[dbc.themes.LUMEN, dbc_css])
header = html.H1("SECURE CLICK DASHBOARD", className="text-white p-2 mb-2 text-center", style={"background-color":"#73a1c7"})

# types dropdown menu
typeDropdown = html.Div(
    [
        html.Br(),
        html.H3('Special Characters Tab'),
        dbc.Label("Select Attack Type: "),
        dcc.Dropdown(
            options=[
            {'label':'benign','value':0},
            {'label':'defacement','value':1},
            {'label':'phishing','value':2},
            {'label':'malware', 'value':3},
            {'label':'All', 'value':4} 
            ],
            value = 4,
            id="attackType",
            clearable=False,
            ),
    ],
    className="mb-4",
)

# Special charcters checklist
charChecklist = html.Div(
    [
        dbc.Label("Select Special Charater: "),
        dbc.Checklist(id="features",
            options=[{"label": names[i], "value": i} for i in names],
            value=features,
            inline=True,
        ),
    ],
    className="mb-4",
)

# Alphabet and digit dropdown
dropdownAlphaNum = html.Div(
    [
        html.Br(), 
        html.H3('Alpha&Digits Count Tab'),
        dbc.Label("Select indicator: "),
        dcc.Dropdown(options=[
            {'label':'Alphabetic','value':1},
            {'label':'Numeric','value':2} 
   
            ],
        
            value = 2,
            id="dropDownCount",
            clearable=False,
        ),
    ],
    className="mb-4",
)

# Alphabet and digit range slider
alphaNumSlider = html.Div(
    [
        dbc.Label("Select Range: "),
        dcc.RangeSlider(
            step=5,
            id='count-slider',
            value=[2,14], #defualt values
            tooltip={"placement": "top", "always_visible": True},
            
            ),
    ],
    className="mb-4",
)

# reset if features dropdown menu
moreFetures = html.Div(
    [
        html.Br(),
        html.H3('More Feature Tab'),
        dbc.Label("Select indicator: "),
        dcc.Dropdown(options=[
            {'label':'Host Name','value':1},
            {'label':'Tiny URL','value':2},
            {'label':'IP Adderss','value':3},
            {'label':'Https','value':4}
   
            ],
        
            value = 1,
            id="moreFetures",
            clearable=False,
        ),
    ],
    className="mb-4",
)

# reset if features yes or no checklist
yesNoChecklist = html.Div(
    [
        dbc.Label("Show feature values: "),
        dbc.Checklist(
            id="yesNoList",
            options=[{"label": "Yes", "value": 1},
                    {"label": "No", "value": 0}],
            value=[0,1],
            inline=True,
        ),
    ],
    className="mb-4",
)


# Controls for URL
controlsTab1 = dbc.Card(
        [typeDropdown, charChecklist,
        dropdownAlphaNum, alphaNumSlider,
        moreFetures, yesNoChecklist]
)


# SMS drop down
textDropdown = html.Div(
    [
        html.Br(),
        html.H3('More Feature Tab'),
        dbc.Label("Select indicator: "),
        dcc.Dropdown(options=[
            {'label':'Word count','value':1},
            {'label':'Letters count','value':2},
            {'label':'Sentence count','value':3}
   
            ],
        
            value = 1,
            id="dropMenu2",
            clearable=False,
        ),
    ],
    className="mb-4",
)

# SMS type checklist
textChecklist = html.Div(
    [
        dbc.Label("Show feature values: "),
        dbc.Checklist(
            id="checkList2",
            options=[{"label": "Ham", "value":'ham'},
                    {"label": "Spam", "value": 'spam'}],
            value=['ham','spam'],
            inline=True,
        ),
    ],
    className="mb-4",
)


# Controls for SMS - Email
Tab2controls = dbc.Card(
        [textDropdown, textChecklist]
)

# URL tabs
tab1 = dbc.Tab([dcc.Graph(id="barGraph")], label="Special Characters Tab")
tab2 = dbc.Tab([dcc.Graph(id="barGraph2")], label="Alpha&Digits Count Tab")
tab3 = dbc.Tab([dcc.Graph(id="barGraph3")],label="More Feature Tab", className="p-4")
tabs = dbc.Card(dbc.Tabs([tab1, tab2, tab3]))


# SMS - Email Tabs
tabfor = dbc.Tab([dcc.Graph(id="barGraph4")],label="Text Features Tab", tab_id="tab-1")
tabsSecond = dbc.Card(dbc.Tabs([tabfor], active_tab="tab-1"))


# Dashboard Layout
app.layout = dbc.Container(
    [
        header,
        dcc.Tabs([        
            dcc.Tab(label='URL',children=[        
                dbc.Row(
                [
                    dbc.Col([controlsTab1], width=4,),
                    dbc.Col([tabs], width=8)
                ])
            ]),
            dcc.Tab(label='Email & SMS',children=[        
                dbc.Row(
                [
                    dbc.Col([Tab2controls],width=4,),
                    dbc.Col([tabsSecond], width=8)
                ])
            ])
        
        
        ]) #Tabs end


    ],
    fluid=True,
    className="dbc") #Container end


@callback(
    Output("barGraph", "figure"),
    [Input("features", "value"),
    Input('attackType','value')
    ]
)
def updateCharters(char,attackType):
    typeDict = {
        0: 'benign',
        1: 'defacement',
        2:'phishing',
        3:'malware'    
    }
    
    if len(char) == 0:
        char =  ['?','=','.','%','//']
    
    All = df_url.groupby('type').mean().reset_index()
    if attackType!=4:
        All = All[All['type']==attackType]
        result = All[['?','=','.','%','//']]
        result['type']=typeDict[attackType]
        fig = px.bar(data_frame=result,x='type',
               y=char,
               barmode='group',title='Average numbe of symbols for each type').update_layout(title_x=0.5)
    else:
        result = All[['?','=','.','%','//']]
        result['type']=['benign','defacement','phishing','malware']
        fig = px.bar(data_frame=result,x='type',
               y=char, barmode='group',title='Average numbe of symbols for each type', 
               color_discrete_map={'?':'#90caf9','=':'#e7cbcb','.':'#567995',
                                   '%':'#73a1c7','//':'#c47d7d'}, template='plotly_white').update_layout(title_x=0.5)
    return fig
    
    
@callback(
    [Output("barGraph2", "figure"),
    Output("count-slider", "max"),
    Output("count-slider", "min")],
    
    [Input("dropDownCount","value"),
     Input("count-slider","value")]
)
def updateNumLetCount(alphaNum, countSlider):
    maxVal, minVal=0, 0
    title=''
    if alphaNum == 1:  
        alphaNum = 'alphabetCount'
        minVal = 33
        maxVal = 70
        title = 'The number of letters for each type'
    else:
        alphaNum = 'numberCount'
        minVal = 2 
        maxVal = 14
        title = 'The number of digits for each type'
        
    AlphaNum = round(df_url[['type',alphaNum]].groupby('type').mean().reset_index(),0)
    AlphaNum = AlphaNum[((AlphaNum[alphaNum]>=countSlider[0]) & (AlphaNum[alphaNum]<=countSlider[1]))]
    letters = pd.DataFrame()
    letters[alphaNum] = AlphaNum[alphaNum]
    letters['type']= AlphaNum['type'].map({0:'benign',1:'defacement',2:'phishing',3:'malware'})
    
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=letters.type,
        y=letters[alphaNum],
        name= alphaNum,
        marker_color='#73a1c7'
        )).update_layout(template='plotly_white')

    return fig2, maxVal, minVal


@callback(
    Output("barGraph3", "figure"),
    
    [Input("moreFetures","value"),
     Input("yesNoList","value")]
)

def updateThirdGraph(featureX, yesNo):
    xAxis = ''
    title = ''
    legendX , legendY ='',''
    ylist=[]
    if featureX == 1:
        xAxis = 'HasHostname'
        title = 'The number of hostname for each type'
        legendX = 'Has HostName'
        legendY = "Don't Has HostName"
    elif featureX == 2:
        xAxis = 'shortUrl'
        title = 'The number of Shortening Services for each type'
        legendX = 'Contains Short URL'
        legendY = "Don't Contains Short URL"
    elif featureX == 3:
        xAxis = 'ipAddress'
        title = 'The number of ip address for each type'
        legendX = 'Contains IP Address'
        legendY = "Don't Contains IP Address"
    elif featureX == 4:
        xAxis = 'IsHttps'
        title = 'The number of https for each type'
        legendX = 'Is Https'
        legendY = 'Not Https'
        
    featuresData = pd.crosstab(df_url.type,df_url[xAxis])
    featuresData['type']=['benign','defacement','phishing','malware']
    featuresData.rename(columns={0:legendY,1:legendX},inplace=True)
    
    if len(yesNo) == 2:
        ylist = [legendY,legendX]
    elif len(yesNo)==0:
        ylist = [legendY,legendX]
    elif yesNo[0] == 1:
        ylist = [legendX]
    else:
        ylist = [legendY]
        
    fig3 = px.bar(data_frame=featuresData,x=featuresData.type,y=ylist ,
           barmode='group',title=title, template='plotly_white', 
                color_discrete_map={legendY:'#73a1c7',legendX:'#c47d7d' }).update_layout(title_x=0.5)

    return fig3


@callback(
    Output("barGraph4", "figure"),
    
    [Input("dropMenu2","value"),
     Input("checkList2","value")]
)
def updateSMSGraph(smsType, checkListChoice):
    
    if smsType == 1:  
        smsType = 'words_count'
    elif smsType == 2:
        smsType = 'charcaters_count'
    else:
        smsType = 'sentence_count'

    if len(checkListChoice) ==2:     
        data = emailSMSData[((emailSMSData["target"]=='ham') | (emailSMSData["target"]=='spam'))]
    elif len(checkListChoice) == 0:
        data = emailSMSData[((emailSMSData["target"]=='ham') | (emailSMSData["target"]=='spam'))]
    elif checkListChoice[0] == 'spam':
         data = emailSMSData[emailSMSData["target"]=='spam']
    else:
         data = emailSMSData[emailSMSData["target"]=='ham']

    fig4 = px.histogram(data, x=smsType,color='target',template='plotly_white', 
                color_discrete_map={checkListChoice[0]:'#73a1c7',checkListChoice[1]:'#c47d7d' })


    return fig4

if __name__ == "__main__":
    app.run_server(debug=True, port=8011)


# In[ ]:




