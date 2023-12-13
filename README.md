## Satscontact

Automatically generates @sats.contact Lightning addresses and real-time converts received amounts in Cashu tokens sent to the Telegram Chat. Very important to setup the Telegram username before accessing the bot the first time.

The generated address will be in this form:

yourusername@sats.contact

Please note that for being compatible with LNURL standards and also with Telegram ones, the username may differ from your Telegram User. For example if your Telegram user contains uppercase letters they will be converted in lowercase and if unallowed chars are in it, they will be stripped.

For cashu tokens redeem, it's suggested [eNuts](https://www.enuts.cash/), which has been tested with this implementation.

How to start on the Bot:

- open the Bot [SatsContactBot](https://t.me/SatsContactBot) on Telegram
- run command /start
- take note of provided LNURL and Lightning address
- start receiving eCash tokens by receiving Lightning Sats to the provided address

### Configuration

- configure parameters in settings.ini (copy from settings.ini.example). Connect to a lnbits source with LNURLp enabled
- configure the default file accordingly
- put a valid certificate as specified in default file
- configure the .env (from .env.example) with details of the mint
- configure the defaultfile with allowed IP and domain name

## Disclaimer

Please be informed that:

- this software is beta software
- Cashu is beta software
- Lightning network itself is in beta development stage

So use the system at your risk.
