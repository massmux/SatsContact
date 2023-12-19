""" simplified library for interacting with the cashu """

import os


class GetCashu:
    def __init__(self):
        self.cashu_command = "cashu"
        self.ecash = ""
        self.invoice = ""


    def get_ecash(self,amount):
        # amount = sats
        amount = int(amount)
        raw_result = os.popen(f"{self.cashu_command} send {amount}").read()
        ecash = raw_result.split("\n")[0].strip()
        print(f"result: {raw_result}")
        self.ecash = {'ecash': ecash, 'amount': amount}
        return self.ecash


    def create_invoice(self,amount):
        amount = int(amount)
        raw_result = os.popen(f"{self.cashu_command} invoice -n {amount}").read()
        invoice = raw_result.split("\n")[3].split(":")[1].strip()
        self.invoice = {'invoice': invoice, 'amount':amount}
        print(f"issued invoice {amount} Sats: {invoice}")
        return self.invoice


