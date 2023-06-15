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
start = '2023-06-01'
temporalidad = "5m"     # h, d, wk,....

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
        # Busca les 
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
             mav=(5, 20, 44),
             volume=True,
             figratio=(12, 8),
             addplot=[mpf.make_addplot(df_graph['max_local'], color='g', scatter = True),
                      mpf.make_addplot(df_graph['min_local'], color='r', scatter = True)])

    plt.show()
    
def GraphConfMaxMin (df, df_max, df_min, ticker, temporalidad, start):
    # AQUEST GRÀFIC ES LA COTITZACIO AMB ELS MAX I MIN LOCALS MARCATS AMB PUNTS
    # Creo un df_graph per unir els dataframes de df_min y de df_max amb el dataframe principal df
    df_graph = pd.merge(df, df_max, on='date', how='left')   # how=outer???
    df_graph = pd.merge(df_graph, df_min, on='date', how='left')
    
    df_graph['trend_temp_x'].fillna(method='ffill', inplace=True)
    df_graph['trend_temp_y'].fillna(method='ffill', inplace=True) 

    # Poso les dates com a índex
    df_graph.index = df_graph['date']
    df_graph.index = pd.to_datetime(df.index)

    # Crear el gràfic
    mpf.plot(df_graph, type='candle', style='charles',
             title= ('Cotització '+ticker+' a '+temporalidad+' desde '+ start+'  max i min locals'),
             ylabel='Precio',
             ylabel_lower='Volumen',
             mav=(5, 10, 20, 44),
             volume=True,
             figratio=(12, 8),
             addplot=[mpf.make_addplot(df_graph['max_conf'], color='g', scatter = True),
                      mpf.make_addplot(df_graph['min_conf'], color='r', scatter = True),
                      mpf.make_addplot(df_graph['trend_temp_x'], type='bar', color='g', panel=2)])

    plt.show()
    
    return df_graph


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


"""
FIXAR ELS MAX I MIN CONFIRMATS PER DEFINIR LA TENDÈNCIA
df_max_conf
df_min_conf
"""
# AFEGEIXO UNA COLUMNA PER MARCAR CADA DADA COM A MAX O MIN
df_max_local['max_type'] = "max"
df_min_local['min_type'] = "min"

# Creo un dataframe amb el max i min locals combinats
df_maxmin_local = pd.merge(df_max_local, df_min_local, on='date', how= 'outer').sort_values('date').reset_index(drop=True)

# AL INICI NO TENIM UNA TENDENCIA DEFINIDA, la definim "a ull" 
# (si en 20 barres a pujat o baixat el preu)
# Creo una columna que controla la tendencia temporal inicialitzant-la amb el primer valor
if df['Close'][20]>= df['Close'][0]:
    df_maxmin_local.loc[0, 'trend_temp'] = 1
else:
    df_maxmin_local.loc[0, 'trend_temp'] = -1
  
    
# Reomplo els buits a max_local i min_local amb el valor anterior de la mateixa columna 
# for i in range(1, len(df_maxmin_local)):
#     if (df_maxmin_local['max_local'].isnull()[i] == True):
#        df_maxmin_local.loc[i, 'max_local']  = df_maxmin_local.loc[i-1, 'max_local'] 
#     if (df_maxmin_local['min_local'].isnull()[i] == True):
#        df_maxmin_local.loc[i, 'min_local']  = df_maxmin_local.loc[i-1, 'min_local'] 
### Fa el mateix que el "for" però més òptim   
df_maxmin_local['max_local'].fillna(method='ffill', inplace=True)
df_maxmin_local['min_local'].fillna(method='ffill', inplace=True)  
    
# Creo les columnes que registren els max y min confirmats
df_maxmin_local.loc[0, 'max_conf'] = df_maxmin_local.loc[0, 'max_local']
df_maxmin_local.loc[0, 'min_conf'] = df_maxmin_local.loc[0, 'min_local']



