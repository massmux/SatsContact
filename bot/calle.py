import asyncio
from cashu.wallet.wallet import Wallet
from cashu.core.settings import settings

#url="http://mint.url:3338",
async def main():
    settings.tor = False
    wallet = await Wallet.with_db(
        url="https://mint.gwoq.com",
        db="mydb.db",
    )
    await wallet.load_mint()
    await wallet.load_proofs()

    # mint tokens into wallet, skip if wallet already has funds
    print(f"Wallet balance: {wallet.available_balance} sat")
    if wallet.available_balance <= 10:
        invoice = await wallet.request_mint(100)
        input(f"Pay this invoice and press any button: {invoice.bolt11}\n")
        await wallet.mint(100, id=invoice.id)

    # create 10 sat token
    proofs_to_send, _ = await wallet.split_to_send(wallet.proofs, 10, set_reserved=True)
    token = await wallet.serialize_proofs(proofs_to_send)
    print(token)


asyncio.run(main())

