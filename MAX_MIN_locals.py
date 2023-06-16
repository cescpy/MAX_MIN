# -*- coding: utf-8 -*-
"""
AQUEST SCRIPT DECARREGA DE YFINANCE LES DADES DE COTITZACIÓ, LOCALITZA ELS MÀXIMS Y MÍNIMS LOCALS I ELS MOSTRA EN UN GRÀFIC:
- MÀXIM LOCAL = SI EL MÀXIM DE LES BARRES ANTERIOR I POSTERIOR SON MÉS BAIXOS QUE L'ACTUAL
- MÍNIM LOCAL = SI EL MÍNIM DE LES BARRES ANTERIOR I POSTERIOR SON MÉS ALTS QUE L'ACTUAL
(ES POT VARIAR A QUE LA CONDICIÓ SIGUI: 
 2 BARRES ANTERIORS I POSTERIORS, UNA BARRA ANTERIOR I DOS POSTERIORS, DOS BARRES ANTERIORS I UNA POSTERIOR,...)

ES NETEJA ELS MIN I MAX LOCALS DE FORMA QUE ENTRE DOS MAX NOMÉS HI HAGI UN MIN I ENTRE DOS MIN NOMÉS HI HAGI UN MAX.
(ES DEIXA EL VALOR MÉS EXTREM EN CAS QUE HI HAGI MÉS D'UN)

UN COP CALCULATS I NETEJATS ELS MAX I MIN LOCALS EN ELS SEUS DATAFRAMES ES COMBINEN AMB EL DATAFRAME PRINCIPAL
ES GRAFICA LA SERIE DE PREUS AMB ELS MAX I MIN LOCALS MARCATS AMB PUNTS
"""


import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf

###########################
### INTRODUIR VARIABLES ###
###########################
ticker = '^SPX'
start = '2023-01-01'
temporalidad = "1d"     # h, d, wk,....

### Versió amb INPUTS
# ticker = str(input("Introduce el ticker (formato yfinance): "))
# start = str(input("Introduce la fecha de inicio de los datos(formato aaaa-mm-dd): "))
# temporalidad = str(input("Introduce la temporalidad (1h, 1d, 1wk,...): "))

#############################
### DEFINICIÓ DE FUNCIONS ###
#############################

def DownloadData(ticker, start, temporalidad):
    # FUNCIÓ PER DESCARREGAR LES DADES DE COTITZACIÓ I ORGANITZAR EL DATAFRAME
    df = pd.DataFrame(yf.download(ticker, start= start, interval= temporalidad))
    # Creo una columna amb les dates per tenir-les independents de l'índex 
    df['date'] = df.index
    # En principi ja el tenen el format de data però per assegurar...
    df['date'] = pd.to_datetime(df['date'])
    # Es reseteja l'index de dates per poder fer els 'iloc/loc' (no es necessari amb el codi actual)
    # df = df.reset_index(drop=True)
    
    return df


def LocalMaxMin(df):
    # Creo els 2 dataframes buits pels max i min locals
    # df_max_local = pd.DataFrame(columns=['date', 'max_local'])
    # df_min_local = pd.DataFrame(columns=['date', 'min_local'])
    
    # Creo els 2 dataframes pels max i min locals. El primer valor de cada un son els Max i Min de la primera barra
    df_max_local = pd.DataFrame({'date': [df.iloc[0]['date']], 'max_local': [df.iloc[0]['High']]})
    df_min_local = pd.DataFrame({'date': [df.iloc[0]['date']], 'min_local': [df.iloc[0]['Low']]})
    
    # Iterem a través del dataframe original 
    # i afegim els valors de min_local i max_local als seus dataframes
            #### Utilitzem al loc "len(df_max_local)" per ubicar la següent fila(la final) que es on s'afegeixen les dades de la nova línia
    for i in range(1, len(df)-1): 
        # Si es un màxim local
        # if (df['High'][i] > df['High'][i-1] and df['High'][i] > df['High'][i+1]) or (df['High'][i] > df['High'][i-1] and df['High'][i] > df['High'][i+2]) or (df['High'][i] > df['High'][i-2] and df['High'][i] > df['High'][i+1]): 
        if df['High'][i] > df['High'][i-1] and df['High'][i] > df['High'][i+1]:
            df_max_local.loc[len(df_max_local)] = {'date': df['date'][i], 'max_local': df['High'][i]}
        # Si es un mínim local
        if df['Low'][i] < df['Low'][i-1] and df['Low'][i] < df['Low'][i+1]:
            df_min_local.loc[len(df_min_local)] = {'date': df['date'][i], 'min_local': df['Low'][i]}
    
    return df_max_local, df_min_local


