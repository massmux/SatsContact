## Satscontact

Automatically generates @sats.contact Lightning addresses and real-time converts received amounts in Cashu tokens sent to the Telegram Chat. Very important to setup the Telegram username before accessing the bot the first time.

The generated address will be in this form:

yourusername@sats.contact

Please note that for being compatible with LNURL standards and also with Telegram ones, the username may differ from your Telegram User. For example if your Telegram user contains uppercase letters they will be converted in lowercase and if unallowed chars are in it, they will be stripped.

For cashu tokens redeem, it's suggested [eNuts](https://www.enuts.cash/), which has been tested with this implementation.

How to Use the Bot:

- open the Bot [SatsContactBot](https://t.me/SatsContactBot) on Telegram
- run command /start
- take note of provided LNURL and Lightning address
- start receiving eCash tokens by receiving Lightning Sats to the provided address

## Configuration

- General: configure parameters in settings.ini (copy from settings.ini.example). Setup Lnbits connection parameters and domain name for the Lightning address. Domain name must have a valid web certificate. This file contains the Telegram API Key as well. Use botfather to get one. 
- Nginx: configure the default file with allowed IP (allow the IP where the Lnbits is located) and domain name (domain name for the Lightning address)
- Certificate: put a valid certificate as specified in default file (for Lightning address' domain name)
- Mint: configure the .env (from .env.example) with details of the mint (you can connect to any mint you wish)

## Disclaimer

Please be informed that:

- This software is beta software
- Cashu is beta software as well
- Lightning network itself is in beta development stage

So use the system at your risk.
