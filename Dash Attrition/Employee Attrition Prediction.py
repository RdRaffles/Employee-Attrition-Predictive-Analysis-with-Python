import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import seaborn as sns
from dash.dependencies import Input, Output, State
import pickle
import numpy as np
import dash_table


def generate_table(dataframe, page_size=10):
    return dash_table.DataTable(
        id='dataTable',
        columns=[{
            "name": i,
            "id": i
        } for i in dataframe.columns],
        data=dataframe.to_dict('records'),
        page_action="native",
        page_current=0,
        page_size=page_size,
        style_table={'overflowX': 'scroll'},
        style_cell={
        'height': 'auto',
        'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
        'whiteSpace': 'normal'}
    )

path = 'HR-Employee-Attrition.csv'
data = pd.read_csv(path)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
loadModel = pickle.load(open('attrition_adb_model.sav', 'rb'))

app.layout = html.Div(
    children=[
        html.H1('Employee Attrition Prediction Machine'),
        html.Div(children='''Created by: Ardhi Raffles'''),

        dcc.Tabs(children=[
                dcc.Tab(value='Tab1', label='Employees Data', children=[
                    html.Div([
                        html.Div(children=[
                            html.P('Department: '),
                            dcc.Dropdown(id='filter-department', value = 'None',
                            options= [{'label' : 'None', 'value' : 'None'},
                                      {'label' : 'R & D', 'value' : 'Research & Development'},
                                      {'label' : 'Sales', 'value' : 'Sales'},
                                      {'label' : 'Human Resource', 'value' : 'Human Resources'},
                                      ]),
                        ],className='col-2'),

                        html.Div(children=[
                            html.P('Over Time: '),
                            dcc.Dropdown(id='filter-overtime', value = 'None',
                            options= [{'label' : 'None', 'value' : 'None'},
                                      {'label' : 'Yes', 'value' : 'Yes'},
                                      {'label' : 'No', 'value' : 'No'},
                                      ])
                        ],className='col-2'),

                        html.Div(children=[
                            html.P('Attrition: '),
                            dcc.Dropdown(id='filter-attrition', value = 'None',
                            options= [{'label' : 'None', 'value' : 'None'},
                                      {'label' : 'Yes', 'value' : 'Yes'},
                                      {'label' : 'No', 'value' : 'No'},
                                      ])
                        ],className='col-2'),

                        html.Div(children=[
                            html.P('Total Working Years:'),
                            dcc.Input(id ='filter-twy', type = 'number', value = '')
                        ], className = 'col-2'),

                        html.Div(children=[
                            html.P('Age:'),
                            dcc.Input(id ='filter-age', type = 'number', value = '')
                        ], className = 'col-2'),

                    ], className='row'),

                    html.Br(),

                    html.Div([
                        html.P('Max Rows: '),
                        dcc.Input(id ='filter-row',
                                    type = 'number', 
                                    value = 10)
                        ], className = 'row col-3'),

                    html.Div(children=[
                        html.Button('search', id = 'filter')
                        ],className = 'row col-4'),

                    html.Div(id='div-table',
                        children=[generate_table(data)])
                ]),

############################################################################################
                
                dcc.Tab(value='Tab2', label='Analysis Dashboard',children=[
                    html.Div(children = dcc.Graph(
                        id = 'Graph0',
                        figure = {'data':[
                                    go.Bar(x = (len(data[data['Attrition'] == 'Yes']), len(data[data['Attrition'] == 'No'])),
                                        y = ['Yes', 'No'], orientation = 'h', opacity = 0.8,
                                        marker=dict(color=['gold', 'lightskyblue'])) 
                                    ],
                                    'layout': go.Layout(
                                        dict(title =  'Count of attrition variable')  
                                )       
                            }
                    ), className = 'col-12'),

                    html.Div(children = dcc.Graph(
                        id = 'Graph1',
                        figure = {'data':[
                                    go.Pie(values  = data[data['Attrition'] == 'Yes']['Gender'].value_counts().values.tolist(),
                                        labels  = data[data['Attrition'] == 'Yes']['Gender'].value_counts().keys().tolist(),
                                        textfont=dict(size=15), opacity = 0.8,
                                        hoverinfo = "label+percent+name",
                                        domain  = dict(x = [0,.48]),
                                        name    = "attrition employes",
                                        marker  = dict(colors = ['gold', 'lightgreen', 'lightcoral', 'lightskyblue', 'lightgrey', 'orange', 'white', 'lightpink'], line = dict(width = 1.5))),
                                    
                                    go.Pie(values  = data[data['Attrition'] == 'No']['Gender'].value_counts().values.tolist(),
                                        labels  = data[data['Attrition'] == 'No']['Gender'].value_counts().keys().tolist(),
                                        textfont=dict(size=15), opacity = 0.8,
                                        hoverinfo = "label+percent+name",
                                        marker  = dict(colors = ['gold', 'lightgreen', 'lightcoral', 'lightskyblue', 'lightgrey', 'orange', 'white', 'lightpink'], line = dict(width = 1.5)),
                                        domain  = dict(x = [.52,1]),
                                        name    = "Non attrition employes" )
                                    ],
                                    'layout': go.Layout(
                                        dict(title = 'Gender' + " distribution in employes attrition ",
                                                annotations = [dict(text = "Yes_attrition",
                                                font = dict(size = 13),
                                                showarrow = False,
                                                x = .22, y = -0.1),
                                        dict(text = "No_attrition",
                                                font = dict(size = 13),
                                                showarrow = False,
                                                x = .8,y = -.1)])  
                                )       
                            }
                    ), className = 'col-12'),

                    html.Div(children = dcc.Graph(
                        id = 'Graph2',
                        figure = {'data':[
                                    go.Bar(
                                    x=data[(data['Attrition'] != 'No')]['OverTime'].value_counts().keys().tolist(),
                                    y=data[(data['Attrition'] != 'No')]['OverTime'].value_counts().values.tolist(),
                                    name='Yes_Attrition',opacity = 0.8, marker=dict(
                                    color='gold',
                                    line=dict(color='#000000',width=1))),
                                
                                    go.Bar(
                                    x=data[(data['Attrition'] == 'No')]['OverTime'].value_counts().keys().tolist(),
                                    y=data[(data['Attrition'] == 'No')]['OverTime'].value_counts().values.tolist(),
                                    name='No_Attrition', opacity = 0.8, marker=dict(
                                    color='lightskyblue',
                                    line=dict(color='#000000',width=1))), 
                                    
                                    go.Scatter(   
                                    x=pd.DataFrame(pd.crosstab(data['OverTime'],data['Attrition'])).sort_values('Yes', ascending = False).index,
                                    y=pd.DataFrame(pd.crosstab(data['OverTime'],data['Attrition'])).sort_values('Yes', ascending = False)['Yes'] / (pd.DataFrame(pd.crosstab(data['OverTime'],data['Attrition'])).sort_values('Yes', ascending = False)['Yes'] + pd.DataFrame(pd.crosstab(data['OverTime'],data['Attrition'])).sort_values('Yes', ascending = False)['No']) * 100,
                                    yaxis = 'y2',
                                    name='% Attrition', opacity = 0.6, marker=dict(
                                    color='black',
                                    line=dict(color='#000000',width=0.5
                                    ))) 
                                ],
                                    'layout': go.Layout(
                                    dict(title =  str('Over Time'),
                                    xaxis=dict(), 
                                    yaxis=dict(title= 'Count'), 
                                    yaxis2=dict(range= [-0, 75], 
                                                overlaying= 'y', 
                                                anchor= 'x', 
                                                side= 'right',
                                                zeroline=False,
                                                showgrid= False, 
                                                title= '% Attrition'
                                                ))  
                                )       
                            }
                    ), className = 'col-12'),

                    html.Div(children = dcc.Graph(
                        id = 'Graph3',
                        figure = {'data':[
                                    go.Bar(
                                    x=data[(data['Attrition'] != 'No')]['Age'].value_counts().keys().tolist(),
                                    y=data[(data['Attrition'] != 'No')]['Age'].value_counts().values.tolist(),
                                    name='Yes_Attrition',opacity = 0.8, marker=dict(
                                    color='gold',
                                    line=dict(color='#000000',width=1))),
                                
                                    go.Bar(
                                    x=data[(data['Attrition'] == 'No')]['Age'].value_counts().keys().tolist(),
                                    y=data[(data['Attrition'] == 'No')]['Age'].value_counts().values.tolist(),
                                    name='No_Attrition', opacity = 0.8, marker=dict(
                                    color='lightskyblue',
                                    line=dict(color='#000000',width=1))), 
                                    
                                    go.Scatter(   
                                    x=pd.DataFrame(pd.crosstab(data['Age'],data['Attrition']), ).index,
                                    y=pd.DataFrame(pd.crosstab(data['Age'],data['Attrition']))['Yes'] / (pd.DataFrame(pd.crosstab(data['Age'],data['Attrition']))['Yes'] + pd.DataFrame(pd.crosstab(data['Age'],data['Attrition']))['No']) * 100,
                                    yaxis = 'y2',
                                    name='% Attrition', opacity = 0.6, marker=dict(
                                    color='black',
                                    line=dict(color='#000000',width=0.5
                                    ))) 
                                ],
                                    'layout': go.Layout(
                                    dict(title =  str('Age'),
                                    xaxis=dict(), 
                                    yaxis=dict(title= 'Count'), 
                                    yaxis2=dict(range= [-0, 75], 
                                                overlaying= 'y', 
                                                anchor= 'x', 
                                                side= 'right',
                                                zeroline=False,
                                                showgrid= False, 
                                                title= '% Attrition'
                                                ))  
                                )       
                            }
                    ), className = 'col-12'),

                    html.Div(children = dcc.Graph(
                        id = 'Graph4',
                        figure = {'data':[
                                    go.Bar(
                                    x=data[(data['Attrition'] != 'No')]['TotalWorkingYears'].value_counts().keys().tolist(),
                                    y=data[(data['Attrition'] != 'No')]['TotalWorkingYears'].value_counts().values.tolist(),
                                    name='Yes_Attrition',opacity = 0.8, marker=dict(
                                    color='gold',
                                    line=dict(color='#000000',width=1))),
                                
                                    go.Bar(
                                    x=data[(data['Attrition'] == 'No')]['TotalWorkingYears'].value_counts().keys().tolist(),
                                    y=data[(data['Attrition'] == 'No')]['TotalWorkingYears'].value_counts().values.tolist(),
                                    name='No_Attrition', opacity = 0.8, marker=dict(
                                    color='lightskyblue',
                                    line=dict(color='#000000',width=1))), 
                                    
                                    go.Scatter(   
                                    x=pd.DataFrame(pd.crosstab(data['TotalWorkingYears'],data['Attrition']), ).index,
                                    y=pd.DataFrame(pd.crosstab(data['TotalWorkingYears'],data['Attrition']))['Yes'] / (pd.DataFrame(pd.crosstab(data['TotalWorkingYears'],data['Attrition']))['Yes'] + pd.DataFrame(pd.crosstab(data['TotalWorkingYears'],data['Attrition']))['No']) * 100,
                                    yaxis = 'y2',
                                    name='% Attrition', opacity = 0.6, marker=dict(
                                    color='black',
                                    line=dict(color='#000000',width=0.5
                                    ))) 
                                ],
                                    'layout': go.Layout(
                                    dict(title =  str('Total Working Years'),
                                    xaxis=dict(), 
                                    yaxis=dict(title= 'Count'), 
                                    yaxis2=dict(range= [-0, 75], 
                                                overlaying= 'y', 
                                                anchor= 'x', 
                                                side= 'right',
                                                zeroline=False,
                                                showgrid= False, 
                                                title= '% Attrition'
                                                ))  
                                )       
                            }
                    ), className = 'col-12'),

                    html.Div(children = dcc.Graph(
                        id = 'Graph5',
                        figure = {'data':[
                                    go.Bar(
                                    x=data[(data['Attrition'] != 'No')]['JobRole'].value_counts().keys().tolist(),
                                    y=data[(data['Attrition'] != 'No')]['JobRole'].value_counts().values.tolist(),
                                    name='Yes_Attrition',opacity = 0.8, marker=dict(
                                    color='gold',
                                    line=dict(color='#000000',width=1))),
                                
                                    go.Bar(
                                    x=data[(data['Attrition'] == 'No')]['JobRole'].value_counts().keys().tolist(),
                                    y=data[(data['Attrition'] == 'No')]['JobRole'].value_counts().values.tolist(),
                                    name='No_Attrition', opacity = 0.8, marker=dict(
                                    color='lightskyblue',
                                    line=dict(color='#000000',width=1))), 
                                    
                                    go.Scatter(   
                                    x=pd.DataFrame(pd.crosstab(data['JobRole'],data['Attrition'])).sort_values('Yes', ascending = False).index,
                                    y=pd.DataFrame(pd.crosstab(data['JobRole'],data['Attrition'])).sort_values('Yes', ascending = False)['Yes'] / (pd.DataFrame(pd.crosstab(data['JobRole'],data['Attrition'])).sort_values('Yes', ascending = False)['Yes'] + pd.DataFrame(pd.crosstab(data['JobRole'],data['Attrition'])).sort_values('Yes', ascending = False)['No']) * 100,
                                    yaxis = 'y2',
                                    name='% Attrition', opacity = 0.6, marker=dict(
                                    color='black',
                                    line=dict(color='#000000',width=0.5
                                    ))) 
                                ],
                                    'layout': go.Layout(
                                    dict(title =  str('Job Role'),
                                    xaxis=dict(), 
                                    yaxis=dict(title= 'Count'), 
                                    yaxis2=dict(range= [-0, 75], 
                                                overlaying= 'y', 
                                                anchor= 'x', 
                                                side= 'right',
                                                zeroline=False,
                                                showgrid= False, 
                                                title= '% Attrition'
                                                ))  
                                )       
                            }
                    ), className = 'col-12'),


                ]),

#########################################################################################################

                dcc.Tab(value='Tab3', label='Attrition Predictor', children=[
                    html.Div([
                        html.Div(children=[
                            html.P('1. How often do you do business trip?'),
                            dcc.Dropdown(id='my-id-1', value = '',
                            options= [{'label' : 'Often', 'value' : 'Travel_Frequently'},
                                {'label' : 'Rarely', 'value' : 'Travel_Rarely'},
                                {'label' : 'Never', 'value' : 'Non-Travel'}])
                        ], className='col-3'),

                        html.Div(children=[
                            html.P('2. Department you work in: '),
                            dcc.Dropdown(id='my-id-2', value = '',
                            options= [{'label' : 'Research & Development', 'value' : 'Research & Development'},
                                    {'label' : 'Sales', 'value' : 'Sales'},
                                {'label' : 'Human Resources', 'value' : 'Human Resources'}]),
                        ], className='col-3'),

                        html.Div(children=[
                            html.P('3. How satisfied are you with your current work environment?'),
                            dcc.Dropdown(id='my-id-3', value = '',
                            options= [{'label' : 'Very Satisfied', 'value' : '4'},
                                    {'label' : 'Satisfied', 'value' : '3'},
                                    {'label' : 'Not Satisfied', 'value' : '2'},
                                    {'label' : 'Very Not Satisfied', 'value' : '1'}])
                        ], className='col-3'),
                    ], className='row'),

                    html.Br(),

                    html.Div([
                        html.Div(children=[
                            html.P('4. In scale 1-4, how much impact of your job involvement on the company:'),
                            dcc.Dropdown(id='my-id-4', value = '',
                            options= [{'label' : '4', 'value' : '4'},
                                    {'label' : '3', 'value' : '3'},
                                    {'label' : '2', 'value' : '2'},
                                    {'label' : '1', 'value' : '1'}])
                        ], className='col-3'),


                        html.Div(children=[
                            html.P('5. Your current job level:'),
                            dcc.Dropdown(id='my-id-5', value = '',
                            options= [{'label' : 'CEO/GM/Director/Senior Manager', 'value' : '5'},
                                    {'label' : 'Manager/Assisten Manager', 'value' : '4'},
                                    {'label' : 'Supervisor/Coordinator', 'value' : '3'},
                                    {'label' : 'Staff(Non-Management & Non Superviser)', 'value' : '2'},
                                    {'label' : 'Non Executive', 'value' : '1'}])
                        ], className='col-3'),

                        html.Div(children=[
                            html.P('6. Your current job role:'),
                            dcc.Dropdown(id='my-id-6', value = '',
                            options= [{'label' : 'Sales Executive', 'value' : 'Sales Executive'},
                                    {'label' : 'Research Scientist', 'value' : 'Research Scientist'},
                                    {'label' : 'Laboratory Technician', 'value' : 'Laboratory Technician'},
                                    {'label' : 'Manufacturing Director', 'value' : 'Manufacturing Director'},
                                    {'label' : 'Healthcare Representative', 'value' : 'Healthcare Representative'},
                                    {'label' : 'Manager', 'value' : 'Manager'},
                                    {'label' : 'Sales Representative', 'value' : 'Sales Representative'},
                                    {'label' : 'Research Director', 'value' : 'Research Director'},
                                    {'label' : 'Human Resource', 'value' : 'Human Resource'}])
                        ], className='col-3'),
                    ], className='row'),

                    html.Br(),

                    html.Div([
                        html.Div(children=[
                        html.P('7. In scale 1-4, how satisfied are you with your current job?'),
                            dcc.Dropdown(id='my-id-7', value = '',
                            options= [{'label' : '4', 'value' : '4'},
                                    {'label' : '3', 'value' : '3'},
                                    {'label' : '2', 'value' : '2'},
                                    {'label' : '1', 'value' : '1'}])
                        ], className='col-3'),

                        html.Div(children=[
                        html.P('8. Your current marital status:'),
                            dcc.Dropdown(id='my-id-8', value = '',
                            options= [{'label' : 'Married', 'value' : 'Married'},
                                    {'label' : 'Single', 'value' : 'Single'},
                                    {'label' : 'Divorced', 'value' : 'Divorced'}])
                        ], className='col-3'),

                        html.Div(children=[
                        html.P('9. Do you often do overtime?'),
                            dcc.Dropdown(id='my-id-9', value = '',
                            options= [{'label' : 'Yes', 'value' : 'Yes'},
                                    {'label' : 'No', 'value' : 'No'}])
                        ], className='col-3'),
                    ], className='row'),

                html.Br(),

                    html.Div([
                        html.Div(children=[
                        html.P('10. Stock option level you have in your company:'),
                            dcc.Dropdown(id='my-id-10', value = '',
                            options= [{'label' : 'Level 0', 'value' : '0'},
                                    {'label' : 'Level 1', 'value' : '1'},
                                    {'label' : 'Level 2', 'value' : '2'},
                                    {'label' : 'Leve 3', 'value' : '3'}])
                        ], className='col-3'),

                        html.Div(children=[
                        html.P('11. Your Work-life balance in scale 1-4:'),
                            dcc.Dropdown(id='my-id-11', value = '',
                            options= [{'label' : '4', 'value' : '4'},
                                    {'label' : '3', 'value' : '3'},
                                    {'label' : '2', 'value' : '2'},
                                    {'label' : '1', 'value' : '1'}])
                        ], className='col-3'),

                        html.Div(children=[
                        html.P('12. How old are you?'),
                            dcc.Input(id='my-id-12', value = '0', type = 'number'),
                        ], className='col-3'),
                    ], className='row'),

                html.Br(),

                    html.Div([
                        html.Div(children=[
                        html.P('13. Your current daily rate:'),
                            dcc.Input(id='my-id-13', value = '0', type = 'number'),
                        ], className='col-3'),

                        html.Div(children=[
                        html.P('14. Distance from office to home (Km): '),
                            dcc.Input(id='my-id-14', value = '0', type = 'number'),
                        ], className='col-3'),

                        html.Div(children=[
                        html.P('15. Your current monthly income:'),
                            dcc.Input(id='my-id-15', value = '0', type = 'number'),
                        ], className='col-3'),
                    ], className='row'),

                html.Br(),

                    html.Div([
                        html.Div(children=[
                        html.P('16. Total work experience (in year): '),
                            dcc.Input(id='my-id-16', value = '0', type = 'number'),
                        ], className='col-3'),

                        html.Div(children=[
                        html.P('17. Training received in the past year: '),
                            dcc.Input(id='my-id-17', value = '0', type = 'number'),
                        ], className='col-3'),

                        html.Div(children=[
                        html.P('18. How many years have you worked in this company?'),
                            dcc.Input(id='my-id-18', value = '0', type = 'number'),
                        ], className='col-3'),
                    ], className='row'),

                html.Br(),

                    html.Div([
                        html.Div(children=[
                        html.P('19. How many years have you been working in your current role?'),
                            dcc.Input(id='my-id-19', value = '0', type = 'number'),
                        ], className='col-3'),

                        html.Div(children=[
                        html.P('20. How many years has it been since your last promotion?'),
                            dcc.Input(id='my-id-20', value = '0', type = 'number'),
                        ], className='col-3'),

                        html.Div(children=[
                        html.P('21. How many years have you been working with your current manager?'),
                            dcc.Input(id='my-id-21', value = '0', type = 'number'),
                        ], className='col-3'),
                    ], className='row'),
                
                html.Br(),

                    html.Div(id = 'my-div')
                
                ])#Tutupan dcc tab 3

            ],#Tutupan children all tab
            
            ## Tabs Content Style
            content_style={
                'fontFamily': 'Arial',
                'borderBottom': '1px solid #d6d6d6',
                'borderLeft': '1px solid #d6d6d6',
                'borderRight': '1px solid #d6d6d6',
                'padding': '44px'
            
        })#Tutupan div all tabb
    
    ],#Tutupan div paling luar
    
    #Div Paling luar Style
    style={
        'maxWidth': '1200px',
        'margin': '0 auto'
    })

