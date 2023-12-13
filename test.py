import re

class CorrectUsername:
    def __init__(self,oString):
        self.oString=oString

    def get_transformed(self):
        transformed = re.sub("[^0-9a-z]", "", self.oString.lower())
        return transformed


orig="Ciao12_comefo-se"

a=CorrectUsername(orig)
b=a.get_transformed()

print(b)
