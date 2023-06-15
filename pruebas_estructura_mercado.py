# -*- coding: utf-8 -*-
"""
https://barcelonageeks.com/como-actualizar-un-grafico-en-la-misma-figura-durante-el-ciclo/

ESTRUCTURA DE MERCADO
https://twitter.com/adrig_iv/status/1521457645982404608?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E1521457645982404608%7Ctwgr%5E35781f8e5c199b5f765bf864459df56944e220d9%7Ctwcon%5Es1_&ref_url=https%3A%2F%2Fen.rattibha.com%2Fthread%2F1542443766270787584
https://en.rattibha.com/thread/1521457645982404608
https://en.rattibha.com/thread/1562181390602448898

Terminologia:
https://en.rattibha.com/thread/1542443766270787584

    - ChoCH / Shift: Cambio de tendencia
https://pbs.twimg.com/media/FWfZd-jWYAAN_Ee.png
    - BoS / MSB : Continuación de la tendencia, en tendencia alcista romper el último HH, en tendencia bajista romper el último LL
https://pbs.twimg.com/media/FWfZhuTWYAEFlHB.jpg   
    - EQHS: Equal Highs, máximos iguales, resistencia retail, por aqui encima nos encontraremos liquidez.
https://pbs.twimg.com/media/FWfZlR2WYAAaDYv.png   
    - EQLS: Equal Lows, mínimos iguales, soporte retail, por aquí debajo nos encontraremos liquidez.
https://pbs.twimg.com/media/FWfZpPoXoAABvtr.png   

    - POI: Punto de Interés, zona del gráfico en la que estaremos atentos para una posible entrada, puede ser un order bloc, un imbalance, unos eqhs, eqls…
https://pbs.twimg.com/media/FWfZtFFXoAACXwu.png    

    - OB / Order Block: Zona donde los big players han construido posiciones, es la vela previa a un gran movimiento en la dirección contraria. 
https://pbs.twimg.com/media/FWfaEkwWIAA2xZp.png    
        - Demand: Zona de demanda, también conocido como order block.
https://pbs.twimg.com/media/FWfaIgoX0AIXr0a.png       
        - Supply: Zona de oferta, también conocido como order block.
https://pbs.twimg.com/media/FWfaL2MWQAEpam9.png

    - Inducement (idm): Me gusta verlo como una trampa, el precio reacciona antes de llegar a nuestro OB / POI, haciendo que compradores / vendedores entren antes de tiempo colocando sus SL entre el POI y el high / low creado, es decir, crean liquidez, será recogida en un futuro.  
https://pbs.twimg.com/media/FWfaTY-WIAUQ_9i.jpg

    - Liquidez: Son los Stop Loss de los operadores retail,
https://pbs.twimg.com/media/FWfaaJoXwAAJwTG.jpg

    - OTE: Optimal Trade Entry, se utiliza para calcular los retrocesos de la tendencia antes de una nueva expansión, se tira de inicio a final de la expansión.
https://pbs.twimg.com/media/FWfadUJXoAAPDNW.jpg

    - 3 Tap Setup: Setup de los tres toques, da el primer toque, expande, el precio vuelve y manipula este primer toque mitigando algún POI, vuelve a expandir y vuelve a visitar algún POI generado en la expansión del segundo toque.
https://pbs.twimg.com/media/FWfagr0WQAIgIOS.jpg

    - Power Of Three: Acumulación - Manipulación - Expansión, también conocido como AMD. Para mi es una forma de entender los movimientos del mercado, se dan de continuo, cada vela en si es un Power of Three
https://pbs.twimg.com/media/FWfalJ-XoAAKSN5.jpg

    - FVG / Imbalance : Son huecos vacíos que se quedan en el gráfico cuando la presión compradora es superior a la presión vendedora (y viceversa), si entendemos que el mercado siempre tiende a equilibrarse entenderemos que son puntos que tenderán a rellenarse.
https://pbs.twimg.com/media/FWfbDeCXkAQVpKy.png

    - RR: Risk / Reward Ratio, es decir, la relación riesgo / beneficio, herramienta que nos ayudará con la gestión del riesgo, a mayor RR, menor proporción de victorias podemos tener para ser rentables, lo explico en este hilo:
https://pbs.twimg.com/media/FWfbPdvWAAMIk0I.png






"""

class Market_Structure():
    def __init__(self):
        self.trend = 0
        self.trend_calc = 0
        self.max_c = 0
        self.min_c = 0
        self.max_t = []
        self.nim_t = []

