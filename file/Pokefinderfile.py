from file.File import File
import re

class PokefinderFile(File):
    
    def parseLine(self):
        data = super().parseLine()

        if data == "":
            return False

        parsed = data.split("\t")

        date = re.findall(r'\d+', parsed[-3])



        seed = {
          "seed": int(parsed[0], 16),
          "ivframe": parsed[2],
          "timer0": parsed[-2],
          "date": parsed [-3],
          "stats": [ int(parsed[-12]), int(parsed[-11]), int(parsed[-10]), int(parsed[-9]), int(parsed[-8]), int(parsed[-7])],
          "keypresses": parsed[-1],
          "month": int(date[1]),
          "day": int(date[2]),
          "second": int(date[-1]),
          "date": parsed[-3],
        }

        print(seed)

        return seed