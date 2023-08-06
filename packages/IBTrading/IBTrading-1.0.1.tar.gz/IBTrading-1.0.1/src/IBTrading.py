import MetaTrader5 as mt5

from __signal import Signal
from __order import Order, ORDER_BUY, ORDER_SELL
from MetaTrader5 import TIMEFRAME_M1, TIMEFRAME_M2, TIMEFRAME_M3, TIMEFRAME_M4, TIMEFRAME_M5, TIMEFRAME_M6, TIMEFRAME_M10, TIMEFRAME_M12, TIMEFRAME_M15, TIMEFRAME_M20, TIMEFRAME_M30, TIMEFRAME_H1, TIMEFRAME_H2, TIMEFRAME_H4, TIMEFRAME_H3, TIMEFRAME_H6, TIMEFRAME_H8, TIMEFRAME_H12, TIMEFRAME_D1, TIMEFRAME_W1, TIMEFRAME_MN1

"""
    bid = Maximum price for buy orders
    ask = Minimum price for sell orders
    deviation = Ecart type de l'ordre (variance)
    volume = Nombre total d'actions de l'ordre (par exemple 0.2 bitcoins, le volume est de 0.2)
    magic = ID de l'ordre (pour la séparer d'un autre ordre) (ici on garde 100 car un n'utilise qu'un seul ordre)
    exposure = Risque
    sma = prix moyen
"""

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