from file.File import File
from rng.util import rngAdvance

class FiveGenSearchFile(File):

    def parseLine(self):
        data = super().parseLine().strip()

        # print(data)
        if data == "":
            return False
        
        parsed = data.split("\t")

        seed = {
            "seed": rngAdvance(int(parsed[0], 16)),
            "keypresses": parsed[19].strip(),
            "date": parsed[1] + "/"+parsed[2]+"/"+parsed[3]+" "+"{:02d}".format(int(parsed[4]))+":"+"{:02d}".format(int(parsed[5]))+":"+"{:02d}".format(int(parsed[6])),
            "month": parsed[2],
            "day": parsed[3],
            "timer0": int(parsed[8], 16),
            "stats": [parsed[12],parsed[13],parsed[14],parsed[15],parsed[16],parsed[17]],
            "second": int(parsed[6]),
            "ability": "N/A",
            "gender": "N/A"
        }
        
        return seed