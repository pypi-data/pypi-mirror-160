import MetaTrader5 as mt5
from MetaTrader5 import TIMEFRAME_M1, TIMEFRAME_M2, TIMEFRAME_M3, TIMEFRAME_M4, TIMEFRAME_M5, TIMEFRAME_M6, TIMEFRAME_M10, TIMEFRAME_M12, TIMEFRAME_M15, TIMEFRAME_M20, TIMEFRAME_M30, TIMEFRAME_H1, TIMEFRAME_H2, TIMEFRAME_H4, TIMEFRAME_H3, TIMEFRAME_H6, TIMEFRAME_H8, TIMEFRAME_H12, TIMEFRAME_D1, TIMEFRAME_W1, TIMEFRAME_MN1
import random

"""
    bid = Maximum price for buy orders
    ask = Minimum price for sell orders
    deviation = Ecart type de l'ordre (variance)
    volume = Nombre total d'actions de l'ordre (par exemple 0.2 bitcoins, le volume est de 0.2)
    magic = ID de l'ordre (pour la séparer d'un autre ordre) (ici on garde 100 car un n'utilise qu'un seul ordre)
    exposure = Risque
    sma = prix moyen
"""

ORDER_BUY = 0
ORDER_SELL = 1

# def GetExposure(symbol):
#     """
#         Récupération du risque d'un symbole
#     """
#     positions = mt5.positions_get(symbol=symbol)
#     if positions:
#         posDF = pd.DataFrame(positions, columns=positions[0]._asdict().keys())
#         exposure = posDF['volume'].sum()
#         return exposure

class IBTrading:
    __signals = None                                                #Liste des signaux
    __orders = None                                                 #Liste des ordres
    __strategyFunction = None                                       #Fonction de stratégie

    def __init__(self, strategyFunction) -> None:
        self.__signals = {}
        self.__orders = {}
        self.__strategyFunction = strategyFunction
        mt5.initialize()
        return

    def AddSignal(self, signalName: str, symbol: str, timeframe: int, SMAPeriod: int) -> None:
        """
            Ajout d'un signal
            Params:
                signalName: str = Nom du signal
                symbol: str = Symbole du signal
                timeframe: int = Timeframe du signal (TIMEFRAME_##)
                SMAPeriod: int = Nombre de periode de la SMA à récupérer
        """
        self.__signals[signalName] = Signal(symbol, timeframe, SMAPeriod)        
        return
    
    def AddOrder(self, orderName: str, symbol: str, volume: float, orderType: int, deviation: float) -> None:
        """
            Ajout d'un ordre
            Params:
                orderName: str = Nom de l'ordre
                symbol: str = Symbole de l'ordre
                volume: float = Nombre d'action de l'ordre
                orderType: int = ORDER_BUY ou ORDER_SELL
                deviation: float = Ecart type de l'ordre
        """
        self.__orders[orderName] = Order(symbol, volume, orderType, deviation)
        return
    
    def CloseOrder(self, orderName: str) -> None:
        """
            Fermeture d'un ordre
            Params:
                orderName: str = Nom de l'ordre
        """
        self.__orders[orderName].Close()
        del self.__orders[orderName]
        return
    
    def Run(self) -> None:
        """
            Exécution de la stratégie
        """
        for signalName in self.__signals.keys():
            self.__signals[signalName].Update()
        self.__strategyFunction(self, self.__signals, self.__orders)
        return

