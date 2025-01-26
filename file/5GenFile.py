from . import File
from ..rng import rngAdvance

class FiveGenSearchFile(File):

    def parseLine(self):
        data = super().parseLine()
        
        parsed = data.split("\t")

        seed = {
            "seed": rngAdvance(int(parsed[0], 16)),
            "keys": parsed[19].strip(),
            "date": parsed[1] + "/"+parsed[2]+"/"+parsed[3]+" "+"{:02d}".format(int(parsed[4]))+":"+"{:02d}".format(int(parsed[5]))+":"+"{:02d}".format(int(parsed[6])),
            "month": parsed[2],
            "day": parsed[3],
            "timer0": parsed[8],
            "ivs": [parsed[12],parsed[13],parsed[14],parsed[15],parsed[16],parsed[17]]
        }
        
        return seed