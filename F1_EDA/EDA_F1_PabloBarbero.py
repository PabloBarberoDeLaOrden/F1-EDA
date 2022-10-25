#############################################################
######### Importamos librerías necesarías ###################
#############################################################

import numpy as np 
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns
#%matplotlib inline

# Comprobamos que el directorio va a utilizar todos los archivos necesarios para el estudio.
import os
for dirname, _, filenames in os.walk(r'C:\Users\MEMORY SISTEMAS\Desktop\Bootcamp\thebridge_ft_sep22 - PB\99-Datos'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
        
pd.set_option('max_columns', 100)

# Creamos una función que nos importe todos los los csv, a la que llamaremos para construir nuestras tablas definitivas
def import_all():
    data = {}
    for dirname, _, filenames in os.walk(r'C:\Users\MEMORY SISTEMAS\Desktop\Bootcamp\thebridge_ft_sep22 - PB\99-Datos'):
        for filename in filenames:
            name = filename.replace('.csv', '')
            data[name] = pd.read_csv(os.path.join(dirname, filename))
            
    return data

#########################################################################################################
## Función para la construcción de las tablas finales con las que se trabajarán a lo largo del estudio ##
#########################################################################################################

def add_ids(data, key):
    
    df = data[key]
    n_lines = df.shape[0]

    #tomamos la información de cada carrera que se identifica de manera única y que aparecerá en todas las futuras tablas
    df = pd.merge(df, data['races'][['raceId', 
                                     'year', 'round', 
                                     'circuitId', 'date', 'time']], 
                  on='raceId', how='left')
    if df.shape[0] != n_lines:
        raise ValueError('Merging raceId dio error')

    df = pd.merge(df, data['circuits'][['circuitId', 
                                        'circuitRef', 'location', 'country']], 
                  on='circuitId', how='left')
    if df.shape[0] != n_lines:
        raise ValueError('Merging circuitId dio error')
        
    df = pd.merge(df, data['drivers'][['driverId', 
                                       'driverRef', 'forename', 'surname', 
                                       'dob', 'nationality']].rename(columns={'nationality': 'drv_nat'}), 
                  on='driverId', how='left')
    if df.shape[0] != n_lines:
        raise ValueError('Merging driverId dio error')
    # Una vez obtenida la información común que compartirán las tablas finales

    # Indicamos las particularidades de cada una de las tablas definitivas
    if (key != 'lap_times') and (key != 'pit_stops'):
        df = pd.merge(df, data['constructors'][['constructorId', 
                                                'constructorRef', 
                                                'name', 'nationality']].rename(columns={'nationality': 'cstr_nat'}), 
                      on='constructorId', how='left')
        if df.shape[0] != n_lines:
            raise ValueError('Merging constructorId dio error')
        
    if key == 'results':
        df = pd.merge(df, data['status'], 
                      on='statusId', how='left')
        if df.shape[0] != n_lines:
            raise ValueError('Merging statusId dio error')
        
    return df

data = import_all()

res = add_ids(data, 'results')
qual = add_ids(data, 'qualifying')
laps = add_ids(data, 'lap_times')

# renombramos las columnas que pueden resultar confusas
laps.rename(columns={'time_x': 'lap_time', 'time_y': 'time'}, inplace=True)
res.rename(columns={'time_x': 'race_time', 'time_y': 'time'}, inplace=True)

# Incluímos la información de los constructores tanto en las vueltas como en las paradas
laps = pd.merge(laps, res[['raceId', 'driverId', 
                           'constructorRef', 'name', 'cstr_nat']], 
                on=['raceId', 'driverId'], how='left')

#####################################################################
###### Normalización del puntaje y creacion de variables ############
#####################################################################

res[['lap_mins', 'lap_secs']] = res['fastestLapTime'].str.split(':', expand=True)
res[['lap_secs', 'lap_millisecs']] = res['lap_secs'].str.split('.', expand=True)
res['lap_mins'] = pd.to_numeric(res['lap_mins'], errors='coerce').fillna(99)
res['lap_secs'] = pd.to_numeric(res['lap_secs'], errors='coerce').fillna(99)
res['lap_millisecs'] = pd.to_numeric(res['lap_millisecs'], errors='coerce').fillna(99)

res['fastestLapTime_ms'] = (60 * res['lap_mins'] + res['lap_secs']) * 1000 + res['lap_millisecs']

res['race_fastestTime'] = res.groupby('raceId').fastestLapTime_ms.transform('min')
res['FastLap'] = np.where(res['race_fastestTime'] == res['fastestLapTime_ms'], 1, 0)

res.drop(['lap_mins', 'lap_secs', 'lap_millisecs'], axis=1, inplace=True)

points = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

res['points'] = res['positionOrder'].map(points).fillna(0)

res['fastestLap'] = pd.to_numeric(res['fastestLap'], errors='coerce')

res['DriverName'] = res['forename'].str[0] + '. ' + res['surname']


res['net_gain'] = -(res['positionOrder'] - res['grid'])
res['abs_gain'] = abs(res['net_gain'])

res['finished'] = np.where(res.status == 'Finished', 1, 0)

#################################################################
################ Informacion temporada actual ###################
#################################################################

res_2022= res[res["year"] == 2022]
qual_2022= qual[qual["year"] == 2022]

clasif_pilotos_2022 = res_2022.groupby('driverRef').sum('points')[['points']].sort_values('points', ascending=False)
clasif_cons_2022 = res_2022.groupby('constructorRef').sum('points')[['points']].sort_values('points', ascending=False)
poles_pilotos_2022 = qual_2022.loc[qual_2022.position==1].groupby('driverRef').sum('position')[['position']].rename(columns={'position': 'Poles'})
poles_cons_2022 = qual_2022.loc[qual_2022.position==1].groupby('constructorRef').sum('position')[['position']].rename(columns={'position': 'Poles'})
podiums_pilotos_2022 = res_2022.loc[res_2022.position.isin(['1','2','3'])].groupby('driverRef')[['position']].count().rename(columns={'position': 'Podiums'}).sort_values('Podiums', ascending=False)
podiums_cons_2022 = res_2022.loc[res_2022.position.isin(['1','2','3'])].groupby('constructorRef')[['position']].count().rename(columns={'position': 'Podiums'}).sort_values('Podiums', ascending=False)
Fastlap_pilotos_2022 = res_2022.groupby('driverRef').sum('FastLap')[['FastLap']].sort_values('FastLap', ascending=False)
Fastlap_cons_2022 = res_2022.groupby('constructorRef').sum('FastLap')[['FastLap']].sort_values('FastLap', ascending=False)
Posiciones_ganadas_pilotos_2022 = res_2022.groupby('driverRef').sum('net_gain')[['net_gain']].sort_values('net_gain', ascending=False)
Posiciones_ganadas_cons_2022 = res_2022.groupby('constructorRef').sum('net_gain')[['net_gain']].sort_values('net_gain', ascending=False)

#####################################################
################# Funciones gráficas ################
#####################################################

# plotly
# import plotly.plotly as py
from plotly.offline import init_notebook_mode, iplot, plot
import plotly as py
init_notebook_mode(connected=True)
import plotly.graph_objs as go
import plotly.express as px

# word cloud library
from wordcloud import WordCloud

# matplotlib
import matplotlib.pyplot as plt

def graph_por_anio(data,x,y,identif,titulo):
    trace1 = go.Scatter(
                    x = data[x],
                    y = data[y],
                    name = 'citations',
                    mode= 'lines',
                    marker = dict(color = 'rgba(160, 5, 20, 0.8)'),
                    text = data[identif])
    layout = dict(title = titulo,
             xaxis= dict(title= 'Temporadas',ticklen= 5)
           )
    fig = go.Figure(data = trace1, layout=layout)
    return iplot(fig)

def graph_barras(data,y,x, titulo):
  ww = data.reset_index()
  fig = px.bar(ww, y=y, x=x, text_auto='.2s',
              title=titulo,
              color_discrete_sequence =['red']*len(data), width=700, height=400 )
  fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
  return fig.show()

  ############################################
  ########## llamada a los gráficos ##########
  ############################################

graph_barras(clasif_pilotos_2022,'points','driverRef', 'Clasificacion pilotos')
graph_barras(clasif_cons_2022,'points','constructorRef', 'Clasificacion constructores')
graph_barras(poles_pilotos_2022,'Poles','driverRef', 'Poles pilotos')
graph_barras(poles_cons_2022,'Poles','constructorRef', 'Poles constructores')
graph_barras(podiums_pilotos_2022,'Podiums','driverRef', 'Podiums pilotos')
graph_barras(podiums_cons_2022,'Podiums','constructorRef', 'Podiums constructores')
graph_barras(Fastlap_pilotos_2022,'FastLap','driverRef', 'Vueltas Rápidas pilotos') 
graph_barras(Fastlap_cons_2022,'FastLap','constructorRef', 'Vueltas Rápidas constructores')
graph_barras(Posiciones_ganadas_pilotos_2022,'net_gain','driverRef', 'Posiciones ganadas en carrera')
graph_barras(Posiciones_ganadas_cons_2022,'net_gain','constructorRef', 'Posiciones ganadas en carrera')

#######################################################################################
##################### Construcción de las tablas por año ##############################
#######################################################################################

podiums_por_anio = res.loc[res.position.isin(['1','2','3'])].groupby(['year','driverRef'])[['position']].count().rename(columns={'position': 'Podiums'})
t = podiums_por_anio.reset_index()
podiums_por_anio = t.iloc[t.groupby('year').agg(max_ = ('Podiums', lambda data: data.idxmax())).max_]
n_carreras = res.groupby(['year']).nunique('raceId')[['raceId']].rename(columns={'raceId': 'num_carreras'})
podiums_por_anio = pd.merge(podiums_por_anio, n_carreras, on = 'year', how = 'left' )
podiums_por_anio['p_podiums'] = podiums_por_anio['Podiums']/podiums_por_anio['num_carreras']

poles_por_anio = qual.loc[qual.position==1].groupby(['year','driverRef']).sum('position')[['position']].rename(columns={'position': 'Poles'})
t = poles_por_anio.reset_index()
poles_por_anio = t.iloc[t.groupby('year').agg(max_ = ('Poles', lambda data: data.idxmax())).max_]
poles_por_anio = pd.merge(poles_por_anio, n_carreras, on = 'year', how = 'left' )
poles_por_anio['p_poles'] = poles_por_anio['Poles']/poles_por_anio['num_carreras']

ganadores_por_anio = res.groupby(['year','driverRef']).sum('points')[['points']]
t = ganadores_por_anio.reset_index()
ganadores_por_anio = t.iloc[t.groupby('year').agg(max_ = ('points', lambda data: data.idxmax())).max_]
ganadores_por_anio = pd.merge(ganadores_por_anio, n_carreras, on = 'year', how = 'left' )
ganadores_por_anio['ptos_carrera'] = ganadores_por_anio['points']/ganadores_por_anio['num_carreras']
ganadores_por_anio

FastLap_por_anio = res.groupby(['year','driverRef']).sum('FastLap')[['FastLap']]
t = FastLap_por_anio.reset_index()
FastLap_por_anio = t.iloc[t.groupby('year').agg(max_ = ('FastLap', lambda data: data.idxmax())).max_]
FastLap_por_anio = pd.merge(FastLap_por_anio, n_carreras, on = 'year', how = 'left' )
FastLap_por_anio['p_FastLap'] = FastLap_por_anio['FastLap']/FastLap_por_anio['num_carreras']
FastLap_por_anio

net_gain2 = res.groupby(['year','driverRef']).sum('net_gain')[['net_gain']]
net_gain2 = net_gain2.reset_index()
ganadores_por_anio = pd.merge(ganadores_por_anio, net_gain2, on = ['year','driverRef'], how = 'left' )
ganadores_por_anio

###########################################################################
###################### Llamada gráficos por año ###########################
###########################################################################

import plotly.graph_objs as go
vueltas_rapidas = FastLap_por_anio.loc[FastLap_por_anio.year>2003]
# Creating trace1
trace1 = go.Scatter(
                    x = podiums_por_anio['year'],
                    y = podiums_por_anio['p_podiums'],
                    name = 'P_podiums',
                    mode= 'lines+markers',
                    marker = dict(color = 'rgba(50, 0, 2, 0.8)'),
                    text = podiums_por_anio['driverRef'])
# Creating trace2
trace2 = go.Scatter(
                    x = poles_por_anio['year'],
                    y = poles_por_anio['p_poles'],
                    name = 'P_poles',
                    mode= 'lines+markers',
                    marker = dict(color = 'rgba(190, 50, 10, 0.8)'),
                    text = poles_por_anio['driverRef'])

trace3 = go.Scatter(
                    x = vueltas_rapidas['year'],
                    y = vueltas_rapidas['p_FastLap'],
                    name = 'P_FastLap',
                    mode= 'lines+markers',
                    marker = dict(color = 'rgba(160, 5, 20, 0.8)'),
                    text = vueltas_rapidas['driverRef'])

data = [trace1, trace2, trace3]
layout = dict(title = 'Proporción de podiums, poles y vueltas rápidas máximas por año',
             xaxis= dict(title= 'Temporada',ticklen= 5)
           )
fig = go.Figure(data = data, layout=layout)
iplot(fig)

trace1 = go.Scatter(
                    x = ganadores_por_anio['year'],
                    y = ganadores_por_anio['ptos_carrera'],
                    name = 'ptos_carrera',
                    mode= 'lines+markers',
                    marker = dict(color = 'rgba(50, 0, 2, 0.8)'),
                    text = podiums_por_anio['driverRef'],
                    xaxis='x1',
                    yaxis='y1')
# Creating trace2
trace2 = go.Scatter(
                    x = ganadores_por_anio['year'],
                    y = ganadores_por_anio['net_gain'],
                    name = 'net_gain',
                    mode= 'lines+markers',
                    marker = dict(color = 'rgba(160, 5, 20, 0.8)'),
                    text = poles_por_anio['driverRef'],
                    xaxis='x2',
                    yaxis='y2')


data = [trace1, trace2]
layout = go.Layout(
    xaxis=dict(
        domain=[0, 1],
        anchor='y1'
    ),
    yaxis=dict(
        domain=[0, 0.45],
        anchor='x1'
    ),
    xaxis2=dict(
        domain=[0, 1],
        anchor='y2'
    ),
    yaxis2=dict(
        domain=[0.55, 1],
        anchor='x2'
    ),
    title = 'Puntos por carrera y posiciones ganadas en ellas'
)

fig = go.Figure(data = data, layout=layout)
iplot(fig)

graph_por_anio(podiums_por_anio,'year','p_podiums','driverRef','Proporción podiums por temporada')
graph_por_anio(poles_por_anio,'year','p_poles','driverRef','Proporción poles por temporada')
graph_por_anio(ganadores_por_anio,'year','ptos_carrera','driverRef','Puntos por carrera')
graph_por_anio(ganadores_por_anio,'year','net_gain','driverRef','Posiciones ganadas en carrera durante la temporada')
graph_por_anio(FastLap_por_anio.loc[FastLap_por_anio.year>2003],'year','p_FastLap','driverRef','Proporción de vueltas rapidas por temporada')

#################################################################
################# Comparacion entre temporadas ##################
#################################################################

res_2002= res[res["year"] == 2002]
qual_2002= qual[qual["year"] == 2002]
res_2011= res[res["year"] == 2011]
qual_2011= qual[qual["year"] == 2011]
res_2021= res[res["year"] == 2021]
qual_2021= qual[qual["year"] == 2021]

clasif_pilotos_2002 = res_2002.groupby('driverRef').sum('points')[['points']].sort_values('points', ascending=False)
clasif_cons_2002 = res_2002.groupby('constructorRef').sum('points')[['points']].sort_values('points', ascending=False)
poles_pilotos_2002 = qual_2002.loc[qual_2002.position==1].groupby('driverRef').sum('position')[['position']].rename(columns={'position': 'Poles'})
poles_cons_2002 = qual_2002.loc[qual_2002.position==1].groupby('constructorRef').sum('position')[['position']].rename(columns={'position': 'Poles'})
podiums_pilotos_2002 = res_2002.loc[res_2002.position.isin(['1','2','3'])].groupby('driverRef')[['position']].count().rename(columns={'position': 'Podiums'}).sort_values('Podiums', ascending=False)
podiums_cons_2002 = res_2002.loc[res_2002.position.isin(['1','2','3'])].groupby('constructorRef')[['position']].count().rename(columns={'position': 'Podiums'}).sort_values('Podiums', ascending=False)
Fastlap_pilotos_2002 = res_2002.groupby('driverRef').sum('FastLap')[['FastLap']].sort_values('FastLap', ascending=False)
Fastlap_cons_2002 = res_2002.groupby('constructorRef').sum('FastLap')[['FastLap']].sort_values('FastLap', ascending=False)
Posiciones_ganadas_pilotos_2002 = res_2002.groupby('driverRef').sum('net_gain')[['net_gain']].sort_values('net_gain', ascending=False)
Posiciones_ganadas_cons_2002= res_2002.groupby('constructorRef').sum('net_gain')[['net_gain']].sort_values('net_gain', ascending=False)

clasif_pilotos_2011 = res_2011.groupby('driverRef').sum('points')[['points']].sort_values('points', ascending=False)
clasif_cons_2011 = res_2011.groupby('constructorRef').sum('points')[['points']].sort_values('points', ascending=False)
poles_pilotos_2011 = qual_2011.loc[qual_2011.position==1].groupby('driverRef').sum('position')[['position']].rename(columns={'position': 'Poles'})
poles_cons_2011 = qual_2011.loc[qual_2011.position==1].groupby('constructorRef').sum('position')[['position']].rename(columns={'position': 'Poles'})
podiums_pilotos_2011 = res_2011.loc[res_2011.position.isin(['1','2','3'])].groupby('driverRef')[['position']].count().rename(columns={'position': 'Podiums'}).sort_values('Podiums', ascending=False)
podiums_cons_2011 = res_2011.loc[res_2011.position.isin(['1','2','3'])].groupby('constructorRef')[['position']].count().rename(columns={'position': 'Podiums'}).sort_values('Podiums', ascending=False)
Fastlap_pilotos_2011 = res_2011.groupby('driverRef').sum('FastLap')[['FastLap']].sort_values('FastLap', ascending=False)
Fastlap_cons_2011 = res_2011.groupby('constructorRef').sum('FastLap')[['FastLap']].sort_values('FastLap', ascending=False)
Posiciones_ganadas_pilotos_2011 = res_2011.groupby('driverRef').sum('net_gain')[['net_gain']].sort_values('net_gain', ascending=False)
Posiciones_ganadas_cons_2011= res_2011.groupby('constructorRef').sum('net_gain')[['net_gain']].sort_values('net_gain', ascending=False)

clasif_pilotos_2021 = res_2021.groupby('driverRef').sum('points')[['points']].sort_values('points', ascending=False)
clasif_cons_2021 = res_2021.groupby('constructorRef').sum('points')[['points']].sort_values('points', ascending=False)
poles_pilotos_2021 = qual_2021.loc[qual_2021.position==1].groupby('driverRef').sum('position')[['position']].rename(columns={'position': 'Poles'})
poles_cons_2021 = qual_2021.loc[qual_2021.position==1].groupby('constructorRef').sum('position')[['position']].rename(columns={'position': 'Poles'})
podiums_pilotos_2021 = res_2021.loc[res_2021.position.isin(['1','2','3'])].groupby('driverRef')[['position']].count().rename(columns={'position': 'Podiums'}).sort_values('Podiums', ascending=False)
podiums_cons_2021 = res_2021.loc[res_2021.position.isin(['1','2','3'])].groupby('constructorRef')[['position']].count().rename(columns={'position': 'Podiums'}).sort_values('Podiums', ascending=False)
Fastlap_pilotos_2021 = res_2021.groupby('driverRef').sum('FastLap')[['FastLap']].sort_values('FastLap', ascending=False)
Fastlap_cons_2021 = res_2021.groupby('constructorRef').sum('FastLap')[['FastLap']].sort_values('FastLap', ascending=False)
Posiciones_ganadas_pilotos_2021 = res_2021.groupby('driverRef').sum('net_gain')[['net_gain']].sort_values('net_gain', ascending=False)
Posiciones_ganadas_cons_2021= res_2021.groupby('constructorRef').sum('net_gain')[['net_gain']].sort_values('net_gain', ascending=False)

q = res_2002.groupby(['raceId','constructorRef']).sum('points')[['points']]
a = q.reset_index()
h = q.groupby('constructorRef').cumsum()
puntos_cons_acumulados_2002 = h.reset_index()

q = res_2011.groupby(['raceId','constructorRef']).sum('points')[['points']]
a = q.reset_index()
h = q.groupby('constructorRef').cumsum()
puntos_cons_acumulados_2011 = h.reset_index()

q = res_2022.groupby(['raceId','constructorRef']).sum('points')[['points']]
a = q.reset_index()
h = q.groupby('constructorRef').cumsum()
puntos_cons_acumulados_2022 = h.reset_index()

q = res_2002.groupby(['raceId','driverRef']).sum('points')[['points']]
a = q.reset_index()
h = q.groupby('driverRef').cumsum()
puntos_pilotos_acumulados_2002 = h.reset_index()

q = res_2011.groupby(['raceId','driverRef']).sum('points')[['points']]
a = q.reset_index()
h = q.groupby('driverRef').cumsum()
puntos_pilotos_acumulados_2011 = h.reset_index()

q = res_2022.groupby(['raceId','driverRef']).sum('points')[['points']]
a = q.reset_index()
h = q.groupby('driverRef').cumsum()
puntos_pilotos_acumulados_2022 = h.reset_index()

q = res_2021.groupby(['raceId','constructorRef']).sum('points')[['points']]
a = q.reset_index()
h = q.groupby('constructorRef').cumsum()
puntos_cons_acumulados_2021 = h.reset_index()

q = res_2021.groupby(['raceId','driverRef']).sum('points')[['points']]
a = q.reset_index()
h = q.groupby('driverRef').cumsum()
puntos_pilotos_acumulados_2021 = h.reset_index()

import plotly.express as px
def plot_comparativa_acumulada(data, identif, temporada):
    fig = px.line(data, x="raceId", y="points", color=identif, title="Acumulación de puntos Temporada "+ temporada, width=600, height=400) 
    return fig.show()


plot_comparativa_acumulada(puntos_pilotos_acumulados_2002, 'driverRef', '2002')
plot_comparativa_acumulada(puntos_cons_acumulados_2002, 'constructorRef', '2002')
plot_comparativa_acumulada(puntos_pilotos_acumulados_2011, 'driverRef', '2011')
plot_comparativa_acumulada(puntos_cons_acumulados_2011, 'constructorRef', '2011')
plot_comparativa_acumulada(puntos_pilotos_acumulados_2022, 'driverRef', '2022')
plot_comparativa_acumulada(puntos_cons_acumulados_2022, 'constructorRef', '2022')
plot_comparativa_acumulada(puntos_pilotos_acumulados_2021, 'driverRef', '2021')
plot_comparativa_acumulada(puntos_pilotos_acumulados_2022, 'driverRef', '2022')
plot_comparativa_acumulada(puntos_cons_acumulados_2021, 'constructorRef', '2021')
plot_comparativa_acumulada(puntos_cons_acumulados_2022, 'constructorRef', '2022')