class Order:
    """
        Gestion d'un ordre d'achat
    """

    id = None                                                   #ID de l'ordre
    ticket = None                                               #Ticket de l'ordre afin de le modifier
    symbol = None                                               #Symbole de l'ordre
    volume = None                                               #Nombre d'action de l'ordre
    orderType = None                                            #Type de l'ordre
    deviation = None                                            #Ecart type de l'ordre

    def __init__(self, symbol: str, volume: float, orderType: int, deviation: float) -> None:
        """
            Ouverture d'un ordre de marché
            Params:
                symbol: str = Symbole de l'ordre
                volume: int = Nombre d'action de l'ordre
                orderType: int = ORDER_BUY ou ORDER_SELL
        """
        self.id = random.randint(1, 1000)
        self.ticket = 0
        self.symbol: str = symbol
        self.volume: float = volume
        self.orderType: int = orderType
        self.deviation: float = deviation

        tick = mt5.symbol_info_tick(symbol)                                     # Récupération des informations du symbole
        bid = tick.bid                                                          # Prix minimum d'un ordre sur ce symbole (sell)
        ask = tick.ask                                                          # Prix maximum d'un ordre sur ce symbole (buy)


        request = {                                                             # Creation de l'ordre (https://www.mql5.com/en/docs/constants/structures/mqltraderequest)
            'action': mt5.TRADE_ACTION_DEAL,                                        # Action de l'ordre (https://www.mql5.com/en/docs/integration/python_metatrader5/mt5ordercheck_py#trade_request_actions)
            'symbol': symbol,                                                       # Symbole de l'ordre
            'volume': volume,                                                       # Volume de l'ordre
            'type': orderType,                                                      # Type de l'ordre (achat (0) ou vente (1))
            'price': bid if orderType == ORDER_SELL else ask,                       # Prix de l'ordre (minimum (sell / bid) ou maximum (buy / ask))
            'deviation': deviation,                                                 # Ecart type de l'ordre
            'magic': self.id,                                                       # ID de l'ordre
            'comment': 'IBTrading',                                                 # Commentaire de l'ordre
            'type_time': mt5.ORDER_TIME_GTC,                                        # Type de temps de l'ordre
            'type_filling': mt5.ORDER_FILLING_IOC                                   # 
        }

        orderResult = mt5.order_send(request)                                       #Envoie de l'ordre
        self.ticket = orderResult.order                                             #ID du ticket de l'ordre
        return

    def Close(self) -> None:
        """
            Fermeture de l'ordre (l'inverse de l'ordre de base)
        """
        tick = mt5.symbol_info_tick(self.symbol)                                    # Récupération des informations du symbole
        bid = tick.bid                                                              # Prix minimum d'un ordre sur ce symbole (sell)
        ask = tick.ask                                                              # Prix maximum d'un ordre sur ce symbole (buy)
        
        request = {                                                                 # Creation de l'ordre (https://www.mql5.com/en/docs/constants/structures/mqltraderequest)
            'action': mt5.TRADE_ACTION_DEAL,
            'position': self.ticket,
            'symbol': self.symbol,
            'volume': self.volume,
            'type': ORDER_BUY if self.orderType == ORDER_SELL else ORDER_SELL,          #Inverse de l'ordre originel (Si c'est un ordre d'achat, on le transforme en ordre de vente et vice versa)
            'price': bid if self.orderType == ORDER_SELL else ask,                      # Prix de l'ordre (minimum (sell / bid) ou maximum (buy / ask))
            'deviation': self.deviation,
            'magic': 100,
            'comment': 'IBTrading',
            'type_time': mt5.ORDER_TIME_GTC,
            'type_filling': mt5.ORDER_FILLING_IOC
        }
        orderResult = mt5.order_send(request)
        return

class SignalTickData:
    """
        Gestion des données d'un tick d'un signal
    """
    time = None
    open = None
    high = None
    low = None
    close = None
    tickVolume = None
    spread = None
    realVolume = None
    def __init__(self, tickData: list) -> None:
        self.time, self.open, self.high, self.low, self.close, self.tickVolume, self.spread, self.realVolume = tickData


class Signal:
    """
        Gestion d'un signal
    """
    symbol = None                                               #Symbole du signale
    timeframe = None                                            #Periode d'analyse du signal
    nbPeriodSMA = None                                          #Nombre de periodes d'analyse de la moyenne

    ticksData = None                                            #Liste des données du signal
    sma = None                                                  #Moyenne du signal    

    def __init__(self, symbol: str, timeframe: int, nbPeriodSMA: int) -> None:
        """
            Params:
                symbol: str = Symbole du signal
                timeframe: int = mt5.TIMEFRAME_##
                nbPeriodSMA: int = Nombre de periodes d'analyse de la moyenne
        """
        self.symbol: str = symbol
        self.timeframe: int = timeframe
        self.nbPeriodSMA: int = nbPeriodSMA

        self.ticksData: list = []
        return

    def __ComputeSMA(self) -> None:
        """
            Calcul de la moyenne du signal
        """
        self.sma = 0
        for tickData in self.ticksData:
            self.sma += tickData.close
        self.sma /= len(self.ticksData)
        return

    def Update(self) -> None:
        """
            Mise à jour des données du signal
        """
        ticks = mt5.copy_rates_from_pos(self.symbol, self.timeframe, 1, self.nbPeriodSMA)#Recuperation des données du signal a partir de la derniere bar
        
        self.ticksData.clear()                                                          #Liste des données du signal 
        for tick in ticks:                                                              #Pour chaque tick de données
            self.ticksData.append(SignalTickData(tick))                                     #Ajout de la donnée dans la liste

        self.__ComputeSMA()                                                             #Calcul de la moyenne du signal

        return
