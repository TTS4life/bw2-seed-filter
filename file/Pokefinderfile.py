from file.File import File
import re

class PokefinderFile(File):
    def __init__(self, filename):
      super().__init__(filename)
      self.static = False

    def open(self):
      try:
        self.file = open(self.filename)
        header_line = self.file.readline().rstrip('\n\r') 
        
        #Static searches have diff columns than Wild
        static_check = header_line.split("\t")[3]
        # print(static_check)
        if static_check == "PID":
           self.static = True


      except:
        raise Exception("File not found")
        
      return True
    
    def parseLine(self):
        data = super().parseLine().rstrip('\n\r')

        if data == "" or data[0] == "\n":
            return False

        parsed = data.split("\t")

        # print(parsed)
        date = re.findall(r'\d+', parsed[-3])

        if self.static:
          print("Static File")

          seed = {
            "seed": int(parsed[0], 16),
            "ivframe": int(parsed[2]),
            "timer0": int(parsed[-2], 16),
            "date": parsed [-3],
            "stats": [ parsed[7], parsed[8], parsed[9], parsed[10], parsed[11], parsed[12] ],
            "gender": parsed[-5],
            "keypresses": parsed[-1],
            "month": int(date[1]),
            "day": int(date[2]),
            "second": int(date[-1]),
            "date": parsed[-3],
          }
        else:
           
           seed = {
            "seed": int(parsed[0], 16),
            "ivframe": int(parsed[2]),
            "timer0": int(parsed[-2], 16),
            "date": parsed [-3],
            "ability": parsed[9],
            "gender": parsed[-5],
            "stats": [ parsed[10], parsed[11], parsed[12], parsed[13], parsed[14], parsed[15] ],
            "keypresses": parsed[-1],
            "month": int(date[1]),
            "day": int(date[2]),
            "second": int(date[-1]),
            "date": parsed[-3],
           }

        print(seed)

        return seed