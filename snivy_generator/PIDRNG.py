#!/usr/bin/python3

class PIDRNG:

    _rngInitTable = [
    [50, 100, 100, 100],
    [50, 50, 100, 100],
    [30, 50, 100, 100],
    [25, 30, 50, 100],
    [20, 25, 33, 50]
]

    def __init__(self, seed):
        self.seed = seed
        self.frame = 0

    def advance(self, iterations=1):
        for i in range(iterations):
            tmp = 0x5D588B656C078965 * self.seed
            tmp +=  0x0000000000269EC3
            self.seed = tmp % 0x10000000000000000
            self.frame += 1
        return self.seed >> 32

    def InitAdvanceRNG(self):
        for i in range(5):
            for j in range(4):
                if (self._rngInitTable[i][j] == 100):
                    break

                initRes = self.advance()
                initRes *= 101
                initRes >>= 32
                if (initRes <= self._rngInitTable[i][j]):
                    break

    def calculateInitialPIDRNG(self):


        #Initial RNG calls
        for i in range(3):
            self.InitAdvanceRNG()
            
        #standard RNG Advance
        self.advance(4)

        #Initial RNG calls (again)
        for i in range(4):
            self.InitAdvanceRNG()


        # Final calls
        self.advance(13)

