from QPO.scraping import *
from QPO.graph import *
from QPO.assets import *


class StateMachine:

    def INIT(self):
        NUM_PAGES = 11
        tp = TickerPage()

        for i in range(1, NUM_PAGES+1):
            tickers = tp.retrieve_tickers(i)
            tp.add_tickers(tickers)

        return tp.tickers

