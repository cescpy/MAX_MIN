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

import MAX_MIN_locals as MM


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

######################
### INICI PROGRAMA ###
######################
"""
TROBAR ELS MAX I MIN LOCALS I MOSTRAR UNA GRÀFICA
"""
# DESCARREGO LES DADES DE COTITZACIÓ
df = MM.DownloadData(ticker, start, temporalidad)
# LOCALITZO ELS MAX I MIN LOCALS
df_max_local, df_min_local = MM.LocalMaxMin(df)
# NETEJO ELS MAX I MIN INTERCALATS EN EXCÉS
df_max_local, df_min_local = MM.CleanLocalMaxMin(df_max_local, df_min_local)
# GRAFICO LA COTITZACIÓ AMB ELS MAX I MIN LOCALS MARCATS AMB PUNTS
MM.GraphLocalMaxMin (df, df_max_local, df_min_local, ticker, temporalidad, start)
