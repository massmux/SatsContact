""" simplified library for interacting with the cashu """

import os


class GetCashu:
    def __init__(self):
        self.cashu_command = "cashu"
        self.ecash = ""


    def get_ecash(self,amount):
        # amount = sats
        amount = int(amount)
        rawresult = os.popen(f"{self.cashu_command} send {amount}").read()
        ecash = rawresult.split("\n")[0].strip()
        print(f"result: {rawresult}")
        self.ecash = {'ecash': ecash, 'amount': int(amount)}
        return self.ecash