def CleanLocalMaxMin(df_max_local, df_min_local):
    # Neteja dels MAX-MIN intercalats en excés
    ## Eliminar mínims intercalats (més d'un mínim entre dos màxims) i deixar el menor
    for i in range(1, len(df_max_local)): 
        start_date = df_max_local['date'][i-1]
        end_date= df_max_local['date'][i]
        df_range = df_min_local.loc[(df_min_local['date'] > start_date) & (df_min_local['date'] < end_date)]
        num_filas = df_range.shape[0]
        if num_filas > 1:
            val_min = df_min_local['min_local'].loc[(df_min_local['date'] > start_date) & (df_min_local['date'] < end_date)].min()        
            rango_filas = df_min_local.loc[(df_min_local['date'] > start_date) & (df_min_local['date'] < end_date)]
            df_min_local = df_min_local.drop(df_min_local[(df_min_local['min_local'] != val_min) & (df_min_local.index.isin(rango_filas.index))].index)
    
    df_min_local = df_min_local.reset_index(drop=True)
    
    ## Eliminar màxims intercalats (més d'un màxim entre dos mínims) i deixar el major
    for i in range(1, len(df_min_local)): 
        start_date = df_min_local['date'][i-1]
        end_date= df_min_local['date'][i]
        df_range = df_max_local.loc[(df_max_local['date'] > start_date) & (df_max_local['date'] < end_date)]
        num_filas = df_range.shape[0]
        if num_filas > 1:
           val_max = df_max_local['max_local'].loc[(df_max_local['date'] > start_date) & (df_max_local['date'] < end_date)].max()        
           rango_filas = df_max_local.loc[(df_max_local['date'] > start_date) & (df_max_local['date'] < end_date)]
           df_max_local = df_max_local.drop(df_max_local[(df_max_local['max_local'] != val_max) & (df_max_local.index.isin(rango_filas.index))].index)
    
    df_max_local = df_max_local.reset_index(drop=True)
    
    # Neteja dels MAX-MIN en una mateixa barra (de moment crec que no fa falta)  

    return df_max_local, df_min_local


def GraphLocalMaxMin (df, df_max, df_min, ticker, temporalidad, start):
    # AQUEST GRÀFIC ES LA COTITZACIO AMB ELS MAX I MIN LOCALS MARCATS AMB PUNTS
    # Creo un df_graph per unir els dataframes de df_min y de df_max amb el dataframe principal df
    df_graph = pd.merge(df, df_max, on='date', how='left')   # how=outer???
    df_graph = pd.merge(df_graph, df_min, on='date', how='left')

    # Poso les dates com a índex
    df_graph.index = df_graph['date']
    df_graph.index = pd.to_datetime(df.index)

    # Crear el gràfic
    mpf.plot(df_graph, type='candle', style='charles',
             title= ('Cotització '+ticker+' a '+temporalidad+' desde '+ start+'  max i min locals'),
             ylabel='Precio',
             ylabel_lower='Volumen',
             volume=True,
             figratio=(12, 8),
             addplot=[mpf.make_addplot(df_graph['max_local'], color='g', scatter = True),
                      mpf.make_addplot(df_graph['min_local'], color='r', scatter = True)])

    plt.show()
    

######################
### INICI PROGRAMA ###
######################
"""
TROBAR ELS MAX I MIN LOCALS I MOSTRAR UNA GRÀFICA
"""
# DESCARREGO LES DADES DE COTITZACIÓ
df = DownloadData(ticker, start, temporalidad)
# LOCALITZO ELS MAX I MIN LOCALS
df_max_local, df_min_local = LocalMaxMin(df)
# NETEJO ELS MAX I MIN INTERCALATS EN EXCÉS
df_max_local, df_min_local = CleanLocalMaxMin(df_max_local, df_min_local)
# GRAFICO LA COTITZACIÓ AMB ELS MAX I MIN LOCALS MARCATS AMB PUNTS
GraphLocalMaxMin (df, df_max_local, df_min_local, ticker, temporalidad, start)


