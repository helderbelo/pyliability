import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output,State, ClientsideFunction
import dash_bootstrap_components as dbc
from dash import Dash, html, Input, Output
import dash_daq as daq
import numpy as np
import pandas as pd
import datetime as dt
from babel.numbers import format_currency

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server
#===========================

banco_tabuas = pd.read_excel('https://github.com/helderbelo/tcc/blob/main/banco_tabuas.xlsx?raw=true', sheet_name='tabuas')

ativo = pd.read_excel('https://github.com/helderbelo/tcc/blob/main/base-bd.xlsx?raw=true', sheet_name='ativos')
aposentado = pd.read_excel('https://github.com/helderbelo/tcc/blob/main/base-bd.xlsx?raw=true', sheet_name='aposentados')
pensionista = pd.read_excel('https://github.com/helderbelo/tcc/blob/main/base-bd.xlsx?raw=true', sheet_name='pensionistas')

opcoes_tabuas = list(banco_tabuas.columns[1:])

database = pd.to_datetime(dt.date(2022, 9, 30)) # DATA BASE DA AVALIAÇÃO (Ano, Mês, Dia)

# =====================================================================
# Layout 
app.layout = dbc.Container(
    children=[
        dbc.Row([
            #dbc.Col([
                    html.Div([
                         dbc.Row([dbc.Col(html.H3(dbc.Badge("pyLiability", color="#a50000", className="me-1"))),
                         
                                  dbc.Col([html.P('Hélder Belo - UFPE', style={'textAlign': 'right','color':'white'})]),
    #html.Img(id="logo", src=app.get_asset_url("logo.png"), height=50)], style={'textAlign': 'right'})
                                  ]),
                        
                            ], style={"background-color": "#003e4c", #003e4c",
                               "margin": "5px", "padding": "25px"},),                    
                    dbc.Col([
                    html.Div([
                        html.H5(dbc.Badge("Selecione a tábua de mortalidade geral - Masculina:", color="#5d8aa7", className="me-1")),
                        dcc.Dropdown(
                                        id="tabua-dropdown1",
                                        options=[{"label": j, "value": j}
                                            for j in opcoes_tabuas
                                        ],
                                        value= 'BR-EMSsb-v.2010-m',
                                        style={"margin-top": "10px",'width': '86%'}
                                    ),                        
                        ], id="teste1")
                    ]),
                    dbc.Col([
                    html.Div([
                        html.H5(dbc.Badge("Selecione a tábua de mortalidade geral - Feminina:", color="#5d8aa7", className="me-1")),
                        dcc.Dropdown(
                                        id="tabua-dropdown2",
                                        options=[{"label": j, "value": j}
                                            for j in opcoes_tabuas
                                        ],
                                        value= 'BR-EMSsb-v.2010-f',
                                        style={"margin-top": "10px",'width': '86%'}
                                    ),                        
                        ], id="teste2")
                    ]),
                    dbc.Col([
                    html.Div([
                        html.H5(dbc.Badge("Selecione a tábua para entrada em invalidez:", color="#5d8aa7", className="me-1")),
                        dcc.Dropdown(
                                        id="tabua-dropdown",
                                        options=[{"label": j, "value": j}
                                            for j in opcoes_tabuas
                                        ],
                                        value= 'ALVARO VINDAS',
                                        style={"margin-top": "10px",'width': '86%'}
                                    ),                        
                        ], id="teste")
                    ]),

                        html.Div(children=[
                        dbc.Row([    
                            dbc.Col([
                            dbc.Row([html.P("Idade mínima de aposentadoria"),
                                    daq.NumericInput(
                                        #label='Idade mínima de aposentadoria',
                                        id='idade_aposentadoria',
                                        min=0,
                                        max=100,
                                        value=55,
                                        style={
                                                "paddingBottom": "3%"
                                                },
                                    ),
                                    ]#,justify='left'
                                    ),       

                            dbc.Row([html.P("Tempo mínimo de patrocinadora"),
                                    daq.NumericInput(
                                        #label='Tempo mínimo de patrocinadora',
                                        id='tempo_patrocinadora',
                                        min=0,
                                        max=100,
                                        value=15,
                                        style={
                                                "paddingBottom": "3%"
                                                },

                                    ),
                                    ]),

                            dbc.Row([html.P("Tempo mínimo de adesão ao plano"),
                                    daq.NumericInput(
                                        #label='Tempo mínimo de adesão ao plano',
                                        id='tempo_plano',
                                        min=0,
                                        max=100,
                                        value=10,
                                        style={
                                                "paddingBottom": "3%"
                                                },

                                    ),
                            ]),

                            dbc.Row([html.P("Última idade que considera probabilidade de desligamento"),
                                    daq.NumericInput(
                                        #label='Última idade que considera probabilidade de desligamento',
                                        id='idade_maxima_rotatividade',
                                        min=0,
                                        max=100,
                                        value=48,
                                        style={
                                                "paddingBottom": "3%"
                                                },
                                    ),
                                    ]),       

                            dbc.Row([html.P("Teto do Salário de Contribuição"),
                                    daq.NumericInput(
                                        #label='Teto do Salário de Contribuição',
                                        id='teto_salario_contribuicao',
                                        min=0,
                                        max=100000,
                                        value=15000,
                                        size=80,
                                        style={
                                                "paddingBottom": "3%"
                                                },

                                        #style={"align-items": "left",
                                        #       "justify-content": "left"}
                                    ),
                                    ]),       

                            dbc.Row([html.P("Contribuiçao Ativo (%)"),
                                    daq.NumericInput(
                                        #label='Contribuiçao Ativo (%)',
                                        id='contribuicao_ativo',
                                        min=0.00,
                                        max=100.00,
                                        value=5.00,
                                        style={
                                                "paddingBottom": "3%"
                                                },
                                    ),
                                    ]),

                            dbc.Row([html.P("Contribuiçao Patrocinadora (%)"),
                                    daq.NumericInput(
                                        #label='Contribuiçao Patrocinadora (%)',
                                        id='contribuicao_patroc',
                                        min=0.00,
                                        max=100.00,
                                        value=5.00,
                                        style={
                                                "paddingBottom": "3%"
                                                },
                                    ),
                                    ]),                                                
                                 ],
                                 style={
                                    "display": "inline-block",
                                    "margin-top": "0px",
                                    "margin-left": "0px",
                                    "verticalAlign": "top",                                        
                                    }
                                    ),
                                 

                            dbc.Col([
                            dbc.Row([html.P("Valor do Benefício (em % do salário)"),
                                    daq.NumericInput(
                                        #label='Valor do Benefício (em % do salário)',
                                        id='perc_beneficio_salario',
                                        min=0.00,
                                        max=100.00,
                                        value=80.00,
                                        style={
                                                "paddingBottom": "3%"
                                                },

                                    ),
                                    ]),       

                            dbc.Row([html.P("Reversão de Pensão (em % do benefício)"),
                                    daq.NumericInput(
                                        #label='Reversão de Pensão (em % do benefício)',
                                        id='perc_reversao_pensao',
                                        min=0.00,
                                        max=100.00,
                                        value=60.00,
                                        style={
                                                "paddingBottom": "3%"
                                                },
                                    ),
                                    ]),

                            dbc.Row([html.P("Taxa de Juros (%)"),
                                    daq.NumericInput(
                                        #label='Taxa de Juros (%)',
                                        id='i',
                                        min=0.00,
                                        max=100.00,
                                        value=6.00,
                                        size=70,
                                        style={
                                                "paddingBottom": "3%"
                                                },
                                    ),
                                    ]),

                            dbc.Row([html.P("% Rotatividade (desligamento)"),
                                    daq.NumericInput(
                                        #label='% Rotatividade (desligamento)',
                                        id='percentual_rotatividade',
                                        min=0,
                                        max=100,
                                        value=1,
                                        size=70,
                                        style={
                                                "paddingBottom": "3%"
                                                },
                                    ),
                                    ]),       

                            dbc.Row([html.P("% Crescimento Real dos Salários a.a."),
                                    daq.NumericInput(
                                        #label='% Crescimento Real dos Salários a.a.',
                                        id='crescimento_salarial',
                                        min=0.00,
                                        max=100.00,
                                        value=2.01,
                                        size=70,
                                        style={
                                                "paddingBottom": "3%"
                                                },
                                    ),
                                    ]),       

                            dbc.Row([html.P("Taxa de Carregamento (% da contrbuição)"),
                                    daq.NumericInput(
                                        #label='Taxa de Carregamento (% da contrbuição)',
                                        id='tx_carregamento',
                                        min=0.00,
                                        max=100.00,
                                        value=15.00,
                                        size=70,
                                        style={
                                                "paddingBottom": "3%"
                                                },
                                    ),
                                    ]),

                            dbc.Row([html.P("Diferença de idade dos Cônjuges (Masculino x Feminino)"),
                                    daq.NumericInput(
                                        #label='Diferença de idade dos Cônjuges (Masculino x Feminino)',
                                        id='dif_conjuge',
                                        min=0,
                                        max=100,
                                        value=4,
                                        style={
                                                "paddingBottom": "3%"
                                                },
                                    ),
                                    ]),                                                
                                 ]),
                                ],#justify="center"
                                ),
                                ],
                                    style={
                                    "display": "inline-block",
                                    "margin-top": "20px",
                                    "margin-left": "20px",
                                    "verticalAlign": "top",                                        
                                    }

                                ),
                    dbc.Row([
                    html.Div([
                            dbc.Button("Calcular", color="primary", id="calculo-button", size="lg", n_clicks=0)
                        ])
                    ]),
                        dbc.Row([
                        dbc.Col([dbc.Card([   
                            dbc.CardBody([
                                html.H4('Provisões', className="card-text"),
                                ])
                            ], color="#003e4c", outline=True,inverse=True, style={"margin-top": "20px",
                                    
                                    #"color": "#FFFFFF"
                                    }
                                    )
                                    ], md=6,
                                    ),]),
                                                
                      html.Div([           
                      dbc.Row([
                    
                        dbc.Col([html.Div(id='table-data')], xs={'size':'auto', 'offset':0}, sm={'size':'auto', 'offset':0}, md={'size':4, 'offset':0}, lg={'size':'auto', 'offset':0},
                                                xl={'size':'auto', 'offset':0}),
                                                
                        dbc.Col([html.Div(id='table-data1')], xs={'size':'auto', 'offset':0}, sm={'size':'auto', 'offset':0}, md={'size':4, 'offset':0}, lg={'size':'auto', 'offset':0},
                                                xl={'size':'auto', 'offset':0}),
                      
                      ],justify="left",style={"margin-top": "20px"}),
                      ]),           
                                          
            ], className="g-0")
            ], fluid=True,
)