# Busco els max i min confirmats i vaig definint tendència
for i in range(1, len(df_maxmin_local)):
    #Columna max_local
    # Si el max_local no es igual que l'anterior
    if df_maxmin_local['max_local'][i] != df_maxmin_local['max_local'][i-1]:
        # 1-Si es tendència alcista i el max es més alt que l'anterior
        if df_maxmin_local.loc[i-1, 'trend_temp'] == 1 and df_maxmin_local.loc[i, 'max_local'] > df_maxmin_local.loc[i-1, 'max_local']:
            # Mantenim tendencia alcista
            df_maxmin_local.loc[i, 'trend_temp'] = 1
            #Si es mes alt que l'últim max_confirmat
            if df_maxmin_local.loc[i, 'max_local'] > df_maxmin_local.loc[i-1, 'max_conf']:
                # Es un max_conf
                df_maxmin_local.loc[i, 'max_conf'] = df_maxmin_local.loc[i, 'max_local']
            #Si no, no es un max_confirmat
            else:
                df_maxmin_local.loc[i, 'max_conf'] = df_maxmin_local.loc[i-1, 'max_conf']
            
        # 2-Si es tendència alcista i el max es més baix que l'anterior
        if df_maxmin_local.loc[i-1, 'trend_temp'] == 1 and df_maxmin_local.loc[i, 'max_local'] < df_maxmin_local.loc[i-1, 'max_local']:
            # Mantenim tendencia alcista
            df_maxmin_local.loc[i, 'trend_temp'] = 1
            # No es un max_conf
            df_maxmin_local.loc[i, 'max_conf'] = df_maxmin_local.loc[i-1, 'max_conf']
            
        # 3-Si es tendència baixista i el max es més alt que l'anterior
        if df_maxmin_local.loc[i-1, 'trend_temp'] == -1 and df_maxmin_local.loc[i, 'max_local'] > df_maxmin_local.loc[i-1, 'max_local']:
            # Canvia a tendencia alcista
            df_maxmin_local.loc[i, 'trend_temp'] = 1
            # Es un max_conf
            df_maxmin_local.loc[i, 'max_conf'] = df_maxmin_local.loc[i, 'max_local']
        
        # 4-Si es tendència baixista i el max es més baix que l'anterior
        if df_maxmin_local.loc[i-1, 'trend_temp'] == -1 and df_maxmin_local.loc[i, 'max_local'] < df_maxmin_local.loc[i-1, 'max_local']:
            # Mantenim tendencia baixista
            df_maxmin_local.loc[i, 'trend_temp'] = -1
            # Es un max_conf pendent
            df_maxmin_local.loc[i, 'max_conf'] = df_maxmin_local.loc[i, 'max_local']
    else: 
        df_maxmin_local.loc[i, 'max_conf'] = df_maxmin_local.loc[i-1, 'max_conf']
    
    
    #Columna min_local
    # Si el min_local no es igual que l'anterior
    if df_maxmin_local['min_local'][i] != df_maxmin_local['min_local'][i-1]:
        # 4-Si es tendència alcista i el min es més alt que l'anterior
        if df_maxmin_local.loc[i-1, 'trend_temp'] == 1 and df_maxmin_local.loc[i, 'min_local'] > df_maxmin_local.loc[i-1, 'min_local']:
            # Mantenim tendencia alcista
            df_maxmin_local.loc[i, 'trend_temp'] = 1
            # Es un min_conf pendent
            df_maxmin_local.loc[i, 'min_conf'] = df_maxmin_local.loc[i, 'min_local']
                    
        # 3-Si es tendència alcista i el min es més baix que l'anterior
        if df_maxmin_local.loc[i-1, 'trend_temp'] == 1 and df_maxmin_local.loc[i, 'min_local'] < df_maxmin_local.loc[i-1, 'min_local']:
            # Canvia a tendencia baixista
            df_maxmin_local.loc[i, 'trend_temp'] = -1
            # Es un min_conf
            df_maxmin_local.loc[i, 'min_conf'] = df_maxmin_local.loc[i, 'min_local']
    
        # 2-Si es tendència baixista i el min es més alt que l'anterior
        if df_maxmin_local.loc[i-1, 'trend_temp'] == -1 and df_maxmin_local.loc[i, 'min_local'] > df_maxmin_local.loc[i-1, 'min_local']:
            # Mantenim tendencia baixista
            df_maxmin_local.loc[i, 'trend_temp'] = -1
            # No es un min_conf 
            df_maxmin_local.loc[i, 'min_conf'] = df_maxmin_local.loc[i-1, 'min_conf']
        
        # 1-Si es tendència baixista i el min es més baix que l'anterior
        if df_maxmin_local.loc[i-1, 'trend_temp'] == -1 and df_maxmin_local.loc[i, 'min_local'] < df_maxmin_local.loc[i-1, 'min_local']:
            # Mantenim tendencia baixista
            df_maxmin_local.loc[i, 'trend_temp'] = -1
            #Si es mes baix que l'últim min_confirmat
            if df_maxmin_local.loc[i, 'min_local'] < df_maxmin_local.loc[i-1, 'min_conf']:
                # Es un min_conf
                df_maxmin_local.loc[i, 'min_conf'] = df_maxmin_local.loc[i, 'min_local']
            #Si no, no es un min_confirmat
            else:
                df_maxmin_local.loc[i, 'min_conf'] = df_maxmin_local.loc[i-1, 'min_conf']
    else: 
        df_maxmin_local.loc[i, 'min_conf'] = df_maxmin_local.loc[i-1, 'min_conf']
    
    
        
    
# S'extreuen les dades a df_max_conf i df_min_conf
df_max_conf = df_maxmin_local.loc[:, ['date', 'max_conf', 'trend_temp']]
df_min_conf = df_maxmin_local.loc[:, ['date', 'min_conf', 'trend_temp']]

# Netejo files i deixo només les que tenen el max i min confirmat
df_max_conf.drop_duplicates(subset=['max_conf'], keep='first', inplace=True)
df_min_conf.drop_duplicates(subset=['min_conf'], keep='first', inplace=True)




# GRAFICO LA COTITZACIÓ AMB ELS MAX I MIN LOCALS MARCATS AMB PUNTS
GraphConfMaxMin (df, df_max_conf, df_min_conf, ticker, temporalidad, start)

df_graph = GraphConfMaxMin(df, df_max_conf, df_min_conf, ticker, temporalidad, start) 


    
    
    
    





""""
for i in range(1, len(df_maxmin_local)): 
    if df_maxmin_local.loc[i-1, 'trend_temp'] == 1:
        pass

    
df_maxmin_local.loc[2, 'min_local'] > df_maxmin_local.loc[1, 'min_local']

if (df_maxmin_local['max_local'].isnull()[i] != True) and (df_maxmin_local.loc[i-1, 'trend_temp'] == 1): 
"""

    
"""
Si max_local té un NaN:
    no fa res
Si no té NaN:
    Si max_local-1 té un NaN:
        loki = 2
    Si max_local-1 no té un Nan:
        loki = 1

    Si (max_local > max_local-loki) and (trend_temp-1 == 1):
        
    Si (max_local > max_local-loki) and (trend_temp-1 == -1):
        
    Si (max_local < max_local-loki) and (trend_temp-1 == 1):
        
    Si (max_local < max_local-loki) and (trend_temp-1 == -1):   

        

Si min_local es Nan:
    no fa res
Si min_local no té Nan:
    Si min_local-1 té un NaN:
        loki = -2
    Si min_local-1 no té un Nan:
        loki = -1





"""