@app.callback(
    Output(component_id = 'div-table', component_property = 'children'),
    [Input(component_id = 'filter', component_property = 'n_clicks')],
    [State(component_id = 'filter-row', component_property = 'value'),
    State(component_id = 'filter-department', component_property = 'value'),
    State(component_id = 'filter-overtime', component_property = 'value'),
    State(component_id = 'filter-twy', component_property = 'value'),
    State(component_id = 'filter-age', component_property = 'value'),
    State(component_id = 'filter-attrition', component_property = 'value')]
)


def update_table(n_clicks,row,department,overtime,twy,age,attrition):
    data = pd.read_csv('HR-Employee-Attrition.csv')
    if department != 'None':
        data = data[data['Department'] == department]
    if overtime != 'None':
        data = data[data['OverTime'] == overtime]
    if attrition != 'None':
        data = data[data['Attrition'] == attrition]
    if twy != '':
        data = data[data['TotalWorkingYears'] == twy]
    if age != '':
        data = data[data['Age'] == age]
    children = [generate_table(data, page_size = row)]
    return children

@app.callback(
    Output('my-div', 'children'),
    [Input('my-id-1', 'value'),
     Input('my-id-2', 'value'),
     Input('my-id-3', 'value'),
     Input('my-id-4', 'value'),
     Input('my-id-5', 'value'),
     Input('my-id-6', 'value'),
     Input('my-id-7', 'value'),
     Input('my-id-8', 'value'),
     Input('my-id-9', 'value'),
     Input('my-id-10', 'value'),
     Input('my-id-11', 'value'),
     Input('my-id-12', 'value'),
     Input('my-id-13', 'value'),
     Input('my-id-14', 'value'),
     Input('my-id-15', 'value'),
     Input('my-id-16', 'value'),
     Input('my-id-17', 'value'),
     Input('my-id-18', 'value'),
     Input('my-id-19', 'value'),
     Input('my-id-20', 'value'),
     Input('my-id-21', 'value')]
)

