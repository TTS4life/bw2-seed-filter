from abc import ABC, abstractmethod

class File(ABC):

    def __init__(self, filename):
        self.filename = filename
        self.file = None

    def open(self):
        try:
            self.file = open(self.filename)
        except:
            # raise Exception("File not found")
            return False
        
        return True

    def close(self):
        self.file.close()
        self.file = None
    
    # @abstractmethod
    # def parseFile():
    #     pass

    @abstractmethod
    def parseLine(self):
        if self.file is None or self.file.closed:
            raise Exception(f"File {self.filename} is not open")
        
        return self.file.readline()
