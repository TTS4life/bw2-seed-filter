import json
from numba_pokemon_prngs.enums import Language, Game, DSType

class parameters:
    def __init__(self):
        
        self.VCount = 0x82
        self.Timer0Min = 0
        self.Timer0Max = 0
        self.GxStat = 0x6
        self.VFrame = 0x8

        self.MAC = 0
        self.Version = Game.NONE
        self.DSType = DSType.DS
        self.Language = Language.ENGLISH

        self.Year = 2000
        self.Month = 1
        self.Day = 1
        self.DOW = 0

    def setENGB1(self):
        self.VCount = 0x60
        self.GxStat = 0x6
        self.Timer0Min = 0xC7C
        self.timer0Max = 0xC7D

    def setENGW2(self):
        self.VCount = 0x82
        self.Timer0Min = 0x10F2
        self.Timer0Max = 0x10F4

