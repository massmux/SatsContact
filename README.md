## Satscontact

Automatically generates @sats.contact Lightning addresses and real-time converts received amounts in Cashu tokens sent to the Telegram Chat. Very important to setup the Telegram username before accessing the bot the first time.

The generated address will be in this form:

yourusername@sats.contact

Please note that for being compatible with LNURL standards and also with Telegram ones, the username may differ from your Telegram User. For example if your Telegram user contains uppercase letters they will be converted in lowercase and if unallowed chars are in it, they will be stripped.

For cashu tokens redeem, it's suggested [cashu.me](https://cashu.me), which has been tested with this implementation. It works fine also when sending sats Lightning payment using redeemed tokens.

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

## Applications for SatsContact

### 1) Receive TPOS Lightning Lnbits payments as eCash

- configure a LNBits instance with the plugins: TPOS, Scrub;
- create a new TPOS that fits your needs;
- create a new Scrub connected to local wallet (the same where TPOS is connected);
- in Scrub configuration set as target LN Address, your address on satscontact;

that's it.
Now everytime someone pays at your POS, you will get the same amount in Sats as eCash in a Telegram message to your Telegram account.

## Disclaimer

Please be informed that:

- This software is beta software
- Cashu is beta software as well
- Lightning network itself is in beta development stage

So use the system at your risk.
