# BURGER BOT

This project retrieves availables slots for the Berlin Burgeramt and sends an email with the list of available slots in the coming three months.
Preferably use it with a raspberry pi or a tiny instance on AWS.

- rename `config_example.py` to `config.py` and fill the variables names in it.
- type `chmod +x burgeramt.sh` to execute the bash script.
- type `crontab -e` and add the following line : `@reboot cd /home/pi/workspace/burgeramt && /home/pi/workspace/burgeramt/burgeramt.sh`. This will start the bot at each reboot of the raspberry.
