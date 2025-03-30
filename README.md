# Myrssbot

Telegram Bot that let you subscribe and follow customs RSS, ADF and ATOM Feeds.

## Donate

Do you like this Bot? Buy me a coffee :)

Paypal:
[https://www.paypal.me/josrios](https://www.paypal.me/josrios)

## How to install, setup and execute the Bot

Note: Use Python 3.6 or above to install and run the Bot, previous version are unsupported.

1. Install Python3 and their tools:

    ```bash
    sudo apt-get install python3 python3-pip python3-venv
    ```

2. Get and setup the project:

    ```bash
    git clone https://github.com/J-Rios/TLG_myrssbot
    cd TLG_myrssbot
    make setup
    ```

3. Specify Telegram Bot account Token (get it from @BotFather) in `src/constants.py` file:

    ```python
    'TOKEN' : 'XXXXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    ```

## Usage

Launch the Bot:

```bash
make start
```

Check if the Bot is running:

```bash
make status
```

- Stop the Bot:

```bash
make stop
```
