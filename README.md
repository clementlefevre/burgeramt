# BURGER BOT

This project retrieve availables slots for the Berlin Burger amt.

- rename `config_example.py` to `config.py` and fill the variables names in it.
- type `chmod +x burgeramt.sh` to execute the bash script.
- type `crontab -e` and add the following line : `@reboot cd /home/pi/workspace/burgeramt && /home/pi/workspace/burgeramt/burgeramt.sh`. This will start the bot at each reboot of the raspberry.
