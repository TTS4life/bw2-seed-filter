from file.File import File

class SSS4(File):

	# def __init__(self, filename):
	# 	super().__init__(filename)
    
	def open(self):
		try:
			self.file = open(self.filename, "r", encoding="Shift-JIS")
			self.file.readline() #Trash header line
		except Exception as e:
			print(str(e))
			return False
		return True

	def parseLine(self):

		data = super().parseLine()
		
		if data == "":
			return False
		
		parsed = data.split(",")

		seed = {
			"seed" : int(parsed[16], 16),
			"ivframe" : int(parsed[7]) - 1,
			"timer0" : str(parsed[6]),
			"year" : int(parsed[0]) + 2000,
			"month" : int(parsed[1]),
			"day" : int(parsed[2]),
			"hour" : int(parsed[3]),
			"minute" : int(parsed[4]),
			"second" : int(parsed[5]),
			"key_presses" : str(parsed[17]),
			"stats": [ int(parsed[8]), int(parsed[9]), int(parsed[10]), int(parsed[11]), int(parsed[12]), int(parsed[13]) ]
		}

		return seed