def update_output_div(my_id_1, my_id_2, my_id_3, my_id_4, my_id_5, my_id_6,my_id_7, my_id_8, my_id_9,
                    my_id_10, my_id_11, my_id_12, my_id_13, my_id_14, my_id_15, my_id_16,my_id_17, my_id_18,
                    my_id_19, my_id_20, my_id_21):
    BusinessTravel_Non_Travel= 0
    BusinessTravel_Travel_Frequently= 0
    if(my_id_1 == 'Non-Travel'):
        BusinessTravel_Non_Travel = 1
    elif(my_id_1 == 'Travel_Frequently'):
        BusinessTravel_Travel_Frequently= 1

    Department_Research_n_Development= 0
    Department_Sales = 0
    if(my_id_2 == 'Research & Development'):
        Department_Research_n_Development = 1
    elif(my_id_2 == 'Sales'):
        Department_Sales= 1

    EnvironmentSatisfaction_1 = 0
    if(my_id_3 == '1'):
        EnvironmentSatisfaction_1 = 1

    JobInvolvement_1 = 0
    if(my_id_4 == '1'):
        JobInvolvement_1 = 1
    
    JobLevel_1 = 0
    JobLevel_2 = 0
    JobLevel_4 = 0
    if(my_id_5 == '1'):
        JobLevel_1 = 1
    elif(my_id_5 == '2'):
        JobLevel_2 = 1
    elif(my_id_5 == '4'):
        JobLevel_4 = 1

    JobRole_Healthcare_Representative = 0
    JobRole_Laboratory_Technician = 0
    JobRole_Manager = 0
    JobRole_Manufacturing_Director = 0
    JobRole_Research_Director = 0
    JobRole_Sales_Representative = 0
    if(my_id_6 == 'Healthcare Representative'):
        JobRole_Healthcare_Representative = 1
    elif(my_id_6 == 'Laboratory Technician'):
        JobRole_Laboratory_Technician = 1
    elif(my_id_6 == 'Manager'):
        JobRole_Manager = 1
    elif(my_id_6 == 'Manufacturing Director'):
        JobRole_Manufacturing_Director = 1
    elif(my_id_6 == 'Research Director'):
        JobRole_Research_Director = 1
    elif(my_id_6 == 'Sales Representative'):
        JobRole_Sales_Representative = 1

    JobSatisfaction_1 = 0
    JobSatisfaction_4 = 0
    if(my_id_7 == '1'):
        JobSatisfaction_1 = 1
    elif(my_id_7 == '4'):
        JobSatisfaction_4 = 1

    MaritalStatus_Divorced = 0
    MaritalStatus_Married = 0
    MaritalStatus_Single = 0
    if(my_id_8 == 'Divorced'):
        MaritalStatus_Divorced = 1
    elif(my_id_8 == 'Married'):
        MaritalStatus_Married = 1
    elif(my_id_8 == 'Single'):
        MaritalStatus_Single = 1

    OverTime_No = 0
    OverTime_Yes = 0
    if(my_id_9 == 'No'):
        OverTime_No = 1
    elif(my_id_9 == 'Yes'):
        OverTime_Yes = 1

    StockOptionLevel_0 = 0
    StockOptionLevel_1 = 0
    StockOptionLevel_2 = 0
    if(my_id_10 == '0'):
        StockOptionLevel_0 = 1
    elif(my_id_10 == '1'):
        StockOptionLevel_1 = 1
    elif(my_id_10 == '2'):
        StockOptionLevel_2 = 1

    WorkLifeBalance_1 = 0
    if(my_id_11 == '1'):
        WorkLifeBalance_1 = 1

    Age = my_id_12

    DailyRate = my_id_13

    DistanceFromHome = my_id_14

    MonthlyIncome = my_id_15

    TotalWorkingYears = my_id_16

    TrainingTimesLastYear = my_id_17

    YearsAtCompany = my_id_18

    YearsInCurrentRole = my_id_19

    YearsSinceLastPromotion = my_id_20

    YearsWithCurrManager = my_id_21

    pred_data = pd.DataFrame(data = [(BusinessTravel_Non_Travel, BusinessTravel_Travel_Frequently, 
            Department_Research_n_Development, Department_Sales, EnvironmentSatisfaction_1,
            JobInvolvement_1, JobLevel_1, JobLevel_2, JobLevel_4, JobRole_Healthcare_Representative,
            JobRole_Laboratory_Technician, JobRole_Manager, JobRole_Manufacturing_Director, JobRole_Research_Director,
            JobRole_Sales_Representative, JobSatisfaction_1, JobSatisfaction_4, MaritalStatus_Divorced,
            MaritalStatus_Married, MaritalStatus_Single, OverTime_No, OverTime_Yes, StockOptionLevel_0,
            StockOptionLevel_1, StockOptionLevel_2, WorkLifeBalance_1, Age, DailyRate, DistanceFromHome,
            MonthlyIncome, TotalWorkingYears, TrainingTimesLastYear, YearsAtCompany, YearsInCurrentRole,
            YearsSinceLastPromotion, YearsWithCurrManager)], 
            columns = ['BusinessTravel_Non-Travel', 'BusinessTravel_Travel_Frequently',
            'Department_Research & Development', 'Department_Sales',
            'EnvironmentSatisfaction_1', 'JobInvolvement_1', 'JobLevel_1',
            'JobLevel_2', 'JobLevel_4', 'JobRole_Healthcare Representative',
            'JobRole_Laboratory Technician', 'JobRole_Manager',
            'JobRole_Manufacturing Director', 'JobRole_Research Director',
            'JobRole_Sales Representative', 'JobSatisfaction_1',
            'JobSatisfaction_4', 'MaritalStatus_Divorced', 'MaritalStatus_Married',
            'MaritalStatus_Single', 'OverTime_No', 'OverTime_Yes',
            'StockOptionLevel_0', 'StockOptionLevel_1', 'StockOptionLevel_2',
            'WorkLifeBalance_1', 'Age', 'DailyRate', 'DistanceFromHome',
            'MonthlyIncome', 'TotalWorkingYears', 'TrainingTimesLastYear',
            'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion',
            'YearsWithCurrManager'])

    predict = loadModel.predict(pred_data)
    if predict == 1: 
        return "\nPotential Attrition."
    if predict == 0:
        return "\nNot Pottential Attrition."

# def set_display_children(pred_data):
#     loadModel = pickle.load(open('attrition_gradient_model.sav.sav', 'rb'))
#     return 'Hasil prediksi adalah {}'.format(loadModel.predict(pred_data))

if __name__ == '__main__':
    app.run_server(debug=True)