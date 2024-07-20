# energy-monitor
Customisable APC UPS power usage monitor.

## Setting up cronjob to run every 5 mins
- `crontab -e`
- `*/5 * * * * /usr/bin/python3 /path/to/energymon/main.py`

## Setting up virtual environment for scripts to run (Debian)
- sudo apt install python3.11-venv
- python3 -m venv env
- source env/bin/activate
- pip install mysql-connector-python==8.4.0 paramiko

The crontab entry should take the following format:
- `*/5 * * * * /bin/bash /home/user/energy-monitor/run_energy_monitor.sh