# =====================================================================
# Interactivity
@app.callback(
    [#Output('table-data', 'children'),
     #Output('contraprestacao', 'children'),
     Output('table-data', 'children'),
     Output('table-data1', 'children'),
     #Output('valor-provisao', 'children')
          ],
    
    [Input("calculo-button", "n_clicks")],
     [State("tabua-dropdown1", "value"),State("tabua-dropdown2", "value"), State("tabua-dropdown", "value"),
     State("idade_aposentadoria", "value"),State("tempo_patrocinadora", "value"),State("tempo_plano", "value"),State("teto_salario_contribuicao", "value"),
     State("perc_beneficio_salario", "value"),State("perc_reversao_pensao", "value"),State("i", "value"),State("idade_maxima_rotatividade", "value"),
     State("percentual_rotatividade", "value"),State("crescimento_salarial", "value"),State("contribuicao_ativo", "value"),State("contribuicao_patroc", "value"),
     State("tx_carregamento", "value"),State("dif_conjuge", "value")]     
)

def provisoes(botao,mortalidade_geral_M,mortalidade_geral_F,entrada_invalidez,idade_aposentadoria,
              tempo_patrocinadora,tempo_plano,teto_salario_contribuicao,perc_beneficio_salario,perc_reversao_pensao,i,
              idade_maxima_rotatividade,percentual_rotatividade,crescimento_salarial,perc_contr_ativo,perc_contr_patroc,
              tx_carregamento,dif_conjuge):  
    
    global ativo,aposentado,pensionista

    ativos,aposentados,pensionistas = ativo.copy(),aposentado.copy(),pensionista.copy()

    database = pd.to_datetime(dt.date(2022, 9, 30)) # DATA BASE DA AVALIAÇÃO (Ano, Mês, Dia)
    
    perc_beneficio_salario/=100
    perc_reversao_pensao/=100
    i/=100
    v = 1/(1+i) 
    percentual_rotatividade/=100
    crescimento_salarial/=100
    perc_contr_ativo/=100
    perc_contr_patroc/=100
    tx_carregamento/=100


    tabua_feminina = pd.DataFrame(None)

    tabua_feminina['qx'] = banco_tabuas[[mortalidade_geral_F]].copy()          # definindo a tábua para a variável qx
    tabua_feminina = tabua_feminina[tabua_feminina['qx'].notna()]       # excluindo as idades sem valores para qx (últimas idades pós idade ômega)

    tabua_feminina.reset_index(inplace=True)
    tabua_feminina.rename(columns={"index":"x"},inplace=True)  # utilizando a coluna índice para representar as idades 'x'

    tabua_feminina['qxi'] =  0.0 #banco_tabuas[[mortalidade_invalidos_F]]
    tabua_feminina['ix'] = banco_tabuas[[entrada_invalidez]].copy().fillna(0)  # preenche os valores 'nan' com zeros

    #======== Tábua Masculina ===============
    # Repetindo o processo para a tábua masculina

    tabua_masculina = pd.DataFrame(None)
    tabua_masculina['qx'] = banco_tabuas[[mortalidade_geral_M]].copy()
    tabua_masculina = tabua_masculina[tabua_masculina['qx'].notna()] 

    tabua_masculina.reset_index(inplace=True)
    tabua_masculina.rename(columns={"index":"x"},inplace=True)

    tabua_masculina['qxi'] = 0.0 #banco_tabuas[[mortalidade_invalidos_M]]
    tabua_masculina['ix'] = banco_tabuas[[entrada_invalidez]].copy().fillna(0)

    #========== Idade ômega ============
    w = max(tabua_feminina.x.values[-1],tabua_masculina.x.values[-1])
    
    tabua_masculina['id'] = 'M-'+tabua_masculina.x.astype(str)
    tabua_feminina['id'] = 'F-'+tabua_masculina.x.astype(str)

    tabuas=[tabua_feminina,tabua_masculina]

    for tabua in tabuas:
        # Rotatividade a partir dos 18 anos até idade máxima considerada na hipótese
        tabua.loc[18:idade_maxima_rotatividade,'wx'] = (np.array([percentual_rotatividade]*(idade_maxima_rotatividade-17))) 
        
        # Preenchendo as demais idades com zeros
        tabua['wx'] = tabua['wx'].fillna(0.0)
        
        # Decrementos sem hipóteses definidas nesse exemplo
        tabua['zx'] = 0.0
        tabua['qr'] = 0.0

        # px = 1 - qx
        tabua['px'] = 1-tabua.qx
        
        # Probabilidades em ambiente de 4 decrementos
        tabua['qx_ai'] = tabua.ix*(1 - 1/2*(tabua.qx + tabua.wx + tabua.qr) + 1/3*(tabua.qx * tabua.wx + tabua.qx * tabua.qr + tabua.wx * tabua.qr) - 1/4*(tabua.qx * tabua.wx * tabua.qr))
        tabua['qx_aw'] = tabua.wx*(1 - 1/2*(tabua.qx + tabua.ix + tabua.qr) + 1/3*(tabua.qx * tabua.ix + tabua.qx * tabua.qr + tabua.ix * tabua.qr) - 1/4*(tabua.qx * tabua.ix * tabua.qr))
        tabua['qx_ar'] = tabua.qr*(1 - 1/2*(tabua.qx + tabua.ix + tabua.wx) + 1/3*(tabua.qx * tabua.ix + tabua.qx * tabua.wx + tabua.ix * tabua.wx) - 1/4*(tabua.qx * tabua.ix * tabua.wx))
        tabua['qx_aa'] = tabua.qx*(1 - 1/2*(tabua.ix + tabua.wx + tabua.qr) + 1/3*(tabua.ix * tabua.wx + tabua.ix * tabua.qr + tabua.wx * tabua.qr) - 1/4*(tabua.ix * tabua.wx * tabua.qr))
        
        # px_aa = probabilidade do participante permanecer ativo = 1 - qx's
        tabua['px_aa'] = 1 - (tabua.qx_aa + tabua.qx_ai + tabua.qx_ar + tabua.qx_aw)

        # Criando as colunas lx's inicialmente com valor zero
        tabua['lx'] = tabua['lx_aa'] = 0.0
        
        # Atribuindo a raiz da tábua na idade zero
        tabua.loc[0,'lx'] = tabua.loc[0,'lx_aa'] = 100000

        # Calculando os lx a partir da idade 1 com base em lx-1 - qx-1 * lx-1
        for i in tabua.x[1:]:
            tabua.loc[i,'lx'] = tabua.lx[i-1] - tabua.qx[i-1] * tabua.lx[i-1]  
            tabua.loc[i,'lx_aa'] = tabua.lx_aa[i-1] * tabua.px_aa[i-1]

        tabua['dx'] = tabua.qx * tabua.lx
    
    #tabua_feminina
        
    # Para construir os valores das rendas conjuntas 
    tabua_feminina['lxy'] = tabua_feminina.lx * tabua_masculina.lx.shift(-dif_conjuge) # No caso da tábua feminina, está pegando o lx da tábua do cônjuge deslocado a diferença de idade para mais
    tabua_masculina['lxy'] = tabua_feminina.lx.shift(dif_conjuge) * tabua_masculina.lx

    tabuas=[tabua_feminina,tabua_masculina]

    for tabua in tabuas:
        
        tabua['Dx'] = tabua.lx * v ** tabua.x
        tabua['Dx_aa'] = tabua.lx_aa * v ** tabua.x    
        tabua['Dxy'] = tabua.lxy * v ** tabua.x

        tabua['Nx']=tabua['Nxy']=tabua['Nx_aa']=0.00
        
        for x in tabua.x:            
            tabua.loc[x,'Nx'] = tabua.loc[x:,'Dx'].sum()
            tabua.loc[x,'Nx_aa'] = tabua.loc[x:,'Dx_aa'].sum()
            tabua.loc[x,'Nxy'] = tabua.loc[x:,'Dxy'].sum()
            tabua['Sx'] = tabua.loc[x:,'Nx'].sum()
        
        tabua['äx'] = tabua.Nx/tabua.Dx
        tabua['äx_aa'] = tabua.Nx_aa/tabua.Dx_aa
        tabua['äxy'] = tabua.Nxy / tabua.Dxy


    colunas_datas=['DT NASC','DT ADMISSÃO','DT ADESÃO']

    # Transformando as colunas de datas em formato de data reconhecível pelo python (caso precise)
    for i in colunas_datas:
        ativos[i] = pd.to_datetime(ativos[i])

    # Idade Atual na Data Base dos Cálculos
    ativos['IDADE_x'] = (database - ativos['DT NASC']).astype('timedelta64[Y]').astype(int)                

    # Idade de Adesão
    ativos['IDADE_e'] = (ativos['DT ADESÃO'] - ativos['DT NASC']).astype('timedelta64[Y]').astype(int)     

    # Tempo na Patrocinadora na Data Base em anos
    ativos['TEMP_PATROC'] = (database - ativos['DT ADMISSÃO']).astype('timedelta64[Y]').astype(int)         

    # Tempo no Plano na Data Base em anos
    ativos['TEMP_PLANO'] = (database - ativos['DT ADESÃO']).astype('timedelta64[Y]').astype(int)            

    # Tempo para estar elegível para aposentadoria em anos
    ativos['TEMP_APOSENT'] = np.maximum(0,
                                        np.maximum(idade_aposentadoria - ativos['IDADE_x'],    # Critério de idade
                                        np.maximum(tempo_plano - ativos['TEMP_PLANO'],          # Critério de Tempo de Adesão ao Plano
                                        tempo_patrocinadora - ativos['TEMP_PATROC'])))          # Critério de Tempo na Patrocinadora

    # Idade na elegibilidade  para aposentadoria em anos
    ativos['IDADE_APOSENT'] = ativos['IDADE_x'] + ativos['TEMP_APOSENT']

    # Salário de Participação = Mínimo entre Teto de Contribuição ou Salário
    ativos['SALARIO_PARTICIPACAO'] = np.minimum(teto_salario_contribuicao , ativos['SALARIO'])

    # Salário na Aposentadoria = Mínimo entre Teto de Contribuição ou Salário Projetado
    ativos['SALARIO_APOSENT'] = np.minimum(teto_salario_contribuicao , ativos['SALARIO'] * (1+crescimento_salarial) ** ativos['TEMP_APOSENT'])

    # Benefício na Aposentadoria = Mínimo entre Teto de Contribuição ou Salário Projetado x % do salário para o benefício
    ativos['BENEFICIO_z'] = np.minimum(teto_salario_contribuicao , ativos['SALARIO_APOSENT'] * perc_beneficio_salario)

    # Sexo do conjuge com base no sexo oposto
    ativos['SEXO_CONJUGE'] = np.where(ativos.SEXO == 'M', 'F', 'M')

    # Idade do conjuge com base nas premissas
    ativos['IDADE_CONJUGE'] = np.where(ativos.SEXO == 'M', ativos.IDADE_x - dif_conjuge, ativos.IDADE_x + dif_conjuge)

    #ativos

    tabua_unica = pd.concat([tabua_masculina,tabua_feminina])

    # Obtenção dos valores das funções de comutação com base no sexo e idade de aposentadoria

    ativos['id'] =  ativos.SEXO+"-"+ativos.IDADE_APOSENT.astype(str)    # Criando uma coluna chave para dar match na tábua única de múltiplos decrementos
    ativos = ativos.merge(tabua_unica[['id','Dx_aa','äx','äxy']], on='id',how='left') # Unindo a base de ativos com os valores das funções de comutação
    ativos.rename(columns={'äx':'äz','Dx_aa':'Dz_aa',},inplace=True)  # Renomeando a coluna para Dz_aa e äz (Renda antecipada vitalícia a partir da data de aposentadoria)
    ativos.drop(columns='id',inplace=True)  # Excluindo a coluna de chave única
    #ativos

    #Trazendo os valores das funções de comutação com base no sexo e idade de atual

    ativos['id'] =  ativos.SEXO+"-"+ativos.IDADE_x.astype(str)  # Criando uma chave única para dar match na tábua multidecremental unificada, dessa vez com a idade atual
    ativos = ativos.merge(tabua_unica[['id','qx_ai','qx_aa','Dx_aa']], on='id',how='left')
    ativos.drop(columns='id',inplace=True)
    #ativos

    #Trazendo os valores das funções de comutação com base no sexo do cônjuge e idade de cônjuge na aposentadoria do beneficiário

    ativos['id'] =  ativos.SEXO_CONJUGE+"-"+(ativos.TEMP_APOSENT + ativos.IDADE_CONJUGE).astype(str)

    ativos = ativos.merge(tabua_unica[['id','äx']], on='id',how='left')
    ativos.rename(columns={'äx':'äy'},inplace=True) # Renomeando a coluna para äy (Renda antecipada vitalícia para o cônjuge a partir da data de aposentadoria do beneficiário)
    ativos.drop(columns='id',inplace=True)

    # Valor Atual dos Benefícios Futuros de Aposentadoria
    # 13 pagamentos mensais x Valor do Benefício x Valor da Renda Vitalícia x nEx (Data de Aposentadoria / Data Atual)
    ativos['VABF_APO'] = 13 * ativos['BENEFICIO_z'] * ativos['äz'] * ativos.Dz_aa/ativos.Dx_aa

    # Valor Atual dos Benefícios Futuros Pecúlio por Invalidez 
    # Maior valor entre o valor do Resgate ou 15x o valor do salário de participação x decremento de invalidez
    ativos['VABF_INV'] =  np.maximum(ativos['RESGATE'], 15 * ativos['SALARIO_PARTICIPACAO']) * ativos['qx_ai']

    # Valor Atual dos Benefícios Futuros Pecúlio por Morte
    # Maior valor entre o valor do Resgate ou 15x o valor do salário de participação x decremento de morte
    ativos['VABF_PEC'] =  np.maximum(ativos['RESGATE'], 15 * ativos['SALARIO_PARTICIPACAO']) * ativos['qx_aa']

    # Valor Atual dos Benefícios Futuros de Aposentadoria com Reversão em Pensão
    # 13 pagamentos mensais x Valor do Benefício x Diferença Valor da Renda Vitalícia do Cônjuge e da Renda Conjunta x nEx
    ativos['VABF_REV_PENS'] = 13 * perc_reversao_pensao * ativos.BENEFICIO_z * (ativos.äy - ativos.äxy) * ativos.Dz_aa/ativos.Dx_aa

    # Variável para armazenar os anos t de zero à idade de aposentadoria
    fluxo = list(np.arange(0,1+max(ativos.TEMP_APOSENT)))

    
    # Cálculo do nEx nos anos futuros com base na idade atual para ser utilizado no cálculo do Valor Atual dos Salários Futuros

    # Criando uma cópia da base apenas com as colunas desejáveis
    nEx_aa = ativos[['MATRICULA','SEXO','IDADE_x','IDADE_APOSENT','SALARIO']].copy()

    for t in fluxo:
        nEx_aa['id'] = np.where(nEx_aa.IDADE_x+t <= nEx_aa.IDADE_APOSENT,   # Condição para trazer o valor do nEx apenas até a data de aposentadoria
                                nEx_aa.SEXO+"-"+(nEx_aa.IDADE_x+t).astype(str), # Criando chave única para cada t ano 
                                'N/A')   # Não se aplica para idades após aposentadoria
        
        nEx_aa = nEx_aa.merge(tabua_unica[['id','Dx_aa']], on='id',how='left')
        nEx_aa.rename(columns={'Dx_aa':t},inplace=True)
        
        nEx_aa[t] = nEx_aa[t] / ativos.Dx_aa # nEx = Dx+n / Dx

    nEx_aa.drop(columns='id',inplace=True)

    # Criando outro dataframe com o salário projetado com base nas premissas

    vasf = ativos[['MATRICULA','SEXO','IDADE_x','IDADE_APOSENT','SALARIO']].copy()
    vasf = vasf.reindex(columns=['MATRICULA','SEXO','IDADE_x','IDADE_APOSENT','SALARIO'] + fluxo)

    for t in fluxo:
        
        vasf.loc[:,t] = (np.where(
            t + vasf['IDADE_x'] > vasf['IDADE_APOSENT'],
            0.00,np.minimum( teto_salario_contribuicao,
                    vasf['SALARIO']*(1+crescimento_salarial) ** t)))

    # Valor Atual dos Salários Futuros = Salários Projetado x Desconto Atuarial (nEX)
    vasf.iloc[:,5:] = vasf.iloc[:,5:] * nEx_aa.iloc[:,5:]    

    # Valor Atual dos Salários Futuros está pegando a soma de todas as colunas para cada linha
    ativos['VASF'] = vasf.iloc[:,5:].sum(axis=1)

    # Valor Atual das Contribuições Futuras = (% de contribuição ativo + patrocinadora) x (1-taxa de carregamento) x Valor Atual dos Salários Futuros
    ativos['VACF'] = 13 * (perc_contr_ativo + perc_contr_patroc) * (1 - tx_carregamento) * ativos['VASF']

    # Custo Normal pelo Médoto Crédito Unitário = Soma dos Valores Atuais dos Benefícios Futuros / diferença entre idade de aposentadoria e idade de adesão
    ativos['CN'] = (ativos.VABF_APO + ativos.VABF_INV + ativos.VABF_PEC + ativos.VABF_REV_PENS) / (ativos.IDADE_APOSENT - ativos.IDADE_e)

    # Provisões Matemáticas dos Benefícios a Conceder Método Crédito Unitário = Custo Normal x diferença entre idade x e idade de adesão
    ativos['PMBaC_UC'] = ativos.CN * (ativos.IDADE_x - ativos.IDADE_e)

    # Custo Normal de contribução anual ao plano
    ativos['CN_CONTRIB_PLANO'] = 13 * ativos.SALARIO_PARTICIPACAO * (perc_contr_ativo + perc_contr_patroc) * (1 - tx_carregamento)


    aposentados['IDADE_x'] = (database - aposentados['DT NASC']).astype('timedelta64[Y]').astype(int)     

    # Sexo do conjuge com base no sexo oposto
    aposentados['SEXO_CONJUGE'] = np.where(aposentados.SEXO == 'M', 'F', 'M')

    # Idade do conjuge com base nas premissas
    aposentados['IDADE_CONJUGE'] = np.where(aposentados.SEXO == 'M',aposentados.IDADE_x-dif_conjuge,aposentados.IDADE_x+dif_conjuge)

    aposentados['id'] =  np.where(aposentados.SEXO_CONJUGE == 'M',      #Se o sexo do cônjuge = Masculino, adicionará/subtrairá idade do aposentado conforme premissa 
                                aposentados.SEXO_CONJUGE+"-"+(aposentados.IDADE_x+dif_conjuge).astype(str),
                                aposentados.SEXO_CONJUGE+"-"+(aposentados.IDADE_x-dif_conjuge).astype(str))

    aposentados = aposentados.merge(tabua_unica[['id','äx']], on='id',how='left')
    aposentados.rename(columns={'äx':'äy'},inplace=True)
    aposentados.drop(columns='id',inplace=True)

    #==================================================

    aposentados['id'] =  aposentados.SEXO+"-"+aposentados.IDADE_x.astype(str)

    aposentados = aposentados.merge(tabua_unica[['id','äx','äxy']], on='id',how='left')
    aposentados.drop(columns='id',inplace=True)

    aposentados['PMBC_APO'] = 13 * aposentados.BENEFICIO * aposentados['äx']

    aposentados['PMBC_REV_PENS'] =  13 * perc_reversao_pensao * aposentados.BENEFICIO * (aposentados.äy - aposentados.äxy)

    #==================================================
    
    pensionistas['IDADE_x'] = (database - pensionistas['DT NASC']).astype('timedelta64[Y]').astype(int)     

    pensionistas['id'] =  pensionistas.SEXO+"-"+pensionistas.IDADE_x.astype(str)

    pensionistas = pensionistas.merge(tabua_unica[['id','äx']], on='id',how='left')
    pensionistas.drop(columns='id',inplace=True)

    pensionistas['PMBC_PENS'] = 13 * pensionistas.BENEFICIO * pensionistas['äx']
          
    pmbc=pd.DataFrame({'PMBC':[
        'Aposentadorias:',
        'Reversão em Pensão:',
        'Pensões Concedidas:',
        'TOTAL PMBC:'], 
        '': [
        format_currency(aposentados.PMBC_APO.sum(), 'BRL', locale='pt_BR'),
        format_currency(aposentados.PMBC_REV_PENS.sum(), 'BRL', locale='pt_BR'),
        format_currency(pensionistas.PMBC_PENS.sum(), 'BRL', locale='pt_BR'),
        format_currency(aposentados.PMBC_APO.sum()+aposentados.PMBC_REV_PENS.sum()+pensionistas.PMBC_PENS.sum(), 'BRL', locale='pt_BR')
        ]})
    
    tabela_pmbc = dash_table.DataTable(pmbc.to_dict('records'),style_as_list_view=True,
                                             style_header={
                    'backgroundColor': '#003e4c',#f8f5f0',
                    'color': 'white',
                    'fontWeight': 'bold'
                },
            style_cell={
                    'textAlign': 'center',
                    'padding': '8px',
                    'font-family': 'Helvetica',
                    'fontSize':15,
                    'color':'#5d8aa7',
                    'fontWeight': 'bold',
                    #'font-family': "Neulis Alt",
                },
                                 )

    pmbac=pd.DataFrame({'PMBaC':[
        'VABF - Aposentadorias:',
        'VABF - Reversão em Pensão:',
        'VABF - Pecúlio por Invalidez:',        
        'VABF - Pecúlio por Morte:',        
        'TOTAL VABF:'
        '',
        '',
        'VACF (13x valor mensal):',
        'VASF (13x valor mensal):',
        '',
        'PMBaC Crédito Unitário:',
        'PMBaC Custo Agregado:'],

        '': [
            format_currency(ativos.VABF_APO.sum(), 'BRL', locale='pt_BR'),
             format_currency(ativos.VABF_REV_PENS.sum(), 'BRL', locale='pt_BR'),
             format_currency(ativos.VABF_INV.sum(), 'BRL', locale='pt_BR'),
             format_currency(ativos.VABF_PEC.sum(), 'BRL', locale='pt_BR'),
             format_currency(ativos.VABF_APO.sum()+ativos.VABF_REV_PENS.sum()+ativos.VABF_INV.sum()+ativos.VABF_PEC.sum(), 'BRL', locale='pt_BR'),
             '',
             format_currency(ativos.VACF.sum(), 'BRL', locale='pt_BR'),
             format_currency(ativos.VASF.sum() * 13, 'BRL', locale='pt_BR'),
             '',
             format_currency(ativos.PMBaC_UC.sum(), 'BRL', locale='pt_BR'),
             format_currency((ativos.VABF_APO.sum()+ativos.VABF_REV_PENS.sum()+ativos.VABF_INV.sum()+ativos.VABF_PEC.sum())-ativos.VACF.sum(), 'BRL', locale='pt_BR')
        ]})
    
    tabela_pmbac = dash_table.DataTable(pmbac.to_dict('records'),style_as_list_view=True,
                                             style_header={
                    'backgroundColor': '#003e4c',#f8f5f0',
                    'color': 'white',
                    'fontWeight': 'bold'
                },
            style_cell={
                    'textAlign': 'center',
                    'padding': '8px',
                    'font-family': 'Helvetica',
                    'fontSize':15,
                    'color':'#5d8aa7',
                    'fontWeight': 'bold',
                    #'font-family': "Neulis Alt",
                },
    )


    return tabela_pmbc,tabela_pmbac


if __name__ == "__main__":
    app.run_server(debug=False)
